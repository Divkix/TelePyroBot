FROM python:3.8.6-slim-buster

ENV PIP_NO_CACHE_DIR 1

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

COPY . /root

WORKDIR /root

# Add Extra Repositories
RUN apt update && apt upgrade -y && apt install software-properties-common -y
RUN add-apt-repository main 
RUN add-apt-repository contrib
RUN add-apt-repository non-free


# Installing Required Packages
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    debian-keyring \
    debian-archive-keyring \
    bash \
    bzip2 \
    curl \
    figlet \
    git \
    util-linux \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libwebp-dev \
    linux-headers-amd64 \
    musl-dev \
    musl \
    neofetch \
    php-pgsql \
    python3-lxml \
    postgresql \
    postgresql-client \
    python3-psycopg2 \
    libpq-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-pip \
    python3-requests \
    python3-sqlalchemy \
    python3-tz \
    python3-aiohttp \
    openssl \
    pv \
    jq \
    tree \
    wget \
    python3 \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    gcc \
    sqlite3 \
    libsqlite3-dev \
    sudo \
    zlib1g \
    ffmpeg \
    libssl-dev \
    libgconf-2-4 \
    libxi6 \
    xvfb \
    unzip \
    libopus0 \
    libopus-dev \
    p7zip-full \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

RUN pip3 install --upgrade pip setuptools

RUN pip install --upgrade -r requirements.txt

CMD ["python3", "-m", "telepyrobot"]
