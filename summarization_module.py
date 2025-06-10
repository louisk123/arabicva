import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from arabert.preprocess import ArabertPreprocessor
import torch

model_name = "malmarjeh/t5-arabic-text-summarization"

@st.cache_resource
def load_summarization_model():
    try:
        # Load preprocessor with a valid AraBERT model
        preprocessor = ArabertPreprocessor(model_name="aubmindlab/bert-base-arabertv02")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        # Use 'cpu' if MPS is not available or preferred
        device = 0 if torch.cuda.is_available() else -1
        summarizer_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=device)
        return preprocessor, summarizer_pipeline, tokenizer
    except Exception as e:
        st.error(f"Failed to load summarization model: {e}.")
        return None, None, None

preprocessor, summarizer_pipeline, tokenizer = load_summarization_model()


def perform_summarization_logic(text, max_new_tokens=150, min_length=30):
    if preprocessor is None or summarizer_pipeline is None or tokenizer is None:
        return "خطأ: نموذج التلخيص غير محمل.", 0.0 # Return similar to other modules

    try:
        # Preprocess text with Arabert
        processed_text = preprocessor.preprocess(text)

        summary_result = summarizer_pipeline(
            processed_text,
            max_new_tokens=max_new_tokens,
            min_length=min_length,
            num_beams=3,
            repetition_penalty=3.0,
            length_penalty=1.0,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id,
        )[0]['generated_text']

        return summary_result
    except Exception as e:
        return f"خطأ أثناء تلخيص النص: {e}"
