# streamlit_app.py

import streamlit as st
# Import functionalities from separate modules
from translation_module import perform_translation_logic
from sentiment_module import perform_sentiment_analysis_logic
from dialect_module import perform_dialect_detection_logic


def clear_input_fields(exclude_key=None):
    """
    Clears all input-related session state.
    """
    input_keys_to_clear = [
        'translation_input_text',
        'sentiment_input_text',
        'dialect_input_text'
    ]
    for key in input_keys_to_clear:
        if key != exclude_key and key in st.session_state:
            st.session_state[key] = ""


# --- 1. Set Page Configuration ---
st.set_page_config(
    page_title="مساعد متعدد الوظائف", # Updated page title
    page_icon="🤖",                   # Updated favicon
    layout="centered"                 # Page layout
)

# --- 2. Display App Title and Main Mode Selection Buttons ---
st.title("مساعد اللغة العربية 🤖")
st.markdown("اختر الوظيفة التي ترغب في استخدامها.")

# Initialize session state for mode management if not already set
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None

# Create main buttons for mode selection
col_main1, col_main2 ,col_main3 = st.columns(3)
# Place this function at the top of your streamlit_app.py, perhaps after st.set_page_config



with col_main1:
    if st.button("وضع الترجمة 🌍", key="mode_translation_button"):
        st.session_state.current_mode = "الترجمة"
        clear_input_fields(exclude_key='translation_input_text') # Clear all except translation

with col_main2:
    if st.button("تحليل المشاعر 😊", key="mode_sentiment_button"):
        st.session_state.current_mode = "المشاعر"
        clear_input_fields(exclude_key='sentiment_input_text') # Clear all except sentiment

with col_main3:
    if st.button("اكتشاف اللهجة 🗣️", key="mode_dialect_button"):
        st.session_state.current_mode = "اللهجة"
        clear_input_fields(exclude_key='dialect_input_text') # Clear all except dialect

st.markdown("---") # Separator line

# --- 3. Render Functionality Sections Based on Selected Mode ---

if st.session_state.current_mode == "الترجمة":
    st.header("خدمة الترجمة (عربي ↔ إنجليزي) 🌍")
    st.markdown("أدخل النص الذي ترغب في ترجمته. سيكتشف النظام اللغة تلقائياً ويقوم بترجمته.")

    text_to_translate = st.text_area("أدخل النص هنا:", height=150, key="translation_input_text")

    if st.button("ترجمة / Translate", key="perform_translation_button_inner"):
        if text_to_translate:
            with st.spinner("جاري الترجمة..."):
                translation_result = perform_translation_logic(text_to_translate)
                st.success(f"**:الترجمة**\n\n{translation_result}")
        else:
            st.warning("الرجاء إدخال نص للترجمة.")

elif st.session_state.current_mode == "المشاعر":
    st.header("تحليل المشاعر (إيجابي، سلبي، محايد) 😊")
    st.markdown("أدخل جملة عربية لتحليل المشاعر فيها.")

    sentiment_input_text = st.text_area("أدخل الجملة هنا:", height=150, key="sentiment_input_text")

    if st.button("تحليل المشاعر", key="perform_sentiment_button_inner"):
        if sentiment_input_text:
            with st.spinner("جاري تحليل المشاعر..."):
                sentiment_label_display = perform_sentiment_analysis_logic(sentiment_input_text)
                st.success(f"**:المشاعر المتوقعة**\n\n{sentiment_label_display}")
        else:
            st.warning("الرجاء إدخال نص لتحليل المشاعر.")

elif st.session_state.current_mode == "اللهجة":
    st.header("اكتشاف اللهجة العربية 🗣️")
    st.markdown("أدخل جملة عربية لاكتشاف لهجتها.")

    dialect_input_text = st.text_area("أدخل الجملة هنا:", height=150, key="dialect_input_text")

    if st.button("اكتشاف اللهجة", key="perform_dialect_button_inner"):
        if dialect_input_text:
            with st.spinner("جاري اكتشاف اللهجة..."):
                dialect, confidence = perform_dialect_detection_logic(dialect_input_text)
                if "Error" in dialect: # Check for specific error message from the dialect module
                    st.error(dialect)
                else:
                    st.success(f"**:اللهجة المتوقعة:** {dialect} (الاحتمالية: {confidence:.2%})")
        else:
            st.warning("الرجاء إدخال نص لاكتشاف اللهجة.")

else: 
    st.info("الرجاء النقر على أحد الأزرار الرئيسية أعلاه للبدء.")


# --- Optional: Footer ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
