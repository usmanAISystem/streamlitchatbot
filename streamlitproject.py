from google import genai
from google.genai import types
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("P2PClouds AI Assistant")
st.write("Ask a Question about P2PClouds")

# 1. Chat history ke liye memory banana
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. API Key ka system
api_key = os.getenv("GEMINI_API_KEY")
try:
    if not api_key:
        api_key = st.secrets["GEMINI_API_KEY"]
except:
    pass

# 3. Purani saari chat ko uper dikhana - ye remove nahi hogi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Neeche se new chat karne ka input - ye hamesha neeche rahega
if user_input := st.chat_input("Ask Anything about P2PClouds..."):
    # User ka message save karo aur dikhao
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ab Agent ka jawab
    if not api_key:
        st.error("API Key nahi mili! .env file check karo")
    else:
        client = genai.Client(api_key=api_key)
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                response = client.models.generate_content(
                    model='gemini-3.5-flash-lite', 
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a P2PClouds AI agent. who answer related question about our company. We are a software house with 7+ yr exp and 15+ products"
                    ),
                )
                st.markdown(response.text)
        
        # Assistant ka jawab bhi save kar lo taake remove na ho
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# 5. Chat clear karne ka button (optional)
if st.sidebar.button("New Chat / Clear Chat"):
    st.session_state.messages = []
    st.rerun()
