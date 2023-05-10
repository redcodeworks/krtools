"""Functions for inserting records into a SQL database

Todo:
    Handling for integrity errors.
    More file formats; currently limited to csv
"""

import csv
import itertools
import logging
import os
import sys
from io import TextIOWrapper, BytesIO
from pathlib import Path
from typing import Any, TextIO, Iterable, Iterator

import typer
from debugpy._vendored.pydevd import _pydev_bundle
from toolz import curry
from toolz.curried import *

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase, Session

from ..conf import conf


def _set_generator(file: TextIO | Path, fieldnames: list[str] | None) -> Iterator[dict]:
    """Structural pattern match on the input type."""
    logging.debug(f"Creating generator from {type(file)}")
    match file:
        case Path() as p:
            return _stream_csv(p, fieldnames)
        case _ as s:
            return csv.DictReader(s, fieldnames)


def _stream_csv(filename: Path, fieldnames: list[str]) -> Iterator[dict]:
    """Generator for buffered reading of input csv.

    The file is lazily read, returning one row at a time. CSV headers are used to create the dictionary keys.
    Since csv's are nortorious for structural errors, this approach is very fragile.

    Args:
        filename (pathlib.Path): A Pathlike object representing the absolute posix path to the csv file.

    Returns:
        dict: A dictionary with keys derived from the file headers.
    """
    with open(filename, "r", buffering=(1024**2) * conf.read_buffer) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            yield row


@curry
def upsert_from_file(
    engine: Engine,
    model: Any,
    file: TextIOWrapper | Path,
    columns: list[str] = None,
    upsert: bool = False,

) -> None:
    """Opens a database session and inserts (or merges) each row.

    Currently only handles csv files.
    Requires that column names match the target database column names.
    A more robust implementation would use a pydantic model for parsing each row before passing it onto the ORM.

    Args:
        engine (sqlalchemy.Engine): An engine from SQL Alchemy.
        model (sql.alchemy.DeclarativeBase): An ORM model from SQL Alchemy.
        file (sys.stdin | list[Path]): Standard input stream or a file path.
        columns (list[str]): Order list of column names. If not specified, will assume first row of file.
        upsert (bool): Flag that determines if matching keys should be merged.
    """
    logging.info(f"Inserting records from `{file}` using `{model.__name__}` ORM.")

    stream = _set_generator(file, columns)

    with Session(engine) as session, session.begin():
        insert = session.merge if upsert else session.add
        [insert(model(**row)) for row in stream]



