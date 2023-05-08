import logging
import sys

import typer
from rich import print
from importlib import import_module
from pathlib import Path

from typing_extensions import Annotated

from .. import conf
import sqlalchemy as sa
from . import create as c

app = typer.Typer()


def _sa_engine(sql_alchemy_tgt: str = None):
    """Generates a SQL Alchemy Engine

    If a target is explicitly provided, it will fall back on the env variable `SQL_ALCHEMY_STRING`

    :param sql_alchemy_tgt: str
    :return: a SQL alchemy engine
    """
    engine = sa.create_engine(
        sql_alchemy_tgt or conf.sql_alchemy_string.get_secret_value()
    )

    logging.info(f"Created engine for `{engine.url}`")

    return engine

@app.callback()
def callback(
        version: bool = typer.Option(
            None, is_eager=True
        )
):
    """
    Set of tools for interacting with SQL databases.
    Uses config specified in .env file.
    """


# TODO: Add support for more file types. Currently expects csvs
@app.command()
def create(
        input_files: list[str] = typer.Argument(None, help="List of files. Ignored if an input_dir is supplied"),
        input_dir: str = typer.Option(None, "--input-dir", "-i",
                                      help="Path to a directory. Will process all filenames with appropriate extension."),
        sql_alchemy_tgt: str = typer.Option(None, "--target", "-t", help="Target using SQL Alchemy string"),
        schema_name: str = typer.Option(..., "--schema", "-s", help="Corresponds to a directory in models."),
        model_name: str = typer.Option(..., "--model", "-m", help="Corresponds to some matched model in a schema."),
        upsert: bool = typer.Option(False, "--upsert", "-u", help="Overwrites if PK exists")
):
    engine = _sa_engine(sql_alchemy_tgt)
    model = import_module(f"models.{schema_name}").get_model(model_name)

    # Generates a list of files normalized to the OS
    files = map(Path, input_dir or input_files)

    [c.upsert_from_file(f, engine, model, upsert=upsert) for f in files]


# TODO: Needs implementation
@app.command()
def read(item: str):
    print(f"Reading {item}")


# TODO: Needs implementation
@app.command()
def update(item: str):
    print(f"Updating {item}")


# TODO: Needs implementation
@app.command()
def delete(item: str):
    print(f"Deleting {item}")


# TODO: Needs implementation
@app.command()
def merge(item: str):
    print(f"Deleting {item}")


if __name__ == "__main__":
    app()
    sys.exit()
