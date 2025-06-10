# translation_module.py

import streamlit as st
import re
from deep_translator import GoogleTranslator

# Heavy resources (like the GoogleTranslator instance) are cached here
# using @st.cache_resource, so they only load once.

@st.cache_resource
def get_google_translator_instance():
    return GoogleTranslator()

# Helper function for Arabic language detection
def _is_arabic(text: str) -> bool:
    #Checks if the given text contains Arabic characters.
    return bool(re.search(r'[\u0600-\u06FF]', text))

def perform_translation_logic(text_to_translate: str) -> str:
    """
    Performs translation of the given text, detecting source language automatically.
    """
    translator = get_google_translator_instance() # Get the cached translator instance

    # Determine source and target language
    source_lang = 'ar' if _is_arabic(text_to_translate) else 'en'
    target_lang = 'en' if source_lang == 'ar' else 'ar'

    try:
        # Perform translation using the cached translator instance
        translation_result = translator.translate(text_to_translate, source=source_lang, target=target_lang)
        return translation_result
    except Exception as e:
        return f"❌ حدث خطأ أثناء الترجمة: {e}"
