__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import os
import streamlit as st
import uuid
import json
from dotenv import load_dotenv
from utils import get_context
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

prompt = ("[SYSTEM] You are an expert customer support agent. Your role is:"
          "1. To understand the user's query and provide the most relevant response using the best available context "
          "in a concise manner."
          "2. Never provide anything apart from the answer based on the context."
          "3. To not answer irrelevant questions with respect to the context. Instead, respond with: \"This question "
          "is not relevant to the documents.\""
          "4. If you do not know the answer to the question, reply with: I am not aware of the answer at this "
          "moment and will raise a ticket for the admin to review."
          "[CONTEXT] {context}"
          "[CONVERSATION_HISTORY] {conversation_history}"
          "[USER] {user_query}")

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False
if 'user_details_entered' not in st.session_state:
    st.session_state.user_details_entered = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'contact_detail' not in st.session_state:
    st.session_state.contact_detail = ""


def chat():
    if "agent_name" not in st.session_state or "org_name" not in st.session_state:
        st.error("Please fill out the Agent Information first.")
        st.stop()

    st.markdown("""
                <style>
                .user-message {
                    background-color: #333;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                    text-align: right;
                    float: right;
                    clear: both;
                    width: 60%;
                }
                .assistant-message {
                    background-color: #444;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                    text-align: left;
                    float: left;
                    clear: both;
                    width: 60%;
                }
                .fixed-bottom {
                    background-color: #222;
                    padding: 5px;
                    border-top: 1px solid #555;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }
                </style>
                """, unsafe_allow_html=True)

    st.title("Customer Support Page")
    if not st.session_state.user_details_entered:
        st.session_state.user_name = st.text_input("Please enter your name:", key="user_name_input")
        st.session_state.contact_detail = st.text_input("Please enter your contact detail:", key="contact_detail_input")
        if st.button("Submit"):
            if st.session_state.user_name and st.session_state.contact_detail:
                st.session_state.user_details_entered = True
                st.experimental_rerun()
            else:
                st.warning("Please fill in both fields before submitting.")
    else:
        st.write(f"Hey, I am {st.session_state.agent_name} from {st.session_state.org_name}, how can I help you?")

        # Chat container
        chat_container = st.container()
        with chat_container:
            for sender, message in st.session_state.conversation:
                if sender == "User":
                    st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)

            st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)

            if st.session_state.clear_input:
                st.session_state.user_input = ""
                st.session_state.clear_input = False

            user_input = st.text_input("You: ", key="user_input")
            print(user_input)
            if st.button("Send"):
                if not user_input:
                    print("In no user input")
                    st.warning("Please enter a message before sending.")
                else:
                    print("In user input")
                    st.session_state.user_query = user_input
                    context = get_context(user_input)
                    history = "\n".join([f"{role}: {message}" for role, message in st.session_state.conversation])
                    formatted_prompt = (prompt.replace("{context}", context)
                                        .replace("{user_query}", user_input)
                                        .replace("{conversation_history}", history) + "[ASSISTANT]")

                    # Ensure that st.session_state.llm is correctly initialized and has an invoke method
                    try:
                        response = st.session_state.llm.generate_content([formatted_prompt])
                        if "I am not aware of the answer at this moment and will raise a ticket for the admin to review" in response:
                            ticket = {
                                "id": str(uuid.uuid4()),
                                "content": prompt,
                                "name": st.session_state.user_name,
                                "phone_number":st.session_state.contact_detail
                            }
                            try:
                                with open('tickets.json', 'r') as file:
                                    tickets = json.load(file)
                            except (FileNotFoundError, json.JSONDecodeError):
                                tickets = []
                            tickets.append(ticket)

                            with open('tickets.json', 'w') as file:
                                json.dump(tickets, file, indent=4)
                        # response = st.session_state.llm.invoke(formatted_prompt, max_length=1000, temperature=0.7)
                        st.session_state.conversation.append(("User", user_input))
                        st.session_state.conversation.append(("Agent", response.text))

                        # Set flag to clear the user input field
                        st.session_state.clear_input = True
                        st.experimental_rerun()

                    except Exception as e:
                        st.error(f"Error generating response: {e}")

                    # Update conversation history in a file
                    conversation_str = "\n".join(
                        [f"{role}: {message}" for role, message in st.session_state.conversation])
                    # Set flag to clear the user input field
                    st.session_state.clear_input = True

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    chat()
