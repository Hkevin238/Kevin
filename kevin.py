import os
import time
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup
st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖", layout="centered")

# Function yo kwinjiza ifoto mu buryo bwa Base64
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
    bg_img_css = f'url("data:image/png;base64,{img_base64}")'
else:
    img_html = '<span style="font-size: 32px;">🤖</span>'
    bg_img_css = 'none'

# Custom CSS
custom_css = f"""
<style>
/* Background ya page yose: Ifoto irahagaze (static), amabara y'umukororobya niyo ahinduka gake gake */
.stApp {{
    background-image: {bg_img_css};
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    position: relative;
}}

/* Color overlay ikora animation y'amabara y'umukororobya utanyeganyeza ifoto */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, 
        rgba(255, 0, 0, 0.25), 
        rgba(255, 165, 0, 0.25), 
        rgba(255, 255, 0, 0.25), 
        rgba(0, 128, 0, 0.25), 
        rgba(0, 0, 255, 0.25), 
        rgba(75, 0, 130, 0.25), 
        rgba(238, 130, 238, 0.25));
    background-size: 400% 400%;
    animation: rainbowShift 15s ease infinite;
    pointer-events: none;
    z-index: 0;
}}

@keyframes rainbowShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Sticky Header y'Ishoza mu birango: Title n'ifoto zihora zigaragara hejuru umu user ascrolla */
.sticky-header {{
    position: sticky;
    top: 3.5rem;
    z-index: 999;
    background: rgba(15, 17, 23, 0.75);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 12px 18px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    margin-bottom: 20px;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4);
}}

.title-container {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.title-avatar {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.9);
    box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5);
}}

.sticky-title {{
    font-size: 1.8rem;
    font-weight: bold;
    color: #ffffff;
    margin: 0;
    text-shadow: 0px 2px 8px rgba(0, 0, 0, 0.7);
}}

/* Chat Container Card styling */
.stChatMessage {{
    background-color: rgba(20, 22, 30, 0.88) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 1;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sticky Title Header ikomeza kugara hejuru igihe cyose ikiganiro cyo gukoresha AI kirimo kuba
st.markdown(f'''
<div class="sticky-header">
    <div class="title-container">
        {img_html}
        <h1 class="sticky-title">Universal AI Assistant (Groq)</h1>
    </div>
</div>
''', unsafe_allow_html=True)

st.caption("AI ivuga indimi zose neza, harimo n'Ikinyarwanda buserukiramuco.")

# Load local environment variables
load_dotenv()

# Gushaka Groq API Key
raw_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not raw_api_key:
    st.error("⚠️ GROQ_API_KEY ntabwo yabonetse! Yishyire muri Streamlit Secrets cyangwa muri .env file.")
    st.stop()

api_key = str(raw_api_key).strip()

# Initialize Groq Client
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

# Display prior chat messages
for message in st.session_state.messages:
    avatar_to_use = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_to_use):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Baza ikibazo cyangwa wandike ubutumwa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("AI iriko iratekereza..."):
            ai_response = None
            
            for model_name in AVAILABLE_MODELS:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=groq_messages,
                        temperature=0.7,
                    )
                    ai_response = response.choices[0].message.content
                    if ai_response:
                        break
                except Exception as e:
                    if "429" in str(e) or "rate_limit" in str(e).lower():
                        time.sleep(2)
                    continue

            if ai_response:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error("⚠️ Rate limit yashize ku ma models yose, cyangwa Groq API key yagize ikibazo. Tegereza umunota 1 ugerageze cyangwa uhindure API key.")
