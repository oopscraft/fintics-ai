import logging
import json
from flask import Blueprint, render_template, request, jsonify, make_response
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from finticsai.modules.ollama import chatOllama

# ollama
prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are a helpful assistant."),
        MessagesPlaceholder(variable_name = "message")
    ])
chain = prompt | chatOllama

# blue print
chat = Blueprint('chat', __name__)

# GET /chat
@chat.route('/chat')
def get_chat():
    return render_template('chat.html')

# POST /chat
@chat.route('/chat', methods = ['POST'])
def post_chat():
    request_message = request.json.get('message')
    logging.info(f"request_message:{request_message}") 

    # interact
    human_message = HumanMessage(content=request_message)
    ai_message = chain.invoke({"message": [human_message]})
    logging.info(f"ai_message: {ai_message}")

    # response
    response_message = ai_message.content;
    logging.info(f"response_message:{response_message}")
    response_data = {"message": response_message}
    response_json = json.dumps(response_data, ensure_ascii=False)
    return make_response(response_json, 200, {'Content-Type': 'application/json'})

