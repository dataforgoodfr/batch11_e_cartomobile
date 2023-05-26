"Score 4 computation"

import os
from pathlib import Path

import numpy as np
import pandas as pd

from e_cartomobile.constants import DATA_PATH
from e_cartomobile.data_transform.immatriculations import (
    CLEAN_IMMATRICULATIONS_FILENAME,
    clean_immatriculations_data,
)


def distance_in_km(current_x, current_y, target_x, target_y):
    return np.sqrt((current_x - target_x) ** 2 + (current_y - target_y) ** 2) / 1000


def score_4_target_commune(
    gamma: float,
    dist_max_km: float,
    electric_cars_array: np.ndarray,
    x_array: np.ndarray,
    y_array: np.ndarray,
    target_commune_x: float,
    target_commune_y: float,
):
    "Computes score 4 for the target commune."
    # Get cars in 20 km around the commune
    distance_to_target_km = (
        np.sqrt((x_array - target_commune_x) ** 2 + (y_array - target_commune_y) ** 2)
        / 1000
    )
    close_cars = np.copy(electric_cars_array[distance_to_target_km < dist_max_km])

    score = np.sum(
        close_cars
        / (1 + gamma * distance_to_target_km[distance_to_target_km < dist_max_km])
    )

    return score


def get_score_4(gamma: float, dist_max_km: float) -> pd.DataFrame:
    """Computes score 4 for all communes in immatriculations dataframe.

    Args:
        gamma (float): Damping coefficient.
          If gamma=0, all cars in the surroundings are summed.
          If gamma->infinite, only the cars from the commune are summed.
        dist_max_km (float): Max distance in km defining commune surroundings.

    Returns:
        pd.DataFrame: DataFrame with insee code of the commune and score 4.
    """
    if not Path(CLEAN_IMMATRICULATIONS_FILENAME).is_file():
        clean_immatriculations_data()
    immatriculations = pd.read_feather(CLEAN_IMMATRICULATIONS_FILENAME)
    immatriculations["score_4"] = immatriculations.apply(
        lambda x: score_4_target_commune(
            gamma,
            dist_max_km,
            immatriculations["nb_vp_rechargeables_el"].values,
            immatriculations["x_crs_2154"].values,
            immatriculations["y_crs_2154"].values,
            x["x_crs_2154"],
            x["y_crs_2154"],
        ),
        axis=1,
    )
    score_4_filename = os.path.join(
        DATA_PATH, f"score_4/gamma_{gamma}_dist_max_{dist_max_km}km.csv"
    )
    immatriculations[["insee", "score_4"]].to_csv(score_4_filename)
    output_score4 = immatriculations[["insee", "score_4"]].set_index("insee")
    # Need to put the same name as the score variable
    output_score4.name = "score_4"
    return output_score4
