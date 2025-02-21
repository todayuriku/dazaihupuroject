# Pythonの公式イメージを使用
FROM python:3.10

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナ内にコピー
COPY . /app/

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flask アプリを起動（ポート 8080）
CMD ["python", "app.py"]
