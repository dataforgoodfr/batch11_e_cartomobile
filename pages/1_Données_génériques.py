import pandas as pd
import streamlit as st

from streamlit_folium import st_folium

from e_cartomobile.data_analytics.vizualisation_folium import plot_basemap_folium_france


maptest = plot_basemap_folium_france()

st.write("## Cartographie des données essentielles")

st_data = st_folium(maptest)
