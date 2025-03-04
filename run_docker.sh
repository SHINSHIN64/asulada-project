#!/bin/bash

# .envファイルが存在しない場合は.env.sampleからコピー
if [ ! -f .env ]; then
  echo "Creating .env file from .env.sample..."
  cp .env.sample .env
  echo "Please edit .env file with your actual API keys before running the application."
  exit 1
fi

# Dockerイメージをビルド
echo "Building Docker image..."
docker-compose build

# Dockerコンテナを起動
echo "Starting Docker container..."
docker-compose up 