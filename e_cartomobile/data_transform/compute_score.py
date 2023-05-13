import numpy as np
import pandas as pd


def get_score_exemple(latitude: float, longitude: float) -> float:
    """
    Fausse fonction de score pour l'exemple
    """
    return latitude + longitude - 45


def get_score_random_communes(gdf_communes) -> pd.Series:
    score_random = pd.Series(
        index=gdf_communes.codgeo,
        data=np.random.uniform(0, 100, len(gdf_communes)),
        name="score_random",  # A name is needed for the merge with gpd
    )

    return score_random
