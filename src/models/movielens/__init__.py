"""Interface for selecting models from this schema."""

from . import orm


def get_model(model_name: str):
    """Takes a model name and returns the SQL Alchemy ORM for that model"""
    match model_name:
        case "base":
            return orm.Base
        case "movie":
            return orm.Movie
        case _:
            raise ValueError(f"{model_name} is not a recognized model.")
