__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"


import streamlit as st

# Set the default page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Register", "Chat"])

# Update the current page in session state
st.session_state.page = page

# Load the appropriate page based on the selection
if st.session_state.page == "Register":
    from Register import main as form_main
    form_main()
elif st.session_state.page == "Chat":
    from Chat import main as chat_main
    chat_main()


