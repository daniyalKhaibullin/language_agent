from core.state import TutorState

class TopicSelectionNode:
    def __call__(self, state: TutorState) -> dict:
        # Determine the topic for this session
        return {"current_topic": state.get("current_topic", "Everyday conversation")}
