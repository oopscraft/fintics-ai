FROM python:3.12

# working directory
WORKDIR /app

# env
ENV PYTHONPATH=/app

# pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps

# source
COPY ./finticsai/ ./finticsai

# expose 
EXPOSE 8080

# command
ENTRYPOINT ["gunicorn", "-w", "5", "-b", "0.0.0.0:8080", "finticsai.app:app"]
