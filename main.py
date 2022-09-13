from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI()

# Movie holds movie data


class Movie(BaseModel):
    title: str
    director: str
    rate: float


# movies holds our movies
movies = []


@app.get("/movies/{id}")
# Path lets us to use validators on path parameters
async def get_movie(id: int = Path(None, description="The ID of the movie you want to view", gt=0)):
    try:
        return movies[id - 1]
    except Exception:
        raise HTTPException(status_code=404, detail="Not Found")


@app.get("/movies")
# Query lets us to use validators on query values
async def list_movies(limit: int = Query(None, description="limit of movies you can get between 3-5", ge=3, le=5), offset: int = Query(None, description="page id", ge=1)):
    try:
        return movies[(offset-1) * limit: limit * offset]
    except:
        raise HTTPException(status_code=400, detail="invalid params")


@app.post("/movies")
async def create_movie(movie: Movie):
    if movie in movies:
        return HTTPException(status_code=400, detail="movie already exists")

    movies.append(movie)
    return movie
