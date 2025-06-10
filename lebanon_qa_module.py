import zipfile
import chromadb
from sentence_transformers import SentenceTransformer
import genai
from functools import lru_cache

# Configure Gemini API once
GE_TOKEN = os.environ.get("GE_TOKEN")
genai.configure(api_key=GE_TOKEN)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Load ChromaDB collection once when module loads
with zipfile.ZipFile("chromadb_data.zip", 'r') as zip_ref:
    zip_ref.extractall("chromadb_data")

client = chromadb.PersistentClient(path="./chromadb_data")
collection = client.get_collection("arabic_pdf_chunks")

# Cache SentenceTransformer model for reuse
@lru_cache(maxsize=1)
def get_embedding_model(model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    return SentenceTransformer(model_name)

# Cache embeddings of queries
@lru_cache(maxsize=128)
def embed_chunks(text, model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    """
    Encodes a single query string or list of chunks into embeddings.
    Caches results to speed up repeated queries.
    """
    model = get_embedding_model(model_name)
    # If input is a string, convert to list for encoding
    if isinstance(text, str):
        texts = [text]
    else:
        texts = text
    embeddings = model.encode(texts)
    return embeddings

def retrieve(query, collection, top_k=5):
    """
    Retrieves top_k most relevant chunks from ChromaDB given a query.
    """
    query_emb = embed_chunks(query)[0]  # get first embedding vector
    results = collection.query(
        query_embeddings=[query_emb.tolist()],
        n_results=top_k
    )
    retrieved_chunks = results['documents'][0]
    return retrieved_chunks

# Cache answers to avoid repeated API calls on same inputs
@lru_cache(maxsize=64)
def answer_question(question, context):
    prompt = f"السياق: {context}\nالسؤال: {question}\nالإجابة:"
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "حدث خطأ في توليد الإجابة."

# Helper function to get answer directly from question:
def get_answer_from_question(question, top_k=5):
    retrieved_chunks = retrieve(question, collection, top_k=top_k)
    context = "\n".join(retrieved_chunks)
    answer = answer_question(question, context)
    return answer

