"""Get communes data"""

import io
import os
import shutil
import zipfile

import geopandas as gpd
import requests

DATA_PATH = "e_cartomobile/data_extract/data"  # Path from the root of the project
FILENAME = "communes-20220101"
TEMP_EXT = ".shp"
URL = "https://www.data.gouv.fr/fr/datasets/r/0e117c06-248f-45e5-8945-0e79d9136165"
TEMP_PATH = "temp_unzip"


def get_communes_data() -> gpd.GeoDataFrame:
    "Saves communes file in DATA_PATH and returns the GeoDataFrame."
    try:
        communes = gpd.read_feather(os.path.join(DATA_PATH, FILENAME + ".feather"))
    except FileNotFoundError:
        zip_file = requests.get(URL).content
        os.makedirs(TEMP_PATH, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(zip_file)) as archive:
            archive.extractall(TEMP_PATH)
        communes = gpd.read_file(os.path.join(TEMP_PATH, FILENAME + TEMP_EXT))
        shutil.rmtree(TEMP_PATH)
        communes.to_feather(os.path.join(DATA_PATH, FILENAME + ".feather"))
    # Get x and y coordinates of communes
    communes_xy = (
        communes.to_crs(2154)
        .drop(["nom", "wikipedia", "surf_ha"], axis=1)
        .rename(columns={"geometry": "geometry_xy"})
    )
    communes = communes.merge(communes_xy, on="insee", how="left")
    communes["x"] = communes["geometry_xy"].apply(lambda x: x.centroid.x)
    communes["y"] = communes["geometry_xy"].apply(lambda x: x.centroid.y)
    return communes
