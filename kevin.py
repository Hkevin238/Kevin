import os
import time
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup - Key Viewport nka ChatGPT
st.set_page_config(
    page_title="Kevin Universal AI", 
    page_icon="newone.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function yo kwinjiza avatar muri Base64
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
    img_html = '<span style="font-size: 30px;">🤖</span>'

# Custom CSS yo kwegereza UI nka ChatGPT Clean Dark Interface
custom_css = f"""
<style>
/* Overall ChatGPT Dark Background */
.stApp {{
    background-color: #212121 !important;
    color: #ececec;
}}

/* Hide default Header & Footer of Streamlit */
header, footer {{ visibility: hidden; }}

/* Sidebar ChatGPT Design */
[data-testid="stSidebar"] {{
    background-color: #171717 !important;
    border-right: 1px solid #303030;
}}

/* Chat Container Styling - Clean & Spacing */
.stChatMessage {{
    background-color: transparent !important;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.stChatMessage[data-testid="stChatMessageAssistant"] {{
    background-color: #212121 !important;
}}

.stChatMessage[data-testid="stChatMessageUser"] {{
    background-color: #2f2f2f !important;
    border-radius: 18px;
    margin-bottom: 10px;
}}

/* Header Styling */
.title-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 20px 0;
}}

.title-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}}

.floating-title {{
    font-size: 1.8rem;
    font-weight: 600;
    color: #ececec;
    margin: 0;
}}

/* Prompt Cards nka ChatGPT Starter UI */
.stButton > button {{
    width: 100%;
    background-color: #2f2f2f !important;
    color: #ececec !important;
    border: 1px solid #424242 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    text-align: left !important;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    background-color: #383838 !important;
    border-color: #676767 !important;
}}

/* Input Box Alignment */
.stChatInputContainer {{
    padding-bottom: 20px;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Load local environment variables
load_dotenv()

# API Key Check
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

# Sidebar Navigation (ChatGPT style)
with st.sidebar:
    st.markdown("### 💬 Chat Controls")
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### ⚙️ Model Options")
    selected_model = st.selectbox("Hitamo Model", AVAILABLE_MODELS, index=0)
    
    st.markdown("---")
    st.caption("Developer: **Developer Kevin**")
    st.caption("Email: therealhacks583@gmail.com")

# Main Page Title
st.markdown(f'''
<div class="title-container">
    {img_html}
    <h1 class="floating-title">Universal AI Assistant</h1>
</div>
''', unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    avatar_to_use = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_to_use):
        st.markdown(message["content"])

# Empty state prompt cards (ChatGPT Home View)
prompt_from_button = None
if len(st.session_state.messages) == 0:
    st.markdown("<h3 style='text-align: center; color: #b4b4b4; margin-bottom: 25px;'>Nkawe nakumfasha iki uyu munsi?</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 **Kwandika Code**\nMfasha gukora aka application mu Python"):
            prompt_from_button = "Mfasha kwandika application yoroshye mu Python."
        if st.button("📝 **Ibaruwa y'Akazi**\nAndika ibaruwa isaba akazi muri IT"):
            prompt_from_button = "Mfasha kwandika ibaruwa isaba akazi mu rwego rwa IT n'ikoranabuhanga."
    with col2:
        if st.button("🧠 **Ibibazo & Ibisubizo**\nBaza ikintu cyose uraza gusobanurirwa"):
            prompt_from_button = "Mbwira uko AI ikora n'uko yafasha mu buzima bwa buri munsi."
        if st.button("🌐 **Ikinyarwanda**\nKora ikiganiro mu Kinyarwanda cy'umwimerere"):
            prompt_from_button = "Mwaramutse! Mbwira uwo uri we n'ibyo ushobora kumfasha."

# Chat Input Box
chat_prompt = st.chat_input("Message Universal AI...")
prompt = chat_prompt or prompt_from_button

if prompt:
    # Append & render User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Render Assistant Response with Streaming (ChatGPT Effect)
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=groq_messages,
                temperature=0.7,
                stream=True
            )
            
            def generate_response():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            ai_response = st.write_stream(generate_response())
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            # Fallback to other models if primary hits rate limit
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
                st.error("⚠️ Rate limit yashize ku ma models yose, cyangwa Groq API key yagize ikibazo. Tegereza umunota 1 ugerageze.")
