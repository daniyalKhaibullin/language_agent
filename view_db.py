from memory.vector_store import TutorVectorStore
import os

def peek_into_memory():
    db = TutorVectorStore()
    user = "user-0001"
    
    # Pull up to 50 words for the export
    documents = db.retrieve_past_vocab(user_id=user, limit=50)
    
    if not documents:
        print("The database is currently empty.")
        return

    # 1. Prepare the output text
    output_text = f"--- 🧠 Memory Vault for {user} ---\n\n"
    for i, doc in enumerate(documents):
        entry = f"[Entry {i+1}]\n{doc}\n{'-' * 30}\n"
        output_text += entry

    # 2. Print to terminal (Keeping the old behavior)
    print(output_text)

    # 3. Write to a text file
    export_path = "memory_export.txt"
    with open(export_path, "w", encoding="utf-8") as file:
        file.write(output_text)
        
    print(f"✅ Successfully exported memory to: {os.path.abspath(export_path)}")

if __name__ == "__main__":
    peek_into_memory()