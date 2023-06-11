import pandas as pd
import numpy as np

from e_cartomobile.data_extract.bornes import get_bornes_data
from e_cartomobile.data_transform.compute_score_4 import score_4_target_commune # same distance collection

POWER_CLUSTER = ['Low','Standard','Fast','Very Fast']

#%%
# Get the bornes count by commuens and power 
def compute_bornes_by_communes(df_irve_power_clean):

    df_cluster_plot = df_irve_power_clean.groupby(
        ["consolidated_code_postal", "cluster"]
    ).agg("count")[
        "puissance_nominale"
    ]  # TODO : use code_insee_commune instead

    df_bornes_communes = df_cluster_plot.reset_index().pivot(index='consolidated_code_postal',columns='cluster')
    df_bornes_communes.columns = POWER_CLUSTER # warning : depends on compute_power_cluster bins

    return df_bornes_communes

def compute_power_cluster(df_irve_power_clean):
    bins = pd.IntervalIndex.from_tuples(
        [
            (0, 7.4),
            (7.4, 22),
            (22, 150),
            (150, df_irve_power_clean.puissance_nominale.max()),
        ]
    )
    df_irve_power_cluster = pd.cut(df_irve_power_clean.puissance_nominale, bins)

    return df_irve_power_cluster

def clean_power_values(gdf_irve):
    df_irve_power_clean = gdf_irve.copy()
    df_irve_power_clean.puissance_nominale = gdf_irve.puissance_nominale.apply(
        lambda x: x if x < 1000 else x / 1000
    )
    return df_irve_power_clean


#%%
#  Combine the communes data
def add_close_bornes_by_power_cluster_simple(df_bornes_communes, gamma, dist_max_km):
    """
    For a dedicated city, add the irve nearby, depending on the gamma and dist_max_km parameters.

    df_bornes_communes must contain x_crs_2154 and y_crs_2154 positions of the cities, in CRS 2154 reference.
    
    Warning : this ponderation is simplified by taking all charging point the commune centers
    
    """
    for cluster in df_bornes_communes.columns:
        if not(cluster.startswith('x') or  cluster.startswith('y')):
            df_bornes_communes[cluster+"_completed"] = df_bornes_communes.apply(
                lambda x: score_4_target_commune(
                    gamma,
                    dist_max_km,
                    df_bornes_communes[cluster].values,
                    df_bornes_communes["x_crs_2154"].values,
                    df_bornes_communes["y_crs_2154"].values,
                    x["x_crs_2154"],
                    x["y_crs_2154"],
                ),
                axis=1,
            )
    return df_bornes_communes

def add_close_bornes_by_power_cluster(df_bornes_communes, df_irve, gamma, dist_max_km):
    """
    For a dedicated city, add the irve nearby, depending on the gamma and dist_max_km parameters.

    df_irve must contain x_crs_2154 and y_crs_2154 positions of the cities, in CRS 2154 reference.
    df_irve must contain power clusters
    
    TODO : Remove of the borne inside the city and add it at the end to avoid double - counting
    """
    for cluster in df_bornes_communes.columns:

        df_irve_extract = df_irve[df_irve.cluster == cluster]
        if not(cluster.startswith('x') or  cluster.startswith('y')):
            df_bornes_communes[cluster+"_completed"] = df_bornes_communes.apply(
                lambda x: score_4_target_commune(
                    gamma,
                    dist_max_km,
                    np.ones((len(df_irve_extract),)), # count 1 by bornes # TODO : or pdc ?
                    df_irve_extract["x_crs_2154"].values,
                    df_irve_extract["y_crs_2154"].values,
                    x["x_crs_2154"],
                    x["y_crs_2154"],
                ),
                axis=1,
            )
    return df_bornes_communes

def complete_df_irve(df_irve):

    # df_irve must contain power clusters
    # Create clusters
    df_irve_power_cluster = compute_power_cluster(df_irve)

    # Count irve by communes & cluster
    df_irve["cluster"] = df_irve_power_cluster

    # df_irve must contain x_crs_2154 and y_crs_2154 positions of the cities, in CRS 2154 reference.
    # TODO  : df_irve pre-traitement
    
    return df_irve

#%%
# apply pondaration depending on the scenario
def compute_unique_bornes_ponderated(s_bornes_communes, weights) -> float:

    return np.sum([s_bornes_communes.get(key,0)*value for key, value in weights.items()])


def compute_bornes_ponderated(df_bornes_communes, weights = None) -> pd.Series:

    # Deal with deafult values
    if weights is None: # by default, 1 for each
        weights = {cluster : 1 for cluster in df_bornes_communes.communes if cluster.contains('_completed')}

    # Normalized the weights
    total_weight = np.sum([values for values in weights.values])
    weights_normalized = {key : value/total_weight for key, value in weights.items()}
    
    # Apply weights
    s_bornes_communes_ponderated = df_bornes_communes.apply(
        lambda x : compute_unique_bornes_ponderated(x,weights_normalized), 
        axis=1
        )

    return s_bornes_communes_ponderated

#%%
# Combine all
def compute_bornes_by_communes_ponderated(gamma = 5, dist_max_km = 20):

    # Read data in database
    gdf_irve = get_bornes_data()

    # Clean Power values
    df_irve = clean_power_values(gdf_irve)

    df_irve = complete_df_irve(df_irve)

    df_bornes_communes = compute_bornes_by_communes(gdf_irve)

    df_bornes_communes_smooth = add_close_bornes_by_power_cluster(df_bornes_communes, df_irve, gamma, dist_max_km)

    return compute_bornes_ponderated(df_bornes_communes_smooth, get_scenario_weight())


def get_scenario_weight():
    # Dummy fonction : to complete
    return {x : 1 for x in POWER_CLUSTER}