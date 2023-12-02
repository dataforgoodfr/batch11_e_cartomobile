# %%
#
import pandas as pd
import plotly.express as px


# %%
# Graph with EV registrations and forecast
def graph_region_evolution(
    region: str,
    hist_path="e_cartomobile/data_extract/data_for_viz/IEA-EV-dataEV salesCarsHistorical.csv",
    steps_path="e_cartomobile/data_extract/data_for_viz/IEA-EV-dataEV salesCarsProjection-STEPS.csv",
):
    df_hist = pd.read_csv(hist_path)
    df_steps = pd.read_csv(steps_path)

    hist_w = df_hist.loc[df_hist.region == region]
    steps_w = df_steps.loc[df_steps.region == region]

    df_w = pd.concat([hist_w, steps_w])

    fig = px.line(
        df_w,
        x="year",
        y="value",
        color="powertrain",
        line_dash="category",
        markers=True,
        title=f"EV Registrations in {region}",
    )
    return fig


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


#
def graph_station_power_repartition(df_irve_power):
    """
    4 Catégories trouvée dans le SDIRVE :
        1) < 7,4 kW, (pour les deux roues…)
        2) 7,4 à 22 kW (petite recharge d'appoint)
        3) 22 à 150 kW (recharge rapide)
        4) > 150 kW (très haute puissance)
    """
    bins = pd.IntervalIndex.from_tuples(
        [(0, 7.4), (7.4, 22), (22, 150), (150, df_irve_power.puissance_nominale.max())]
    )
    df_irve_power_cluster = pd.cut(df_irve_power.puissance_nominale, bins)

    df_irve_power["cluster"] = df_irve_power_cluster
    df_cluster_plot = df_irve_power.groupby("cluster").agg("sum")
    df_cluster_plot["cluster_name"] = ["Low", "Standard", "Fast", "Very Fast"]

    fig = px.bar(
        df_cluster_plot,
        x="cluster_name",
        y="count",
        labels={
            "count": "Nombre de bornes",
            "cluster_name": "Gamme de puissance de recharge",
        },
        title="Répartiton des puissances des points de recharge",
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
