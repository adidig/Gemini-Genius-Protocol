import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# 1. Page Configuration
gemini_icon = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304651130.png"
st.set_page_config(page_title="Gemini Stable", page_icon=gemini_icon, layout="centered")

# 2. Advanced CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #131314; color: #e3e3e3; }}
    .stChatMessage {{ background-color: #1e1f20; border-radius: 24px; padding: 12px 18px; margin: 10px 0; border: none; }}
    .stChatInputContainer {{ bottom: 20px !important; border-radius: 28px !important; background-color: #1e1f20 !important; }}
    div[data-testid="stHeader"] {{ display: none; }}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# 3. Protocol Setup
SYSTEM_PROMPT = "Answer in the user's language. Start with '🇮🇱 Gemini תשובת'. Put 📝 before text. End with '🇮🇱 Gemini שאלת'."

# 4. API Key Retrieval
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Google AI API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # שימוש במודל המעודכן ביותר לפתרון שגיאת 404
        model = genai.GenerativeModel("gemini-1.5-flash-latest", system_instruction=SYSTEM_PROMPT)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        col_input, col_mic = st.columns([0.85, 0.15])
        with col_mic:
            voice_query = speech_to_text(language='he', start_prompt="🎤", just_once=True, key="mic_button")
        with col_input:
            text_query = st.chat_input("Ask Gemini anything...")

        final_query = voice_query if voice_query else text_query

        if final_query:
            st.session_state.messages.append({"role": "user", "content": final_query})
            with st.chat_message("user"):
                st.markdown(final_query)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(final_query)
                    full_response = response.text
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
else:
    st.info("Please enter your API Key in the sidebar or add it to Secrets.")
