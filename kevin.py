import os
import time
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup - Centered & Mobile Style View
st.set_page_config(
    page_title="ChatGPT", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Function yo kwinjiza avatar muri Base64 niba ihari
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

ASSISTANT_AVATAR = "newone.png"

# Custom CSS yo kwegereza UI 100% ku ifoto ya ChatGPT Mobile
custom_css = """
<style>
/* Pure Black Background like Mobile OLED Theme */
.stApp {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Hide default Streamlit Elements */
header, footer, [data-testid="stHeader"] { 
    display: none !important; 
}

/* Container Spacing */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
    max-width: 600px !important;
}

/* Top App Bar UI */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0px 25px 0px;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 20px;
}

.top-bar-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #ffffff;
}

.top-bar-icons {
    display: flex;
    gap: 18px;
    font-size: 1.2rem;
    color: #cccccc;
}

/* User Message Bubble - Right Aligned, Dark Rounded Pill */
.user-msg-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
    width: 100%;
}

.user-msg-bubble {
    background-color: #2f2f2f;
    color: #ffffff;
    padding: 12px 18px;
    border-radius: 22px;
    max-width: 80%;
    font-size: 1rem;
    line-height: 1.4;
    word-wrap: break-word;
}

/* Assistant Message - Left Aligned, Plain Text style */
.assistant-msg-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 25px;
    width: 100%;
}

.assistant-msg-text {
    color: #ffffff;
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 8px;
    width: 100%;
}

/* Action Bar below AI Responses (Copy, Like, Dislike, Audio, Refresh, Share) */
.action-bar {
    display: flex;
    gap: 16px;
    color: #8e8e93;
    font-size: 1.05rem;
    margin-top: 4px;
    cursor: pointer;
}

/* Custom Chat Input styling at bottom */
.stChatInputContainer {
    background-color: #000000 !important;
}

.stChatInput > div {
    background-color: #2f2f2f !important;
    border-radius: 25px !important;
    border: none !important;
    color: #ffffff !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Load Environment Variables
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

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Top Mobile Navigation Header
st.markdown("""
<div class="top-bar">
    <div style="font-size: 1.4rem; cursor: pointer;">☰</div>
    <div class="top-bar-title">ChatGPT</div>
    <div class="top-bar-icons">
        <span style="cursor: pointer;">📝</span>
        <span style="cursor: pointer;">⋮</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Render Chat History exact like image layout
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-msg-container">
            <div class="user-msg-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-msg-container">
            <div class="assistant-msg-text">{msg["content"]}</div>
            <div class="action-bar">
                <span>📋</span>
                <span>👍</span>
                <span>👎</span>
                <span>🔊</span>
                <span>🔄</span>
                <span>🔗</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chat Input Box
if prompt := st.chat_input("Message ChatGPT..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
    <div class="user-msg-container">
        <div class="user-msg-bubble">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Generate Response
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
        except Exception:
            continue

    if ai_response:
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.markdown(f"""
        <div class="assistant-msg-container">
            <div class="assistant-msg-text">{ai_response}</div>
            <div class="action-bar">
                <span>📋</span>
                <span>👍</span>
                <span>👎</span>
                <span>🔊</span>
                <span>🔄</span>
                <span>🔗</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Hubayeho ikibazo mu kubona igisubizo. Gerageza tena.")
