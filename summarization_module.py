import streamlit as st
from transformers import pipeline
from arabert.preprocess import ArabertPreprocessor

# 1. Use a compatible model that doesn't require SentencePiece
MODEL_NAME = "aubmindlab/aragpt2-base"  # Alternative Arabic model

@st.cache_resource
def load_components():
    # 2. Initialize components
    preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
    
    # 3. Load model (simplified pipeline)
    summarizer = pipeline(
        "text-generation",  # Changed from text2text-generation
        model=MODEL_NAME,
        device="cpu"
    )
    return preprocessor, summarizer

def perform_summarization_logic(text):
    try:
        preprocessor, summarizer = load_components()
        processed_text = preprocessor.preprocess(text)
        
        # Adjusted parameters for GPT-style model
        output = summarizer(
            processed_text,
            max_new_tokens=100,  # Reduced length for GPT
            num_beams=3,
            no_repeat_ngram_size=2
        )
        return output[0]['generated_text']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

