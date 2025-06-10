# streamlit_app.py

import streamlit as st
# Import your translation function from the new module
from translation_module import perform_translation_logic

# --- 1. Set Page Configuration ---
st.set_page_config(
    page_title="مساعد متعدد الوظائف",
    page_icon="🤖",
    layout="centered"
)

# --- Initialize Session State for Mode Management ---
# This helps keep track of which main function is active
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None # No mode selected initially

# --- 2. Display App Title and Main Mode Selection Buttons ---
st.title("مساعد اللغة العربية 🤖")
st.markdown("اختر الوظيفة التي ترغب في استخدامها.")

# Create main buttons for mode selection
col_main1, col_main2 = st.columns(2)

with col_main1:
    if st.button("وضع التحية 👋", key="mode_greeting_button"):
        st.session_state.current_mode = "التحية"
        # Reset any previous input from other modes if necessary (optional)
        if 'translation_input_text' in st.session_state:
            st.session_state.translation_input_text = ""

with col_main2:
    if st.button("وضع الترجمة 🌍", key="mode_translation_button"):
        st.session_state.current_mode = "الترجمة"
        # Reset any previous input from other modes if necessary (optional)
        if 'greeting_response_message' in st.session_state:
            st.session_state.greeting_response_message = ""

st.markdown("---") # Separator line

# --- 3. Render Functionality Sections Based on Selected Mode ---

if st.session_state.current_mode == "التحية":
    st.header("التحية 👋")
    st.markdown("اختر تحية وسأرد عليها.")

    # Initialize a variable to hold the response message for greetings
    if 'greeting_response_message' not in st.session_state:
        st.session_state.greeting_response_message = ""

    col_greet1, col_greet2 = st.columns(2) # Columns for greeting sub-buttons

    with col_greet1:
        if st.button("قل مرحباً", key="say_hi_button"):
            st.session_state.greeting_response_message = "مرحباً!"

    with col_greet2:
        if st.button("قل أهلاً", key="say_hello_button"):
            st.session_state.greeting_response_message = "أهلاً بك!"

    # Display the greeting response
    if st.session_state.greeting_response_message:
        st.write(st.session_state.greeting_response_message)
    else:
        st.info("الرجاء اختيار تحية من الأزرار أعلاه.")

elif st.session_state.current_mode == "الترجمة":
    st.header("خدمة الترجمة (عربي ↔ إنجليزي) 🌍")
    st.markdown("أدخل النص الذي ترغب في ترجمته. سيكتشف النظام اللغة تلقائياً.")

    text_to_translate = st.text_area("أدخل النص هنا:", height=150, key="translation_input_text")

    if st.button("ترجمة / Translate", key="perform_translation_button"):
        if text_to_translate:
            with st.spinner("جاري الترجمة..."):
                translation_result = perform_translation_logic(text_to_translate)
                st.success(f"**الترجمة:**\n{translation_result}")
        else:
            st.warning("الرجاء إدخال نص للترجمة.")

else: # Initial state, no mode selected
    st.info("الرجاء النقر على أحد الأزرار الرئيسية أعلاه للبدء.")

# --- Optional: Footer ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
