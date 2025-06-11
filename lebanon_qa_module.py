
import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules['pysqlite3']

import os
import zipfile
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from functools import lru_cache
import streamlit as st 
import time 

# --- Gemini API Configuration (for RAG's answer generation) ---
@st.cache_resource
def get_gemini_rag_model():
    """
    Configures and caches the Gemini Generative Model for RAG.
    Loads API key from the environment variable 'GE_TOKEN'.
    """
    try:
        # Access GEMINI_API_KEY from environment variable GE_TOKEN as requested
        api_key = os.environ.get("GE_TOKEN")
        if not api_key:
            st.error("خطأ: مفتاح Gemini API (GE_TOKEN) غير موجود في متغيرات البيئة. يرجى إضافته.")
            st.stop() # Stop the app if API key is not found
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.error(f"خطأ في تهيئة نموذج Gemini: {e}")
        st.stop()
        
# Call the cached function to get the model instance
_gemini_model = get_gemini_rag_model()


# --- ChromaDB Collection Loading ---
@st.cache_resource
def get_chromadb_collection():
    """
    Extracts and loads the ChromaDB collection.
    Handles zip extraction and client initialization.
    """
    db_path = "./chromadb_data"
    zip_path = "chromadb_data.zip"

    if not os.path.exists(db_path):
        if os.path.exists(zip_path):
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(db_path)
                st.success("تم استخراج بيانات ChromaDB بنجاح لوظيفة RAG!")
            except Exception as e:
                st.error(f"خطأ في استخراج ملف {zip_path}: {e}. قد لا تعمل وظيفة RAG.")
                return None # Return None if extraction fails
        else:
            st.error(f"بيانات RAG ({zip_path} أو مجلد {db_path}) غير موجودة. وظيفة RAG معطلة.")
            return None # Return None if data is missing
    
    client = chromadb.PersistentClient(path=db_path)
    try:
        # Assuming your collection is named "arabic_pdf_chunks"
        collection_obj = client.get_collection("arabic_pdf_chunks")
        return collection_obj
    except Exception as e:
        st.error(f"خطأ في تحميل مجموعة ChromaDB 'arabic_pdf_chunks': {e}. وظيفة RAG معطلة.")
        return None

# Call the cached function to get the collection instance
_chroma_collection = get_chromadb_collection()


# --- Embedding Model and Caching (for retrieving) ---
@st.cache_resource
def get_embedding_model_for_rag(model_name: str = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    """
    Loads and caches the SentenceTransformer model for generating embeddings.
    """
    return SentenceTransformer(model_name)

# Use lru_cache for specific function calls if needed, but the model itself is cached by st.cache_resource
@lru_cache(maxsize=128)
def embed_query_text(text: str) -> list[float]: # Return type changed to list[float] as .tolist() is used later
    """
    Encodes a single query string into a vector embedding.
    Caches results to speed up repeated queries.
    """
    model = get_embedding_model_for_rag() # Get the cached model instance
    embeddings = model.encode([text]) # Encode expects a list
    return embeddings[0].tolist() # Return as list for ChromaDB query_embeddings


# --- RAG Core Functions (internal to this module) ---
def _retrieve_chunks_internal(query: str, collection_obj: chromadb.api.models.Collection.Collection, top_k: int = 5) -> list[str]:
    """
    Retrieves top_k most relevant chunks from ChromaDB given a query.
    (Private helper function)
    """
    if collection_obj is None: # Defensive check if collection failed to load
        return []
    
    query_emb = embed_query_text(query)
    results = collection_obj.query(
        query_embeddings=[query_emb], # query_emb is already a list from .tolist()
        n_results=top_k
    )
    # Ensure 'documents' key exists and is not empty before accessing
    retrieved_chunks = results.get('documents', [[]])[0] if results and 'documents' in results else []
    return retrieved_chunks

@lru_cache(maxsize=64) # Cache generated answers to avoid repeated API calls on same inputs
def _generate_answer_from_context_internal(question: str, context: str) -> str:
    """
    Uses Gemini to generate an answer based on the provided context and question.
    (Private helper function)
    """
    if _gemini_model is None: # Defensive check if Gemini config failed
        return "نموذج Gemini غير مهيأ. لا يمكن توليد الإجابة."

    prompt = f"السياق: {context}\nالسؤال: {question}\nالإجابة:"
    try:
        response = _gemini_model.generate_content(prompt)
        time.sleep(4) # Enforce delay for Gemini API call
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API for question: '{question[:50]}...'. Error: {e}")
        return "حدث خطأ في توليد الإجابة."

def answer_qa_logic(question: str, top_k: int = 5) -> str:
    """
    Main logic for RAG-based Question Answering.
    Retrieves relevant context and uses an LLM to generate an answer.
    """
    # Check if the ChromaDB collection was successfully loaded
    if _chroma_collection is None:
        return "خدمة الاستعلام غير متاحة: قاعدة بيانات المعرفة لم يتم تحميلها بشكل صحيح."

    # Retrieve chunks based on the question
    retrieved_chunks = _retrieve_chunks_internal(question, _chroma_collection, top_k=top_k)
    
    # If no relevant chunks are found, inform the user
    if not retrieved_chunks:
        return "لم يتم العثور على معلومات ذات صلة بسؤالك في قاعدة البيانات المتاحة."
        
    # Combine retrieved chunks into a single context string
    context = "\n".join(retrieved_chunks)
    
    # Generate the answer using Gemini based on the context and question
    answer = _generate_answer_from_context_internal(question, context)
    
    return answer

