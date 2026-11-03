
import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Page configuration
st.set_page_config(
    page_title="LLM Contextual Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LLM Contextual Chatbot")
st.caption("Powered by Google Gemini and FastAPI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                payload = {
                    "message": user_input,
                    "conversation_id": st.session_state.conversation_id
                }

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=40
                )

                response.raise_for_status()

                data = response.json()

                bot_response = data["bot_response"]

                # Save conversation ID
                st.session_state.conversation_id = data["conversation_id"]

                st.markdown(bot_response)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response
                })

            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the chatbot server. Please check whether FastAPI is running.")

            except requests.exceptions.HTTPError as e:
                st.error(f"Backend error: {e}")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


# New conversation button
if st.button("Start New Conversation"):

    st.session_state.messages = []
    st.session_state.conversation_id = None

    st.rerun()
