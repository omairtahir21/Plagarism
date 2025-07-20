from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def google_check(sentence):
    query = '+'.join(sentence.split())
    url = f"https://www.google.com/search?q={query}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        return "plagiarized" if "did not match any documents" not in response.text else "original"
    except:
        return "error"

@app.route("/plagiarism-check", methods=["POST"])
def plagiarism_check():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    results = []
    for sentence in text.split("."):
        sentence = sentence.strip()
        if len(sentence) < 5:
            continue
        result = google_check(sentence)
        results.append({"sentence": sentence, "result": result})
        time.sleep(1.5)  # avoid Google blocking you

    plagiarized_count = sum(1 for r in results if r["result"] == "plagiarized")
    total = len(results)
    plagiarism_percent = round((plagiarized_count / total) * 100, 2) if total else 0

    return jsonify({
        "plagiarism_percent": plagiarism_percent,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True)
