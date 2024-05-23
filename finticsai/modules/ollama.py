from langchain_community.chat_models import ChatOllama
import os

# ollama
ollama_url = os.getenv('OLLAMA_URL', "http://127.0.0.1:11434")
chatOllama = ChatOllama(model = "gemma:2b", base_url = ollama_url)
