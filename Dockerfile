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
    aiohttp==3.6.3
    APScheduler==3.6.3
    asn1crypto==0.24.0
    async-timeout==3.0.1
    attrs==20.3.0
    Automat==0.6.0
    beautifulsoup4==4.9.3
    blinker==1.4
    bs4==0.0.1
    certifi==2020.12.5
    chardet==4.0.0
    click==6.7
    cloud-init==20.3
    colorama==0.3.7
    command-not-found==0.3
    configobj==5.0.6
    constantly==15.1.0
    cryptography==2.1.4
    discord==1.0.1
    discord.py==1.5.1
    distro-info===0.18ubuntu0.18.04.1
    html5lib==1.1
    httplib2==0.9.2
    hyperlink==17.3.1
    idna==2.10
    idna-ssl==1.1.0
    incremental==16.10.1
    Jinja2==2.10
    jsonpatch==1.16
    jsonpointer==1.10
    jsonschema==2.6.0
    keyring==10.6.0
    keyrings.alt==3.0
    language-selector==0.1
    MarkupSafe==1.0
    mechanize==0.4.5
    multidict==4.7.6
    netifaces==0.10.4
    oauthlib==3.1.0
    PAM==0.4.2
    pyasn1==0.4.2
    pyasn1-modules==0.2.1
    pycrypto==2.6.1
    pygobject==3.26.1
    PyJWT==1.5.3
    pyOpenSSL==17.5.0
    pyserial==3.4
    PySocks==1.7.1
    python-apt==1.6.5+ubuntu0.4
    python-crontab==2.5.1
    python-dateutil==2.8.1
    python-debian==0.1.32
    pytz==2020.5
    pyxdg==0.25
    PyYAML==3.12
    requests==2.25.1
    requests-oauthlib==1.3.0
    requests-unixsocket==0.1.5
    SecretStorage==2.3.1
    service-identity==16.0.0
    six==1.15.0
    soupsieve==2.1
    ssh-import-id==5.7
    systemd-python==234
    tweepy==3.10.0
    Twisted==17.9.0
    typing-extensions==3.7.4.3
    tzlocal==2.1
    ufw==0.36
    unattended-upgrades==0.1
    urllib3==1.26.2
    webencodings==0.5.1
    yarl==1.5.1
    zope.interface==4.3.2
"
RUN pip3 install ${PIP3_PACKAGES}

# Clone GitHub Repo and Bot Units
RUN git clone https://github.com/Atemosta/FEH-Gauntlet-Bot

# COPY . /app
# RUN make /app
# CMD python /app/app.py
