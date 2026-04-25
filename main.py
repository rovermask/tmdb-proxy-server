from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from time import time

app = FastAPI()

cache = {}
CACHE_TTL = 60 * 30  # 30 minutes

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_cached_data(key, fetch_function):
    current_time = time()
    if key in cache:
        data, timestamp = cache[key]
        if current_time - timestamp < CACHE_TTL:
            return data
    data = fetch_function()
    cache[key] = (data, current_time)
    return data


# ── SEARCH ──────────────────────────────────────────────────────────────────
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


# ── TRENDING ─────────────────────────────────────────────────────────────────
@app.get("/trending/{media_type}")
def trending(media_type: str):
    def fetch():
        url = f"{TMDB_BASE_URL}/trending/{media_type}/week"
        params = {"api_key": TMDB_API_KEY}
        return requests.get(url, params=params).json()

    data = get_cached_data(f"trending_{media_type}", fetch)
    filtered = [
        item for item in data.get("results", [])
        if item.get("original_language") in ["en", "hi"]
    ]
    return {"results": filtered}


# ── MOVIE DETAILS ────────────────────────────────────────────────────────────
@app.get("/movie/{movie_id}")
def movie_details(movie_id: int):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    return r.json()


# ── SERIES DETAILS ───────────────────────────────────────────────────────────
@app.get("/tv/{tv_id}")
def tv_details(tv_id: int):
    url = f"{TMDB_BASE_URL}/tv/{tv_id}"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    return r.json()


# ── DISCOVER BY GENRE (movie OR tv) ─────────────────────────────────────────
@app.get("/discover/{media_type}")
def discover_by_genre(media_type: str, genre_id: int):
    """
    Supports both /discover/movie?genre_id=28
    and         /discover/tv?genre_id=28
    """
    cache_key = f"discover_{media_type}_{genre_id}"

    def fetch():
        url = f"{TMDB_BASE_URL}/discover/{media_type}"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
        }
        return requests.get(url, params=params).json()

    data = get_cached_data(cache_key, fetch)

    filtered = [
        item for item in data.get("results", [])
        if item.get("original_language") in ["en", "hi"]
    ]
    return {"results": filtered}