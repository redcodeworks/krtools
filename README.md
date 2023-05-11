# KR Tools

A personal toolkit for data malnipulation. A WIP.

## Installation
- Requires Python 3.11 and up. Project uses newer constructs like structual pattern matching.
- Ensure [`poetry`](https://github.com/python-poetry/poetry) is installed.
  - Since poetry is a standalone CLI app, it's preferable to _not_ use `pip`. Use `pipx`, a package manager, or the installer.
- `cp .env.template .env` and enter your configuration into the `.env` file.
  -  Alternatively, you can use environment variables.
  -  As of now, the most important configuration is the SQL Alchemy connection string, which specifies your target database. This is treated as a secret in the confiuration.
  -  **REMINDER:** Never commit your `.env` file to git.
- Then use `poetry install` to install all project dependencies.
- Finally, use `poetry run krtools --help` for usage instructions.

## Usage

See documentation in `docs/`. Use `$ sphinx-build docs/ docs/_build` to build
API reference. Currently, this has not been tested as a package, so the application is run with either 
`poetry run` or `python -m krtools`.

## SQL Tools

Conceptually, this application is meant to be used with a SQL Alchemy ORM. This is an area I'm brainstorming, but I would like to get this working so you can import your organizations ORM from a package from a private registry and then supply it on the command line. The challenge here is handling multiple SQL dialects, since not all are interchangable. As of now, The tests work with both SQLite and Postgres, but I'm not using any dialect-specific features of either.

### Sample commands

Build an ORM model in a database.

`krtools sql build --schema movielens`

Insert a CSV file into a database from standard input.
`cat tests/data/movies_test.csv | krtools sql create --schema movielens --model movie`

Insert a single CSV file into a database.
`poetry run krtools sql create --schema movielens --model movie --upsert --input-files tests/data/movies_test.csv`

Insert many CSV files into a database.
`poetry run krtools sql create --schema movielens --model movie --upsert --input-files tests/data/`
