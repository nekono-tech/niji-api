FROM python:3.12-slim

# 必要なパッケージのインストール
RUN apt update && \
    apt install -y --no-install-recommends \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    wget \
    gnupg \
    zip \
    unzip \
    curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# google-chrome のインストール
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# pip のアップグレード
RUN pip install --upgrade pip

# ワーキングディレクトリを設定
WORKDIR /nijiapi

# プロジェクトに必要なパッケージをインストール
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt