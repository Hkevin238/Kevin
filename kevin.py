import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Universal AI Assistant")
st.caption("AI ivuga indimi zose neza, harimo n'Ikinyarwanda buserukiramuco.")

# Load local environment variables (.env file niba ihari)
load_dotenv()

# Gushaka API Key muri Streamlit Secrets cyangwa muri Environment Variables (.env)
raw_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not raw_api_key:
    st.error("⚠️ GEMINI_API_KEY ntabwo yabonetse! Yishyire muri Streamlit Secrets cyangwa muri .env file.")
    st.stop()

# Clean key String
api_key = str(raw_api_key).strip()
os.environ["GEMINI_API_KEY"] = api_key

# Initialize Gemini Client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Ikosa mu gutangiza Gemini Client: {str(e)}")
    st.stop()

# System Instruction yo gufasha AI kuvuga neza Ikinyarwanda n'izindi ndimi
system_instruction = """
You are a highly capable, multilingual AI assistant. 
You excel at understanding and generating natural, fluent, and grammatically precise text in all human languages.
When responding in Kinyarwanda, use proper grammar, authentic phrasing, and clear expressions without mechanical or literal translations.
Always align tone and language directly with the user's input language unless requested otherwise.
"""

# List y'amamenyo ya models mu buryo bw'icyiciro (Fallback Order)
AVAILABLE_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-pro"
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

    # Gutegura context yo yoherereza Gemini
    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    # Gushaka igisubizo kivuye kuri Gemini
    with st.chat_message("assistant"):
        with st.spinner("AI iriko iratekereza..."):
            ai_response = None
            last_error = None
            
            # Subiramo buri model kugeza imwe ikoze
            for model_name in AVAILABLE_MODELS:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        )
                    )
                    ai_response = response.text
                    if ai_response:
                        break # Ikoze! Sohinga muri loop
                except Exception as e:
                    last_error = str(e)
                    # Niba ari 429 (Resource Exhausted), tegereza amasegonda 2 mbere yo kujya ku yindi model
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        time.sleep(2)
                    continue

            # Kugaragaza igisubizo niba kiyikiriwe
            if ai_response:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error("⚠️ Free Tier Quota yose yashize ku ma models yose, cyangwa API key yagize ikibazo. Tegereza umunota 1 ugerageze cyangwa uhindure API key mu ma Secrets.")
