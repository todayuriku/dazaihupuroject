# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 日本語フォントとビルドに必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python パッケージの依存関係をコピー
COPY requirements.txt .

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# ポート8080を公開
EXPOSE 8080

# Waitressでアプリケーションを実行（0.0.0.0で全てのインターフェースをリッスン）
CMD ["python", "-c", "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=8080)"]

# requirements.txt
flask==2.0.1
waitress==2.0.0
pillow==8.4.0
wordcloud==1.8.1
janome==0.4.1
numpy==1.21.0

# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./templates:/app/templates
      - ./static:/app/static
      - ./picture:/app/picture
      - ./fonts:/app/fonts
      - ./poems.json:/app/poems.json
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
    restart: always

# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.log
.git
.gitignore
Dockerfile
docker-compose.yml
README.md