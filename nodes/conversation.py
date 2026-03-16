from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from core.state import TutorState

class ConversationNode:
    def __init__(self):
        # THE CREATIVE BRAIN
        # gpt-4o is premium for bilingual nuance. 
        # max_tokens=150 ensures each reply costs fractions of a cent.
        # temperature=0.7 allows for natural, conversational variety.
        self.llm = ChatOpenAI(model="gpt-4o", max_tokens=150, temperature=0.7)

    def __call__(self, state: TutorState) -> dict:
        # 1. Define the Tutor's Persona
        sys_msg = SystemMessage(content=(
            f"You are a strict but encouraging German language tutor. "
            f"Current topic: {state.get('current_topic', 'Everyday conversation')}. "
            f"RULES: "
            f"1. If the user makes a mistake, DO NOT rewrite their entire sentence. Point out the specific error concisely like this: 'Correction: [wrong word] -> [correct word] (Brief English reason)'. "
            f"2. Introduce exactly ONE new German vocabulary word, **bolded**, with its English translation in parentheses. "
            f"3. Respond to their actual message naturally in German. "
            f"4. Always end with a question to keep the conversation going. "
            f"5. Keep responses structured and easy to read."
        ))
        
        # 2. Combine the persona with the conversation history
        messages = [sys_msg] + state["messages"][-10:] #NEW BY USER: Sliding window of the last 10 messages to keep context but avoid token overload
        
        # 3. Call OpenAI gpt-4o
        response = self.llm.invoke(messages)
        
        # 4. Return the new message to append it to the LangGraph state
        return {"messages": [response]}