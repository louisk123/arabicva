import streamlit as st
from transformers import pipeline
from arabert.preprocess import ArabertPreprocessor

# Configuration - Using smaller model for stability
MODEL_NAME = "aubmindlab/aragpt2-base"

# Cache the preprocessor separately
@st.cache_resource
def load_preprocessor():
    return ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")

# Cache the model with explicit reload handling
@st.cache_resource(show_spinner=False)
def load_summarizer():
    try:
        return pipeline(
            "text-generation",
            model=MODEL_NAME,
            device="cpu",
            torch_dtype="auto"  # Better memory management
        )
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()  # Halt app if model fails to load

def perform_summarization_logic(text):
    if not text.strip():
        return None
        
    try:
        # Load cached components
        preprocessor = load_preprocessor()
        summarizer = load_summarizer()
        
        # Process and summarize
        processed_text = preprocessor.preprocess(text)
        output = summarizer(
            processed_text,
            max_new_tokens=80,  # Reduced further for stability
            num_beams=2,  # Fewer beams for less memory
            early_stopping=True,
            no_repeat_ngram_size=2,
            temperature=0.7  # More predictable outputs
        )
        return output[0]['generated_text']
    except Exception as e:
        st.error(f"Summarization error: {str(e)}")
        return None
