import json
import getpass
import os
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.messages import HumanMessage, SystemMessage
import time
import streamlit as st
#from langchain.memory import ConversationBufferMemory
import google.generativeai as genai
#from config import API_KEY
import re
import json


genai.configure(api_key = st.secrets['API_KEY'])

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = [])

def chat_with_gemini(prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except:
        return st.error("An Error Occured! Please Try Again.")
    # for word in result.content.split():
    #     yield word + " "
    #     time.sleep(0.05)

def generate_description_string(df, slice_number, full = False):
    if not full:
        return '\n'.join(f'{i + 1}. {desc}' for i, desc in enumerate(df['description'][:slice_number], start=0))
    else:
        return '\n'.join(f'{i + 1}. {desc}' for i, desc in enumerate(df['description'], start = 0))

def set_initial_message():
    chat.history.clear()
    try:
        chat.send_message(st.session_state.desc_string)
    except:
        pass

def get_json():
    prompt = """
        Extract a bunch of relevant keywords related to this job role. Here is how the format needed:

            General Kewords (List[words]):
            Skills (List[words]):
            Qualification (List[words]):
            Soft Skills (List[words]):
            Additional (List[words]):
            Other (List[words]):

            Instructions while filling:

            1. Fill those and give it as a JSON file, values must be a list.
            2. Don't Give any other suggestion or comments.
            3. Each Items inside the list must be a one word string or number (as required).
            4. Fill all the fields, its mandatory.

        """
    try:
        response = chat.send_message(prompt)
        return response.text
    except:
        st.error("An Error Occured! Please Try Again.")
    
def preprocess_json_string(json_string):
    inner_json_match = re.search(r'{(.+)}', json_string, re.DOTALL)
    if inner_json_match:
        inner_json = '{' + inner_json_match.group(1) + '}'
        json_to_dict = json.loads(inner_json)
        return json_to_dict
    else:
        st.error("Parse Error! Try Again!")
