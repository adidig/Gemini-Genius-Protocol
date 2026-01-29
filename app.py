import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# 1. Page Config
st.set_page_config(page_title="Gemini Stable", layout="centered")

# 2. API Key Retrieval
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # ניסיון התחברות למודל Pro - הכי יציב שיש
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        text_query = st.chat_input("Ask me something...")
        voice_query = speech_to_text(language='he', start_prompt="🎤", key="mic")

        final_query = voice_query if voice_query else text_query

        if final_query:
            st.session_state.messages.append({"role": "user", "content": final_query})
            with st.chat_message("user"):
                st.markdown(final_query)

            with st.chat_message("assistant"):
                # הוספת הפרוטוקול ישירות לשאלה
                prompt = f"Answer in Hebrew. Start with '🇮🇱 Gemini תשובת'. {final_query}"
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("Please enter your API Key.")
