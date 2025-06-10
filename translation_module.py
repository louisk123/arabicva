# translation_module.py

import streamlit as st
import re
from deep_translator import GoogleTranslator

# --- Where to Load Libraries and Cache Models ---
# Libraries for this module are loaded directly here.
# Heavy resources (like the GoogleTranslator instance) are cached here
# using @st.cache_resource, so they only load once.

@st.cache_resource
def get_google_translator_instance():
    """
    Initializes and caches the GoogleTranslator instance.
    This function should only be called once across the app's lifetime.
    """
    return GoogleTranslator()

# Helper function to detect if text is Arabic or English
def _is_arabic(text: str) -> bool:
    """
    Checks if the given text contains Arabic characters.
    """
    return bool(re.search(r'[\u0600-\u06FF]', text))

def perform_translation_logic(text_to_translate: str) -> str:
    """
    Performs translation of the given text, detecting source language automatically.
    """
    translator = get_google_translator_instance() # Get the cached translator instance

    # Detect language using the local helper function and use text_to_translate
    if _is_arabic(text_to_translate):
        source_lang = 'ar'
        target_lang = 'en'
    else:
        source_lang = 'en'
        target_lang = 'ar'

    try:
        # Perform translation using the cached translator instance's translate method
        translation_result = translator.translate(text_to_translate, source=source_lang, target=target_lang)
        return translation_result
    except Exception as e:
        return f"❌ حدث خطأ أثناء الترجمة: {e}"

