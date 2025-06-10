import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ✅ Lightweight model that supports Arabic summarization
MODEL_NAME = "google/mt5-small"

@st.cache_resource(ttl=3600)
def load_model_components():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )

def perform_summarization_logic(text):
    try:
        summarizer = load_model_components()
        result = summarizer(
            text,
            max_length=100,
            min_length=30,
            do_sample=False
        )
        return result[0]["summary_text"]
    except Exception as e:
        return f"حدث خطأ أثناء التلخيص: {str(e)}"
