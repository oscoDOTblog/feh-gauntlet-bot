# Select Docker image
FROM python:3.8-slim-buster

# Create app directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Bundle app source
COPY api.py /app
COPY config.py /app
COPY gauntlet_template.py /app
# COPY secrets.py /app


