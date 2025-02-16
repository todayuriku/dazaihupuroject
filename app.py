import os
import re
import json
import io
import numpy as np              
from PIL import Image 

from flask import Flask, render_template, request, jsonify, send_file
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer

app = Flask(__name__)

# JSONデータをロード（エラーハンドリング付き）
DATA_FILE = "poems.json"
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"データファイル {DATA_FILE} が見つかりません")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    try:
        poems = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("poems.json の JSON 形式が正しくありません")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    """
    単語検索・タグ検索・その組み合わせ検索
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request, no JSON data provided"}), 400

        query = data.get("query", "").strip().lower()
        tag_filter = data.get("tag", "").strip().lower()

        results = []
        for poem in poems:
            poem_text = poem["句"].lower()

            # "AIタグ" がリストまたは文字列の場合の処理
            if isinstance(poem["AIタグ"], list):
                poem_tags = [tag.lower() for tag in poem["AIタグ"]]
            else:
                poem_tags = [poem["AIタグ"].lower()]

            # 単語検索とタグ検索の組み合わせ
            query_match = re.search(re.escape(query), poem_text, re.IGNORECASE) if query else True
            tag_match = any(tag_filter == tag or tag_filter in tag for tag in poem_tags) if tag_filter else True

            # 両方にヒットした場合のみ結果に追加
            if query_match and tag_match:
                results.append(poem)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/wordcloud", methods=["POST"])
def generate_wordcloud():
    """
    検索結果の["句"]から、形態素解析で単語に分割し、ストップワードを除外したテキストから
    ワードクラウド画像を生成し、PNG画像として返す
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request, no JSON data provided"}), 400

        query = data.get("query", "").strip().lower()
        tag_filter = data.get("tag", "").strip().lower()

        results = []
        for poem in poems:
            poem_text = poem["句"].lower()
            if isinstance(poem["AIタグ"], list):
                poem_tags = [tag.lower() for tag in poem["AIタグ"]]
            else:
                poem_tags = [poem["AIタグ"].lower()]

            query_match = re.search(re.escape(query), poem_text, re.IGNORECASE) if query else True
            tag_match = any(tag_filter == tag or tag_filter in tag for tag in poem_tags) if tag_filter else True

            if query_match and tag_match:
                results.append(poem)

        # 形態素解析用のトークナイザーを生成
        tokenizer = Tokenizer()

        # ストップワードの設定（必要に応じて追加・調整してください）
        stopwords = set([
            'や', 'し', 'ず', 'ん', 'お', 'ば', 'さ', 'だっ', 'れ', 'か', 'み', 'で', 'い',
            'の', 'に', 'は', 'を', 'が', 'と', 'た', 'よ', 'ね', 'する', 'れる', 'いる',
            'ある', 'なる', 'これ', 'それ', "です", "ます", "も", "だ", "成る", "為る", "居る",
            "て", "な", "思う", "。", "、", "！", "？", ",", "から", "ぬ"
        ])

        words = []
        # 各句ごとに形態素解析して単語に分割
        for poem in results:
            tokens = tokenizer.tokenize(poem["句"])
            for token in tokens:
                word = token.surface
                # ストップワードや不要な単語を除外
                if word not in stopwords:
                    words.append(word)
        
        # 単語がない場合の対応
        if not words:
            text = "データなし"
        else:
            text = " ".join(words)

        # マスク画像の読み込み（try ブロック内に正しくインデントする）
        mask = np.array(Image.open("./picture/n.png"))

        # ワードクラウド生成（日本語フォントを指定）
        wc = WordCloud(
            font_path="./fonts/NotoSansJP-Medium.ttf",
            background_color="#fff8e8",
            width=1000,
            height=1000,
            max_words=100,
            mask=mask,
        ).generate(text)

        img_io = io.BytesIO()
        wc.to_image().save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
