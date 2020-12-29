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
    beautifulsoup4==4.9.3 \
    bs4==0.0.1 \
    certifi==2020.12.5 \
    chardet==4.0.0 \
    html5lib==1.1 \
    idna==2.10 \
    mechanize==0.4.5 \
    oauthlib==3.1.0 \
    PySocks==1.7.1 \
    requests==2.25.1 \
    requests-oauthlib==1.3.0 \
    six==1.15.0 \
    soupsieve==2.1 \
    tweepy==3.9.0 \
    urllib3==1.26.2 \
    webencodings==0.5.1 \
"
RUN pip3 install ${PIP3_PACKAGES}

# Clone GitHub Repo and Bot Units
RUN git clone https://github.com/Atemosta/FEH-Gauntlet-Bot

# COPY . /app
# RUN make /app
# CMD python /app/app.py
