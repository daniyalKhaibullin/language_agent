import uuid
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from core.state import TutorState
from schemas.pydantic_models import ExtractionRecord
from memory.vector_store import TutorVectorStore

class ExtractorNode:
    def __init__(self):
        # THE REASONING BRAIN
        # gpt-4o-mini is ultra-cheap and perfect for data extraction.
        # temperature=0 ensures it is purely analytical and predictable.
        # .with_structured_output forces it to return your Pydantic model.
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ExtractionRecord)
        self.db = TutorVectorStore()

    def __call__(self, state: TutorState) -> dict:
        # 1. Define the analytical instructions
        sys_msg = SystemMessage(content=(
            "You are an expert linguistic analyzer. Review the conversation transcript. "
            "Extract any NEW German vocabulary introduced by the tutor. "
            "Extract any grammatical mistakes made by the English-speaking user in German. "
            "If none exist, return empty lists. Output strictly in the requested format."
        ))
        
        # 2. Feed the conversation history to the analyzer
        messages = [sys_msg] + state["messages"]
        
        # 3. Call OpenAI gpt-4o-mini (It returns a populated ExtractionRecord object)
        extracted: ExtractionRecord = self.llm.invoke(messages)
        
        # 4. Save to ChromaDB if there is actually data
        if extracted and (extracted.new_vocabulary or extracted.grammatical_mistakes):
            session_id = str(uuid.uuid4())
            self.db.save_extraction(state["user_id"], extracted.dict(), session_id)
            return {"extracted_vocab": extracted.dict()}
        
        return {"extracted_vocab": {}}