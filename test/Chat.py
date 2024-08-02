import streamlit as st
import asyncio
from greyman import generate_response


def display_chat_history():
    for chat in st.session_state.chat_history:
        if chat['role'] == 'user':
            st.markdown(f'<div class="user-message"><b>You:</b> {chat["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message"><b>Assistant:</b> {chat["content"]}</div>', unsafe_allow_html=True)


def main():
    if "agent_name" not in st.session_state:
        st.error("Please fill out the Agent Information first.")
        st.stop()

    st.title("Customer Support Page")
    st.write(f"Hey, I am {st.session_state.agent_name} from {st.session_state.org_name}, how can I help you?")

    # CSS for message styling
    st.markdown("""
        <style>
        .user-message {
            background-color: #333333;
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: right;
            float: right;
            clear: both;
            width: 60%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .assistant-message {
            background-color: #444444;
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: left;
            float: left;
            clear: both;
            width: 60%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .chat-container {
            height: 70vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column-reverse;
            padding: 10px;
            border: 1px solid #555;
            border-radius: 10px;
            background-color: #222;
        }
        </style>
        """, unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        display_chat_history()

    with st.container():
        customer_problem = st.text_area("How can I help you", key="problem_input")

    if st.button("Submit"):
        if customer_problem:
            prompt = customer_problem
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            response = run_async_function(generate_response, prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with chat_container:
                display_chat_history()
        st.rerun()


def run_async_function(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func(*args))
    return result


if __name__ == "__main__":
    main()