import os
import time
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup
st.set_page_config(page_title="Kevin Universal AI", page_icon="newone.png", layout="centered")

# Agasobanuro k'uburyo bwo kwinjiza ifoto mu buryo bwa Base64 ku background no kuri avatar
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

ASSISTANT_AVATAR = "newone.png"
img_base64 = get_base64_of_bin_file(ASSISTANT_AVATAR)

# Encoding HTML y'ifoto iri muri Title hejuru
if img_base64:
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="title-avatar">'
    bg_img_css = f'url("data:image/png;base64,{img_base64}")'
else:
    img_html = '<span style="font-size: 32px;">🤖</span>'
    bg_img_css = 'none'

# Custom CSS: Background Image ihagaze pfe (Static) + Rainbow Color Shift
custom_css = f"""
<style>
/* Background ya page yose: Ifoto iri hamwe itanyeganyega */
.stApp {{
    background-image: {bg_img_css};
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    position: relative;
}}

/* Rainbow Layer: Color shift ku mabara gusa, utanyeganyeza ifoto */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, 
        rgba(255, 0, 0, 0.2), 
        rgba(255, 165, 0, 0.2), 
        rgba(255, 255, 0, 0.2), 
        rgba(0, 128, 0, 0.2), 
        rgba(0, 0, 255, 0.2), 
        rgba(75, 0, 130, 0.2), 
        rgba(238, 130, 238, 0.2));
    background-size: 400% 400%;
    animation: rainbowShift 16s ease infinite;
    pointer-events: none;
    z-index: 0;
}}

@keyframes rainbowShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Chat Container Card semi-transparent styling */
.stChatMessage {{
    background-color: rgba(20, 22, 30, 0.88) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 1;
}}

/* Floating Title Animation Header (Move Up & Down gake gake + Ifoto) */
.title-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    animation: floatUpDown 3.8s ease-in-out infinite;
    margin-bottom: 5px;
    position: relative;
    z-index: 1;
}}

.title-avatar {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0px 0px 12px rgba(255, 255, 255, 0.4);
}}

.floating-title {{
    font-size: 2.2rem;
    font-weight: bold;
    color: #ffffff;
    margin: 0;
    text-shadow: 0px 4px 12px rgba(0, 0, 0, 0.6);
}}

@keyframes floatUpDown {{
    0% {{
        transform: translateY(0px);
    }}
    50% {{
        transform: translateY(-8px);
    }}
    100% {{
        transform: translateY(0px);
    }}
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header nshya irimo ifoto ya newone.png n'inyandiko ya Title
st.markdown(f'''
<div class="title-container">
    {img_html}
    <h1 class="floating-title">Universal AI Assistant</h1>
</div>
''', unsafe_allow_html=True)

st.caption("This Kevin Universal AI made for you !.")

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

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kugaragaza ubutumwa bwose bwashize mu kiganiro
for message in st.session_state.messages:
    avatar_to_use = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_to_use):
        st.markdown(message["content"])

# Agasanduku k'umukoresha (User Input)
if prompt := st.chat_input("Ask anything..."):
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
        with st.spinner("Kevin AI thinking......."):
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
