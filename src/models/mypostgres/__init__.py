from . import movielens

def get_model(model_name: str):
    match model_name:
        case "movie":
            return movielens.Movie
        case _:
            raise ValueError(f"{model_name} is not a recognized model.")