import json
import logging

from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, make_response
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from finticsai.modules.ollama import chatOllama
from finticsai.modules.browser import get_html_content
from urllib.parse import urlparse
import re

# ollama
prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
                      You are a helpful assistant. 
                      Please perform sentiment analysis on the given news article.
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

    # news content
    news_content = get_news_content(request.json.get('url'))
    logging.info(f"news_content:{news_content}")

    # call
    human_message_content = f"""
        {request.json.get('title')}
        {news_content}
        """
    human_message = HumanMessage(content=human_message_content)
    ai_message = chain.invoke({"message": [human_message]})
    logging.info(f"ai_message.content: {ai_message.content}")

    # response
    response_json = json.loads(ai_message.content)
    logging.info(f"response_json: {response_json}")
    return make_response(json.dumps(response_json, ensure_ascii=False), 200, {'Content-Type': 'application/json'})


def get_news_content(url):
    if ("www.hankyung.com" in url):
        soup = get_soup(url)
        element = soup.find(id="articletxt")
        return element.get_text() if element else ""

    if ("finance.yahoo.com" in url):
        soup = get_soup(url)
        element = soup.find('div', class_="caas-body")
        return element.get_text() if element else ""

    if ("www.investing.com" in url):
        soup = get_soup(url)
        pattern = re.compile(r'article_.*')
        element = soup.find('div', class_=pattern)
        return element.get_text() if element else ""

    if ("www.defenseworld.net" in url):
        soup = get_soup(url)
        element = soup.find('article')
        return element.get_text() if element else ""

    if ("www.marketbeat.com" in url):
        soup = get_soup(url)
        element = soup.find('article', id_='shareableArticle')
        return element.get_text() if element else ""

    return ""

def get_soup(url):
    html_content = get_html_content(url)
    return BeautifulSoup(html_content, 'html.parser')

