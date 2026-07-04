import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Set API Key directly (Put your real key inside the quotes!)
os.environ["GEMINI_API_KEY"] = "AIzaSyBbYac0ZmBaJLg6kQhjxUcq-5lJmoTDlWU"

# 2. Initialize Client
client = genai.Client()

# 3. Web Page Styling Setup
st.set_page_config(page_title="JARVIS AI", page_icon="🤖", layout="centered")
st.title("🤖 JARVIS Assistant")
st.caption("Online and ready, sir.")

# 4. Keep memory active across web pages
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display past chat history smoothly as normal text
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. User typing interaction loop
if user_input := st.chat_input("How can I help you, sir?"):
    # Display what you typed
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get clean AI response
    with st.chat_message("assistant"):
        config = types.GenerateContentConfig(
            system_instruction="You are JARVIS, a polite, highly intelligent AI assistant. Speak directly in clean, plain human text sentences. Do not use code markdown syntax style blocks for conversation.",
            temperature=0.7
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=config
        )
        
        # Pull text string cleanly
        ai_response = response.text
        st.write(ai_response)
        
    # Save text response to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
