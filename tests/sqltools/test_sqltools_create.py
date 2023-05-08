
from sqltools_fixtures import engine, db_session
from pathlib import Path

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.movielens.orm import Movie
from krtools.sqltools.create import upsert_from_file

tgt_results = (100, 4203739173, 6.219)


@pytest.fixture()
def smt_summary():
    return select(
        func.count().label("count"),
        func.sum(Movie.revenue).label("total_revnue"),
        func.round(func.avg(Movie.vote_average), 3).label("average_vote"),
    )


def test_insert_file(engine, db_session: Session, smt_summary):
    upsert_from_file(Path("data/movies_test.csv"), engine, Movie, upsert=False)

    result = db_session.execute(smt_summary)
    assert result.first() == tgt_results


def test_upsert_file(engine, db_session: Session, smt_summary):
    upsert_from_file(Path("data/movies_test.csv"), engine, Movie, upsert=True)

    result = db_session.execute(smt_summary)
    assert result.first() == tgt_results
