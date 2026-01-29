import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Fix")

# משיכת המפתח מה-Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # נסיון אחרון עם השם הכי גנרי שיש
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        user_input = st.chat_input("Say hello...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            response = model.generate_content(user_input)
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Tip: Try to create a NEW API Key in a NEW Project in AI Studio.")
else:
    st.warning("Please add the NEW API Key to Streamlit Secrets.")
