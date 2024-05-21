import logging
import json
from flask import Blueprint, render_template, request, make_response
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

# ollama
chatOllama = ChatOllama(model = "phi3")
prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
                      You are a helpful assistant. 
                      Please perform sentiment analysis on the given news article.
                      - Response is JSON format with 'sentiment','confidence','reason'.
                      - Ensure the response is only the JSON string with no additional text.
                      - 'sentiment' is one of POSITIVE, NUETRAL, NEGATIVE.
                      - 'confidence' is 0~100 numeric value.
                      - 'reason' value is translated into the language of the article.
                      """),
        MessagesPlaceholder(variable_name = "message")
    ])
chain = prompt | chatOllama

# blue print
news = Blueprint('news', __name__)

# GET /news
@news.route('/news')
def get_news():
    return render_template('news.html')

# POST /news
@news.route('/news', methods = ['POST'])
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

