import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor
import os

# Get Hugging Face token - make sure this is set in your environment variables
hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    st.error("HF_TOKEN environment variable not set!")
    st.stop()

model_name = "malmarjeh/t5-arabic-text-summarization"

try:
    # Initialize preprocessor
    preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
    
    # Load tokenizer and model with auth token
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, use_auth_token=hf_token)
    
    # Create summarization pipeline
    summarizer = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    st.stop()

def summarize_text(text, max_new_tokens=150, min_length=30):
    try:
        # Preprocess text with Arabert
        text = preprocessor.preprocess(text)

        result = summarizer(
            text,
            max_length=max_new_tokens,  # Changed from max_new_tokens to max_length
            min_length=min_length,
            num_beams=3,
            repetition_penalty=3.0,
            length_penalty=1.0,
            no_repeat_ngram_size=3,
        )[0]['generated_text']

        return result
    except Exception as e:
        st.error(f"Summarization error: {str(e)}")
        return None

def perform_summarization_logic(text):
    if not text.strip():
        return "الرجاء إدخال نص لتلخيصه"
    
    try:
        return summarize_text(text)
    except Exception as e:
        st.error(f"Error during summarization: {str(e)}")
        return None
