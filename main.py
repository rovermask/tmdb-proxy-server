from fastapi import FastAPI, Query
import requests
import os

app = FastAPI()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"

@app.get("/search")
def search_movies(q: str = Query(...)):
    response = requests.get(TMDB_BASE_URL, params={
        "api_key": TMDB_API_KEY,
        "query": q
    })
    return response.json()
