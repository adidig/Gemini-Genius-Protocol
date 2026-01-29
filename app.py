import streamlit as st
import google.generativeai as genai

# 1. Config
st.set_page_config(page_title="Gemini Stable")

# 2. API Key from Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # נשתמש ב-gemini-pro כי הוא הכי וותיק ויציב
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask me something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please add GOOGLE_API_KEY to your Secrets.")
