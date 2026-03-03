from langchain_core.messages import SystemMessage, HumanMessage

class Prompts:
    AGENT_SYSTEM_PROMPT = """
    You are a pharmaceutical assistant planner.

    You must NOT answer the user.
    You must ONLY choose exactly ONE tool.

    Available tools:

    substitute_tool
    - Use when the user requests:
    alternatives, substitutes, similar medicines,
    or cheaper versions of a specific medicine.

    search_tool
    - Use when the user:
    asks about a medicine,
    wants information,
    searches or discovers medicines.

    followup_tool
    - Use ONLY when the user refers to previous results,
    such as:
    "among them", "cheapest", "compare these",
    "which one", or similar follow-up context.

    Strict Rules:
    - Return ONLY one of these exact strings:
    substitute_tool
    search_tool
    followup_tool
    - Do NOT explain.
    - Do NOT add extra text.
    - If uncertain, default to search_tool.
    """

    def build_prompt_new(self, query, data, mode):

        if mode == "substitute":
            system_text = """
            You are a pharmaceutical assistant.

            Use ONLY the provided medicine data.
            Do NOT invent medicines or medical claims.
            Use only the given data as your pharmaceutical source.

            The medicines listed are substitutes or alternatives
            based on similar composition.

            Explain clearly:
            - which medicines are equivalent substitutes
            - important composition similarities
            - price differences
            - which options may be cheaper
            Keep the explanation concise and factual.
            """

        elif mode == "followup":
            system_text = """
            You are a pharmaceutical assistant helping with a follow-up question.

            The user is asking about a previous set of medicines already retrieved.
            Use ONLY the provided medicine data (previous results).
            Do NOT invent new medicines.

            Based on the user's question:
            - If asking about cheapest/affordable: highlight the lowest price option clearly.
            - If asking to compare: contrast the two medicines on composition, manufacturer, and price.
            - Otherwise: answer specifically from the provided medicines context.

            Be concise, direct, and factual.
            """

        else:  # mode == "general"
            system_text = """
            You are a pharmaceutical assistant.

            Use ONLY the provided medicine data.
            Do NOT invent medicines.

            The user wants information about a medicine.

            Explain clearly:
            - what the medicine is
            - its composition
            - manufacturer
            - price (INR)
            If multiple medicines appear, summarize them briefly.
            """

        return [
            SystemMessage(content=system_text),
            HumanMessage(
                content=f"""
            User query:
            {query}

            Medicine database results:
            {data}
            """
            )
        ]

prompts = Prompts()