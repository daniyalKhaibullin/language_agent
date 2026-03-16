from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class TutorState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_id: str
    is_new_user: bool
    current_topic: str
    retrieved_vocab: List[Dict[str, Any]]
    extracted_vocab: Dict[str, Any]
    end_session: bool  # <-- NEW: Tells the graph when to run the extractor