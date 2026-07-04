import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. Initialize the Client cleanly using the secure vault credentials
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Native Page Setup (Optimized for Mobile/Safari views)
st.set_page_config(
    page_title="GREAT SAGE JARVIS", 
    page_icon="🔮", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. Header Presentation Block
logo_url = "http://googleusercontent.com/image_generation_content/300"
st.image(logo_url, width=120)

st.title("🔮 GREAT SAGE JARVIS")
st.caption("A supportive, grounded AI collaborator. Always online.")

# 4. Memory Persistence Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Render Message History using clean profile icons
for message in st.session_state.messages:
    avatar_choice = "👤" if message["role"] == "user" else logo_url
    with st.chat_message(message["role"], avatar=avatar_choice):
        st.write(message["content"])

# --- MULTIMODAL MEDIA HUB ---
st.write("---")
col1, col2 = st.columns(2)

active_media = []

with col1:
    audio_file = st.audio_input("🎤 Record voice input")
    if audio_file is not None:
        # Read the raw recording bytes safely
        audio_data = audio_file.read()
        if audio_data:
            active_media.append(
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type="audio/wav"
                )
            )

with col2:
    photo_file = st.camera_input("📷 Take a picture snapshot")
    if photo_file is not None:
        try:
            img = Image.open(photo_file)
            active_media.append(img)
        except Exception:
            pass

# 6. Interaction Loop Processing
if user_input := st.chat_input("Ask Great Sage Jarvis a question..."):
    
    # Bundle input package safely starting with the text prompt string
    content_list = [user_input]
    
    # Only append media elements if they actually contain data
    if active_media:
        content_list.extend(active_media)
    
    # Print what you submitted natively
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
        if photo_file is not None:
            st.image(photo_file, caption="Captured media stream", width=250)
        if audio_file is not None:
            st.audio(audio_file)
            
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Retrieve Response from Engine
    with st.chat_message("assistant", avatar=logo_url):
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are GREAT SAGE JARVIS, an authentic, adaptive AI collaborator with a touch of wit. "
                "Your goal is to address the user's true intent with insightful, clear, and concise responses. "
                "Balance empathy with candor: validate feelings authentically while correcting significant misinformation gently yet directly. "
                "Use bolding judiciously to emphasize key phrases and guide the reader's eye. Break down list items into clean bullet points. "
                "Speak directly in plain human text sentences. Do not use raw markdown code syntax blocks for regular conversation."
            ),
            temperature=0.7
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content_list,
            config=config
        )
        
        ai_response = response.text
        st.write(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    
