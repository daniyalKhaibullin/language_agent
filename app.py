import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from core.state import TutorState
from core.graph_builder import build_graph

# Load environment variables (your OpenAI key)
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="German Tutor", page_icon="🇩🇪")
st.title("🇩🇪 AI German Tutor")

# --- Initialize Session State ---
# Streamlit re-runs the script on every click, so we store the graph and state here 
# so it doesn't reset your conversation every time you type.
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
    
if "tutor_state" not in st.session_state:
    st.session_state.tutor_state = {
        "messages": [],
        "user_id": "user-0001",
        "is_new_user": False,
        "current_topic": "Everyday conversation",
        "retrieved_vocab": [],
        "extracted_vocab": {},
        "end_session": False
    }

# --- Sidebar (Settings & Memory) ---
with st.sidebar:
    st.header("🧠 Memory & Controls")
    st.write("Click below when you are done chatting to save your new vocabulary to the database.")
    
    # This replaces typing "quit" in the terminal!
    if st.button("End Session & Save Memory", type="primary"):
        with st.spinner("Extracting vocabulary and saving to ChromaDB..."):
            st.session_state.tutor_state["end_session"] = True
            st.session_state.graph.invoke(st.session_state.tutor_state)
            st.success("Notes saved successfully! You can now close the tab.")

# --- Chat Interface ---
# 1. Display all previous messages in the UI
for msg in st.session_state.tutor_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 2. The Chat Input box at the bottom of the screen
if prompt := st.chat_input("Schreib etwas auf Deutsch..."):
    
    # Immediately show the user's message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Add it to the LangGraph state
    st.session_state.tutor_state["messages"].append(HumanMessage(content=prompt))
    
    # Run the graph and show a loading spinner
    with st.spinner("Der Tutor überlegt... (Thinking...)"):
        st.session_state.tutor_state = st.session_state.graph.invoke(st.session_state.tutor_state)
        
    # Get the tutor's response and display it
    tutor_response = st.session_state.tutor_state["messages"][-1].content
    with st.chat_message("assistant"):
        st.markdown(tutor_response)