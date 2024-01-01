# %%
# Importation
import pandas as pd

from e_cartomobile.infra.database.sql_connection import get_db_connector


# %%
# Récupération des Scores
def get_score_4(gamma: float, dist_max_km: float) -> pd.DataFrame:
    conn = get_db_connector()

    req_score = f"""SELECT insee, score_4
    FROM score_4
    where gamma = {gamma} and max_distance_km = {dist_max_km}"""

    output_score4 = pd.read_sql(req_score, conn, index_col="insee")
    output_score4 = output_score4.squeeze()
    output_score4.name = "score_4"

    return output_score4


def get_score_2() -> pd.DataFrame:
    conn = get_db_connector()

    req = "SELECT insee, score_2 FROM score_2"

    output = pd.read_sql(req, conn)

    output = output.set_index("insee").squeeze()
    output.name = "score_2"

    return output


def get_score_1() -> pd.DataFrame:
    conn = get_db_connector()

    req = "SELECT insee, score_1 FROM score_1"

    output = pd.read_sql(req, conn)

    output = output.set_index("insee").squeeze()
    output.name = "score_1"

    return output


# %%
# Récupération des bornes
def get_bornes_from_scenario(table_name: str) -> pd.DataFrame:
    conn = get_db_connector()

    req = f"SELECT insee, bornes_score FROM {table_name}"

    output = pd.read_sql(req, conn)

    output = output.set_index("insee").squeeze()
    output.name = table_name

    return output


def get_bornes_smoothed_uniform_scenario() -> pd.DataFrame:
    return get_bornes_from_scenario("bornes_smoothed_uniform_scenario")


def get_bornes_smoothed_local() -> pd.DataFrame:
    return get_bornes_from_scenario("bornes_smoothed_local")


def get_bornes_smoothed_tourisme() -> pd.DataFrame:
    return get_bornes_from_scenario("bornes_smoothed_toursime")


def get_bornes_smoothed_reseau() -> pd.DataFrame:
    return get_bornes_from_scenario("bornes_smoothed_reseau")
