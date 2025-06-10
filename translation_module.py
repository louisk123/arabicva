# translation_module.py

import streamlit as st
import re
from deep_translator import GoogleTranslator

# --- Where to Load Libraries and Cache Models ---
# Libraries for this module are loaded directly here.
# Heavy resources (like the GoogleTranslator instance) are cached here
# using @st.cache_resource, so they only load once.

@st.cache_resource
def get_google_translator_instance(source,target):
    return GoogleTranslator(source,target)

# Helper function to detect if text is Arabic or English
def is_arabic(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))

def perform_translation_logic(text_to_translate: str) -> str:
    translator = get_google_translator_instance() # Get the cached translator instance

    # Detect language using the local helper function and use text_to_translate
    if is_arabic(text_to_translate):
        translator = get_google_translator_instance('ar','en') # Get the cached translator instance
    else:
        translator = get_google_translator_instance('en','ar') # Get the cached translator instance

    try:
        # Perform translation
        translation_result = translator.translate(text)
        return translation_result
    except Exception as e:
        return f"❌ حدث خطأ أثناء الترجمة: {e}"

