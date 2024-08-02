__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import os
import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
import uuid
import json
import streamlit as st

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCYebCy9wl3fR-zHvrO4Ambx-5xsakyZ80'
os.environ['HF_API_KEY'] = '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'
HF_API_KEY = os.getenv('HF_API_KEY')

client1 = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=HF_API_KEY)
client2 = InferenceClient("meta-llama/Meta-Llama-3-70B-Instruct", api_key=HF_API_KEY)
DESCRIPTION = """ # <center><b>PROTOTYPE1 Support Chatbot⚡</b></center>
        ### <center>Ask questions based on your uploaded PDF documents.</center>
        """

system_instructions = ("[SYSTEM] You are an expert customer support agent for the application. Your role is "
                       "to understand the user's query and provide the most relevant response using the best "
                       "available context. If the question is not relevant to the provided documents, only respond with"
                       "'This question is not relevant to the documents.'"
                       " If you do not know the answer to the "
                       "question, just reply with 'I am not aware of the answer at this moment and will raise a "
                       "ticket for the admin to review.' and stop after that. [CONTEXT] {context}.[USER]")


def read_pdf_text(document):
    text = ""
    reader = PdfReader(document)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def process_pdfs(files):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    all_text = ""

    for file in files:
        if file.name.lower().endswith(".pdf"):
            document = read_pdf_text(file)
            all_text += document

    splits = text_splitter.split_text(all_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(splits, embeddings)
    vector_store.save_local("faiss_index")
    return "PDFs processed and vector store created. You can now ask questions."


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


async def generate_response(prompt):
    chat_history = st.session_state.chat_history
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(prompt)
    context = docs[0].page_content if docs else ""

    formatted_history = ""
    for exchange in chat_history:
        formatted_history += f"[{exchange['role'].upper()}]: {exchange['content']}\n"

    formatted_prompt = system_instructions.replace("{context}", context) + formatted_history + "[ASSISTANT]"

    stream = client1.text_generation(
        formatted_prompt, stream=True, details=True, return_full_text=True)
    output = ""
    for response in stream:
        output += response.token.text

    if "I am not aware of the answer at this moment and will raise a ticket for the admin to review" in output:
        ticket = {
            "id": str(uuid.uuid4()),
            "content": prompt
        }
        try:
            with open('tickets.json', 'r') as file:
                tickets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            tickets = []
        tickets.append(ticket)

        with open('tickets.json', 'w') as file:
            json.dump(tickets, file, indent=4)
    return output


async def run_async_function(func, *args):
    return await func(*args)


if __name__ == "__main__":
    generate_response("Can you tell me about you")
