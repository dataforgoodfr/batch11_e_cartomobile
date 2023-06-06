"""Get bornes data"""
import geopandas as gpd
import streamlit as st

from e_cartomobile.infra.database.sql_connection import get_db_connector


@st.cache_data(ttl=3600)
def get_bornes_data() -> gpd.GeoDataFrame:
    conn = get_db_connector()

    req_bornes = "SELECT * FROM consolidation_etalab_irve_clean"

    gdf_bornes = gpd.read_postgis(req_bornes, conn, geom_col="geometry")

    return gdf_bornes
