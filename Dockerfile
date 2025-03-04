FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 環境変数のデフォルト値を設定
ENV DIFY_API_KEY=""
ENV DIFY_API_ENDPOINT=""

# コンテナ起動時のコマンド
CMD ["python", "asulada_zonos_integration.py"] 