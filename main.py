from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# 👉 Add this middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all domains (or restrict to yours later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# ------------------ SEARCH ------------------
@app.get("/search")
def search(q: str, type: str = "movie"):
    """
    type = movie | tv
    """
    url = f"{TMDB_BASE_URL}/search/{type}"
    params = {"api_key": TMDB_API_KEY, "query": q}
    r = requests.get(url, params=params)

    filtered = [item for item in r.get("results", []) if item.get("original_language") == "en"]
    return {"results" : filtered}

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