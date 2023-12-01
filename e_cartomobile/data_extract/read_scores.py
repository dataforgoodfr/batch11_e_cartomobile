# %%
# Importation
import pandas as pd
from sklearn.preprocessing import QuantileTransformer

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
def get_bornes_smoothed_uniform_scenario() -> pd.DataFrame:
    conn = get_db_connector()

    req = "SELECT insee, bornes_score FROM bornes_smoothed_uniform_scenario"

    output = pd.read_sql(req, conn)

    output = output.set_index("insee").squeeze()
    output.name = "bornes_smoothed_uniform_scenario"

    return output


# %%
# Calcul des besoins
def compute_besoin_local() -> pd.DataFrame:
    bornes_smoothed_uniform_scenario = get_bornes_smoothed_uniform_scenario()
    score_4 = get_score_4(5, 20)

    besoin_local = bornes_smoothed_uniform_scenario / score_4
    besoin_local = besoin_local.fillna(0)
    scaler = QuantileTransformer()
    besoin_local_scaled = scaler.fit_transform(besoin_local.values.reshape(-1, 1))

    s_besoin_local = pd.Series(
        besoin_local_scaled.T[0], index=besoin_local.index, name="besoin_local"
    )

    return s_besoin_local


def compute_besoin_tourisme(esp=1e-5) -> pd.DataFrame:
    """
    The esp value is necessary to impose a minimum value to the need of charging station
    """
    bornes_smoothed_uniform_scenario = get_bornes_smoothed_uniform_scenario()
    score_2 = get_score_2()

    besoin_tourisme = bornes_smoothed_uniform_scenario / (score_2 + esp)
    besoin_tourisme = besoin_tourisme.fillna(0)

    scaler_tourisme = QuantileTransformer()
    besoin_tourisme_scaled = scaler_tourisme.fit_transform(
        besoin_tourisme.values.reshape(-1, 1)
    )

    s_besoin_tourisme = pd.Series(
        besoin_tourisme_scaled.T[0], index=besoin_tourisme.index, name="besoin_tourisme"
    )

    return s_besoin_tourisme


def compute_besoin_reseau() -> pd.DataFrame:
    bornes_smoothed_uniform_scenario = get_bornes_smoothed_uniform_scenario()
    score_1 = get_score_1()

    besoin_reseau = bornes_smoothed_uniform_scenario / score_1
    besoin_reseau = besoin_reseau.fillna(0)

    scaler_reseau = QuantileTransformer()
    besoin_reseau_scaled = scaler_reseau.fit_transform(
        besoin_reseau.values.reshape(-1, 1)
    )

    s_besoin_reseau = pd.Series(
        besoin_reseau_scaled.T[0], index=besoin_reseau.index, name="besoin_reseau"
    )

    return s_besoin_reseau
