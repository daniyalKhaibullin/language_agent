# 🇩🇪 AI German Tutor Agent (v1.0)

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_AI-orange.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-purple.svg)

An intelligent, stateful language tutoring agent built with **LangGraph** and **OpenAI**. This agent acts as a strict but encouraging German language tutor that holds natural, bilingual conversations, corrects grammar with surgical precision, and quietly extracts and saves new vocabulary/mistakes into a local vector database for long-term memory.

## 🚀 Key Features

* **Dual-Brain LLM Architecture:**
    * **Creative Brain (`gpt-4o`):** Handles the nuanced, bilingual conversation, providing immediate grammar corrections and introducing new vocabulary in context.
    * **Reasoning Brain (`gpt-4o-mini`):** Runs quietly in the background using Pydantic structured outputs to extract vocabulary and grammar mistakes without interrupting the chat flow.
* **Stateful Graph Routing:** Utilizes LangGraph to manage session states, enabling dynamic routing (e.g., separating setup logic from active conversation and background extraction).
* **Local Vector Memory:** Integrates **ChromaDB** and `sentence-transformers` (`all-MiniLM-L6-v2`) to index and store extracted vocabulary locally, setting the foundation for long-term RAG (Retrieval-Augmented Generation).
* **Context Window Optimization:** Implements a sliding window memory algorithm to prevent token bloat and API crashes during extended tutoring sessions.
* **Interactive Web UI:** Features a clean, responsive frontend built entirely in pure Python using **Streamlit**.

## 🛠️ Technology Stack

* **Orchestration & State Management:** [LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) & [LangChain](https://www.langchain.com/)
* **Large Language Models (LLMs):** [OpenAI API](https://platform.openai.com/) (`gpt-4o` & `gpt-4o-mini`)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Local)
* **Embeddings:** HuggingFace `sentence-transformers`
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
* **Frontend GUI:** [Streamlit](https://streamlit.io/)

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10 or higher
* An OpenAI API Key

### 1. Clone the Repository
```bash
git clone [https://github.com/daniyalKhaibullin/language_agent.git](https://github.com/daniyalKhaibullin/language_agent.git)
cd language_agent
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```
This version V1.0 only works for the OpenAI API key.

### 🎮 Usage
To launch the web-based tutoring interface, ensure your virtual environment is active and run:
```bash
streamlit run app.py
```

This will automatically open the UI in your default web browser.

* Chat: Interact with the tutor naturally. It will speak in German, provide English corrections, and introduce new words.

* Save Memory: When you are finished, click the "End Session & Save Memory" button in the sidebar. The system will extract the session's vocabulary and safely index it into your local ChromaDB.

### 🗺️ Roadmap (Upcoming in v2.0)
* [ ] Active RAG Integration: Wake up the RAGAssessorNode to retrieve the user's past struggled vocabulary from ChromaDB at the start of a session and inject it into the tutor's prompt.

* [ ] Database Visualization: Build a secondary dashboard page to allow users to view, search, and manage their saved flashcards.

* [ ] Audio/Voice Integration: Add Text-to-Speech (TTS) and Speech-to-Text capabilities for pronunciation practice.


### 👨‍💻 Author: 
**Built by Daniyal Khaibullin**
