import streamlit as st
import google.generativeai as genai

# 1. Config
st.set_page_config(page_title="Gemini AI")

# 2. Get API Key from Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # שימוש בגרסה הכי מעודכנת וספציפית כדי למנוע 404
        # אם gemini-1.5-flash לא עבד, ננסה את השם המלא והרשמי
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Write something...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                # הוספת הגדרות ישירות לבקשה
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # כאן נראה בדיוק מה הבעיה אם זה נכשל
        st.error(f"Error Details: {str(e)}")
else:
    st.warning("Please add GOOGLE_API_KEY to Secrets.")
