from langchain_community.chat_models import ChatOllama
import os

# ollama
ollama_base_url = os.getenv('OLLAMA_BASE_URL', "http://127.0.0.1:11434")
ollama_model = os.getenv('OLLAMA_MODEL', "gemma:2b")
chatOllama = ChatOllama(model=ollama_model, base_url=ollama_base_url)
