import streamlit as st

# --- 1. Set Page Configuration (Optional, but good practice) ---
st.set_page_config(
    page_title="مساعد التحية البسيط", # Page title in browser tab
    page_icon="👋",                  # Favicon
    layout="centered"                # Page layout
)

# --- 2. Display the App Title and Introduction ---
st.title("مساعد التحية البسيط 👋")
st.markdown("اختر تحية وسأرد عليها.")

# --- 3. Create Options for the User as Buttons ---
# We'll use st.button() for each greeting.
# The button returns True when clicked, so we check that.

# Initialize a variable to hold the response message
response_message = ""

col1, col2 = st.columns(2) # Create two columns for buttons

with col1:
    if st.button("قل مرحباً", key="say_hi_button"):
        response_message = "مرحباً!"

with col2:
    if st.button("قل أهلاً", key="say_hello_button"):
        response_message = "أهلاً بك!"

# --- 4. Logic to Respond Based on Button Clicks ---
# Display the response if a button was clicked
if response_message:
    st.write(response_message)
else:
    st.info("الرجاء اختيار تحية من الأزرار أعلاه.") # Provide a hint if no button clicked yet

# --- Optional: Add a footer or other elements ---
st.markdown("---")
st.caption("مساعد بسيط تم إنشاؤه باستخدام Streamlit.")
