# from tqdm.notebook import tqdm
# from tqdm import tqdm

import os

import folium
import geopandas as gpd
import joblib
import numpy as np
import pandas as pd
import requests
from branca.colormap import LinearColormap
from folium.plugins import MarkerCluster
from shapely.geometry import Point, Polygon


# tqdm().pandas()

os.environ["USE_PYGEOS"] = "0"
# data_path = 'C:/Users/demo/Desktop/Lattitude/datas/'
data_path = "datas"
# os.makedirs(data_path, exist_ok=True)


def get_datas(file_path, file_name_1, date):
    parent_path = os.path.dirname(os.getcwd())
    path_to_datas = os.path.join(parent_path, file_path)

    # get file catalog and load communes datas at date
    catalog = joblib.load(os.path.join(path_to_datas, "file_catalog.joblib"))
    df = None
    for file in catalog[date]:
        if df is None:
            df = gpd.read_feather(os.path.join(path_to_datas, file))
        else:
            df = pd.concat(
                [df, gpd.read_feather(os.path.join(path_to_datas, file))], axis=0
            )

    return (gpd.read_feather(os.path.join(path_to_datas, file_name_1)), df)


# Function to make a column color 
def make_color(df, col='VE_per_inhab', color_type=None):
    # Define the color map
    colors = ["red", "green", "blue"]
    bins = np.array([0, 1, 5, 10, 25, 50, 100]) / 100

    labels = [1, 2, 3, 4, 5, 6]

    cmap = LinearColormap(colors=colors, vmin=1, vmax=6)

    """color argument of Icon should be one of:
    {'red', 'darkred', 'gray', 'blue', 'black', 'darkpurple', 'white', 'darkblue',
    'purple', 'lightred', 'green', 'orange', 'cadetblue', 'beige', 'lightblue',
    'lightgray', 'darkgreen', 'pink', 'lightgreen'}."""
    icon_labels = [
        "darkred",
        "lightred",
        "lightgreen",
        "darkgreen",
        "lightblue",
        "blue",
    ]

    if color_type:
        color = pd.cut(
            df[col], bins=bins, labels=icon_labels  # .apply(lambda x:  x ** (1/3)),
        )
    else:
        color = pd.cut(
            df[col], bins=bins, labels=labels  # .apply(lambda x:  x ** (1/3)),
        ).apply(cmap)
    return color


"""
icons from https://fontawesome.com/v4/icons/

"""


def make_map(df, com_df, pdc_df, color_col="VE_per_inhab"):
    # Get center
    if df is not None:
        center = df.iloc[0, 1]

        # Create a folium map centered on the town_
        m = folium.Map(location=[center.y, center.x], zoom_start=10, crs="EPSG3857")

        # Create colors by binning the VE_per_inhab column
        # com_df = make_color_by_date(com_df, 'VE_per_inhab',icons='XXX')

        # communes markers
        print("Adding isochrones...", end=" ")
        for index, row in df.iterrows():
            # style the polygons based on "values" property
            # color = cmap(row.VE_per_inhab ** (1/3))
            def style_fn(feature):
                ss = {
                    "fillColor": "blue",
                    "fillOpacity": 0.09,
                    "weight": 0.3,
                    "color": "black",
                }
                # print(row['style'], end='   ')
                return ss  # row['style']

            if index > 0:
                group = folium.FeatureGroup(name=row.layer_name)

                folium.GeoJson(row.geometry, style_function=style_fn).add_to(group)
                group.add_to(m)
            # print('done')
            if index == 1:  # iso = 1 is the largest polygon
                mask = row.geometry
            del style_fn
        print("done.")

        # Take POI in larger isochrone
        print("Ceating communes things...", end=" ")
        com_df = com_df.copy()[com_df.within(mask)]
        com_df["color"] = make_color(com_df, col=color_col)
        print("done.")

        print("Creating bornes things...", end=" ")
        pdc_df = pdc_df.copy()[pdc_df.within(mask)]
        print("done.")

        print("Creating communes clusters...", end=" ")

        # create custom cluster icon customization function in JS
        icon_create_function = """\
        function(cluster) {
        return L.divIcon({
        html: '<b>' + cluster.getChildCount() + '</b>',
        className: 'marker-cluster marker-cluster-large',
        iconSize: new L.Point(30, 30)
        })
        }"""

        # Create a marker cluster layer for the data
        cluster_com = MarkerCluster(
            name="Communes", icon_create_function=icon_create_function
        )

        # communes markers
        for index, row in com_df.iterrows():
            # communes child markers
            popup = folium.Popup(row.html_popup, parse_html=False)
            cluster_com.add_child(
                folium.Marker(
                    location=[row.geometry.centroid.y, row.geometry.centroid.x],
                    popup=popup,
                    tooltip="infos",
                    icon=folium.Icon(prefix="fa", icon="institution", color=row.color),
                )
            )

        cluster_com.add_to(m)
        print("done.")

        print("Creating bornes clusters...", end=" ")
        # Create a marker cluster layer for the data
        cluster_bdr = MarkerCluster(name="Points de charge")

        # bornes markers
        for index, row in pdc_df.iterrows():
            popup = folium.Popup(row.html_popup, parse_html=False)
            cluster_bdr.add_child(
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    popup=popup,
                    tooltip="pdc infos",
                    icon=folium.Icon(prefix="fa", icon="bolt", color="blue"),
                )
            )

        cluster_bdr.add_to(m)
        print("done.")

        # Add a layer control to the map
        folium.LayerControl().add_to(m)
    else:
        center = com_df.query("nom == 'Reims'").geometry.centroid
        m = folium.Map(location=[center.y, center.x], zoom_start=10, crs="EPSG3857")

    return m


def get_isochrones(df, town, iso, token):
    if iso != [0, 0, 0, 0]:
        origin = df.query("nom == @town").iloc[0].geometry.centroid

        d = {
            "name": [town],
            "geometry": [origin],
            "style": [
                {
                    "fill": "black",
                    "fillOpacity": 1.0,
                    "fill-opacity": 0.33,
                    "fillColor": "black",
                    "color": "black",
                    "contour": 0,
                    "opacity": 1.0,
                    "weight": 10,
                    "metric": "distance",
                }
            ],
            "layer_name": ["ville"],
        }

        # denoise for polygons, denoise = 0 for road trace

        request = (
            "https://api.mapbox.com/isochrone/v1/mapbox/driving/"
            + f"{origin.x}%2C{origin.y}?"
            + f"contours_meters={iso[0]}%2C{iso[1]}%2C{iso[2]}%2C{iso[3]}"
            + f"&polygons=true&denoise=1&access_token={token}"
        )

        isos = requests.get(request).json()

        for i, feature in enumerate(isos["features"]):
            # print(i,feature['geometry']['coordinates'][0])
            points = [Point(point) for point in feature["geometry"]["coordinates"][0]]
            # print(points)
            # print(Polygon(points))
            d["name"].append(f"iso_{i}")
            d["geometry"].append(Polygon(points))
            style = feature["properties"]
            style.pop("fill-opacity")
            style.pop("fill")
            style.pop("contour")
            style.pop("metric")
            d["style"].append(feature["properties"])
            d["layer_name"].append(str(iso[i])[:-5] + " km")

        centre_df = gpd.GeoDataFrame(d, crs="EPSG:3857")  # "EPSG:4326")
    else:
        centre_df = None

    return centre_df
