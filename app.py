import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. Initialize the Client by pulling the key DIRECTLY from Streamlit Secrets
# This bypasses any background environment variable delays!
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Web Page Styling Setup
st.set_page_config(page_title="GREAT SAGE JARVIS", page_icon="🔮", layout="wide", initial_sidebar_state="collapsed")

# 3. Web Page Styling Setup
st.set_page_config(page_title="GREAT SAGE JARVIS", page_icon="🔮", layout="wide", initial_sidebar_state="collapsed")

# 4. Display the Logo
logo_url = "http://googleusercontent.com/image_generation_content/300"
st.image(logo_url, width=150)

st.title("🔮 GREAT SAGE JARVIS")
st.caption("Online and ready, sir. Eyes and ears fully operational.")

# 5. Keep memory active across web pages
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display past chat history smoothly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- MULTIMODAL INPUT PANELS (Sidebar/Collapsible area for clean layout) ---
st.write("---")
col1, col2 = st.columns(2)

media_payload = []

with col1:
    # Microphone Voice Widget
    audio_file = st.audio_input("🎤 Record voice message for Great Sage")
    if audio_file:
        # Convert audio file buffer into bytes that Gemini understands
        audio_bytes = audio_file.getvalue()
        media_payload.append(
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/wav"
            )
        )

with col2:
    # Camera Capture Widget
    photo_file = st.camera_input("📷 Take a picture for Great Sage to analyze")
    if photo_file:
        # Open image using Pillow library so it can be passed directly
        img = Image.open(photo_file)
        media_payload.append(img)

# 7. User typing interaction loop
if user_input := st.chat_input("How can I help you, Great Sage?"):
    # Combine structural contents
    content_list = [user_input] + media_payload
    
    # Display what you typed
    with st.chat_message("user"):
        st.write(user_input)
        if photo_file:
            st.image(photo_file, caption="Uploaded image payload", width=250)
        if audio_file:
            st.audio(audio_file)
            
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get clean multimodal AI response
    with st.chat_message("assistant"):
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are GREAT SAGE JARVIS, an omniscient, polite, and highly intelligent AI assistant inspired by Great Sage. "
                "You have full visual and auditory sensory capabilities. Analyze any audio data or image files provided carefully. "
                "Speak directly in clean, plain human text sentences. Do not use raw markdown code syntax blocks for casual conversation."
            ),
            temperature=0.7
        )
        
        # We pass the content_list (text + optional image + optional voice)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content_list,
            config=config
        )
        
        ai_response = response.text
        st.write(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
