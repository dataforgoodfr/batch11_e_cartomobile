import folium
import pandas as pd
from folium import plugins


def plot_basemap_folium_france():
    """
    Fonction basique, simplement pour exemple
    """
    maptest = folium.Map(location=[46.9, 3], zoom_start=6)

    minimap = plugins.MiniMap()
    maptest.add_child(minimap)

    # afficher l'image
    return maptest


def map_irve_ve_par_dep(
    irve_file_path="e_cartomobile/data_extract/data_for_viz/irve_par_loc.csv",
    immat_per_dep_file_path="e_cartomobile/data_extract/data_for_viz/immatriculations_par_dep.csv",
    geojson_dep_file_path="e_cartomobile/data_extract/data_for_viz/departements.geojson",
):
    """
    Fonction qui affiche les stations
    et colore les département en fonction de son nombre de véhicules électriques immatriculés
    """

    # Read IRVE data
    pdc_per_loc = pd.read_csv(irve_file_path)

    # Read immatriculations data
    immat_per_dep = pd.read_csv(immat_per_dep_file_path)
    # Keep only most recent data (last quarter 2022)
    immat_per_dep_2022_12 = immat_per_dep[immat_per_dep["date_arrete"] == "2022-12-31"]

    # Create map centered on France
    m = folium.Map(location=[46.8534, 2.3488], zoom_start=6)

    # Color departements based on the number of electric cars
    folium.Choropleth(
        columns=["code_departement", "nb_vp_rechargeables_el"],
        data=immat_per_dep_2022_12,
        fill_color="BuPu",
        fill_opacity=0.7,
        key_on="feature.properties.code",
        legend_name="Voitures à recharge électrique",
        line_opacity=0.2,
        geo_data=geojson_dep_file_path,
        highlight=True,
        name="Recharge électrique",
    ).add_to(m)

    # Plot the charging stations (1 marker = 1 charging station)
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)
    for index, row in pdc_per_loc.iterrows():
        folium.CircleMarker(
            location=[row["consolidated_latitude"], row["consolidated_longitude"]],
            # radius=row['nbre_pdc']/10+1,
            radius=1,
            color="crimson",
            fill=True,
            fill_color="crimson",
            line_opacity=0.5,
        ).add_to(marker_cluster)

    return m
