from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

# Movie holds movie data


class Movie:
    title: str
    director: str
    rate: float

    def __init__(self, title, director, rate):
        self.title = title
        self.director = director
        self.rate = rate


# movies holds our movies
movies = [Movie("Fight Club", "David Fincher", 8.8),
          Movie("Pulp Fiction", "Quentin Tarantino", 8.9),
          Movie("Wolf of the Wall Street", "Martin Scorsese", 8.2),
          Movie("Interstellar", "Cristopher Nolan", 8.6),
          Movie("Tenet", "Cristopher Nolan", 7.3),
          Movie("Goodfellas", "Martin Scorsese", 8.7)]


@app.get("/movies/{id}")
# Path lets us to use validators on path parameters
async def get_movie(id: int = Path(None, description="The ID of the movie you want to view", gt=0, le=len(movies))):
    try:
        return {movies[id - 1]}
    except Exception:
        raise HTTPException(status_code=404, detail="invalid id")


@app.get("/movies")
# Query lets us to use validators on query values
async def list_movies(limit: int = Query(None, description="limit of movies you can get between 3-5", ge=3, le=5), offset: int = Query(None, description="start point", ge=1)):
    try:
        return movies[(offset-1) * limit: limit * offset]
    except:
        raise HTTPException(status_code=400, detail="invalid params")
