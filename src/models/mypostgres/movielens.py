import re
import datetime

from pydantic import BaseModel

import sqlalchemy as sa
from pydantic.dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Numeric, DateTime, BIGINT
import sqlalchemy.types as types
from sqlalchemy.orm import DeclarativeBase, Mapped, validates
from sqlalchemy.orm import mapped_column as col


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BIGINT,
        datetime.datetime: DateTime(timezone=True)
    }


# TODO: Add more precise constraints
class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = col(primary_key=True)
    imdb_id: Mapped[str]
    title: Mapped[str]
    release_date: Mapped[datetime.datetime | None]
    adult: Mapped[str]
    belongs_to_collection: Mapped[str | None]
    budget: Mapped[int]
    genres: Mapped[str]
    homepage: Mapped[str | None]
    original_language: Mapped[str]
    original_title: Mapped[str]
    overview: Mapped[str]
    popularity: Mapped[float | None]
    poster_path: Mapped[str]
    production_companies: Mapped[str]
    production_countries: Mapped[str]
    revenue: Mapped[int | None]
    runtime: Mapped[float | None]
    spoken_languages: Mapped[str]
    status: Mapped[str]
    tagline: Mapped[str | None]
    video: Mapped[str]
    vote_average: Mapped[float | None]
    vote_count: Mapped[int | None]

    # TODO: Put validator on CSV parsing side.
    @validates("runtime", "budget", "revenue", "popularity", "vote_average", "vote_count")
    def _empty_string_to_none(self, key, value):
        return value if value else None

    @validates("release_date")
    def _correct_date_format(self, key, value):
        date_pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
        # date_pattern = "%Y-%m-%d"
        if not value:
            return None
        elif isinstance(value, datetime.datetime):
            return value
        elif re.match(date_pattern, value):
            return datetime.datetime.strptime(value, "%Y-%m-%d")
        else:
            raise ValueError("Not a valid date format")

    def __repr__(self):
        return f"Movie({self.id}, {self.title}, {self.release_date})"


