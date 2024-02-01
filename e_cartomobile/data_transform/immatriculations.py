"""Clean raw immatriculations dataset."""

import os

import pandas as pd

from e_cartomobile.constants import DATA_PATH
from e_cartomobile.data_extract.communes import get_communes_data
from e_cartomobile.data_extract.immatriculations import get_immatriculations_data_local

DATE_ARRETE = "2023-03-31"
CITIES_WITH_ARRONDISSEMENTS = ["PARIS", "MARSEILLE", "LYON"]
CLEAN_IMMATRICULATIONS_FILENAME = os.path.join(
    DATA_PATH, "immatriculations_clean.feather"
)
COMMUNES_FILENAME = os.path.join(DATA_PATH, "communes-20220101.feather")


def clean_immatriculations_data_local():
    "Clean raw immatriculations dataset and add communes info"
    immatriculations = get_immatriculations_data_local()
    # Get more recent data
    immatriculations = immatriculations[
        immatriculations["date_arrete"] == DATE_ARRETE
    ].copy()

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
    # Drop NaN columns (forains, unidentified or very small communes, maybe parts of bigger ones before)
    immatriculations = immatriculations[~immatriculations["epci"].isna()]
    immatriculations.codgeo = immatriculations.codgeo.astype(str)
    # Join communes data, get x,y coordinates and drop geometry (heavy column)
    communes = get_communes_data()
    communes_xy = (
        communes.copy()
        .to_crs({"init": "epsg:2154"})
        .drop(["nom", "surf_ha", "x", "y"], axis=1)
        .rename(columns={"geometry": "geometry_xy"})
    )
    communes = communes.merge(communes_xy, on="insee", how="left")
    communes["x_crs_2154"] = communes["geometry_xy"].apply(lambda x: x.centroid.x)
    communes["y_crs_2154"] = communes["geometry_xy"].apply(lambda x: x.centroid.y)
    communes.drop(["geometry_xy"], axis=1, inplace=True)
    immatriculations = immatriculations.merge(
        communes, left_on="codgeo", right_on="insee", how="left"
    ).drop(["geometry"], axis=1)
    # Correct the format to cover EPCI ZZZZZZZZZ case (commune without EPCI)
    immatriculations["epci"] = immatriculations["epci"].astype("str")
    # Save
    immatriculations.to_feather(CLEAN_IMMATRICULATIONS_FILENAME)


def clean_immatriculations_data(raw_immatriculations):
    "Clean raw immatriculations dataset and add communes info"

    immatriculations = raw_immatriculations.copy()

    immatriculations["date_arrete"] = (
        immatriculations["date_arrete"].apply(pd.to_datetime).dt.date
    )

    # Get more recent data
    immatriculations = immatriculations.sort_values(by="date_arrete").drop_duplicates(
        subset=["codgeo"], keep="last"
    )

    # Sort the codgeo
    immatriculations = immatriculations.sort_values(by="codgeo")

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
    # Drop NaN columns (forains, unidentified or very small communes, maybe parts of bigger ones before)
    immatriculations = immatriculations[~immatriculations["epci"].isna()]
    immatriculations.codgeo = immatriculations.codgeo.astype(str)
    # Join communes data, get x,y coordinates and drop geometry (heavy column)
    communes = get_communes_data()
    communes_xy = (
        communes.copy()
        .to_crs({"init": "epsg:2154"})
        .drop(["nom", "surf_ha", "x", "y"], axis=1)
        .rename(columns={"geometry": "geometry_xy"})
    )
    communes = communes.merge(communes_xy, on="insee", how="left")
    communes["x_crs_2154"] = communes["geometry_xy"].apply(lambda x: x.centroid.x)
    communes["y_crs_2154"] = communes["geometry_xy"].apply(lambda x: x.centroid.y)
    communes.drop(["geometry_xy"], axis=1, inplace=True)
    immatriculations = immatriculations.merge(
        communes, left_on="codgeo", right_on="insee", how="left"
    ).drop(["geometry"], axis=1)
    # Correct the format to cover EPCI ZZZZZZZZZ case (commune without EPCI)
    immatriculations["epci"] = immatriculations["epci"].astype("str")
    # Drop NaN columns (communes fusionnées)
    immatriculations = immatriculations[~immatriculations["insee"].isna()]
    return immatriculations
