FROM python:3.12

# working directory
WORKDIR /app

# env
ENV PYTHONPATH=/app

# pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# source
COPY ./finticsai/ ./finticsai

# start.sh
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 3\n\
ollama run llama3\n\
python3 ./finticsai/app.py\n' > /app/start.sh

# chmod
RUN chmod +x /app/start.sh

# expose 
EXPOSE 8080

# command 
ENTRYPOINT ["./start.sh"]

