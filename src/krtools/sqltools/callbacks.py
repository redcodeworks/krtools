import typing
from typing import TextIO

import typer
from toolz.curried import *
from pathlib import Path
import re


def parse_paths(ctx: typer.Context, name: str) -> typing.Iterable[Path] | None:
    """Transforms a directory name into a list of Posix file paths
        If the supplied name is already a file, then it will return a
        monadic collection.
    """
    if not name:
        return
    elif Path(name).is_file():
        return iter([Path(name)])
    else:
        return pipe(
            Path(name).iterdir(),
            filter(lambda x: x.is_file()),
            filter(lambda x: re.match("^.*\.(csv|CSV)$", str(x))),
            iter
        )


def parse_list(ctx: typer.Context, param: typer.CallbackParam, ls: list) -> list | None:
    return ls if ls else None
