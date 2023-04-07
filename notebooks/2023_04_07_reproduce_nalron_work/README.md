# Mise à jour d'un projet sur les IRVE

Dans le cadre du projet Data For Good saison 11 intitulé "Évolution des infrastructures de recharge pour les véhicules électriques", nous avons commencé par rechercher si d'autres développeurs avaient déjà exploité les données ouvertes du gouvernement sur les bornes de recharge pour véhicules électriques (IRVE) disponibles en France : https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/.

Un projet développé par Nalron est pertinent et poussé, avec de l'analyse de données, des prédictions avec la librairie Prophet puis des visualisations faites sur Tableau. Cependant, ses derniers commits datent d'août 2020 et certaines data sources nécessitent une mise à jour. 


Projet de nalron: https://github.com/nalron/project_electric_cars_france2040

Projet data for good saison 11 :
- Notion page: https://dataforgood.notion.site/volution-des-infrastructures-de-recharge-pour-les-v-hicules-lectriques-984f4f4256f547a5bf13ea88c033e061
- Repo github: https://github.com/dataforgoodfr/batch11_e_cartomobile


# Setup

Créer un environnement virtuel avec toutes les dépendances pour exécuter les notebooks de ce repo :
```
poetry install
```
Ensuite, vous pouvez sélectionner cet environnement virtuel dans VSCode pour exécuter les notebooks. Si vous préférez exéctuer vos notebooks dans le navigateur:
```
poetry run ipython kernel install --user --name=<YOUR_KERNEL_NAME>
jupyter notebook
```
Ensuite, sélectionnez le kernel créé dans l'interface web.


# TODO in next weeks

- Sync avec les autres équipes qui utilisent les mêmes données
- Check pourquoi certaines communes sont manquantes dans le join communes - immatriculations dans le notebook ```enrichissement_dataset_voitures_par_commune_et_type_de_charge.ipynb```. Comparer les données communes obtenues sur "https://geo.api.gouv.fr/communes/<code>" avec le csv ```raw_data/communes-departement-region.csv```. Il faut s'assurer qu'il n'y a pas trop de valeurs manquantes pour avoir des vizs fiables -> Cela semble avoir été fait par Michaël Leroy.
- Continuer les vizs folium, intégrer les plus intéressantes dans une application streamlit. Reproduire les vizs du Tableau public de Nalron à partir de nos premiers notebooks -> Pareil, voir comment les autres équipes ont fixé leurs données et valider la méthodo.
- Bien valider la qualité des données consolidées IRVE + continuer le nettoyage du notebook, certaines méthodes d'imputation sont moches -> contact avec Michaël Leroy, Hugo et Esther qui ont aussi travaillé dessus.
- Problème de join avec les communes à fixer
- Visualiser la concentration des IRVE en France via des heatmaps, ou par département / commune en utilisant folium.
- Croiser ces vizs avec les données de population et de trafic routier.


# Détails sur les data sources utilisées par Nalron & comparaison les notres

Nalron a utilisé de nombreuses data sources, certaines sont pertinentes pour notre sujet à court ou long terme, d'autres peuvent être écartées. Nous allons les détailler et faire des liens avec les datasources repérées pour le projet Data For Good.

## Principales data sources utilisées par nalron


### Données des immatriculations des véhicules : [statistiques.developpement-durable.gouv.fr](https://www.statistiques.developpement-durable.gouv.fr/donnees-sur-les-immatriculations-des-vehicules)

Ces infos d'immatriculations par type de motorisation + par puissance ne sont plus disponible tel quel en 2022 sur le site statistiques.developpement-durable.gouv.fr. Il y a cependant 3 datasets intéressants:


- Sur data.gouv se trouve un fichier qui correspond : [voitures par commune et type de recharge](https://www.data.gouv.fr/fr/datasets/voitures-particulieres-immatriculees-par-commune-et-par-type-de-recharge/). Nous l'avons exploité et enrichi avec des informations sur le découpage des communes et des départements.

- Fichier de répartition des véhicules privés par motorisation et ancienneté : [data](https://www.statistiques.developpement-durable.gouv.fr/donnees-sur-le-parc-de-vehicules-en-circulation-au-1er-janvier-2022). Pourquoi pas.
    
### Tableau comparatif des voitures électriques : [fiches-auto.fr](http://www.fiches-auto.fr/articles-auto/electrique/s-852-comparatif-des-voitures-electriques.php)

Ces fiches auto sont intéressantes mais pas indispensables. Les colonnes ont changé donc à rescrapper si nécessaire. On verra pour la suite de projet mais on ne les utilisera pas dans l'immédiat.

### Données des bornes de recharge pour véhicules électriques (IRVE) : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/)


Ce fichier est la base de notre étude. Il est exploité principalement dans le notebook 2 du projet de nalron. Cette data source est une consolidation à partir de plusieurs autres sources, fournissant des indications de géolocalisation, département, région, opérateur d'exploitation, type de prise, etc…
Une nouvelle version de ce fichier consolidé a été publié en fin 2022: https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/
Cette nouvelle version est beaucoup plus fiable que la version de 2020. Il n'est pas nécessaire de faire le même travail d'imputation que nalron a fait, même si nous devons être prudents et checker ces données.

### Auchan, Leclerc, Tesla, Nissan...

Nalron a consolidé le fichier consolidé ci-dessus avec les données mises à disposition par différentes enseignes qui n'apparaissaient apparamment plus à partir de juin 2020 dans son fichier. Nous vérifierons si c'est toujours le cas dans la nouvelle consolidation de la data source data.gouv. Nous devrons peut-être consolider nous aussi ce fichier avec de nouvelles sources comme celles mentionnées dans la page Notion : [Partage ma borne](https://partagemaborne.fr/), [Clem](https://www.clem-e.com/), [Clem déjà présent sur data.gouv](https://www.data.gouv.fr/fr/datasets/bornes-de-recharge-clem-mobilite/)...


### Données des points de charge par typologie : [data.enedis.fr](https://data.enedis.fr/explore/dataset/nombre-de-points-de-charge-par-typologie/information/)

Ce dataset est très intéressant. Une version mise à jour existe sur le site d'Enedis avec les typologies déjà présentes en colonnes, donc pas besoin de pivoter la table : [points de charge fichier Enedis](https://data.enedis.fr/explore/dataset/nombre-total-de-points-de-charge/information/?dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiU1VNIiwieUF4aXMiOiJzb2NpZXRlIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0E2QjlFNCJ9LHsidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJTVU0iLCJ5QXhpcyI6InBhcnRpY3VsaWVyIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZDOEQ2MiJ9LHsidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJTVU0iLCJ5QXhpcyI6ImFjY2Vzc2libGVfYXVfcHVibGljIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2QzJBNSJ9XSwieEF4aXMiOiJ0cmltZXN0cmUiLCJtYXhwb2ludHMiOjUwLCJzb3J0IjoiIiwic3RhY2tlZCI6Im5vcm1hbCIsImNvbmZpZyI6eyJkYXRhc2V0Ijoibm9tYnJlLXRvdGFsLWRlLXBvaW50cy1kZS1jaGFyZ2UiLCJvcHRpb25zIjp7fX19XSwidGltZXNjYWxlIjoiIiwic2luZ2xlQXhpcyI6dHJ1ZSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&sort=-trimestre).

Enedis précise que leurs données sont combinées avec les données de [Girève](https://www.data.gouv.fr/fr/organizations/gireve-2/) et AAA data (qui ne semblent pas être open).  Il est possible de checker cela en récupérant ces données. On pourra aussi croiser les données Enedis avec celles de [ODRE](https://odre.opendatasoft.com/explore/dataset/bornes-irve/information/?disjunctive.region&disjunctive.departement&sort=n_amenageur&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJ5QXhpcyI6ImNvZGVfaW5zZWUiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1jdXN0b20ifV0sInhBeGlzIjoiZGVwYXJ0ZW1lbnQiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwiY29uZmlnIjp7ImRhdGFzZXQiOiJib3JuZXMtaXJ2ZSIsIm9wdGlvbnMiOnsiZGlzanVuY3RpdmUucmVnaW9uIjp0cnVlLCJkaXNqdW5jdGl2ZS5kZXBhcnRlbWVudCI6dHJ1ZX19LCJzZXJpZXNCcmVha2Rvd24iOiJwdWlzc19tYXgifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWUsInRpbWVzY2FsZSI6IiJ9&location=5,46.79635,2.65923&basemap=jawg.light) ou d'autres source comme [celle-ci](https://odre.opendatasoft.com/explore/dataset/bornes-irve/api/?disjunctive.region&disjunctive.departement)


### Parc des installations de production raccordées par departement : [data.enedis.fr](https://data.enedis.fr/explore/dataset/parc-des-installations-de-production-raccordees-par-departement/information/?disjunctive.type_injection)

Les sites de production sont des infos complémentaires à notre étude, à mettre à jour si on juge cela intéressant : nouvelle version très similaire à l'ancienne.
    
### Données en puissance sur la consommation et production par filière d'énergie : [rte-france.com](https://www.rte-france.com/fr/eco2mix/eco2mix-telechargement)


--> Les sites de production sont des infos complémentaires à notre étude, à mettre à jour si on juge cela intéressant : https://www.rte-france.com/eco2mix


## Data sources mentionnées dans notre Notion et non creusées par nalron

### "Trafic moyen journalier annuel sur le réseau routier national"

Non utilisé par nalron. Intéressant mais seulement traffic autoroutier d'après Michael Leroy.

### "Institut National de la Statistique et des Etudes Economiques (Insee) - Population"

Intéressant pour notre problématique.

### "Foncier"

Selon les besoins client.

### Scrapping additionnel

Partage ma borne, Clem... sites de bornes à partager à scrapper.


# Critique constructive de ce qui a été fait dans le repo de nalron

## Notebook 1

- Partie 1 : Evolution du nombre de nouvelles immatriculations par type de motorisation et groupes de puissance : Trop précis dans la catégorisation des véhicules. La typologie par type de motorisation est suffisante.
- Partie 2 : Pareil par type de motorisation : Intéressant, nous allons reproduire cette visualisation en utilisant folium puis l'exposer avec streamlit plutôt que passer par un serveur Tableau public.
- Partie 3 : Scrapping d'informations sur les véhicules éléctriques : Peut être exploité dans un second temps mais pas essentiel à ce stade
- Partie 4 : Prédictions, projections à 2 ans de l'évolution du nombre de véhicules électriques, diesel, essence... Pas beaucoup de points de données, la prédiction est délicate.


## Notebook 2

- Partie 1 : Données points de charge par typologie, bonne initiative. Aujourd'hui un dataset avec les typologies en colonne existe ce qui évite le passage par le pivot_table. Aussi, les boxplots sont inutiles ici, on n'a pas besoin de voir de moyenne ni de quantile par année, cela ne fait pas sens. A certains endroits le code peut être optimisé. Dans l'ensemble ceci est très utile pour notre projet.
- Partie 2 : Données IRVE, partie clé pour nous. Une bonne partie du notebook cherche à remplacer les valeurs NaN des enseignes / aménageurs. Est-ce vraiment utile ? De plus, les dernières consolidations de la datasource data.gouv sont beaucoup plus fiables que celles de 2020. De nombreuses données manquantes ont été ajoutées. Une catégorisation des aménageurs de points de charge est faite dans ce notebook.
- La dernière partie sur les prédictions est, comme pour le notebook 1, pas très pertinente. Mais cela fait joli. On saura que si on reste sur la cadence actuelle, on aura un certain nombre d'IRVE... C'est pourquoi l'évaluation et la comparaison avec Holtwinter n'est pas nécessaire. On sait que notre modèle est limité.


## Notebook 3

- Analyse de la consommation d'électricité en France et des filières de production. Profiler un pic d’utilisation des bornes de recharge. Courbe de charge réseau électrique pour répondre aux nouveaux modes de consommation.

Intéressant mais on ne traitera pas ce sujet dans l'immédiat.
