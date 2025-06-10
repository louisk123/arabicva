import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor
import torch
import os

model_name = "malmarjeh/t5-arabic-text-summarization"
arabert_preprocessor_model_name = "aubmindlab/bert-base-arabertv02"

hf_token = os.environ.get("HF_TOKEN")

@st.cache_resource
def load_summarization_model():
    if not hf_token: # Check if token is available
        st.error("خطأ: لم يتم العثور على رمز Hugging Face (HF_TOKEN) في Secrets. يرجى إضافته.")
        return None, None, None

    try:
        preprocessor = ArabertPreprocessor(model_name=arabert_preprocessor_model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, token=hf_token)

        device = 0 if torch.cuda.is_available() else -1

        # Define default generation arguments and pass them to the pipeline
        default_generate_kwargs = {
            "max_new_tokens": 150,  
            "min_length": 30,
            "num_beams": 3,
            "repetition_penalty": 3.0,
            "length_penalty": 1.0,
            "no_repeat_ngram_size": 3,
            "pad_token_id": tokenizer.eos_token_id,
        }

        # Pass generate_kwargs to the pipeline
        summarizer_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device,
            token=hf_token,
            generate_kwargs=default_generate_kwargs 
        )
        return preprocessor, summarizer_pipeline, tokenizer
    except Exception as e:
        st.error(f"فشل تحميل نموذج التلخيص: {e}. يرجى التأكد من صحة رمز Hugging Face والتبعيات.")
        return None, None, None

preprocessor, summarizer_pipeline, tokenizer = load_summarization_model()

# Remove fixed_max_new_tokens and fixed_min_length from function signature
def perform_summarization_logic(text):
    if preprocessor is None:
        return "preprocessor error."

    if summarizer_pipeline is None:
        return "summarizer_pipeline error."
        
    if tokenizer is None:
        return "tokenizer error."

    try:
        processed_text = preprocessor.preprocess(text)

        summary_result = summarizer_pipeline(processed_text)[0]['generated_text']

        return summary_result
    except Exception as e:
        return f"خطأ أثناء تلخيص النص: {e}"
