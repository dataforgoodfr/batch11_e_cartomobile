# %%
# Importation
from e_cartomobile.data_extract.immatriculations import get_immatriculations_data_online
from e_cartomobile.data_transform.immatriculations import clean_immatriculations_data
from e_cartomobile.data_transform.compute_score_4 import compute_score_4

from e_cartomobile.infra.database.sql_connection import get_db_engine


# %%
# Connexion
engine = get_db_engine()

# %%
# Workflow
# On suppose que les données de communes sont présentes dans la base
raw_immatriculations = get_immatriculations_data_online()

immatriculations = clean_immatriculations_data(raw_immatriculations)

immatriculations.to_sql(
    name="immatriculations_cleaned_test", con=engine, if_exists="replace"
)

output_score4 = compute_score_4(immatriculations, gamma=5, dist_max_km=20)
output_score4["gamma"] = 5.0
output_score4["max_distance_km"] = 20.0
output_score4 = output_score4.reset_index()
output_score4.index.name = "id"
output_score4.to_sql(name="score_4_test", con=engine, if_exists="replace")
