# %%
# Importation
import os
import sys

import pandas as pd

sys.path.insert(0, os.getcwd())

from e_cartomobile.data_extract.bornes import get_bornes_data_combined  # noqa: E402
from e_cartomobile.data_transform.compute_besoins import (  # noqa: E402
    compute_besoin_local,
    compute_besoin_reseau,
    compute_besoin_tourisme,
)
from e_cartomobile.data_transform.compute_bornes import (  # noqa: E402
    compute_bornes_by_communes_ponderated,
    compute_bornes_by_communes_smoothed,
)
from e_cartomobile.infra.database.sql_connection import get_db_engine  # noqa: E402

# %%
# Connexion
# engine = get_db_engine()

# %%
# Workflow
# On suppose que les scores locaux, tourisme et reseau sont pré-calculés
# Et à jour dans la base de données : on ne met à jour que les bornes et l'aval
# df_bornes_data_combined = get_bornes_data_combined()
# df_bornes_data_combined.to_sql(
#     name="bornes_etalab_cleaned_combined", con=engine, if_exists="replace"
# )

df_bornes_communes_smooth = compute_bornes_by_communes_smoothed()
# df_bornes_communes_smooth.to_sql(
#     name="bornes_communes_smoothed", con=engine, if_exists="replace"
# )
df_bornes_communes_smooth.to_csv(
    "./e_cartomobile/content/local_data/bornes/df_bornes_communes_smooth.csv"
)

# Besoin local
s_bornes_communes_smoothed_local = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_local"
)
df_bornes_communes_smoothed_local = pd.DataFrame(
    s_bornes_communes_smoothed_local
).reset_index()
# df_bornes_communes_smoothed_local.to_sql(
#     name="bornes_smoothed_local", con=engine, if_exists="replace"
# )
df_bornes_communes_smoothed_local.to_csv(
     "./e_cartomobile/content/local_data/bornes/bornes_smoothed_local.csv"
)
# df_bornes_smoothed_local = get_bornes_smoothed_local()  # Should be the same as df_bornes_communes_smoothed_*
s_besoin_local = compute_besoin_local()
# df_besoin_local = pd.DataFrame(s_besoin_local).reset_index()
# df_besoin_local.index.name = "id"
# df_besoin_local.to_sql(name="besoin_local", con=engine, if_exists="replace")

# Besoin tourisme
s_bornes_communes_smoothed_tourisme = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_tourisme"
)
df_bornes_communes_smoothed_tourisme = pd.DataFrame(
    s_bornes_communes_smoothed_tourisme
).reset_index()
# df_bornes_communes_smoothed_tourisme.to_sql(
#     name="bornes_smoothed_tourisme", con=engine, if_exists="replace"
# )
df_bornes_communes_smoothed_tourisme.to_csv(
    "./e_cartomobile/content/local_data/bornes/bornes_smoothed_tourisme.csv"
)
# df_bornes_smoothed_tourisme = get_bornes_smoothed_tourisme()
s_besoin_tourisme = compute_besoin_tourisme()
# df_besoin_tourisme = pd.DataFrame(s_besoin_tourisme).reset_index()
# df_besoin_tourisme.index.name = "id"
# df_besoin_tourisme.to_sql(name="besoin_tourisme", con=engine, if_exists="replace")

# Besoin reseau
s_bornes_communes_smoothed_reseau = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_reseau"
)
df_bornes_communes_smoothed_reseau = pd.DataFrame(
    s_bornes_communes_smoothed_reseau
).reset_index()
# df_bornes_communes_smoothed_reseau.to_sql(
#     name="bornes_smoothed_reseau", con=engine, if_exists="replace"
# )
df_bornes_communes_smoothed_reseau.to_csv(
    "./e_cartomobile/content/local_data/bornes/bornes_smoothed_reseau.csv"
)
# df_bornes_smoothed_reseau = get_bornes_smoothed_reseau()
s_besoin_reseau = compute_besoin_reseau()
# df_besoin_reseau = pd.DataFrame(s_besoin_reseau).reset_index()
# df_besoin_reseau.index.name = "id"
#df_besoin_reseau.to_sql(name="besoin_reseau", con=engine, if_exists="replace")

# %%
# Save final results
df_besoin = pd.concat([s_besoin_local, s_besoin_tourisme, s_besoin_reseau], axis=1)
df_besoin.columns = ["local", "tourisme", "reseau"]
df_besoin["cumul"] = df_besoin.mean(axis=1)
df_besoin.to_csv("./e_cartomobile/content/df_besoin.csv")

for col in df_besoin.columns:
    df_besoin[col].to_csv(f"./e_cartomobile/content/df_besoin_{col}.csv")
