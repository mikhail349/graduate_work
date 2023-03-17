import json
import os
from dataclasses import dataclass

from django.conf import settings
from django.templatetags.static import static


@dataclass
class Movie:
    id: int
    name: str
    description: str
    pic_path: str
    duration: str
    genres: str


class MoviesService:
    def __init__(self):
        self.movies: dict[int, Movie] = {}

    def add_movie(self, movie: Movie):
        self.movies[movie.id] = movie

    def get_movies(self) -> list[Movie]:
        return self.movies.values()

    def get_movie(self, id: int) -> Movie:
        return self.movies.get(id)

movies_service = MoviesService()
movies_path = os.path.join(settings.BASE_DIR, 'ui', 'static', 'ui', 'json', 'movies.json')

with open(movies_path, encoding='utf-8') as file:
    movies = json.loads(file.read())
for movie in movies:
    movies_service.add_movie(Movie(**movie))
