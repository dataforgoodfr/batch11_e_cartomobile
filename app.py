from pathlib import Path

import streamlit as st

from e_cartomobile.data_extract.bornes import get_bornes_data, get_bornes_power_data

from e_cartomobile.data_analytics.vizualisation_plotly import (
    graph_connector_types,
    graph_station_types,
    graph_stations_evolution,
    graph_station_power_repartition
)

st.set_page_config(
    page_title="E-CartoMobile",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

MD_METHODO = "e_cartomobile/content/methodologie.md"

st.write("## Vision du projet")

st.markdown(Path(MD_METHODO).read_text(), unsafe_allow_html=True)


st.write("## Quelques chiffres de contexte")


tab1, tab2, tab3 = st.tabs(
    [
        "Les Bornes de recharges actuelles",
        "Evolution du parc automobile",
        "Quelques chiffres internationaux",
    ]
)


with tab1:
    gdf_irve = get_bornes_data()

    with st.expander("Répartion des puissances", expanded=False):

        df_irve_power = get_bornes_power_data() 
        fig_power = graph_station_power_repartition(df_irve_power)
        st.plotly_chart(fig_power)

        st.info("""
On répartit les bornes classiquement en quatre catégories de puissance :
1. Low : < 7,4 kW, pour les deux roues
2. Standard : 7,4 à 22 kW, pour une petite recharge d'appoint
3. Fast : 22 à 150 kW, pour un recharge rapide 
4. Very Fast : > 150 kW, pour une recharge très haute puissance
""")

    with st.expander("Evolution des points de recharge", expanded=False):
        fig1, fig2 = graph_stations_evolution()
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

    with st.expander("Type d'implantation des points de recharge", expanded=False):
        st.plotly_chart(graph_station_types(gdf_irve))

    with st.expander("Types de connecteurs", expanded=False):
        st.plotly_chart(graph_connector_types(gdf_irve))

with tab2:
    st.write(
        "### En chantier"
    )  # TODO : evolution temporelle du parc - cf immatriculations

with tab3:
    with st.expander("Europe", expanded=False):
        # st.write("### En chantier")
        st.plotly_chart(viz_evolution('Europe'))

    with st.expander("Monde", expanded=False):
        # st.write("### En chantier - chiffres IEA à intégrer")
        st.plotly_chart(viz_evolution('World'))
