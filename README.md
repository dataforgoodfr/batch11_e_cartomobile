# batch11_e_cartomobile

Encourager et planifier la mobilité électrique dans les territoires avec l’Open-Data

## Installer l'environnement virtuel

Versions Python supportées : ">=3.8.1,<3.9.7 || >3.9.7,<3.10"

Si votre version ne respecte pas ces critères, référez vous à la partie [Comment changer ma version Python locale](#changer-ma-version-python-locale).

Pour installer l'environnement virtuel avec toutes les dépendences du projet:
```
poetry install
```
L'environnement sera installé dans le folder .venv à la racine de ce projet.

## Lancer l'application streamlit en local

Pour lancer l'application streamlit en local, run:
```
make run_streamlit
```
Si l'environnement virtuel python n'a pas été installé au prélable, il sera installé en utilisant poetry.

## Changer ma version Python locale

TODO pyenv short tuto
