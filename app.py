import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. Initialize the Client directly from Streamlit Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Page Configuration
st.set_page_config(
    page_title="GREAT SAGE JARVIS", 
    page_icon="🔮", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. Custom CSS to injection: Changes backgrounds, borders, and fonts
st.markdown("""
<style>
    /* Main background theme */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Input field customization */
    .stChatInputContainer > div {
        background-color: #161b22 !important;
        border: 1px solid #58a6ff !important;
        border-radius: 8px;
    }
    
    /* Font style inside input box */
    [data-testid="stChatInput"] {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Media box separation layout line */
    hr {
        border-color: #30363d !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. Interface Header Elements
logo_url = "http://googleusercontent.com/image_generation_content/300"
st.image(logo_url, width=120)

st.title("🔮 GREAT SAGE JARVIS")
st.caption("SYSTEM STATE: ACTIVE // SENSORY LOGS: ONLINE")

# 5. Keep memory active across web pages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Avatar image settings
USER_AVATAR = "👤"
ASSISTANT_AVATAR = logo_url

# 6. Display past chat history smoothly with custom avatars
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# --- MULTIMODAL INPUT PANELS ---
st.write("---")
col1, col2 = st.columns(2)

active_audio_part = None
active_image_part = None

with col1:
    audio_file = st.audio_input("🎤 Sync Audio Core")
    if audio_file is not None:
        audio_bytes = audio_file.getvalue()
        active_audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/wav"
        )

with col2:
    photo_file = st.camera_input("📷 Sync Visual Feed")
    if photo_file is not None:
        active_image_part = Image.open(photo_file)

# 7. User typing interaction loop
if user_input := st.chat_input("Input command sequence..."):
    
    # Dynamic Payload Builder
    content_list = [user_input]
    if active_audio_part is not None:
        content_list.append(active_audio_part)
    if active_image_part is not None:
        content_list.append(active_image_part)
    
    # Display message with custom avatar profile frame
    with st.chat_message("user", avatar=USER_AVATAR):
        st.write(user_input)
        if photo_file is not None:
            st.image(photo_file, caption="Visual buffer stream", width=250)
        if audio_file is not None:
            st.audio(audio_file)
            
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get clean multimodal AI response
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are GREAT SAGE JARVIS, an omniscient, highly intelligent tactical AI console assistant inspired by Great Sage. "
                "Address the user formally. Speak directly in clean, crisp, human text sentences. Do not use raw markdown code syntax blocks for casual conversation."
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
