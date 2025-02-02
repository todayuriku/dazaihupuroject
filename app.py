from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


with open("poems.json", "r", encoding="utf-8") as f:
    poems = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query", "")
    results = [poem for poem in poems if query in poem["句"]]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)