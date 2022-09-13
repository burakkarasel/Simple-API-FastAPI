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

# post request lets us to create a new movie and add it to the list


@app.post("/movies")
async def create_movie(movie: Movie):
    if movie in movies:
        return HTTPException(status_code=400, detail="movie already exists")

    movies.append(movie)
    return movie

# put request lets us to update the rate of a movie given


@app.put("/movies")
async def update_movie(movie: Movie):
    i = -1
    for idx, m in enumerate(movies):
        if m.title == movie.title:
            i = idx
            break
    else:
        return HTTPException(status_code=404, detail="movie not found")
    if movie.title and movie.director and movie.rate:
        movies[i].rate = movie.rate
        return movie

# delete lets us to remove a specific movie by it's id


@app.delete("/movies/{id}")
async def delete_movie(id: int = Path(None, description="The ID of the movie you want to delete", gt=0)):
    try:
        del movies[id - 1]
        return {"success": "movie is successfully deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="movie not found")
