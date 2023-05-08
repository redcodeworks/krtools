import csv
import json
from typing import Any

import sqlalchemy as sa
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session
import os
from ..conf import conf
import itertools
from rich import print
from rich.pretty import pprint
import logging


def build_database(engine: Engine, model: Any) -> None:
    model.metadata.create_all(engine)
    metadata = MetaData()
    metadata.reflect(engine)
    logging.info(f"Created database with tables {dict(metadata.tables)}")
    pprint(dict(metadata.tables))
