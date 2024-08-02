__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import streamlit as st
from greyman import process_pdfs

def main():
    st.title("Agent Information")

    # Input fields for agent details
    agent_name = st.text_input("Agent Name")
    org_name = st.text_input("Organization Name")
    description = st.text_area("Organization Description")
    website = st.text_input("Website (if any)")
    documents = st.file_uploader("Upload Documents (PDFs)", type="pdf", accept_multiple_files=True)

    if st.button("Submit"):
        # Save details in session state
        st.session_state.agent_name = agent_name
        st.session_state.org_name = org_name
        st.session_state.description = description
        st.session_state.website = website
        st.session_state.documents = documents
        # Redirect to Inquiry page
        processed_docs = process_pdfs(documents)
        st.write(processed_docs)
        st.session_state.page = "Inquiry"


if __name__ == "__main__":
    main()