
from sqltools_fixtures import engine, db_session # isort: skip
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from krtools.sqltools.create import upsert_from_file
from models.movielens.orm import Movie

tgt_results = (100, 4203739173, 6.219)


@pytest.fixture()
def smt_summary():
    return select(
        func.count().label("count"),
        func.sum(Movie.revenue).label("total_revnue"),
        func.round(func.avg(Movie.vote_average), 3).label("average_vote"),
    )


def test_insert_file(engine, db_session: Session, smt_summary):
    upsert_from_file(engine, Movie, Path("tests/data/movies_test.csv"), upsert=False)

    result = db_session.execute(smt_summary)
    assert result.first() == tgt_results


def test_upsert_file(engine, db_session: Session, smt_summary):
    upsert_from_file(engine, Movie, Path("tests/data/movies_test.csv"), upsert=True)

    result = db_session.execute(smt_summary)
    assert result.first() == tgt_results
