__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"
import os
import gradio as gr
import edge_tts
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
import tempfile
import uuid
import json

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCYebCy9wl3fR-zHvrO4Ambx-5xsakyZ80'
os.environ['HF_API_KEY'] = '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'
HF_API_KEY = os.getenv('HF_API_KEY')

client1 = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=HF_API_KEY)
client2 = InferenceClient("meta-llama/Meta-Llama-3-70B-Instruct", api_key=HF_API_KEY)
DESCRIPTION = """ # <center><b>PROTOTYPE1 Support Chatbot⚡</b></center>
        ### <center>Ask questions based on your uploaded PDF documents.</center>
        """

system_instructions = ("[SYSTEM] Act as a customer support agent who is an expert on the application GreymanAI. "
                       "You need to understand the question the user asks and then provide a relevant reply from the "
                       "best context. NOTE: If you do not get the relevant answer to the question dont say anything "
                       "extra and reply that: /'I am not aware of the answer at this moment"
                       " and will raise a ticket for the admin to review/'"
                       "[CONTEXT] {context}. [USER]")


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
            document = read_pdf_text(file.name)
            all_text += document

    splits = text_splitter.split_text(all_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(splits, embeddings)
    vector_store.save_local("faiss_index")
    return "PDFs processed and vector store created. You can now ask questions."


async def generate_response(prompt):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(prompt)
    context = docs[0].page_content if docs else ""

    formatted_prompt = system_instructions.replace("{context}", context) + prompt + "[ASSISTANT]"
    stream = client1.text_generation(
        formatted_prompt, stream=True, details=True, return_full_text=True)
    output = ""
    for response in stream:
        output += response.token.text
    if "I am not aware of the answer at this moment and will raise a ticket for the admin to review" in output:
        # Create a JSON object with an ID and the content of the prompt
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

        # Save the updated list back to the file
        with open('tickets.json', 'w') as file:
            json.dump(tickets, file, indent=4)

    communicate = edge_tts.Communicate(output)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    return tmp_path


with gr.Blocks(css="style.css") as demo:
    with gr.Tab("Upload your Documents"):
        gr.Markdown(DESCRIPTION)
        upload_files = gr.File(label="Upload Your Files", type="filepath", file_count="multiple", elem_id="pdf_upload")
        process_btn = gr.Button("Process PDFs")
        process_output = gr.Textbox(label="Status")
        process_btn.click(fn=process_pdfs, inputs=upload_files, outputs=process_output)

    with gr.Tab("Questions"):
        gr.Markdown("### Feel Free to ask your questions about GreymanAI")
        user_input = gr.Textbox(label="Prompt", value="")
        output_audio = gr.Audio(label="Response", type="filepath", interactive=False, autoplay=True)
        query_btn = gr.Button("Get Response")
        query_btn.click(fn=generate_response, inputs=user_input, outputs=output_audio)


if __name__ == "__main__":
    demo.queue(max_size=200).launch()
