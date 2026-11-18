"""import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the same folder as app.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("API key loaded successfully!")
else:
    print("API key not found!")"""







import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Groq AI Chatbot")
st.caption("Your personal AI assistant powered by Groq")

# Check API key
if not api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# Select model
model = "openai/gpt-oss-120b"

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Groq AI is thinking..."):

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant. Give clear and simple answers."
                        },
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"Error: {e}")







