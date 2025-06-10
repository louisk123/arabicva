# sentiment_module.py

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch # For device handling

# --- Load and Cache Sentiment Model ---
@st.cache_resource
def get_camelbert_sentiment_pipeline():
    """
    Loads and caches the CAMeLBERT sentiment analysis pipeline.
    This ensures the model is loaded only once across user sessions.
    """
    model_name = 'CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment'
    device = 0 if torch.cuda.is_available() else -1
    return pipeline('sentiment-analysis', model=model_name, device=device)

# Get the pipeline instance
_sentiment_analyzer = get_camelbert_sentiment_pipeline()

def perform_sentiment_analysis_logic(text_to_analyze: str) -> str:
    """
    Performs sentiment analysis on the given Arabic text using CAMeLBERT.
    Returns a user-friendly sentiment label (without score).
    """
    try:
        result = _sentiment_analyzer(text_to_analyze)[0]
        label = result['label']
        # score = result['score'] # Removed the score variable as it's no longer displayed

        # Map labels for better Arabic display with emojis
        display_label = {
            'LABEL_0': 'سلبي 😠',
            'LABEL_1': 'محايد 😐',
            'LABEL_2': 'إيجابي 🤩'
        }.get(label, label) # Fallback to original label if not found

        # Removed score from the return string
        return f"{display_label}"
    except Exception as e:
        return f"❌ حدث خطأ أثناء تحليل المشاعر: {e}"
