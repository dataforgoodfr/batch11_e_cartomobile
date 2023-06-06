import pandas as pd
import plotly.express as px


# Graph of different implantation types of charging stations
def graph_station_types(gdf_irve):
    """
    Graphique plotly montrant la répartition du type d'implantation des stations
    """

    # Create the graph (plotly express)
    fig = px.treemap(
        gdf_irve["implantation_station"].value_counts().reset_index(),
        values="implantation_station",
        path=["index"],
        title="Répartition des types d'implantations des bornes de recharge",
        labels={"implantation_station": "Nombre de bornes"},
    )
    fig.update_traces(textinfo="label+percent entry")
    return fig


# Graph of the different connector types and the number of stations available
def graph_connector_types(gdf_irve):
    """
    Graphique plotly représentant le nombre de connecteurs de chaque type
    """

    # count the number of connectors of each type
    type_prise = pd.DataFrame(
        [
            ["Autre", gdf_irve["prise_type_autre"].sum()],
            ["Chademo", gdf_irve["prise_type_chademo"].sum()],
            ["Combo CCS", gdf_irve["prise_type_combo_ccs"].sum()],
            ["Type 2", gdf_irve["prise_type_2"].sum()],
            ["EF", gdf_irve["prise_type_ef"].sum()],
        ],
        columns=["Type", "Nombre de points de charge"],
    )
    # Create the graph (plotly express)
    fig = px.bar(
        type_prise,
        y="Type",
        x="Nombre de points de charge",
        orientation="h",
        text_auto=".5",
        title="Types de connecteurs",
    )
    return fig


# Graphs depicting the evolution of the number of charging stations
def graph_stations_evolution(
    irve_ts_file_path="e_cartomobile/data_extract/data_for_viz/irve_time_series.csv",
):
    """
    2 graphiques plotly:
      - Evolution du nombre de stations (à partir de 2015)
      - Evolution du nombre de bornes de recharge (à partir de 2015)
    """
    # Read the file
    irve_ts = pd.read_csv(irve_ts_file_path, index_col=0).set_index(
        "date_mise_en_service"
    )
    # Keep only data after 2015
    irve_ts_2015_now = irve_ts[irve_ts.index.values > "2015"]
    # Create the 1st graph (stations) (plotly express)
    fig1 = px.line(
        irve_ts_2015_now.reset_index(),
        markers=True,
        x="date_mise_en_service",
        y="nb_stations",
        title="Evolution du nombre de stations",
        labels={"date_mise_en_service": "Date", "nb_stations": "Nombre de stations"},
    )
    # Create the 2nd graph (charging points) (plotly express)
    fig2 = px.line(
        irve_ts_2015_now.reset_index(),
        markers=True,
        x="date_mise_en_service",
        y="nb_pdc",
        title="Evolution du nombre de bornes de recharge",
        labels={"date_mise_en_service": "Date", "nb_pdc": "Nombre de bornes"},
    )
    fig2.update_traces(line_color="crimson")
    return fig1, fig2


# Graph of charging stations per electric vehicle per french departments
def graph_pdc_par_ve(
    pdc_immat_file_path="e_cartomobile/data_extract/data_for_viz/pdc_immat_par_dep.csv",
):
    """
    Graphique plotly représentant le nombre de bornes de recharge par vehicule électrique
    et par département
    """
    # Read the file
    pdc_immat_par_dep = pd.read_csv(pdc_immat_file_path)
    # Create the graph (plotly express)
    fig = px.bar(
        pdc_immat_par_dep.sort_values(by="pdc_par_vp_el", ascending=True),
        x="pdc_par_vp_el",
        y="nom_departement",
        orientation="h",
        text_auto=".2",
        height=2000,
        title="Bornes par voiture à recharge électrique",
        labels={
            "nom_departement": "Département",
            "pdc_par_vp_el": "Bornes par voiture électrique",
            "nb_vp_rechargeables_el": "Voitures électriques",
            "nb_vp": "Toutes les voitures",
        },
        hover_name="nom_departement",
        hover_data={
            "nb_vp_rechargeables_el": True,
            "nb_vp": True,
            "population": True,
            "pdc_par_vp_el": False,
            "nom_departement": False,
        },
        color="population",
    )
    return fig
