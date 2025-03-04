@echo off
echo Asurada GPT + Zonos 統合システム - Docker起動スクリプト

REM .envファイルが存在しない場合は.env.sampleからコピー
if not exist .env (
  echo Creating .env file from .env.sample...
  copy .env.sample .env
  echo Please edit .env file with your actual API keys before running the application.
  pause
  exit /b 1
)

REM Dockerイメージをビルド
echo Building Docker image...
docker-compose build

REM Dockerコンテナを起動
echo Starting Docker container...
docker-compose up

pause 