import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor

# Use a compatible model
model_name = "UBC-NLP/AraT5-base-summarization"  

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
    
    summarizer = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device="cpu"  # Ensures compatibility
    )
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    st.stop()

def summarize(text):
    processed_text = preprocessor.preprocess(text)
    output = summarizer(processed_text, max_length=150, min_length=30)
    return output[0]['generated_text']
