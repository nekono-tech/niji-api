FROM python:latest

RUN apt update && \
    apt install -y --no-install-recommends \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    curl
RUN pip install --upgrade pip

# ワーキングディレクトリを設定
WORKDIR /nijiapi

# プロジェクトに必要なパッケージをインストール
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt