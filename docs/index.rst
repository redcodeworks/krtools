KR Tools
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A set of CLI tools for data malnipulation developed for
personal use.

Installation
------------

To install the `KR Tools` project, ensure you have
Python 3.11 or later.
run this command in your terminal:

.. code-block:: console

   $ pip install krtools

Or if you've clone the repo, use `poetry`.

.. code-block::

    $ poetry install

Usage
-----

KR Tools usage looks like:

.. code-block:: console

   $ krtools [OPTIONS]


.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.

KR Tools is a package of subcommands. For example,
to build an ORM model's DDL:

.. code-block:: console

    $ krtools sql build --schema movielens

Or to insert CSV files into a database:

.. code-block:: console

    $ krtools sql create ~/movies_test.csv --schema movielens --model movie


