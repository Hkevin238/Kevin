import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Page setup
st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Universal AI Assistant (Groq)")
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

# System Instruction irimo amabwiriza y'umwimerere w'uwayikoze (Developer Identity)
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

# List y'amamenyo ya models za Groq mu buryo bw'icyiciro (Fallback Order)
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]

# Initialize Chat History muri Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kugaragaza ubutumwa bwose bwashize mu kiganiro
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Agasanduku k'umukoresha (User Input)
if prompt := st.chat_input("Baza ikibazo cyangwa wandike ubutumwa..."):
    # Gushyira ubutumwa bw'umukoresha muri chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gutegura ubutumwa bwose buyoborwa na Groq (harimo na system instruction)
    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Gushaka igisubizo kivuye kuri Groq
    with st.chat_message("assistant"):
        with st.spinner("AI iriko iratekereza..."):
            ai_response = None
            last_error = None
            
            # Subiramo buri model kugeza imwe ikoze
            for model_name in AVAILABLE_MODELS:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=groq_messages,
                        temperature=0.7,
                    )
                    ai_response = response.choices[0].message.content
                    if ai_response:
                        break # Ikoze! Sohinga muri loop
                except Exception as e:
                    last_error = str(e)
                    # Niba ari Rate Limit error (429), tegereza amasegonda 2 mbere yo kujya ku yindi model
                    if "429" in str(e) or "rate_limit" in str(e).lower():
                        time.sleep(2)
                    continue

            # Kugaragaza igisubizo niba kiyikiriwe
            if ai_response:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error("⚠️ Rate limit yashize ku ma models yose, cyangwa Groq API key yagize ikibazo. Tegereza umunota 1 ugerageze cyangwa uhindure API key.")
