from google import genai
from google.genai import types
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv() # .env file load hogi

st.title("P2PClouds AI Assistant")
st.write("Ask a Question about P2PClouds")

user_input = st.text_input("Ask Anything")

if st.button("Chat"):
    # PEHLE .env se lega, agar na mile to phir secrets se - is se error nahi ayega
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Agar laptop par nahi mili to Cloud wali check karega
    try:
        if not api_key:
            api_key = st.secrets["GEMINI_API_KEY"]
    except:
        pass

    if not api_key:
        st.error("API Key nahi mili! .env file check karo")
    else:
        client = genai.Client(api_key=api_key)
        with st.spinner("Agent is thinking..."):
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite', 
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction="You are a P2PClouds AI agent. who answer related question about our company. We are a software house with 7+ yr exp and 15+ products"
                ),
            )
            st.write(response.text)