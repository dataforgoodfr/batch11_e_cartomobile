# %%
# Importation
import pandas as pd
from sklearn.preprocessing import QuantileTransformer

from e_cartomobile.data_extract.read_scores import (
    get_bornes_smoothed_local,
    get_bornes_smoothed_reseau,
    get_bornes_smoothed_tourisme,
    get_score_1,
    get_score_2,
    get_score_4,
)


# %%
# Calcul des besoins
def compute_besoin_local() -> pd.Series:
    bornes_smoothed = get_bornes_smoothed_local()
    score_4 = get_score_4(5, 20)

    besoin_local = bornes_smoothed / score_4
    besoin_local = besoin_local.fillna(0)
    scaler = QuantileTransformer()
    besoin_local_scaled = scaler.fit_transform(besoin_local.values.reshape(-1, 1))

    s_besoin_local = pd.Series(
        besoin_local_scaled.T[0], index=besoin_local.index, name="besoin"
    )

    return s_besoin_local


def compute_besoin_tourisme(esp=1e-5) -> pd.Series:
    """
    The esp value is necessary to impose a minimum value to the need of charging station
    """
    bornes_smoothed = get_bornes_smoothed_tourisme()
    score_2 = get_score_2()

    besoin_tourisme = bornes_smoothed / (score_2 + esp)
    besoin_tourisme = besoin_tourisme.fillna(0)

    scaler_tourisme = QuantileTransformer()
    besoin_tourisme_scaled = scaler_tourisme.fit_transform(
        besoin_tourisme.values.reshape(-1, 1)
    )

    s_besoin_tourisme = pd.Series(
        besoin_tourisme_scaled.T[0], index=besoin_tourisme.index, name="besoin"
    )

    return s_besoin_tourisme


def compute_besoin_reseau() -> pd.Series:
    bornes_smoothed = get_bornes_smoothed_reseau()
    score_1 = get_score_1()

    besoin_reseau = bornes_smoothed / score_1
    besoin_reseau = besoin_reseau.fillna(0)

    scaler_reseau = QuantileTransformer()
    besoin_reseau_scaled = scaler_reseau.fit_transform(
        besoin_reseau.values.reshape(-1, 1)
    )

    s_besoin_reseau = pd.Series(
        besoin_reseau_scaled.T[0], index=besoin_reseau.index, name="besoin"
    )

    return s_besoin_reseau
