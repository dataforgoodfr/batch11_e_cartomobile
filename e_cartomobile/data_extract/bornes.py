"""Get bornes data"""
import geopandas as gpd
import pandas as pd
import streamlit as st

from e_cartomobile.infra.database.sql_connection import get_db_connector


@st.cache_data(ttl=3600)
def get_bornes_data() -> gpd.GeoDataFrame:
    """
    Available features :
        id serial,
        id_pdc_itinerance text COLLATE pg_catalog."default",
        last_modified text COLLATE pg_catalog."default",
        nom_amenageur text COLLATE pg_catalog."default",
        siren_amenageur text COLLATE pg_catalog."default",
        contact_amenageur text COLLATE pg_catalog."default",
        nom_operateur text COLLATE pg_catalog."default",
        contact_operateur text COLLATE pg_catalog."default",
        telephone_operateur text COLLATE pg_catalog."default",
        nom_enseigne text COLLATE pg_catalog."default",
        id_station_itinerance text COLLATE pg_catalog."default",
        id_station_local text COLLATE pg_catalog."default",
        nom_station text COLLATE pg_catalog."default",
        implantation_station text COLLATE pg_catalog."default",
        adresse_station text COLLATE pg_catalog."default",
        code_insee_commune text COLLATE pg_catalog."default",
        "coordonneesXY" text COLLATE pg_catalog."default",
        nbre_pdc integer,
        id_pdc_local text COLLATE pg_catalog."default",
        puissance_nominale double precision,
        prise_type_ef boolean,
        prise_type_2 boolean,
        prise_type_combo_ccs boolean,
        prise_type_chademo boolean,
        prise_type_autre boolean,
        gratuit boolean,
        paiement_acte boolean,
        paiement_cb boolean,
        paiement_autre boolean,
        tarification text COLLATE pg_catalog."default",
        condition_acces text COLLATE pg_catalog."default",
        reservation boolean,
        horaires text COLLATE pg_catalog."default",
        accessibilite_pmr text COLLATE pg_catalog."default",
        restriction_gabarit text COLLATE pg_catalog."default",
        station_deux_roues boolean,
        raccordement text COLLATE pg_catalog."default",
        num_pdl text COLLATE pg_catalog."default",
        date_mise_en_service date,
        observations text COLLATE pg_catalog."default",
        date_maj date,
        cable_t2_attache boolean,
        datagouv_dataset_id text COLLATE pg_catalog."default",
        datagouv_resource_id text COLLATE pg_catalog."default",
        datagouv_organization_or_owner text COLLATE pg_catalog."default",
        consolidated_longitude text COLLATE pg_catalog."default",
        consolidated_latitude text COLLATE pg_catalog."default",
        consolidated_code_postal text COLLATE pg_catalog."default",
        consolidated_commune text COLLATE pg_catalog."default",
        consolidated_is_lon_lat_correct boolean,
        consolidated_is_code_insee_verified boolean,
        puissance_categorie text COLLATE pg_catalog."default",
        "code_commune_INSEE" text COLLATE pg_catalog."default",
        code_departement text COLLATE pg_catalog."default",
        nom_departement text COLLATE pg_catalog."default",
        point geometry,
        code_dpt text COLLATE pg_catalog."default",
        region text COLLATE pg_catalog."default",
        superficie_km2 double precision,
        nbre_habitants double precision,
        "hab/km2" double precision,
    """
    conn = get_db_connector()

    req_bornes = "SELECT * FROM consolidation_irve_cleaned"

    gdf_bornes = gpd.read_postgis(req_bornes, conn, geom_col="point")

    return gdf_bornes


@st.cache_data(ttl=3600)
def get_bornes_power_data() -> pd.DataFrame:
    conn = get_db_connector()

    req_bornes = """select puissance_nominale, count(id) from consolidation_etalab_irve_clean
group by puissance_nominale
order by puissance_nominale"""

    df_bornes_power = pd.read_sql(req_bornes, conn)

    # Clean power in W instead of kW (>1MW should not exist)
    df_irve_power_clean = df_bornes_power.copy()
    df_irve_power_clean.puissance_nominale = df_bornes_power.puissance_nominale.apply(
        lambda x: x if x < 1000 else x / 1000
    )
    df_irve_power_clean = (
        df_irve_power_clean.groupby("puissance_nominale").agg("sum").reset_index()
    )

    return df_irve_power_clean


def clean_insee(insee_label):
    try:
        label = float(insee_label)
        return f"{int(label):05d}"
    except ValueError:
        return insee_label


def get_bornes_data_combined():
    filelink = "https://raw.githubusercontent.com/BastienGauthier/clean_french_irve/main/data/df_irve_etalab_cleaned_combined.csv"
    df_bornes = pd.read_csv(filelink, index_col=0)
    df_bornes["code_insee_commune"] = df_bornes["code_insee_commune"].apply(clean_insee)
    return df_bornes
