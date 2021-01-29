# Install Ubuntu Dependencies
FROM ubuntu:18.04
ARG UBUNTU_PACKAGES="\
    git \
    golang-go \
    python3 \
    python3-pip \
    vim \
"
RUN apt-get update && apt-get install -y ${UBUNTU_PACKAGES}

# Install Python Dependencies
ARG PIP3_PACKAGES="\
    APScheduler==3.7.0 \ 
    beautifulsoup4==4.9.3 \
    discord==1.0.1 \
    mechanize==0.4.5 \
    pytest-6.2.1 \
    tweepy==3.10.0 \
"
RUN pip3 install ${PIP3_PACKAGES}

# Clone GitHub Repo and Bot Units
RUN git clone https://github.com/Atemosta/FEH-Gauntlet-Bot

# COPY . /app
# RUN make /app
# CMD python /app/app.py
