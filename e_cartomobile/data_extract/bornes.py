"""Get bornes data"""
import geopandas as gpd
import pandas as pd
import streamlit as st

from e_cartomobile.infra.database.sql_connection import get_db_connector


@st.cache_data(ttl=3600)
def get_bornes_data() -> gpd.GeoDataFrame:
    conn = get_db_connector()

    req_bornes = "SELECT * FROM consolidation_etalab_irve_clean"

    gdf_bornes = gpd.read_postgis(req_bornes, conn, geom_col="geometry")

    return gdf_bornes


@st.cache_data(ttl=3600)
def get_bornes_power_data() -> pd.DataFrame:
    conn = get_db_connector()

    req_bornes = """select puissance_nominale, count(id) from consolidation_etalab_irve_clean
group by puissance_nominale
order by puissance_nominale"""

    df_bornes_power = pd.read_sql(req_bornes, conn)

    # Clean power in W instead of kW (>1MW should not exist)
    df_irve_power_clean = df_bornes_power.copy()
    df_irve_power_clean.puissance_nominale = df_bornes_power.puissance_nominale.apply(
        lambda x: x if x < 1000 else x / 1000
    )
    df_irve_power_clean = (
        df_irve_power_clean.groupby("puissance_nominale").agg("sum").reset_index()
    )

    return df_irve_power_clean
