# KR Tools

A personal toolkit for data malnipulation. A WIP.

## Installation

- Copy `.env.template` to `.env` and enter your configuration.
- Then use `poetry install` to install all project dependencies.
- Finally, use `poetry run krtools --help` for usage instructions.

## Usage

See documentation in `docs/`. Use `$ sphinx-build docs/ docs/_build` to build
API reference.

## SQL Tools

### Sample commands

Build an ORM model in a database.

`krtools sql build --schema movielens`

Insert a CSV file into a database from standard input.
`cat tests/data/movies_test.csv | krtools sql create --schema movielens --model movie`

Insert a single CSV file into a database.
`krtools sql create --schema movielens --model movie --upsert --input-files tests/data/movies_test.csv`

Insert many CSV files into a database.
`krtools sql create --schema movielens --model movie --upsert --input-files tests/data/`