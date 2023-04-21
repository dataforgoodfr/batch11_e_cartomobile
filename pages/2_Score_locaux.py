import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from e_cartomobile.data_transform.compute_score import get_score_exemple


@st.cache_data()
def cached_get_score_exemple(latitude, longitude):
    return get_score_exemple(latitude, longitude)


lat = st.sidebar.number_input("Latitude")
lon = st.sidebar.number_input("Longitude")

st.write("### Exemple de page - inclure une carte")

score = cached_get_score_exemple(lat, lon)
st.write(
    f"Pour une latitude de {lat} et une longitude de {lon}, le score est de {score}"
)
