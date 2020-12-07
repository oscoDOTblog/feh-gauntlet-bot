FROM ubuntu:18.04

# COPY . /app
# RUN make /app
# CMD python /app/app.py

ARG UBUNTU_PACKAGES="\
    git \
"

RUN apt-get update && apt-get install -y ${UBUNTU_PACKAGES}

RUN git clone https://github.com/Atemosta/FEH-Gauntlet-Bot

RUN cd FEH-Gauntlet-Bot/

RUN git checkout k8s
