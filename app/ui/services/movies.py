import json
import os
from dataclasses import dataclass

from django.conf import settings

from ui import messages as msg
from ui.exceptions import MovieNotFoundError


@dataclass
class Movie:
    """Класс фильма."""
    id: int
    name: str
    description: str
    pic_path: str
    duration: str
    genres: str


class MoviesService:
    """Сервис фильмов."""

    def __init__(self) -> None:
        self.movies: dict[int, Movie] = {}

    def add_movie(self, movie: Movie):
        """Добавить фильм.

        Args:
            movie: фильм

        """
        self.movies[movie.id] = movie

    def get_movies(self) -> list[Movie]:
        """Получить список фильмов.

        Returns:
            list[Movie]: список фильмов

        """
        return list(self.movies.values())

    def get_movie(self, id: int) -> Movie:
        """Получить фильм по ID.

        Returns:
            Movie: фильм

        Raises:
            MovieNotFoundError: фильм не найден

        """
        if id not in self.movies:
            raise MovieNotFoundError(msg.MOVIE_NOT_FOUND)
        return self.movies[id]


movies_service = MoviesService()
movies_path = os.path.join(settings.BASE_DIR,
                           'ui', 'static', 'ui', 'json', 'movies.json')

with open(movies_path, encoding='utf-8') as file:
    movies = json.loads(file.read())
for movie in movies:
    movies_service.add_movie(Movie(**movie))
