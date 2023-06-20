Auteur: Michaël Leroy

Série de notebooks pour obtenir:

    - OCM_helper_functions.py:
        differentes fonctions reprises des notebooks precedents, à élaguer car tout n'est pas utilisé
    - OSM_helper_functions.py:
        idem
    - Step0A1_Graph_osm.ipynb:
        Construction du graph routier
    - Step0A2_Graph_tjma.ipynb:
        Report des tmja de data.gouv dans le graph routier
    - Step0A3_Graph_interpolate_tmja.ipynb
        Extrapolation des tmja à un maximum d'edges
    - Step0B1_Communes_boundaries_osm.ipynb
        Récuperation via API Nominatim, du point central et de l'osmid pour chaque commune ( 4 requètes echouent, correction manuelle dans les notebooks suivants)
    - Step0B2_datas_osm copy.ipynb:
        Extraction des activtées depuis osm.
        Ne sert plus, mais je le laisse au cas où on voudrait se lacher sur les tags
    - Step0B3_data_tourisme.ipynb:
        Reprise de l'idée du notebook précédent sur le fichier data-tourisme
        triage rdes tags et regroupement en catégories (exploitables?, sinon à affiner)
    - Step0C0_Graph_routier_paths_matrix.ipynb:
        Super mauvaise idée de précalculer la distance matrix sur la france entière ==> OOM
    - Step0C1_Nodes.ipynb:
        Cretion des nodes du Graph tourisme
    - Step0C2_Edges.ipynb:
        Création des edges du Graph tourisme
    - Step0C3_Graph.ipynb:
        Calcul de stats sur le graph tourisme
    
    Explications plus détaillés en entête de chaque notebook

    Fichiers crées pour chaque graph:
        - .graphml : export au format graphml
        - .pkl : geopandas pour les nodes et edges

A faire:
    * Nettoyer le code dégeu
    * Reprendre le typage des fonctions
    * Générer les docstring

    * GNN sur le graph tourisme pour obtenir un ranking des communes, en l'état actuel juste sur le tourisme, mais en modifiant juste la géodataframe []Gnodes_tourism.pkl on peut faire des graphs avec toutes les features que nous avons récupéré ( population, bornes, etc), il suffit d'updater le dictionnaire des attributs du noeud, chaque noeud contenant le codgeo de la commune.    


[+] Infos complémentaires:
        
        * Les OOM se produisent à 48Go sur mon PC   
        * Tous les graphs sont des MultiDiGraphs ( voir doc Networkx)
        * Le graph routier tient compte du sens de circulation, donc à la construction des edges du graph tourisme les distances peuvent être diférentes en fonction du sen de circulation   

[TODO] Si tous les notebooks s'enchainent bien (pas encore pû verifier entièrement), créer un pipeline DIAG DVC pour automatiser la création des dataframes 