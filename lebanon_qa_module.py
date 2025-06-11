

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


#==================Option 1: RAG
#Embed chunks
def embed_chunks(chunks, model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    """
    Encodes each text chunk into a vector embedding.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks)
    return embeddings, model


#Retrieve relevant chunks

    """
    Retrieves top_k most relevant chunks from ChromaDB given a query.
    """
def retrieve(query, collection, top_k=5):
    query_emb =embed_chunks(query)[0]
    results = collection.query(
        query_embeddings=[query_emb.tolist()],
        n_results=top_k
    )
    retrieved_chunks = results['documents'][0]
    return retrieved_chunks

# Use a language model to generate answers (Arabic-capable)


genai.configure(api_key="AIzaSyAV-v_NVmeoiuRRtJ4R95zLx2TdAJOXUwY")
gemini_model = genai.GenerativeModel("gemini-2.0-flash")



def answer_question(question, context):
    prompt = f"السياق: {context}\nالسؤال: {question}\nالإجابة:"
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "error"


# load the collection
with zipfile.ZipFile("chromadb_data.zip", 'r') as zip_ref:
    zip_ref.extractall("chromadb_data")
client = chromadb.PersistentClient(path="./chromadb_data")
collection = client.get_collection("arabic_pdf_chunks")



def answer_qa_lebanon(question: str, context: str) -> str:
    retrieved = retrieve(question, collection)
    answer = answer_question(question, context)    
    return answer
