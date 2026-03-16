import chromadb
from chromadb.utils import embedding_functions

class TutorVectorStore:
    def __init__(self, persist_directory="./chroma_data", collection_name="user_vocab"):
        """
        Initializes the local ChromaDB. 
        It uses an extremely fast, lightweight, and local embedding model.
        """
        # all-MiniLM-L6-v2 is standard for fast, local semantic search
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # PersistentClient saves the data to a local folder so memory survives reboots
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create the namespace for our vocabulary
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def save_vocabulary(self, user_id: str, german_word: str, english_translation: str, context_sentence: str):
        """
        Takes data extracted by the Extractor Node and saves it to the vector database.
        """
        # Create a unique ID for this user's word to avoid duplicates
        doc_id = f"{user_id}_{german_word.lower().replace(' ', '_')}"
        
        document_text = f"Word: {german_word}\nTranslation: {english_translation}\nContext: {context_sentence}"
        
        self.collection.upsert(
            documents=[document_text],
            metadatas=[{
                "user_id": user_id, 
                "word": german_word,
                "type": "vocabulary"
            }],
            ids=[doc_id]
        )
        print(f"[Vector DB] Saved '{german_word}' for user {user_id}.")

    def retrieve_past_vocab(self, user_id: str, limit: int = 5):
        """
        Used by the RAG Assessor Node to pull words the user previously struggled with.
        """
        # We can query directly by metadata (user_id) to get their specific flashcards
        results = self.collection.get(
            where={"user_id": user_id},
            limit=limit
        )
        
        documents = results.get("documents", [])
        return documents

    def search_similar_mistakes(self, user_id: str, query: str, limit: int = 2):
        """
        Semantic search: If the user makes a grammar mistake, search if they made a 
        similar one in the past.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        
        # .query returns a list of lists, so we grab the first element
        return results.get("documents", [[]])[0]
    
    def save_extraction(self, user_id: str, extracted_data: dict, session_id: str):
        """
        Takes the structured dictionary from the Extractor Node and saves the pieces.
        """
        # 1. Extract and save the vocabulary safely
        vocab_list = extracted_data.get("new_vocabulary", [])
        
        # If the LLM returned nothing, it might be None, so we safeguard it
        if vocab_list:
            for item in vocab_list:
                self.save_vocabulary(
                    user_id=user_id,
                    german_word=item.get("german_word", ""),
                    english_translation=item.get("english_translation", ""),
                    context_sentence=item.get("example_sentence", "")
                )
        
        # 2. You can add logic here later to save the grammatical mistakes 
        # to a different ChromaDB collection if you want!
        
        print(f"[Vector DB] Processed extraction for session {session_id}")