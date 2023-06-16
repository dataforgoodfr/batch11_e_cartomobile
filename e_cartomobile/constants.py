"""Define high level constants."""

DATA_PATH = "e_cartomobile/data_extract/data"  # Path from the root of the project

# Arrondissements
MARSEILLE_ARRO = {str(13201 + i): "13055" for i in range(16)}
PARIS_ARRO = {str(75101 + i): "75056" for i in range(20)}
LYON_ARRO = {str(69381 + i): "69123" for i in range(9)}

ARRONDISSEMENT_DICT = {**MARSEILLE_ARRO, **PARIS_ARRO, **LYON_ARRO}
