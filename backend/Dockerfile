FROM python:3.10-bookworm
ENV GOOGLE_SERVICE_JSON_FILE=google-services.json

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY google-services.json .
COPY ./src ./src

EXPOSE 10000

CMD ["python", "src/demo_web_app.py"]

# docker build -t transcription-service .
# docker run -p 10000:10000 --name transcription-container transcription-service