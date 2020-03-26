#download the python image
FROM python:3.7.2

#set a directory for the app
WORKDIR /app

ADD . /app
ADD requirements.txt requirements.txt

#install dependencies
RUN pip install -r requirements.txt

#run the command
CMD [ "uwsgi", "app.ini" ]