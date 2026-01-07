import streamlit as st
import apikey
from openai import OpenAI
import os

# Set your key (prefer env var in real apps)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"  # or "deepseek-reasoner"

st.title("DeepSeek Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]

# Show previous messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call DeepSeek
    resp = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
        max_tokens=200,
    )
    answer = resp.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
