import folium
import geopandas as gpd
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
