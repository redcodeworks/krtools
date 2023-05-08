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
    with open(filename, "r", buffering=(1024**2) * conf.read_buffer) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def upsert_from_file(
    filename: Path, engine: Engine, model: Any, upsert: bool = False
) -> None:
    logging.info(f"Inserting records from `{filename}` using `{model.__name__}` ORM.")

    with Session(engine) as session, session.begin():
        insert = session.merge if upsert else session.add
        [insert(model(**row)) for row in _stream_csv(filename)]
