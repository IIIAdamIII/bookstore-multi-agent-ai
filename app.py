import streamlit as st
import requests

#  CONFIGURATION #
ENDPOINT_URL =
API_KEY =
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

st.set_page_config(page_title="📚 Bookstore Assistant", layout="centered")

st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png' width='80'/>
        <h1 style='color: #2c3e50;'>Welcome to BookSmart 🧠📚</h1>
        <p style='color: #555;'>Your AI-powered assistant for recommendations, support, and insights</p>
    </div>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def ask_assistant(user_msg):
    payload = {"user_question": user_msg}
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return (
            data.get("recommendation_response")
            or data.get("asv_response")
            or data.get("analysis_report")
            or "🤷 Sorry, I couldn't understand your request."
        )
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your question here (e.g. book suggestion, help, or analysis)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    assistant_reply = ask_assistant(user_input)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/236/236832.png", width=100)
    st.markdown("### ℹ️ About this assistant")
    st.write(
        """
        This is a multi-agent system for a smart bookstore:
        - **📚 Recommender Agent**: Suggests books based on your interests.
        - **🛠️ Support Agent**: Answers customer service questions.
        - **📊 Analyst Agent**: makes analysis between booktores and returns summary reports.

        Type naturally and the system will route your query automatically!
        """
    )
