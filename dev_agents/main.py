__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def main():

    if 'page' not in st.session_state:
        st.session_state.page = 'register'
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio("Go to", ["register", "chat"], key="navigation_radio")

    if st.session_state.page == "register":
        from register import register
        register()
    elif st.session_state.page == "chat":
        from chat import chat
        chat()


if __name__ == "__main__":
    main()
