# translation_module.py

import streamlit as st
import re
from deep_translator import GoogleTranslator

# Heavy resources (like the GoogleTranslator instance) are cached here
# using @st.cache_resource, so they only load once.

@st.cache_resource
def get_google_translator_instance(source,target):
    return GoogleTranslator(source,target)

# Fucntion to detetc is text is Arabic or English
def _is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def perform_translation_logic(text_to_translate):
    
    # Detect language
    if is_arabic(question):
       translator = get_google_translator_instance(source='ar', target='en')
     else:
       translator = get_google_translator_instance(source='en', target='ar')

    try:
        translation_result = translation = translator.translate(question)
        return translation_result
    except Exception as e:
        return f"❌ حدث خطأ أثناء الترجمة: {e}"
