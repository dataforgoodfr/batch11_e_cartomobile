"""Get immatriculations data"""

import csv
import os
import re
from pathlib import Path

import pandas as pd
import requests

from e_cartomobile.constants import DATA_PATH
from e_cartomobile.infra.database.sql_connection import get_db_connector

FILENAME = "voitures-rechargeables-par-commune"
IMMATRICULATIONS_FILENAME = os.path.join(DATA_PATH, FILENAME + ".csv")
URL = "https://object.files.data.gouv.fr/hydra-parquet/hydra-parquet/90e0d717-deda-4bdc-9987-f82faac5bc93.parquet" # parquet


def get_immatriculations_data_local() -> pd.DataFrame:
    if not Path(IMMATRICULATIONS_FILENAME).is_file():
        bytes_file = requests.get(URL).content
        data = bytes_file.decode("utf-8").splitlines()
        with open(IMMATRICULATIONS_FILENAME, "w") as output:
            writer = csv.writer(output, delimiter=";")
            for line in data:
                writer.writerow(re.split(";", line))
    immatriculations = pd.read_csv(
        IMMATRICULATIONS_FILENAME,
        sep=";",
        dtype={"codgeo": "str"},
        encoding="iso-8859-1",
    )
    return immatriculations


def get_immatriculations_data_online() -> pd.DataFrame:
    immatriculations = pd.read_parquet(URL)
    return immatriculations


def get_immatriculations_data() -> pd.DataFrame:
    conn = get_db_connector()

    req_immat = """SELECT codgeo, libgeo, epci, libepci, date_arrete,
       nb_vp_rechargeables_el, nb_vp_rechargeables_gaz, nb_vp
       FROM immatriculations_cleaned"""

    immat = pd.read_sql(req_immat, conn)

    return immat


def get_clean_immatriculations_data():
    conn = get_db_connector()

    req_immat = """SELECT insee, nom_commune,
nb_vp_rechargeables_el, nb_vp_rechargeables_gaz, nb_vp,
x, y, x_crs_2154, y_crs_2154
FROM immatriculations_cleaned"""

    immat = pd.read_sql(req_immat, conn)

    return immat
