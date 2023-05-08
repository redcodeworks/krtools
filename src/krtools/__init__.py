import logging
import os
from pathlib import Path

import click

from .conf import conf

# App scaffolding
__version__ = "0.1.0"

# App directory where logs and other artifacts are saved
__appdir__ = Path(click.get_app_dir(__name__))
__appdir__.mkdir(parents=True, exist_ok=True)

# Base logging config to file
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=__appdir__.joinpath(f"{__name__}.log"),
    filemode="a",
    force=True,
)

# Live logger
console = logging.StreamHandler()
console.setLevel(conf.log_level)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)
# logging.getLogger("").addHandler(console) if __env__ is Environment.DEBUG else None

# Setup complete!
logging.info(f"Starting {__name__} v{__version__}!")
logging.warning(f"Log level set to '{conf.log_level.upper()}'")
logging.info(f"Log files writing to {__appdir__}")
# </editor-fold>

