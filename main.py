from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# 👉 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# ------------------ SEARCH ------------------
@app.get("/search")
def search(q: str, type: str = "movie"):
    url = f"{TMDB_BASE_URL}/search/{type}"
    params = {"api_key": TMDB_API_KEY, "query": q}
    r = requests.get(url, params=params).json()

    filtered = [
        item for item in r.get("results", [])
        if item.get("original_language") in ["en", "hi"]
    ]
    return {"results": filtered}

# ------------------ TRENDING ------------------
@app.get("/trending/{media_type}")
def trending(media_type: str):
    """
    media_type = movie | tv
    """
    url = f"{TMDB_BASE_URL}/trending/{media_type}/week"
    params = {"api_key": TMDB_API_KEY}

    r = requests.get(url, params=params).json()

    # optional filtering (same as search)
    filtered = [
        item for item in r.get("results", [])
        if item.get("original_language") in ["en", "hi"]
    ]

    return {"results": filtered}

# ------------------ MOVIE DETAILS ------------------
@app.get("/movie/{movie_id}")
def movie_details(movie_id: int):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    return r.json()

# ------------------ SERIES DETAILS ------------------
@app.get("/tv/{tv_id}")
def tv_details(tv_id: int):
    url = f"{TMDB_BASE_URL}/tv/{tv_id}"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    return r.json()