import streamlit as st
from transformers import pipeline
from arabert.preprocess import ArabertPreprocessor

# CORRECT Arabic T5 model (public, no auth needed)
MODEL_NAME = "UBC-NLP/AraT5-base-title-generation"  

@st.cache_resource  # Cache model for performance
def load_model():
    preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
    summarizer = pipeline(
        "text2text-generation",
        model=MODEL_NAME,
        device="cpu"
    )
    return preprocessor, summarizer

def perform_summarization_logic(text):
    preprocessor, summarizer = load_model()
    processed_text = preprocessor.preprocess(text)
    return summarizer(
        processed_text,
        max_length=150,
        min_length=30,
        num_beams=3
    )[0]['generated_text']
