import pandas as pd
import streamlit as st
from streamlit_folium import folium_static  # st_folium regénère la map en continu

from e_cartomobile.data_analytics.vizualisation_folium import get_commune_map
from e_cartomobile.data_extract.communes import get_communes_data
from e_cartomobile.data_extract.read_scores import get_score_4


@st.cache_data(ttl=3600)
def cached_get_communes_metropole_geo():
    return get_communes_data()


@st.cache_data(ttl=3600)
def cached_get_score_4(gamma, dist_max_km):
    return get_score_4(gamma=gamma, dist_max_km=dist_max_km)


st.write("# Données par communes")


gdf_communes = cached_get_communes_metropole_geo()
score_to_map = cached_get_score_4(gamma=5, dist_max_km=20)

m = get_commune_map(gdf_communes, score_to_map)

st_data = folium_static(m)
