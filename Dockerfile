FROM python:3.12

# working directory
WORKDIR /app

# env
ENV PYTHONPATH=/app

# pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# source
COPY ./finticsai/ ./finticsai

# expose 
EXPOSE 8080

# command 
ENTRYPOINT ["python", "finticsai/app.py"]

