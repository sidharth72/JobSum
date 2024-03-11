import json
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import time
import streamlit as st
import config


model = ChatGoogleGenerativeAI(model = 'gemini-pro', convert_system_message_to_human=True)

def chat_with_gemini(prompt):
    result = model.invoke(prompt)
    
    for word in result.content.split():
        yield word + " "
        time.sleep(0.05)