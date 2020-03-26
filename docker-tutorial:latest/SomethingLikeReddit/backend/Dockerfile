# FROM python:2.7-alpine
FROM python:alpine


# keep this file separate to avoid pip install for every change in source
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /backend/

EXPOSE 5005

# auto-restart on file changes
ENV FLASK_DEBUG=0
ENV PYTHONPATH=/backend/server

ENV MONGO_URI="mongodb://admin:imse@localhost:27017/slr?authSource=admin"

WORKDIR /backend

ENTRYPOINT ["python", "app.py"]
