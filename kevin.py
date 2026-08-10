import os
import time
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup - wide layout yo guha umwanya uhagije interface
st.set_page_config(
    page_title="Kevin Universal AI", 
    page_icon="newone.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function yo gukora encoding y'ifoto muri Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

ASSISTANT_AVATAR = "newone.png"
img_base64 = get_base64_of_bin_file(ASSISTANT_AVATAR)

if img_base64:
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="title-avatar">'
else:
    img_html = '<span style="font-size: 32px;">🤖</span>'

# Custom CSS & Glassmorphism Styling
custom_css = f"""
<style>
/* Background hamwe n'agaciro k'amabara agezweho */
.stApp {{
    background: linear-gradient(124deg, rgba(15, 17, 23, 0.95), rgba(26, 28, 36, 0.9)),
                url("app/static/newone.png") no-repeat center center fixed;
    background-size: cover;
    background-blend-mode: overlay;
}}

/* Chat Container Card (Glassmorphism Effect) */
.stChatMessage {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}}

/* Floating Title Styling */
.title-container {{
    display: flex;
    align-items: center;
    gap: 15px;
    animation: floatUpDown 3.5s ease-in-out infinite;
    margin-bottom: 15px;
}}

.title-avatar {{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0px 0px 15px rgba(0, 200, 255, 0.4);
}}

.floating-title {{
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, #8a2be2, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}}

@keyframes floatUpDown {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-6px); }}
    100% {{ transform: translateY(0px); }}
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Load local environment variables
load_dotenv()

raw_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not raw_api_key:
    st.error("⚠️ GROQ_API_KEY ntabwo yabonetse! Yishyire muri Streamlit Secrets cyangwa muri .env file.")
    st.stop()

api_key = str(raw_api_key).strip()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Ikosa mu gutangiza Groq Client: {str(e)}")
    st.stop()

# System Instruction
system_instruction = """
You are a highly capable, multilingual AI assistant created and developed by Developer Kevin. 

CRITICAL IDENTITY RULES:
1. Whenever someone asks who created you, who developed you, who built you, or who your creator is, state clearly and proudly that you were developed by Developer Kevin.
2. NEVER say or claim that you were created by Meta, OpenAI, Groq, Google, or any other company/person. Always credit Developer Kevin as your developer.
3. If anyone asks for the developer's contact information or email address, provide this exact email: therealhacks583@gmail.com.

LANGUAGE AND TONE INSTRUCTIONS:
- You excel at understanding and generating natural, fluent, and grammatically precise text in all human languages.
- When responding in Kinyarwanda, use proper grammar, authentic phrasing, and clear expressions without mechanical or literal translations.
- Always align tone and language directly with the user's input language unless requested otherwise.
"""

AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Navigation & Settings
with st.sidebar:
    st.image(ASSISTANT_AVATAR if os.path.exists(ASSISTANT_AVATAR) else "🤖", width=80)
    st.title("Kevin AI Settings")
    
    # Model Selection UI
    selected_model = st.selectbox(
        "Hitamo AI Model:",
        AVAILABLE_MODELS,
        index=0
    )
    
    st.divider()
    
    # Clear Chat Feature
    if st.button("🗑️ Siba Ibiganiro (Clear Chat)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.caption("Developer: **Developer Kevin**")
    st.caption("Contact: therealhacks583@gmail.com")

# Main Header
st.markdown(f'''
<div class="title-container">
    {img_html}
    <h1 class="floating-title">Kevin Universal AI</h1>
</div>
''', unsafe_allow_html=True)

st.caption("Powered by Groq • Developed by Developer Kevin")

# Display Messages
for message in st.session_state.messages:
    avatar_to_use = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_to_use):
        st.markdown(message["content"])

# Quick Prompt Suggestions (Erekana gusa niba chat ikiri nshya)
prompt_to_submit = None
if len(st.session_state.messages) == 0:
    st.write("💡 **Urugero rw'ibyo yabaza:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Ndamutsa mu Kinyarwanda"):
            prompt_to_submit = "Mwaramutse! Mbwira uwo uri we n'uko ushobora kumfasha."
    with col2:
        if st.button("💻 Nyereka urugero rwa HTML Code"):
            prompt_to_submit = "Nyandikira urugero rwa HTML & CSS k'urupapuro rugezweho."
    with col3:
        if st.button("📝 Mfasha kwandika Ibaruwa"):
            prompt_to_submit = "Mfasha kwandika ibaruwa isaba akazi mu buryo bw'umwuga."

# Chat Input
user_input = st.chat_input("Ask anything...")
if user_input:
    prompt_to_submit = user_input

# Logic yo kwakira ubutumwa no kuguha Streaming Response
if prompt_to_submit:
    st.session_state.messages.append({"role": "user", "content": prompt_to_submit})
    with st.chat_message("user"):
        st.markdown(prompt_to_submit)

    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        # Stream response kubera UX nziza
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=groq_messages,
                temperature=0.7,
                stream=True
            )
            
            def generate_chunks():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            ai_response = st.write_stream(generate_chunks())
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            # Fallback ku yindi models niba habayeho erreur
            st.warning(f"Model {selected_model} igize ikibazo, irimo kugeza ku yindi model...")
            ai_response = None
            for model_name in AVAILABLE_MODELS:
                if model_name == selected_model:
                    continue
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=groq_messages,
                        temperature=0.7,
                    )
                    ai_response = response.choices[0].message.content
                    if ai_response:
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        break
                except Exception:
                    continue

            if not ai_response:
                st.error("⚠️ Rate limit yashize ku ma models yose. Tegereza umunota 1 ugerageze cyangwa uhindure API key.")
