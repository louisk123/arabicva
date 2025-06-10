import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor
import os

# Configuration
hf_token = os.environ.get("HF_TOKEN")
model_name = "UBC-NLP/AraT5-base-title-generation"  # Alternative model

try:
    # Initialize with slow tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_auth_token=hf_token,
        use_fast=False
    )
    
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        use_auth_token=hf_token
    )
    
    preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
    
    summarizer = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device="cpu"  # More reliable for deployment
    )
except Exception as e:
    st.error(f"Model loading failed: {str(e)}")
    st.stop()

def summarize_text(text):
    try:
        processed_text = preprocessor.preprocess(text)
        output = summarizer(
            processed_text,
            max_length=150,
            min_length=30,
            num_beams=3
        )
        return output[0]['generated_text']
    except Exception as e:
        st.error(f"Summarization error: {str(e)}")
        return None
