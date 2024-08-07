__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

from dotenv import load_dotenv
from utils import get_context
import os
from langchain_huggingface import HuggingFaceEndpoint
load_dotenv()

system_instructions = ("[SYSTEM] You are an expert customer support agent. Your role is "
                       "to understand the user's query and provide the most relevant response using the best "
                       "available context in concise manner. Do not provide anything apart from the answer"
                       "If the question is not relevant to the provided documents, only respond with"
                       "'This question is not relevant to the documents.'"
                       " If you do not know the answer to the "
                       "question, just reply with 'I am not aware of the answer at this moment and will raise a "
                       "ticket for the admin to review.' and stop after that. [CONTEXT] {context}.[USER] {user_query}")

prompt = ("[SYSTEM] Can you tell me which resource will be best to answer to the user query out of SQL DATABASE and Pdf"
          "documents? Just give the name - 'SQL DATABASE' or 'DOCUMENT' when answering. Your response should be only "
          "one word."
          " [USER] {user_query} "
          "[EXAMPLE USER QUERY: 'What is the revenue for the last quarter?'] "
          "[EXAMPLE ASSISTANT RESPONSE: 'SQL DATABASE'] "
          "[EXAMPLE USER QUERY: 'Can I get the user manual?'] "
          "[EXAMPLE ASSISTANT RESPONSE: 'DOCUMENT']")


def test(user_input):
    sec_key = os.getenv("HUGGINGFACE_KEY")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = sec_key
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=200, temperature=0.7, token=sec_key)
    context = get_context(user_input)
    with open('a.txt', 'w') as f:
        f.write(context)
    formatted_prompt = (system_instructions.replace("{context}", context).replace("{user_query}", user_input)
                        + "[ASSISTANT]")
    print(llm.invoke(formatted_prompt))
    # formatted_prompt = prompt.replace("{user_query}", user_input) + "[ASSISTANT]"
    # print(formatted_prompt)
    # print(llm.invoke(formatted_prompt))


if __name__ == '__main__':
    test("Can you tell me how much calories can i burn ?")