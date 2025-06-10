# sentiment_module.py

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch # For device handling

# --- Load and Cache Sentiment Model ---
@st.cache_resource
def get_camelbert_sentiment_pipeline():
    model_name = 'CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment'
    device = 0 if torch.cuda.is_available() else -1
    return pipeline('sentiment-analysis', model=model_name, device=device)

# Get the pipeline instance
_sentiment_analyzer = get_camelbert_sentiment_pipeline()

def perform_sentiment_analysis_logic(text_to_analyze: str) -> str:

    try:
        result = _sentiment_analyzer(text_to_analyze)[0]
        label = result['label']

        # Convert Labels to Arabic and add emoji
        display_label = {
            'negative': 'سلبي 😠',
            'neutral': 'محايد 😐',
            'positive': 'إيجابي 🤩'
        }.get(label, label) # Fallback to original label if not found

        return f"{display_label}"
    except Exception as e:
        return f"❌ حدث خطأ أثناء تحليل المشاعر: {e}"
