"""CLI tool for working with SQL databases.

Todo:
    While neat, it does raise questions on the reusability as a command line tool.
    ORM models, to get the most out of them, can be DBMS-specific. In this instance
    the `movielens.Movie` model can be built with SQLite or Postgres with no problem,
    but this starts to break down when using more advanced features in any given
    SQL dialect.
    Brainstorm on a way on how to BYO-ORM.
"""

import logging
import sys
from importlib import import_module
from pathlib import Path

import sqlalchemy as sa
import typer
from rich import print
from sqlalchemy import Engine
from typing_extensions import Annotated

from .. import conf
from . import build as b
from . import create as c

app = typer.Typer()


def _sa_engine(sql_alchemy_tgt: str = None) -> Engine:
    """Generates a SQL Alchemy Engine

    Args:
        sql_alchemy_tgt (str, optional): The SQL alchemy connection string. If left blank,
            this will fallback on the value of `SQL_ALCHEMY_STRING` in the .env file or the
            system environment variable.

    Return:
        engine (sqlalchemy.Engine): An engine from SQL Alchemy. Can be used to open a DB session.
    """
    engine = sa.create_engine(
        sql_alchemy_tgt or conf.sql_alchemy_string.get_secret_value()
    )

    logging.info(f"Created engine for `{engine.url}`")

    return engine


@app.callback()
def callback(version: bool = typer.Option(None, is_eager=True)):
    """
    Set of tools for interacting with SQL databases.
    Uses config specified in .env file.
    """


@app.command()
def build(
    sql_alchemy_tgt: str = typer.Option(
        None, "--target", "-t", help="Target using SQL Alchemy string"
    ),
    schema_name: str = typer.Option(
        ..., "--schema", "-s", help="Corresponds to a directory in models."
    ),
) -> None:
    """Command line entry point for `sql build`

    Takes an ORM Model and builds the schema in the target database.
    See the `--help` flag for details.
    """
    engine = _sa_engine(sql_alchemy_tgt)
    model = import_module(f"models.{schema_name}").get_model("base")

    b.build_database(engine, model)


# TODO: Add support for more file types. Currently expects csvs
@app.command()
def create(
    input_files: list[str] = typer.Argument(
        None, help="List of files. Ignored if an input_dir is supplied"
    ),
    input_dir: str = typer.Option(
        None,
        "--input-dir",
        "-i",
        help="Path to a directory. Will process all filenames with appropriate extension.",
    ),
    sql_alchemy_tgt: str = typer.Option(
        None, "--target", "-t", help="Target using SQL Alchemy string"
    ),
    schema_name: str = typer.Option(
        ..., "--schema", "-s", help="Corresponds to a directory in models."
    ),
    model_name: str = typer.Option(
        ..., "--model", "-m", help="Corresponds to some matched model in a schema."
    ),
    upsert: bool = typer.Option(
        False, "--upsert", "-u", help="Overwrites if PK exists"
    ),
) -> None:
    """Command line entry poit for `sql create`

    This takes a file, or a directory of files, and inserts them into the target database.
    See the `--help` flag for details.
    """
    engine = _sa_engine(sql_alchemy_tgt)
    model = import_module(f"models.{schema_name}").get_model(model_name)

    # Generates a list of files normalized to the OS
    files = map(Path, input_dir or input_files)

    [c.upsert_from_file(f, engine, model, upsert=upsert) for f in files]


# TODO: Needs implementation
@app.command()
def read(item: str) -> None:
    print(f"Reading {item}")


# TODO: Needs implementation
@app.command()
def update(item: str) -> None:
    print(f"Updating {item}")


# TODO: Needs implementation
@app.command()
def delete(item: str) -> None:
    print(f"Deleting {item}")


# TODO: Needs implementation
@app.command()
def merge(item: str) -> None:
    print(f"Deleting {item}")


if __name__ == "__main__":
    app()
    sys.exit()
