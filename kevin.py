import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="Kevin AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Universal AI Assistant")
st.caption("Universal AI built for you ! Welcome.")

# Secure API Key retrieval
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Ntabwo API Key yabonetse. Baza umuyobozi cyangwa uyishyire muri Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# System Instructions to ensure high-quality multilingual and Kinyarwanda capability
system_instruction = """
You are a highly capable, multilingual AI assistant. 
You excel at understanding and generating natural, fluent, and grammatically precise text in all human languages.
When responding in Kinyarwanda, use proper grammar, authentic phrasing, and clear expressions without mechanical or literal translations.
Always align tone and language directly with the user's input language unless requested otherwise.
"""

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Baza ikibazo cyangwa wandike ubutumwa..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare chat context for Gemini
    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    # Generate Response from Gemini 2.5 Flash
    with st.chat_message("assistant"):
        with st.spinner("AI iriko iratekereza..."):
            try:
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
