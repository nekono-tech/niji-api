FROM python:3.12-slim

# 必要なパッケージのインストール
RUN apt update && \
    apt install -y --no-install-recommends \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# pip のアップグレード
RUN pip install --upgrade pip

# ワーキングディレクトリを設定
WORKDIR /nijiapi

# プロジェクトに必要なパッケージをインストール
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt