import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup
st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖", layout="centered")

# Custom CSS yo guhindura Avatar, Rainbow Background, Background Image, na Floating Title Animation
custom_css = """
<style>
/* Rainbow Animation + Background Image ku page yose */
.stApp {
    background: linear-gradient(124deg, rgba(255,0,0,0.15), rgba(255,154,0,0.15), rgba(208,222,33,0.15), rgba(79,220,74,0.15), rgba(63,218,216,0.15), rgba(47,201,226,0.15), rgba(28,127,238,0.15), rgba(95,21,242,0.15), rgba(186,12,248,0.15)),
                url("app/static/newone.png") no-repeat center center fixed;
    background-size: cover;
    background-blend-mode: overlay;
    animation: rainbow 18s ease infinite;
}

@keyframes rainbow { 
    0%{background-position:0% 82%}
    50%{background-position:100% 19%}
    100%{background-position:0% 82%}
}

/* Chat Container Card semi-transparent styling yo kugaragaza text neza */
.stChatMessage {
    background-color: rgba(26, 28, 36, 0.85) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Floating Title Animation (Move Up & Down gake gake) */
.floating-title {
    display: inline-block;
    animation: floatUpDown 3.5s ease-in-out infinite;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
}

@keyframes floatUpDown {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-10px);
    }
    100% {
        transform: translateY(0px);
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title nshya ikoresha floatUpDown animation
st.markdown('<h1 class="floating-title">🤖 Universal AI Assistant (Groq)</h1>', unsafe_allow_html=True)
st.caption("AI ivuga indimi zose neza, harimo n'Ikinyarwanda buserukiramuco.")

# Load local environment variables (.env file niba ihari)
load_dotenv()

# Gushaka Groq API Key muri Streamlit Secrets cyangwa muri Environment Variables (.env)
raw_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not raw_api_key:
    st.error("⚠️ GROQ_API_KEY ntabwo yabonetse! Yishyire muri Streamlit Secrets cyangwa muri .env file.")
    st.stop()

# Clean key String
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

# List y'amamenyo ya models za Groq
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]

# Path y'ifoto nshya ya Assistant Avatar
ASSISTANT_AVATAR = "newone.png"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kugaragaza ubutumwa bwose bwashize mu kiganiro
for message in st.session_state.messages:
    avatar_to_use = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_to_use):
        st.markdown(message["content"])

# Agasanduku k'umukoresha (User Input)
if prompt := st.chat_input("Baza ikibazo cyangwa wandike ubutumwa..."):
    # Gushyira ubutumwa bw'umukoresha muri chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gutegura ubutumwa buyoborwa na Groq
    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Gushaka igisubizo kivuye kuri Groq hamwe n'avatar nshya ya newone.png
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("AI iriko iratekereza..."):
            ai_response = None
            last_error = None
            
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
                    last_error = str(e)
                    if "429" in str(e) or "rate_limit" in str(e).lower():
                        time.sleep(2)
                    continue

            if ai_response:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error("⚠️ Rate limit yashize ku ma models yose, cyangwa Groq API key yagize ikibazo. Tegereza umunota 1 ugerageze cyangwa uhindure API key.")
