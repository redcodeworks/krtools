"""Typer app group and CLI entry point"""
import sys

import typer

from . import __version__
from .sqltools.__main__ import app as sqltools

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"KR Tools: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    )
):
    """
    KR Tools By Kevin Riley
    A collection of data-focused command line tools
    :param version: __version__
    :return:
    """


app.add_typer(sqltools, name="sql")


if __name__ == "__main__":
    app()
    sys.exit()
