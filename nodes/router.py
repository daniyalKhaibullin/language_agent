from core.state import TutorState

class RouterNode:
    def __call__(self, state: TutorState) -> dict:
        # Determine if user has past sessions
        return {"is_new_user": state.get("is_new_user", True)}
