"""Functions for writing DDL commands to a database."""

import csv
import itertools
import json
import logging
import os
from typing import Any

import sqlalchemy as sa
from rich import print
from rich.pretty import pprint
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session

from ..conf import conf


def build_database(engine: Engine, model: Any) -> None:
    """Takes an ORM and builds the DDL in the target database.

    Args:
        engine (sqlalchemy.Engine): A engine from SQL Alchemy.
        model (sqlalchemy.DeclarativeBase): An ORM model from SQL Alchemy.
    """
    model.metadata.create_all(engine)
    metadata = MetaData()
    metadata.reflect(engine)
    logging.info(f"Created database with tables {dict(metadata.tables)}")
    pprint(dict(metadata.tables))
