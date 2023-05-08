from . import orm


def get_model(model_name: str):
    match model_name:
        case "base":
            return orm.Base
        case "movie":
            return orm.Movie
        case _:
            raise ValueError(f"{model_name} is not a recognized model.")
