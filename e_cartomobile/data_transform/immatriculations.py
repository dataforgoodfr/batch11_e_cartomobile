"""Clean raw immatriculations dataset."""

import os

import pandas as pd

from e_cartomobile.constants import DATA_PATH
from e_cartomobile.data_extract.communes import get_communes_data
from e_cartomobile.data_extract.immatriculations import (
    IMMATRICULATIONS_FILENAME,
    get_immatriculations_data,
)

DATE_ARRETE = "2023-03-31"
CITIES_WITH_ARRONDISSEMENTS = ["PARIS", "MARSEILLE", "LYON"]
CLEAN_IMMATRICULATIONS_FILENAME = os.path.join(
    DATA_PATH, "immatriculations_clean.feather"
)
COMMUNES_FILENAME = os.path.join(DATA_PATH, "communes-20220101.feather")


def clean_immatriculations_data():
    "Clean raw immatriculations dataset and add communes info"
    immatriculations = get_immatriculations_data()
    # Get more recent data
    immatriculations = immatriculations[
        immatriculations["date_arrete"] == DATE_ARRETE
    ].copy()
    # Drop NaN columns (forains, unidentified or very small communes, maybe parts of bigger ones before)
    immatriculations = immatriculations[~immatriculations["epci"].isna()]
    immatriculations.codgeo = immatriculations.codgeo.astype(str)
    # Process short codgeo
    immatriculations["codgeo"] = immatriculations["codgeo"].apply(
        lambda x: "0" + x if len(x) == 4 else x
    )
    # Aggregate arrondissements stats in city row to join on communes data
    for city in CITIES_WITH_ARRONDISSEMENTS:
        immatriculations.loc[
            immatriculations["libgeo"] == f"{city} ND",
            ["nb_vp", "nb_vp_rechargeables_gaz", "nb_vp_rechargeables_el"],
        ] = (
            immatriculations[
                (immatriculations["libgeo"].str.contains(city))
                & (
                    immatriculations["libgeo"].str.contains("ARRONDISSEMENT")
                    | immatriculations["libgeo"].str.contains("ND")
                )
            ][["nb_vp", "nb_vp_rechargeables_gaz", "nb_vp_rechargeables_el"]]
            .sum()
            .values
        )
    # Drop rows with arrondissement
    immatriculations.drop(
        immatriculations[
            (immatriculations["libgeo"].str.contains("ARRONDISSEMENT"))
        ].index,
        inplace=True,
    )
    # Join communes data, drop geometry (heavy column)
    communes = get_communes_data()
    immatriculations = immatriculations.merge(
        communes, left_on="codgeo", right_on="insee", how="left"
    ).drop(["geometry"], axis=1)
    # Save
    immatriculations.to_feather(CLEAN_IMMATRICULATIONS_FILENAME)
