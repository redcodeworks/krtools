"""Functions for inserting records into a SQL database

Todo:
    Handling for integrity errors.
    More file formats; currently limited to csv
"""

import csv
import itertools
import logging
import os
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase, Session

from ..conf import conf


# Create a generator for streaming in the csv file's lines
def _stream_csv(filename: Path) -> dict:
    """Generator for buffered reading of input csv.

    The file is lazily read, returning one row at a time. CSV headers are used to create the dictionary keys.
    Since csv's are nortorious for structural errors, this approach is very fragile.

    Args:
        filename (pathlib.Path): A Pathlike object representing the absolute posix path to the csv file.

    Returns:
        dict: A dictionary with keys derived from the file headers.
    """
    with open(filename, "r", buffering=(1024**2) * conf.read_buffer) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def upsert_from_file(
    filename: Path, engine: Engine, model: Any, upsert: bool = False
) -> None:
    """Opens a database session and inserts (or merges) each row.

    Currently only handles csv files.
    Requires that column names match the target database column names.
    A more robust implementation would use a pydantic model for parsing each row before passing it onto the ORM.

    Args:
        filename (pathlib.Path): A posix-compliant pathlike object.
        engine (sqlalchemy.Engine): An engine from SQL Alchemy.
        model (sql.alchemy.DeclarativeBase): An ORM model from SQL Alchemy.
        upsert (bool): Flag that determines if matching keys should be merged.
    """
    logging.info(f"Inserting records from `{filename}` using `{model.__name__}` ORM.")

    with Session(engine) as session, session.begin():
        insert = session.merge if upsert else session.add
        [insert(model(**row)) for row in _stream_csv(filename)]
