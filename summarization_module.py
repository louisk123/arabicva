import streamlit as st
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from arabert.preprocess import ArabertPreprocessor

# 1. Use a smaller model that definitely works on Streamlit
MODEL_NAME = "aubmindlab/bert-base-arabertv02-twitter"  # Smaller Arabic model

# 2. Cache components separately with memory limits
@st.cache_resource(ttl=3600, max_entries=1)  # Cache for 1 hour
def load_preprocessor():
    return ArabertPreprocessor(model_name=MODEL_NAME)

@st.cache_resource(ttl=3600, max_entries=1, show_spinner=False)
def load_model_components():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        return pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device="cpu",
            framework="pt",
            torch_dtype="auto"
        )
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        st.stop()

def perform_summarization_logic(text):
    if not text or not isinstance(text, str) or len(text.strip()) < 10:
        return "الرجاء إدخال نص عربي أطول (10 أحرف على الأقل)"
    
    try:
        # Load with progress indicator
        with st.spinner("جاري تحميل النموذج..."):
            preprocessor = load_preprocessor()
            generator = load_model_components()
        
        # Process with strict length limits
        processed_text = preprocessor.preprocess(text)[:512]  # Truncate long inputs
        
        # Generate with conservative settings
        result = generator(
            processed_text,
            max_new_tokens=50,  # Very short output
            num_return_sequences=1,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            early_stopping=True
        )
        
        return result[0]['generated_text'].replace(processed_text, "")
    
    except Exception as e:
        st.error(f"خطأ في التلخيص: {str(e)}")
        return None
