

import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules['pysqlite3']

import os
import zipfile
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from functools import lru_cache
import streamlit as st # Crucial for @st.cache_resource
import time # For time.sleep() to respect API rate limits


# --- Gemini API Configuration (for RAG's answer generation) ---
@st.cache_resource
def get_gemini_model_instance():
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
        
# Initialize the Gemini model instance (cached)
gemini_model = get_gemini_model_instance()


# --- ChromaDB Collection Loading ---
@st.cache_resource
def get_chromadb_collection_instance():
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

# Initialize the ChromaDB collection (cached) and make it publicly available
collection = get_chromadb_collection_instance()


# --- SentenceTransformer Embedding Model ---
@st.cache_resource
def get_embedding_model_instance(model_name: str = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    """
    Loads and caches the SentenceTransformer model for generating embeddings.
    """
    return SentenceTransformer(model_name)

# Cache embeddings of queries (using lru_cache for quick lookups)
@lru_cache(maxsize=128)
def embed_chunks(text: str, model_name: str = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2') -> list[float]:
    """
    Encodes a single query string into a vector embedding.
    Caches results to speed up repeated queries.
    This function's name is kept as 'embed_chunks' as per your original snippet.
    """
    model = get_embedding_model_instance(model_name)
    embeddings = model.encode([text]) # Encode expects a list
    return embeddings[0].tolist() # Return as list for ChromaDB query_embeddings


# --- Retrieval Function (Publicly available as 'retrieve') ---
def retrieve(query: str, collection_obj: chromadb.api.models.Collection.Collection, top_k: int = 5) -> list[str]:
    """
    Retrieves top_k most relevant chunks from ChromaDB given a query.
    This function's name is kept as 'retrieve' as per your original snippet.
    """
    if collection_obj is None: # Defensive check if collection failed to load
        return []
    
    query_emb = embed_chunks(query) # Call the cached embedding function
    results = collection_obj.query(
        query_embeddings=[query_emb], # query_emb is already a list from .tolist()
        n_results=top_k
    )
    # Ensure 'documents' key exists and is not empty before accessing
    retrieved_chunks = results.get('documents', [[]])[0] if results and 'documents' in results else []
    return retrieved_chunks


# --- Answer Generation Function (Publicly available as 'answer_question') ---
@lru_cache(maxsize=64) # Cache generated answers to avoid repeated API calls on same inputs
def answer_question(question: str, context: str) -> str:

    if gemini_model is None: # Defensive check if Gemini config failed
        return "نموذج Gemini غير مهيأ. لا يمكن توليد الإجابة."

    prompt = f"السياق: {context}\nالسؤال: {question}\nالإجابة:"
    try:
        response = gemini_model.generate_content(prompt)
        time.sleep(4) # Enforce delay for Gemini API call (essential for rate limits)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API for question: '{question[:50]}...'. Error: {e}")
        return "حدث خطأ في توليد الإجابة."


def answer_qa_lebanon(question: str, context: str) -> str:
    answer = answer_question(question, context)    
    return answer
