import pandas as pd
import streamlit as st
from streamlit_folium import folium_static  # st_folium regénère la map en continu

from e_cartomobile.data_analytics.vizualisation_folium import get_commune_map
from e_cartomobile.data_extract.communes import get_communes_metropole_geo
from e_cartomobile.data_transform.compute_score import (
    get_score_exemple,
    get_score_random_communes,
)


@st.cache_data()
def cached_get_score_exemple(latitude, longitude):
    return get_score_exemple(latitude, longitude)


@st.cache_data(ttl=3600)
def cached_get_communes_metropole_geo():
    return get_communes_metropole_geo()


@st.cache_data(ttl=3600)
def cached_get_score_random_communes(_gdf_communes):
    return get_score_random_communes(_gdf_communes)


st.write("# Données par communes")

gdf_communes = cached_get_communes_metropole_geo()
score_to_map = cached_get_score_random_communes(gdf_communes)

m = get_commune_map(gdf_communes, score_to_map)

st_data = folium_static(m)
