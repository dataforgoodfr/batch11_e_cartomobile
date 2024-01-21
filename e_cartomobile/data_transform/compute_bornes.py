# %%
# Importations
import numpy as np
import pandas as pd

from e_cartomobile.constants import ARRONDISSEMENT_DICT, DATA_PATH
from e_cartomobile.data_extract.bornes import get_bornes_data, get_bornes_data_combined
from e_cartomobile.data_extract.communes import get_communes_data
from e_cartomobile.data_transform.compute_score_4 import (  # same distance collection
    score_4_target_commune,
)
from e_cartomobile.data_transform.core import get_x_y_from_lat_lon

POWER_CLUSTER = ["Low", "Standard", "Fast", "Very Fast"]


# %%
def compute_bornes_by_communes(df_irve_power_clean, insee_label="code_commune_INSEE"):
    """Get the bornes count by commune and power"""
    df_cluster_plot = df_irve_power_clean.groupby([insee_label, "cluster"]).agg(
        "count"
    )["puissance_nominale"]

    df_bornes_communes = df_cluster_plot.reset_index().pivot(
        index=insee_label, columns="cluster"
    )
    df_bornes_communes.columns = (
        POWER_CLUSTER  # warning : depends on compute_power_cluster bins
    )

    return df_bornes_communes


def compute_pdc_by_communes(df_irve_power_clean, insee_label="code_commune_INSEE"):
    # Si l'insee_label n'existe pas, le pdc n'est pas compté
    df_cluster_plot = df_irve_power_clean.groupby([insee_label, "cluster"]).agg("count")[
        "nbre_pdc"
    ]

    df_bornes_communes = df_cluster_plot.reset_index().pivot(
        index=insee_label, columns="cluster"
    )
    df_bornes_communes.columns = (
        POWER_CLUSTER  # warning : depends on compute_power_cluster bins
    )

    return df_bornes_communes


def compute_power_cluster(df_irve_power_clean, cluster_labels=POWER_CLUSTER):
    bins = pd.IntervalIndex.from_tuples(
        [
            (0, 7.4),
            (7.4, 22),
            (22, 150),
            (150, df_irve_power_clean.puissance_nominale.max()),
        ]
    )
    df_irve_power_cluster = pd.cut(df_irve_power_clean.puissance_nominale, bins)

    # Set the labels instead of the bins values
    df_irve_power_cluster = df_irve_power_cluster.map(dict(zip(bins, cluster_labels)))

    return df_irve_power_cluster


def clean_power_values(gdf_irve):
    df_irve_power_clean = gdf_irve.copy()
    df_irve_power_clean.puissance_nominale = gdf_irve.puissance_nominale.apply(
        lambda x: x if x < 1000 else x / 1000
    )
    return df_irve_power_clean


def add_close_bornes_by_power_cluster_simple(df_bornes_communes, gamma, dist_max_km):
    """
    For a dedicated city, add the irve nearby, depending on the gamma and dist_max_km parameters.

    df_bornes_communes must contain x_crs_2154 and y_crs_2154 positions of the cities, in CRS 2154 reference.

    Warning : this ponderation is simplified by taking all charging point the commune centers

    """
    df_b = df_bornes_communes.copy()

    for cluster in df_b.columns:
        if not (cluster.startswith("x") or cluster.startswith("y")):
            df_b[cluster + "_completed"] = df_b.apply(
                lambda x: score_4_target_commune(
                    gamma,
                    dist_max_km,
                    df_b[cluster].values,
                    df_b["x_crs_2154"].values,
                    df_b["y_crs_2154"].values,
                    x["x_crs_2154"],
                    x["y_crs_2154"],
                ),
                axis=1,
            )
    return df_b


def add_close_pdc_by_power_cluster(df_bornes_communes, df_irve, gamma, dist_max_km):
    """
    For a dedicated city, add the irve nearby, depending on the gamma and dist_max_km parameters.

    df_irve must contain x_crs_2154 and y_crs_2154 positions, in CRS 2154 reference.
    df_irve must contain power clusters

    """
    df_b = df_bornes_communes.copy()
    for cluster in df_b.columns:
        df_irve_extract = df_irve[df_irve.cluster == cluster]
        if not (cluster.startswith("x") or cluster.startswith("y")):
            df_b[cluster + "_completed"] = df_b.apply(
                lambda x: score_4_target_commune(
                    gamma,
                    dist_max_km,
                    df_irve_extract["nbre_pdc"].values,
                    df_irve_extract["x_crs_2154"].values,
                    df_irve_extract["y_crs_2154"].values,
                    x["x_crs_2154"],
                    x["y_crs_2154"],
                ),
                axis=1,
            )
    return df_b


def complete_df_irve(df_irve):
    # df_irve must contain power clusters
    # Create clusters
    df_irve_power_cluster = compute_power_cluster(df_irve)

    # Count irve by communes & cluster
    df_irve["cluster"] = df_irve_power_cluster

    # df_irve must contain x_crs_2154 and y_crs_2154 positions of the cities, in CRS 2154 reference.
    df_irve[["x_crs_2154", "y_crs_2154"]] = np.array(
        get_x_y_from_lat_lon(
            df_irve.consolidated_latitude, df_irve.consolidated_longitude
        )
    ).T

    return df_irve


def compute_unique_bornes_ponderated(s_bornes_communes, weights) -> float:
    """Apply pondaration depending on the scenario"""
    return np.sum(
        [s_bornes_communes.get(key, 0) * value for key, value in weights.items()]
    )


def compute_bornes_ponderated(df_bornes_communes, weights=None) -> pd.Series:
    # Deal with default values
    if weights is None:  # by default, 1 for each
        weights = {
            cluster: 1
            for cluster in df_bornes_communes.communes
            if cluster.contains("_completed")
        }

    # Normalized the weights
    total_weight = np.sum([values for values in weights.values()])
    weights_normalized = {key: value / total_weight for key, value in weights.items()}

    # Apply weights
    s_bornes_communes_ponderated = df_bornes_communes.apply(
        lambda x: compute_unique_bornes_ponderated(x, weights_normalized), axis=1
    )

    s_bornes_communes_ponderated.index.name = "insee"
    s_bornes_communes_ponderated.name = "bornes_score"

    return s_bornes_communes_ponderated


# Combine all
def compute_bornes_by_communes_smoothed(
    gamma=5, dist_max_km=20, arro_dict=ARRONDISSEMENT_DICT, origin="default"
):
    if origin in ["default", "github"]:
        # Read data in github - already cleaned values
        df_irve = get_bornes_data_combined()
        insee_label = "code_insee_commune"
    elif origin in ["database"]:
        # Read data in database - old format
        gdf_irve = get_bornes_data()
        # Clean Power values
        df_irve = clean_power_values(gdf_irve)
        insee_label = "code_commune_INSEE"

    # Get features for IRVE
    df_irve = complete_df_irve(df_irve)
    # Aggregate the cities with arrondissement
    ## if in the dict, change it, else do nothing
    df_irve[insee_label] = df_irve[insee_label].apply(lambda x: arro_dict.get(x, x))

    # Compute bornes for each city
    df_bornes_communes = compute_pdc_by_communes(df_irve, insee_label=insee_label)
    # Complete city with position data
    gdf_comm = get_communes_data()
    gdf_comm[["x_crs_2154", "y_crs_2154"]] = np.array(
        get_x_y_from_lat_lon(gdf_comm.y, gdf_comm.x)
    ).T
    df_bornes_communes_completed = df_bornes_communes.join(
        gdf_comm[["insee", "x_crs_2154", "y_crs_2154"]].set_index("insee"), how="outer"
    )
    df_bornes_communes_completed = df_bornes_communes_completed.fillna(
        0
    )  # communes sans aucune borne

    # smooth
    df_bornes_communes_smooth = add_close_pdc_by_power_cluster(
        df_bornes_communes_completed, df_irve, gamma, dist_max_km
    )

    return df_bornes_communes_smooth


def compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, scenario="default"
):
    """
    Compute the bornes by communes ponderated, depending on the scenario.

    Parameters:
        df_bornes_communes_smooth (pd.DataFrame): The dataframe containing the bornes by communes.
        scenario (str, optional): The scenario to be used for computation. Defaults to "default".

    Returns:
        The result of the computation (pd.Series).
    """
    return compute_bornes_ponderated(
        df_bornes_communes_smooth, get_scenario_weight(scenario)
    )


def get_scenario_weight(scenario):
    # POWER_CLUSTER = ["Low", "Standard", "Fast", "Very Fast"]
    if scenario in ["default", "smoothed_uniform"]:
        return {x: 1 for x in [cluster + "_completed" for cluster in POWER_CLUSTER]}
    elif scenario in ["smoothed_reseau"]:
        return {
            "Low_completed": 0,
            "Standard_completed": 0.02,
            "Fast_completed": 0.28,
            "Very Fast_completed": 0.70,
        }
    elif scenario in ["smoothed_tourisme"]:
        return {
            "Low_completed": 0.05,
            "Standard_completed": 0.20,
            "Fast_completed": 0.40,
            "Very Fast_completed": 0.35,
        }
    elif scenario in ["smoothed_local"]:
        return {
            "Low_completed": 0.10,
            "Standard_completed": 0.35,
            "Fast_completed": 0.40,
            "Very Fast_completed": 0.15,
        }
    elif scenario == "uniform":
        return {x: 1 for x in POWER_CLUSTER}
    else:
        raise NotImplementedError(f"Le scénario {scenario} n'a pas de poids associés")


# %%
# Main
if __name__ == "__main__":
    df_bornes_communes_smooth = compute_bornes_by_communes_smoothed()
    df_bornes_communes_smooth.drop(columns=["x_crs_2154", "y_crs_2154"]).to_csv(
        f"{DATA_PATH}/bornes/df_bornes_communes_smooth.csv"
    )
    df_bornes_communes_uniform = compute_bornes_by_communes_ponderated(
        df_bornes_communes_smooth, "uniform"
    )
    df_bornes_communes_uniform.to_csv(
        f"{DATA_PATH}/bornes/df_bornes_communes_uniform.csv"
    )
    df_bornes_communes_smoothed_uniform = compute_bornes_by_communes_ponderated(
        df_bornes_communes_smooth, "smoothed_uniform"
    )
    df_bornes_communes_smoothed_uniform.to_csv(
        f"{DATA_PATH}/bornes/df_bornes_communes_smoothed_uniform.csv"
    )
