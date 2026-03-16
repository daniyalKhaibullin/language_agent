import os
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage # ADDED: Needed to format your input
# from langchain_ollama import ChatOllama      # REMOVED: Switching to OpenAI
# from lesson import get_lesson                # LEGACY (from your V1)
# import agents                                # LEGACY (from your V1)
from core.state import TutorState
from core.graph_builder import build_graph


load_dotenv()
# --- CONFIG ---
# VOCAB_FILE = "vocab.json"                    # LEGACY: Replaced by TutorVectorStore
# model = ChatOllama(model="gemma3:latest")    # REMOVED: Now handled inside the nodes
# current_lesson_name = "first_lesson"         # LEGACY
# lesson = get_lesson(current_lesson_name)     # LEGACY

# --- STATE ---
# current_step = 1                             # LEGACY: State is now handled by TutorState
# interaction_count = 0                        # LEGACY
# chat_history = []                            # LEGACY: Replaced by state["messages"]
# last_tutor_msg = ""                          # LEGACY

# LEGACY FUNCTION: Your new ExtractorNode handles saving vocabulary to ChromaDB now!
# def save_vocab(words):
#     if not words: return
#     existing = []
#     if os.path.exists(VOCAB_FILE):
#         with open(VOCAB_FILE, "r") as f: existing = json.load(f)
#     for w in words:
#         if w.lower() not in [x.lower() for x in existing]: existing.append(w)
#     with open(VOCAB_FILE, "w") as f: json.dump(existing, f, indent=2)

def main():
    # 1. Your correctly mapped state variables
    state: TutorState = {
        "messages": [],
        "user_id": "user-0001",
        "is_new_user": False,
        "current_topic": "Everyday conversation",
        "retrieved_vocab": [],
        "extracted_vocab": {}
    }

    # 2. Retrieve the compiled StateGraph from graph_builder.py
    graph = build_graph()
    
    print("🇩🇪 Terminal Tutor Started! (Type 'quit' to exit) 🇩🇪")
    print("-" * 50)

    # 3. ADDED: The Interactive Loop
    # LangGraph needs to pause and wait for your input, otherwise it just crashes or ends immediately.
    while True:
        user_text = input("\nYou: ")
        
        if user_text.lower() in ["quit", "exit", "q"]:
            print("Tutor: Einen Moment bitte, ich speichere unsere Notizen... (Saving notes...)")
            # Tell the graph to run the extractor
            state["end_session"] = True
            graph.invoke(state)
            print("Auf Wiedersehen!")
            break
            
        # Add human message and run chat
        state["messages"].append(HumanMessage(content=user_text))
        state = graph.invoke(state)
        
        tutor_response = state["messages"][-1].content
        print(f"Tutor: {tutor_response}")
if __name__ == "__main__":
    main()