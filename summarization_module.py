import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor
import torch
import os

model_name = "malmarjeh/t5-arabic-text-summarization"
preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")  # use a valid AraBERT model for preprocessing

tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, token=hf_token)
summarizer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
hf_token = os.environ.get("HF_TOKEN")

def summarize_text(text, max_new_tokens=150, min_length=30):
    # Preprocess text with Arabert
    text = preprocessor.preprocess(text)

    result = summarizer(
        text,
        max_new_tokens=max_new_tokens, 
        min_length=min_length,
        num_beams=3,
        repetition_penalty=3.0,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        pad_token_id=tokenizer.eos_token_id,
    )[0]['generated_text']

    return result

# Remove fixed_max_new_tokens and fixed_min_length from function signature
def perform_summarization_logic(text):
    try:
        summary_result = summarize_text(text)
        return summary_result
    except Exception as e:
        return f"خطأ أثناء تلخيص النص: {e}"
