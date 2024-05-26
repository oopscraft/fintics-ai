import logging
from flask import Flask 
from finticsai.routes.chat import chat
from finticsai.routes.news import news
from langchain_community.chat_models import ChatOllama
import nest_asyncio

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# app
app = Flask(__name__)

# nest_asyncio 적용
nest_asyncio.apply()

# register module
app.register_blueprint(chat)
app.register_blueprint(news)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port="8080",
        debug=True, 
        use_reloader=False
    )
