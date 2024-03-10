# %%
# Importation
import datetime as dt
import os
import sys

sys.path.insert(0, os.getcwd())

from e_cartomobile.data_extract.immatriculations import (  # noqa: E402
    get_immatriculations_data_online,
)
from e_cartomobile.data_transform.compute_score_4 import compute_score_4  # noqa: E402
from e_cartomobile.data_transform.immatriculations import (  # noqa: E402
    clean_immatriculations_data,
)
from e_cartomobile.infra.database.sql_connection import get_db_engine  # noqa: E402

# %%
# Connexion
# engine = get_db_engine()

# %%
# Workflow
# On suppose que les données de communes sont présentes dans la base
raw_immatriculations = get_immatriculations_data_online()

immatriculations = clean_immatriculations_data(raw_immatriculations)

# immatriculations.to_sql(
#     name="immatriculations_cleaned", con=engine, if_exists="replace"
# )
immatriculations.to_csv(
    "./e_cartomobile/content/local_data/immatricutations.csv"
)

output_score4 = compute_score_4(immatriculations, gamma=5, dist_max_km=20)
output_score4["gamma"] = 5.0
output_score4["max_distance_km"] = 20.0
output_score4["last_update"] = dt.date.today()
output_score4 = output_score4.reset_index()
output_score4.index.name = "id"
# output_score4.to_sql(name="score_4", con=engine, if_exists="replace")
output_score4.to_csv("./e_cartomobile/content/local_data/scores/score_4.csv")
