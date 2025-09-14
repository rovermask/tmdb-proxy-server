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
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"

@app.get("/search")
def search_movies(q: str = Query(...)):
    response = requests.get(TMDB_BASE_URL, params={
        "api_key": TMDB_API_KEY,
        "query": q
    })
    return response.json()
