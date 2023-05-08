from sqltools_fixtures import engine, db_session, valid_movie, orm_metadata
from sqlalchemy import select, MetaData, Column
from sqlalchemy.orm import Session
from models.mypostgres.movielens import Movie


def test_tables_exists(engine, db_session: Session, orm_metadata: MetaData):
    assert "movies" in orm_metadata.tables, "movies table exists"
    assert {col.name for col in orm_metadata.tables['movies'].c} >= {'id', 'title', 'release_date'}, "basic column names exist"


def test_simple_query(engine, db_session: Session, valid_movie: Movie):
    db_session.add(valid_movie)
    smt = select(Movie)
    result = db_session.execute(smt)
    assert result.scalars().first().title == "True Romance"