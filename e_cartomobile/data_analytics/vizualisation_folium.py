import folium
import geopandas as gpd
import pandas as pd
from folium import plugins

from e_cartomobile.data_extract.communes import get_departement_data


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
    plot_markers = False
):
    """
    Fonction qui affiche les stations
    et colore les département en fonction de son nombre de véhicules électriques immatriculés
    """
    # Get departement contour
    gdf_departement = get_departement_data()

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
        geo_data=gdf_departement,
        highlight=True,
        name="Recharge électrique",
    ).add_to(m)

    if plot_markers:
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


def get_json_commune(gdf_commune, index_label, tooltip, tol=0.001):
    if isinstance(tooltip, list):
        properties_list = list(set(tooltip + [index_label]))
    else:
        properties_list = [index_label]

    gdf_simple = gdf_commune[properties_list]
    gdf_simple = gdf_simple.set_geometry(gdf_commune.simplify(tolerance=tol))
    gdf_simple.index = gdf_commune[index_label]

    return gdf_simple.to_json()


def get_commune_choropleth(
    gdf_commune: gpd.GeoDataFrame,
    color_key: str,
    label=None,
    index_label="codgeo",
    tooltip=None,  # exemple : ["codgeo","libgeo", "score"]
) -> folium.Choropleth:
    if label is None:
        label = color_key

    json_commune = get_json_commune(gdf_commune, index_label, tooltip)

    color_layer = folium.Choropleth(
        geo_data=json_commune,
        data=gdf_commune,
        columns=[index_label, color_key],
        key_on="feature.id",
        name="choropleth",
        fill_color="Spectral",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=label,
        highlight=True,
    )

    if tooltip is not None:
        folium.GeoJsonTooltip(tooltip).add_to(color_layer.geojson)

    return color_layer


def get_commune_map(gdf_commune: gpd.GeoDataFrame, score_to_map: pd.Series):
    m = folium.Map(location=[46.9, 3], zoom_start=6, prefer_canvas=True)

    gdf_commune_extended = gdf_commune.merge(
        score_to_map, left_on="codgeo", right_index=True
    )

    s_name = score_to_map.name

    color_layer = get_commune_choropleth(
        gdf_commune_extended,
        color_key=s_name,
        label=None,
        index_label="codgeo",
        tooltip=["codgeo", "libgeo", s_name],
    )

    m.add_child(color_layer)

    plugins.Geocoder(collapsed=False, position="topright", add_marker=False).add_to(m)

    folium.LayerControl().add_to(m)

    return m
