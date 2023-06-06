import pandas as pd

from e_cartomobile.infra.database.sql_connection import get_db_connector


def get_score_4(gamma: float, dist_max_km: float) -> pd.DataFrame:
    conn = get_db_connector()

    req_score = f"""SELECT insee, score_4
    FROM score_4
    where gamma = {gamma} and max_distance_km = {dist_max_km}"""

    output_score4 = pd.read_sql(req_score, conn, index_col="insee")
    output_score4 = output_score4.squeeze()
    output_score4.name = "score_4"

    return output_score4
