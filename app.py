import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Cloud Computing Guide",
    page_icon="☁️"
)

st.title("☁️ Cloud Computing Guide")
st.write("Your AI assistant for learning cloud computing!")

st.info(
    "Ask me about cloud services, AWS, Azure, "
    "Google Cloud, virtualization, and cloud security."
)

if not API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are Cloud Computing Guide, an educational chatbot.
Explain cloud computing topics in simple English.
Use examples, headings, and bullet points.
Explain IaaS, PaaS, SaaS, cloud deployment models,
virtualization, cloud storage, security, AWS, Azure,
and Google Cloud.
Give exam-friendly answers when requested.
Politely guide unrelated questions back to cloud computing.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your cloud computing question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                    [
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": SYSTEM_INSTRUCTION
                                    + "\n\nStudent question: "
                                    + prompt
                                }
                            ]
                        }
                    ]
                )

                answer = response.text
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()