# streamlit_app.py

import streamlit as st
from translation_module import perform_translation_logic 

# --- 1. Set Page Configuration ---
st.set_page_config(
    page_title="مساعد متعدد الوظائف",
    page_icon="🤖",
    layout="centered"
)

# --- 2. Display App Title and Main Navigation ---
st.title("مساعد اللغة العربية 🤖")
st.markdown("اختر وظيفة من القائمة الجانبية.")

selected_function = st.sidebar.selectbox(
    "اختر الوظيفة:",
    ("التحية", "الترجمة"),
    index=0
)

# --- 3. Functionality ---

if selected_function == "التحية":
    st.header("التحية 👋")
    st.markdown("اختر تحية وسأرد عليها.")

    greeting_response_message = ""
    col1, col2 = st.columns(2)

    with col1:
        if st.button("قل مرحباً", key="say_hi_button"):
            greeting_response_message = "مرحباً!"

    with col2:
        if st.button("قل أهلاً", key="say_hello_button"):
            greeting_response_message = "أهلاً بك!"

    if greeting_response_message:
        st.write(greeting_response_message)
    else:
        st.info("الرجاء اختيار تحية من الأزرار أعلاه.")

elif selected_function == "الترجمة":
    st.header("خدمة الترجمة (عربي ↔ إنجليزي) 🌍")
    st.markdown("أدخل النص الذي ترغب في ترجمته. سيكتشف النظام اللغة تلقائياً.")

    text_to_translate = st.text_area("أدخل النص هنا:", height=150, key="translation_input_text")

    if st.button("ترجمة / Translate", key="perform_translation_button"):
        if text_to_translate:
            with st.spinner("جاري الترجمة..."):
                # Call the translation logic from the separate module
                translation_result = perform_translation_logic(text_to_translate)
                st.success(f"**الترجمة:**\n{translation_result}")
        else:
            st.warning("الرجاء إدخال نص للترجمة.")

# --- Optional: Footer ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
