import streamlit as st
from google import genai
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="PersonalBot",
    layout="centered"
)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in Render Environment Variables.")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.5-flash"

# ---------------- UI ----------------
st.title("🤖 PersonalBot")
st.markdown("An intelligent assistant powered by **Gemini + Streamlit**")

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- GEMINI FUNCTION ----------------
def get_gemini_response(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

# ---------------- CHAT DISPLAY ----------------
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                bot_response = get_gemini_response(user_input)
            except Exception as e:
                bot_response = f"Error: {e}"

        st.markdown(bot_response)

    st.session_state.history.append(("assistant", bot_response))
