from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from core.retrieval import Retriever
from core.tools import search_tool,substitute_tool, followup_tool
from core.memory import ConversationMemory
from core.prompts import prompts
from core.config import settings

class PharmaAgent:

    VALID_TOOLS = {"search_tool", "substitute_tool", "followup_tool"}

    def __init__(self):
        self.retriever = Retriever()
        self.memory = ConversationMemory()
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )

    def choose_tool(self, query):
        messages = [
            SystemMessage(content=prompts.AGENT_SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]

        raw = self.llm.invoke(messages).content.strip().lower()
        # Normalize: strip punctuation, take first word only
        decision = raw.split()[0].rstrip(".,;:") if raw else "search_tool"
        if decision not in self.VALID_TOOLS:
            print(f"[WARN] Unexpected tool choice: '{raw}'. Defaulting to search_tool.")
            decision = "search_tool"

        return decision
    

    def agent_execute(self,query, session_id: str = "default"):

        tool_name = self.choose_tool(query)
        print("Tool: ",tool_name)
        state = self.memory.get(session_id)

        if tool_name == "followup_tool" and state["last_results"]:
            print("followed up")
            result = followup_tool(query, self.memory, self.retriever, session_id)
            mode = state["last_mode"]

        elif tool_name == "substitute_tool":
            result = substitute_tool(query,self.retriever)
            mode = "substitute"

        else:
            result = search_tool(query, self.retriever)
            mode = "general"

        # update memory
        if result and "results" in result:
            self.memory.update(
                session_id=session_id,
                mode=mode,
                results=result.get("results")
            )

        return result, mode
    
    def pharma_assistant(self,query, session_id: str = "default"):

        structured_result, mode = self.agent_execute(query, session_id)

        # print(mode)
        
        prompt = prompts.build_prompt_new(query, structured_result, mode)

        response = self.llm.invoke(prompt)

        return response.content