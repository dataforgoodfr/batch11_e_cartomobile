"""Get immatriculations data"""

import csv
import os
import re
from pathlib import Path

import pandas as pd
import requests

from e_cartomobile.constants import DATA_PATH

FILENAME = "voitures-rechargeables-par-commune"
IMMATRICULATIONS_FILENAME = os.path.join(DATA_PATH, FILENAME + ".csv")
URL = "https://www.data.gouv.fr/fr/datasets/r/4e4fccdb-6acb-4e31-8b2d-cb170f639f1a"


def get_immatriculations_data() -> pd.DataFrame:
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
    )
    return immatriculations
