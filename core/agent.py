from typing import Literal, AsyncGenerator
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from core.retrieval import Retriever
from core.tools import search_tool, substitute_tool, followup_tool
from core.memory import ConversationMemory
from core.prompts import prompts
from core.config import settings


class ToolDecision(BaseModel):
    tool_name: Literal["substitute_tool", "search_tool", "followup_tool"] = Field(
        description="Selected tool: substitute_tool for alternatives, search_tool for medicine info, followup_tool for context queries."
    )
    reasoning: str = Field(
        default="",
        description="Short justification for selecting this tool."
    )


class PharmaAgent:

    VALID_TOOLS = {"search_tool", "substitute_tool", "followup_tool"}

    def __init__(self):
        self.retriever = Retriever()
        self.memory = ConversationMemory()
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        try:
            self.structured_router = self.llm.with_structured_output(ToolDecision)
        except Exception as e:
            print(f"[WARN] Structured output router init warning: {e}. Falling back to standard LLM.")
            self.structured_router = None

    def choose_tool(self, query: str) -> str:
        messages = [
            SystemMessage(content=prompts.AGENT_SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]

        if self.structured_router:
            try:
                decision: ToolDecision = self.structured_router.invoke(messages)
                if decision and decision.tool_name in self.VALID_TOOLS:
                    print(f"[Router Structured] Tool: {decision.tool_name} | Reasoning: {decision.reasoning}")
                    return decision.tool_name
            except Exception as e:
                print(f"[Router Structured Error] Fallback to string parsing due to: {e}")

        # String parsing fallback
        raw = self.llm.invoke(messages).content.strip().lower()
        decision_str = raw.split()[0].rstrip(".,;:") if raw else "search_tool"
        if decision_str not in self.VALID_TOOLS:
            print(f"[WARN] Unexpected tool choice: '{raw}'. Defaulting to search_tool.")
            decision_str = "search_tool"

        return decision_str

    def agent_execute(self, query: str, session_id: str = "default"):
        tool_name = self.choose_tool(query)
        print("Executing Tool: ", tool_name)
        state = self.memory.get(session_id)

        if tool_name == "followup_tool" and state.get("last_results"):
            print("[Agent] Executing follow-up handler")
            result = followup_tool(query, self.memory, self.retriever, session_id)
            mode = state.get("last_mode", "general")

        elif tool_name == "substitute_tool":
            result = substitute_tool(query, self.retriever)
            mode = "substitute"

        else:
            result = search_tool(query, self.retriever)
            mode = "general"

        # Update persistent memory
        if result and "results" in result:
            self.memory.update(
                session_id=session_id,
                mode=mode,
                results=result.get("results")
            )

        return result, mode

    def pharma_assistant(self, query: str, session_id: str = "default") -> str:
        structured_result, mode = self.agent_execute(query, session_id)
        prompt = prompts.build_prompt_new(query, structured_result, mode)
        response = self.llm.invoke(prompt)
        return response.content

    async def pharma_assistant_stream(self, query: str, session_id: str = "default") -> AsyncGenerator[str, None]:
        structured_result, mode = self.agent_execute(query, session_id)
        prompt = prompts.build_prompt_new(query, structured_result, mode)

        async for chunk in self.llm.astream(prompt):
            if chunk.content:
                yield chunk.content