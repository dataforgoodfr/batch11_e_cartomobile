"""Get communes data"""

import io
import os
import shutil
import zipfile
from pathlib import Path

import geopandas as gpd
import requests

from e_cartomobile.constants import DATA_PATH

FILENAME = "communes-20220101"
TEMP_EXT = ".shp"
URL = "https://www.data.gouv.fr/fr/datasets/r/0e117c06-248f-45e5-8945-0e79d9136165"
TEMP_PATH = "temp_unzip"


def get_communes_data() -> gpd.GeoDataFrame:
    "Saves communes file in DATA_PATH and returns the GeoDataFrame."
    if not Path(os.path.join(DATA_PATH, FILENAME + ".feather")).is_file():
        zip_file = requests.get(URL).content
        os.makedirs(TEMP_PATH, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(zip_file)) as archive:
            archive.extractall(TEMP_PATH)
        communes = gpd.read_file(os.path.join(TEMP_PATH, FILENAME + TEMP_EXT))
        shutil.rmtree(TEMP_PATH)
        communes.insee = communes.insee.astype(str)
        communes.to_feather(os.path.join(DATA_PATH, FILENAME + ".feather"))
    communes = gpd.read_feather(os.path.join(DATA_PATH, FILENAME + ".feather"))
    # Get x and y coordinates of communes
    communes_xy = (
        communes.copy()
        .to_crs(2154)
        .drop(["nom", "wikipedia", "surf_ha"], axis=1)
        .rename(columns={"geometry": "geometry_xy"})
    )
    communes = communes.merge(communes_xy, on="insee", how="left")
    communes["x"] = communes["geometry_xy"].apply(lambda x: x.centroid.x)
    communes["y"] = communes["geometry_xy"].apply(lambda x: x.centroid.y)
    communes.drop(["geometry_xy"], axis=1, inplace=True)
    return communes
