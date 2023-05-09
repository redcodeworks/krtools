import csv
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
import sqlalchemy as sa
from pytest_mock import MockFixture
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session

from krtools import conf as app_conf
from models.movielens.orm import Base, Movie


@pytest.fixture(scope="module")
def engine() -> Engine:
    return sa.create_engine(app_conf.sql_alchemy_string.get_secret_value())


@pytest.fixture(scope="module")
def orm_metadata(engine) -> MetaData:
    metadata = MetaData()
    metadata.reflect(engine)
    return metadata


@pytest.fixture(scope="module")
def db_session(engine) -> Session:
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.rollback()
    session.close()


# TODO: Add a fixture for a minimal movie with the bare minimum info populated.
@pytest.fixture(scope="session")
def valid_movie() -> Movie:
    return Movie(
        adult=False,
        belongs_to_collection=None,
        budget=12500000,
        genres=str(
            [
                {"id": 28, "name": "Action"},
                {"id": 53, "name": "Thriller"},
                {"id": 80, "name": "Crime"},
                {"id": 10749, "name": "Romance"},
            ]
        ),
        homepage=None,
        id=319,
        imdb_id="tt0108399",
        original_language="en",
        original_title="True Romance",
        overview="REDACTED",
        popularity=17.189328,
        poster_path="/xBO8R3CZfrJ9rrwrZoJ68PgJyAR.jpg",
        production_companies=str(
            [
                {"name": "Davis-Films", "id": 342},
                {"name": "August Entertainment", "id": 3322},
                {"name": "Warner Bros.", "id": 6194},
                {"name": "Morgan Creek Productions", "id": 10210},
            ]
        ),
        production_countries=str(
            [{"iso_3166_1": "US", "name": "United States of America"}]
        ),
        release_date="1993-01-01",
        revenue=12281551,
        runtime=120,
        spoken_languages=str(
            [
                {"iso_639_1": "en", "name": "English"},
                {"iso_639_1": "it", "name": "Italiano"},
            ]
        ),
        status="Released",
        tagline="Stealing, Cheating, Killing. Who said romance was dead?",
        title="True Romance",
        video=False,
        vote_average=7.5,
        vote_count=762,
    )


@pytest.fixture(scope="session")
def movies_csv():
    with open(Path("tests/data/movies_test.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
