# Install Ubuntu Dependencies
FROM ubuntu:18.04
ARG UBUNTU_PACKAGES="\
    vim \
    git \
    python3 \
    python3-pip \
"
RUN apt-get update && apt-get install -y ${UBUNTU_PACKAGES}

# Install Python Dependencies
ARG PIP3_PACKAGES="\
    mechanize \
    bs4 \
    tweepy \
"
RUN pip3 install ${PIP3_PACKAGES}

# Clone GitHub Repo and Start Genny Bot
RUN git clone https://github.com/Atemosta/FEH-Gauntlet-Bot

RUN cd FEH-Gauntlet-Bot/

RUN git checkout k8s

# COPY . /app
# RUN make /app
# CMD python /app/app.py
