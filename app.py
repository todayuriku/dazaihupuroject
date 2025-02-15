import os
import re
import json
from flask import Flask, render_template, request, jsonify

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
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request, no JSON data provided"}), 400

        query = data.get("query", "").strip().lower()
        tag_filter = data.get("tag", "").strip().lower()

        results = []
        for poem in poems:
            poem_text = poem["句"].lower()

            # "AIタグ" がリストまたは文字列である場合の処理
            if isinstance(poem["AIタグ"], list):
                poem_tags = [tag.lower() for tag in poem["AIタグ"]]
            else:
                poem_tags = [poem["AIタグ"].lower()]

            # 単語検索とタグ検索の組み合わせ
            query_match = re.search(re.escape(query), poem_text, re.IGNORECASE) if query else True
            tag_match = any(tag_filter == tag or tag_filter in tag for tag in poem_tags) if tag_filter else True

            # 単語検索とタグ検索の両方にヒットした場合のみ結果に追加
            if query_match and tag_match:
                results.append(poem)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")

