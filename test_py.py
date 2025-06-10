import streamlit as st
# Import functionalities from separate modules
from translation_module import perform_translation_logic
from sentiment_module import perform_sentiment_analysis_logic
from dialect_module import perform_dialect_detection_logic
from summarization_module import perform_summarization_logic # New import for summarization

# Place this function at the very top, before st.set_page_config
def clear_input_fields(exclude_key=None):
    """
    Clears all input-related session state variables except the one specified.
    """
    input_keys_to_clear = [
        'translation_input_text',
        'sentiment_input_text',
        'dialect_input_text',
        'summarization_input_text' # Add new summarization input key
    ]
    for key in input_keys_to_clear:
        if key != exclude_key and key in st.session_state:
            st.session_state[key] = ""


# --- 1. Set Page Configuration ---
st.set_page_config(
    page_title="مساعد متعدد الوظائف",
    page_icon="🤖",
    layout="centered"
)

# --- 2. Display App Title and Main Mode Selection Buttons ---
st.title("مساعد اللغة العربية 🤖")
st.markdown("اختر الوظيفة التي ترغب في استخدامها.")

# Initialize session state for mode management if not already set
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None

# Create main buttons for mode selection
col_main1, col_main2, col_main3, col_main4 = st.columns(4) # Added a 4th column

with col_main1:
    if st.button("وضع الترجمة 🌍", key="mode_translation_button"):
        st.session_state.current_mode = "الترجمة"
        clear_input_fields(exclude_key='translation_input_text')

with col_main2:
    if st.button("تحليل المشاعر 😊", key="mode_sentiment_button"):
        st.session_state.current_mode = "المشاعر"
        clear_input_fields(exclude_key='sentiment_input_text')

with col_main3:
    if st.button("اكتشاف اللهجة 🗣️", key="mode_dialect_button"):
        st.session_state.current_mode = "اللهجة"
        clear_input_fields(exclude_key='dialect_input_text')

with col_main4: # New button for summarization
    if st.button("تلخيص النص 📝", key="mode_summarization_button"):
        st.session_state.current_mode = "التلخيص"
        clear_input_fields(exclude_key='summarization_input_text')


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
                if isinstance(dialect, str) and ("خطأ" in dialect or "تعذر الكشف عن اللغة" in dialect or "النص ليس باللغة العربية" in dialect):
                    st.error(dialect)
                else:
                    st.success(f"**:اللهجة المتوقعة:** {dialect} (الاحتمالية: {confidence:.2%})")
        else:
            st.warning("الرجاء إدخال نص لاكتشاف اللهجة.")

elif st.session_state.current_mode == "التلخيص": # New mode for summarization
    st.header("خدمة تلخيص النصوص العربية 📝")
    st.markdown("أدخل نصًا عربيًا طويلاً للحصول على ملخص له.")

    summarization_input_text = st.text_area("أدخل النص هنا:", height=200, key="summarization_input_text")

    # Optional parameters for summarization
    col_sum_params1, col_sum_params2 = st.columns(2)
    with col_sum_params1:
        max_tokens = st.slider("الحد الأقصى للكلمات في الملخص:", min_value=50, max_value=500, value=150, step=10)
    with col_sum_params2:
        min_tokens = st.slider("الحد الأدنى للكلمات في الملخص:", min_value=10, max_value=max_tokens, value=30, step=5)


    if st.button("تلخيص النص", key="perform_summarization_button_inner"):
        if summarization_input_text:
            if len(summarization_input_text.split()) < min_tokens:
                st.warning(f"النص قصير جداً للتلخيص. يجب أن يحتوي على الأقل على {min_tokens} كلمة.")
            else:
                with st.spinner("جاري تلخيص النص..."):
                    summary_result = perform_summarization_logic(
                        summarization_input_text,
                        max_new_tokens=max_tokens,
                        min_length=min_tokens
                    )
                    if isinstance(summary_result, str) and "خطأ" in summary_result:
                        st.error(summary_result)
                    else:
                        st.success(f"**:الملخص:**\n\n{summary_result}")
        else:
            st.warning("الرجاء إدخال نص للتلخيص.")

else:
    st.info("الرجاء النقر على أحد الأزرار الرئيسية أعلاه للبدء.")

# --- Optional: Footer ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
