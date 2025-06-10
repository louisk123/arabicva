import streamlit as st
# Import functionalities from separate modules
from translation_module import perform_translation_logic
from sentiment_module import perform_sentiment_analysis_logic
from dialect_module import perform_dialect_detection_logic
from summarization_module import perform_summarization_logic
from lebanon_qa_module import answer_qa_lebanon
from rag_module import retrieve, answer_question, collection

# Place this function at the very top, before st.set_page_config
def clear_input_fields(exclude_key=None):
    """
    Clears all input-related session state variables except the one specified.
    """
    input_keys_to_clear = [
        'translation_input_text',
        'sentiment_input_text',
        'dialect_input_text',
        'summarization_input_text,
        "lebanon_qa_input_text";
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
col_main5, col_main1, col_main2, col_main3, col_main4 = st.columns(45

                                                                   
with col_maint:
    if st.button("وضع الترجمة 🌍", key="mode_lebanon_qa_button"):
        st.session_state.current_mode = "لبنان"
        clear_input_fields(exclude_key='lebanon_qa_input_text')
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

with col_main4:
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
    st.markdown("مصر, العراق, لبنان, المغرب, المملكة العربية السعودية, السودان, تونس")

    dialect_input_text = st.text_area("أدخل الجملة هنا:", height=150, key="dialect_input_text")

    if st.button("اكتشاف اللهجة", key="perform_dialect_button_inner"):
        if dialect_input_text:
            with st.spinner("جاري اكتشاف اللهجة..."):
                dialect = perform_dialect_detection_logic(dialect_input_text)
                if isinstance(dialect, str) and ("خطأ" in dialect or "تعذر الكشف عن اللغة" in dialect or "النص ليس باللغة العربية" in dialect):
                    st.error(dialect)
                else:
                    st.success(f"**:اللهجة المتوقعة:**\n\n {dialect}")
        else:
            st.warning("الرجاء إدخال نص لاكتشاف اللهجة.")

elif st.session_state.current_mode == "التلخيص":
    st.header("خدمة تلخيص النصوص العربية 📝")
    st.markdown("أدخل نصًا عربيًا طويلاً للحصول على ملخص له.")

    summarization_input_text = st.text_area("أدخل النص هنا:", height=200, key="summarization_input_text")

    # Removed the sliders for max_tokens and min_tokens

    if st.button("تلخيص النص", key="perform_summarization_button_inner"):
        if summarization_input_text:
            # Use default or fixed values for max_new_tokens and min_length
            # You can adjust these values directly here or keep them as constants in summarization_module
            default_max_new_tokens = 150
            default_min_length = 30

            if len(summarization_input_text.split()) < default_min_length: 
                st.warning(f"النص قصير جداً للتلخيص. يجب أن يحتوي على الأقل على {default_min_length} كلمة.")
            else:
                with st.spinner("جاري تلخيص النص..."):
                    summary_result = perform_summarization_logic(
                        summarization_input_text
                    )
                    if isinstance(summary_result, str) and "خطأ" in summary_result:
                        st.error(summary_result)
                    else:
                        st.success(f"**:الملخص:**\n\n{summary_result}")
        else:
            st.warning("الرجاء إدخال نص للتلخيص.")
            
elif st.session_state.current_mode == "لبنان":
    st.header("اسأل عن لبنان 🇱🇧")
    st.markdown("اكتب سؤالك هنا، وسأجيب عليه بناءً على قاعدة البيانات الخاصة بلبنان.")

    question_text = st.text_area("سؤالك:", height=150, key="lebanon_qa_input")

    if st.button("اسأل", key="ask_lebanon_button"):
        if question_text and len(question_text.strip()) > 5:
            with st.spinner("جاري البحث..."):
                retrieved_chunks = retrieve(question_text, collection)
                context = "\n".join(retrieved_chunks)
                answer = answer_qa_lebanon(question_text, context)
                st.markdown("### الإجابة:")
                st.success(answer)
        else:
            st.warning("من فضلك أدخل سؤالًا واضحًا.")

else:
    st.info("الرجاء النقر على أحد الأزرار الرئيسية أعلاه للبدء.")

# --- Optional: Footer ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
