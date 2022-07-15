# Select Docker image
FROM python:3.9-slim-buster

# Create app directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install app dependencies
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pip install --upgrade pip
RUN pip install pipenv --upgrade
RUN pipenv install --system --deploy

# Bundle app source
COPY genny.py /app
COPY config.py /app
COPY discordclient.py /app


