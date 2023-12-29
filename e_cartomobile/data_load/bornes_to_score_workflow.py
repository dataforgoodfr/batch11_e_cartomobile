# %%
# Importation
from e_cartomobile.data_extract.bornes import get_bornes_data_combined
from e_cartomobile.data_extract.read_scores import (
    get_bornes_smoothed_local,
    get_bornes_smoothed_tourisme,
    get_bornes_smoothed_reseau,
)
from e_cartomobile.data_transform.compute_bornes import (
    compute_bornes_by_communes_smoothed,
    compute_bornes_by_communes_ponderated,
)
from e_cartomobile.data_transform.compute_besoins import (
    compute_besoin_local,
    compute_besoin_tourisme,
    compute_besoin_reseau,
)


# TODO : infra.database.send_to_db(df, table_name, connector)


# %%
# Workflow
# On suppose que les scores locaux, tourisme et reseau sont pré-calculés
# Et à jour dans la base de données : on ne met à jour que les bornes et l'aval

df_bornes_data_combined = get_bornes_data_combined()  # TODO : send_to_db
df_bornes_communes_smooth = compute_bornes_by_communes_smoothed()  # TODO : send_to_db

# Besoin local
df_bornes_communes_smoothed_local = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_local"
)  # TODO : send_to_db
df_bornes_smoothed_local = get_bornes_smoothed_local()  # TODO : send_to_db
s_besoin_local = compute_besoin_local()  # TODO : send_to_db

# Besoin tourisme
df_bornes_communes_smoothed_tourisme = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_tourisme"
)  # TODO : send_to_db
df_bornes_smoothed_tourisme = get_bornes_smoothed_tourisme()  # TODO : send_to_db
s_besoin_tourisme = compute_besoin_tourisme()  # TODO : send_to_db

# Besoin reseau
df_bornes_communes_smoothed_reseau = compute_bornes_by_communes_ponderated(
    df_bornes_communes_smooth, "smoothed_reseau"
)  # TODO : send_to_db
df_bornes_smoothed_reseau = get_bornes_smoothed_reseau()  # TODO : send_to_db
s_besoin_reseau = compute_besoin_reseau()  # TODO : send_to_db
