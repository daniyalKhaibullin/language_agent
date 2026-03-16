from langgraph.graph import StateGraph, START, END
from core.state import TutorState

from nodes.router import RouterNode
from nodes.rag_assessor import RAGAssessorNode
from nodes.warmup import WarmupNode
from nodes.topic_selection import TopicSelectionNode
from nodes.conversation import ConversationNode
from nodes.extractor import ExtractorNode

def route_start(state: TutorState):
    """If it's the first message, run setup. Otherwise, jump to conversation."""
    if len(state["messages"]) <= 1:
        return "router"
    return "conversation"

def route_after_conversation(state: TutorState):
    """If the user quit, run the extractor. Otherwise, pause and wait for the user."""
    if state.get("end_session", False):
        return "extractor"
    return END

def build_graph():
    workflow = StateGraph(TutorState)

    workflow.add_node("router", RouterNode())
    workflow.add_node("rag_assessor", RAGAssessorNode())
    workflow.add_node("warmup", WarmupNode())
    workflow.add_node("topic_selection", TopicSelectionNode())
    workflow.add_node("conversation", ConversationNode())
    workflow.add_node("extractor", ExtractorNode())

    # 1. Dynamic Start Routing
    workflow.add_conditional_edges(START, route_start)
    
    # 2. Setup Pipeline (Only runs on turn 1)
    workflow.add_edge("router", "rag_assessor") # Skipping conditional warmup for now to keep it simple
    workflow.add_edge("rag_assessor", "topic_selection")
    workflow.add_edge("topic_selection", "conversation")
    
    # 3. Dynamic End Routing
    workflow.add_conditional_edges("conversation", route_after_conversation)
    
    workflow.add_edge("extractor", END)

    return workflow.compile()