import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Self, Union


class BaseClass:
    def post_init(self) -> Self:
        if hasattr(self, 'updated_at') and self.updated_at:
            self.updated_at = self.updated_at.strftime('%Y-%m-%d')
        self.created_at = self.created_at.strftime('%Y-%m-%d')
        return self

    def cut_date(self) -> Self:
        if hasattr(self, 'updated_at') and self.updated_at:
            self.updated_at = self.updated_at[0:10]
        self.created_at = self.created_at[0:10]
        return self


@dataclass
class Genre(BaseClass):
    id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Person(BaseClass):
    id: uuid.UUID
    full_name: str
    created_at: str
    updated_at: str


@dataclass
class FilmWork(BaseClass):
    id: uuid.UUID
    title: str
    type: str
    description: Optional[str]
    creation_date: str
    file_path: str
    created_at: str
    updated_at: str
    rating: float = field(default=0.0)


@dataclass
class GenreFilmWork(BaseClass):
    id: uuid.UUID
    film_work_id: str
    genre_id: str
    created_at: Optional[Union[str, datetime]]


@dataclass
class PersonFilmWork(BaseClass):
    id: uuid.UUID
    film_work_id: str
    person_id: str
    role: str
    created_at: Optional[Union[str, datetime]]
