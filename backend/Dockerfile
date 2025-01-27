FROM python:3.10-bookworm
ENV GOOGLE_SERVICE_JSON_FILE=google-services.json

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY google-services.json .
COPY ./src ./src

EXPOSE 10000

CMD ["python", "src/demo_web_app.py"]

# docker build -t transcription-service .
# docker run -it -p 10000:10000 --name transcription-container transcription-service




# docker build --platform linux/amd64,linux/arm64 -t tsi2 . 
# docker tag e2d059d76f8d us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image
# docker push us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image 