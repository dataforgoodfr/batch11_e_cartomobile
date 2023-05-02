import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from e_cartomobile.data_analytics.vizualisation_folium import map_irve_ve_par_dep
from e_cartomobile.data_analytics.vizualisation_plotly import graph_pdc_par_ve

maptest = map_irve_ve_par_dep()

st.write("## Cartographie des données essentielles")

st_data = st_folium(maptest)

st.write("## Points de recharge par voiture électrique")

st.plotly_chart(graph_pdc_par_ve())
