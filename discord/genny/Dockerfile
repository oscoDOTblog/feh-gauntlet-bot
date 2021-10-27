# Select Docker image
FROM python:3.8-slim

# Create app directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Bundle app source
COPY genny.py /app
COPY config.py /app
COPY discordclient.py /app


