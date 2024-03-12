import json
import getpass
import os
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.messages import HumanMessage, SystemMessage
import time
import streamlit as st
#from langchain.memory import ConversationBufferMemory
import google.generativeai as genai
from config import API_KEY

genai.configure(api_key = API_KEY)

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

def generate_description_string(df, slice_number):
    return '\n'.join(f'{i + 1}. {desc}' for i, desc in enumerate(df['description'][:slice_number], start=0))

def set_initial_message():
    try:
        chat.send_message(st.session_state.desc_string)
    except:
        pass

print(chat.history)