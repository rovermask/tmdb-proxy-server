from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # store key safely in env variable
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

@app.route("/")
def home():
    return {"message": "TMDB Proxy Server is running!"}

@app.route("/suggest")
def suggest():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1
    }

    try:
        response = requests.get(TMDB_SEARCH_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = [
            {"title": m["title"], "year": m.get("release_date", "")[:4]}
            for m in data.get("results", [])
        ]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})
