import csv

import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
from ..conf import conf
import itertools

import logging


# Create a generator for streaming in the csv file's lines
def _stream_csv(filename):
    with open(filename, "r", buffering=(1024**2)*conf.read_buffer) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def upsert_from_file(filename, engine, model, merge=False):
    logging.info(f"Inserting records from `{filename}` using `{model.__name__}` ORM.")

    with Session(engine) as session, session.begin():
        insert = session.merge if merge else session.add
        [insert(model(**row)) for row in _stream_csv(filename)]

