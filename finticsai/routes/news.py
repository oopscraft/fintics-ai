import logging
import json
from flask import Blueprint, render_template, request, make_response
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from finticsai.modules.ollama import chatOllama

# ollama
prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
                      You are a helpful assistant. 
                      Please perform sentiment analysis on the given news article.
                      [input]
                      - 1st line is news URL
                      - 2nd line is news title
                      [output]
                      Response is JSON format with 'sentiment','confidence','reason'.
                      Ensure the response is only the JSON string with no additional text.
                      - 'sentiment' is one of POSITIVE, NEUTRAL, NEGATIVE.
                      - 'confidence' is 0~100 numeric value.
                      - 'reason' value must be translated into the language of input title.
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
    logging.info(f"request.json: {request.json}")

    # call
    content = f"""
        url: {request.json.get('url')}
        title: {request.json.get('title')}
        """
    human_message = HumanMessage(content=content)
    ai_message = chain.invoke({"message": [human_message]})
    logging.info(f"ai_message.content: {ai_message.content}")

    # response
    response_json = json.loads(ai_message.content)
    logging.info(f"response_json: {response_json}")
    return make_response(json.dumps(response_json, ensure_ascii=False), 200, {'Content-Type': 'application/json'})

