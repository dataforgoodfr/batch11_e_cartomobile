import pandas as pd

from e_cartomobile.data_extract.bornes import get_bornes_data


def compute_bornes_by_communes():
    # Read data in database
    gdf_irve = get_bornes_data()

    # Clean Power values
    df_irve_power_clean = gdf_irve.copy()
    df_irve_power_clean.puissance_nominale = gdf_irve.puissance_nominale.apply(
        lambda x: x if x < 1000 else x / 1000
    )

    # Create clusters
    bins = pd.IntervalIndex.from_tuples(
        [
            (0, 7.4),
            (7.4, 22),
            (22, 150),
            (150, df_irve_power_clean.puissance_nominale.max()),
        ]
    )
    df_irve_power_cluster = pd.cut(df_irve_power_clean.puissance_nominale, bins)

    # Count irve by communes & cluster
    df_irve_power_clean["cluster"] = df_irve_power_cluster
    df_cluster_plot = df_irve_power_clean.groupby(
        ["consolidated_code_postal", "cluster"]
    ).agg("count")[
        "puissance_nominale"
    ]  # TODO : use code_insee_commune instead

    return df_cluster_plot.reset_index()
