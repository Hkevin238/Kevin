import os
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
            try:
                # Gukoresha model y'umwimerere yakiriwe muri google-genai SDK
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Habaye ikosa: {str(e)}")
