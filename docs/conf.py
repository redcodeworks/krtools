# docs/conf.py
"""Sphinx configuration.

Run with:
    $ sphinx-build docs/ docs/_build
"""
project = "KR Tools"
author = "Kevin Riley"
copyright = f"2023, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
