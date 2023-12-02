## Generation du graph routier national sous NEO4J

### Lancer le container Neo4J

Depuis ce même dossier, lancer le container Neo4j avec docker-compose
Au préalable, les variables d'environnement "NEO4J_server.memory.pagecache.size", etc... peuvent être modifiés selon la capacité de calcul que l'on veut attribuer au graph. (8Go de RAM est déjà bien.)

``` docker compose up ```

Au moment de la compilation et du lancement du container, les dossiers conf, data, import, logs et plugins sont automatiquement créés.

Vérifier que les deux fichiers de plugins en .jar (apoc et graph-data-science) ont bien été générés le dossier plugins.

### Interface Neo4J et première connexion

Visualisation :

Deux interfaces de visualisations sont possibles:

Pour "dialoguer" avec le graph de manière simple et rapide, une interface web browser existe à l'adresse http://localhost:7474

- Utiliser "Neo4j Desktop" si le logiciel est présent sur l'ordinateur. Une fois le logiciel lancé, "Add" => "Remote connection". Nommer la nouvelle base de données.

À la première visite, il est demandé de définir les idientifiants et mots de passe.

Par défaut, Initialement, l'id_user par défaut est : neo4j
Et le mot de passe est : neo4j

À la première connexion, il est possible de redéfinir ce user et  mot de passe.


### Reqêtes en langage Cypher

Toutes les requêtes d'écritures et de consultation du graph se font grâce au langage Cypher, qui est un langage déclaratif qui peu ressembler, très souvent au SQL.

Il peut être bon de s'y familiariser pour pouvoir checker ce qui se passe du côtès du graph, et vérifier, par exemple, sa bonne génération.

Exemple :

Visualiser toutes les villes qui ont des points d'intérêts touristiques (visit_score) au-delà de 10, et limiter le résultat à 25 villes.

``` MATCH (c:CITY) WHERE c.visit_score > 10 RETURN c LIMIT 25 ```

LE c utilisé ici est une variable qui sert d' "alias" et peut se ré-employer dans la suite de la requête

(La requête ressemble en effet, dans sa logique, à "SELECT cities AS c FROM cities WHERE c.visit_score > 10 LIMIT 25; " en SQL ...)

Pour apprendre facilement (et rapidement) le langage Cypher c'est ici -> https://graphacademy.neo4j.com/categories/beginners/


### Requêtes imbriquées dans le code python

Pour les requêtes plus complexes que de la simple visualisation, il faut utiliser le module "neo4j" (pip install neo4j) dans un script python.

Des exemples sont donnés à travers les notebooks de génération du graph...

Le driver doit être initialisé comme suit :

``` driver = GraphDatabase.driver("bolt://localhost:7687",auth=basic_auth("neo4j", PASSWORD_NEO4J)) ```

avec le nom de l'user (par défaut : neo4j) et le mot de passe défini.

L'adresse bolt://localhost:7687 est l'adresse de requête du graph sous Neo4j.

Ensuite on éxécute les reqêtes comme suit :

with driver.session() as session:

    count_list = []

    result = session.execute_write(delete_all)

driver.close()

(Attention, ici c'est une requête pour tout supprimer !)


Note : On peut utiliser "session.execute_read" pour optimiser la requête s'il s'agit seulement d'une requête de lecture et non d'écriture.

Il faut préciser la fonction de requête en amont comme une simple fonction python comme suit par exemple :

def delete_all(tx):
    query = 'MATCH (n) \
                DETACH DELETE n \
                RETURN count(*) AS COUNT'
    result = tx.run(query)
    return result.data() 


#### Génération du graph de points routiers :

- Tout d'abord, il faut importer le fichier de Micka du graph généré à partir des données d'Open Street Map.
Comme le fichier est voluminieux pour Git, il faut demander à Micka ou Jesshuan, ce fichier par WeTransfer, par exemple.

Le fichier .graphml est à mettre dans le dossier "import" qui a été généré par le container Neo4j.
Il est possible que le dossier 'import" ait été généré avec des droits "root". Il faut donc faire la copie en ligne de commande :

``` sudo cp [path/file/...] [path/import/] ```

Ensuite, se rendre sur l'interface simple à l'adresse http://localhost:7474.

Lancer, dans la barre de requête de la partie droite de l'écran, la requête suivante :

```CALL apoc.import.graphml("[france]graph.graphml", {readLabels: true})```

Après quelques minutes, le graph des points routes est généré.

On peut vérifier avec la requête :

```MATCH (p) RETURN p LIMIT 25```

- Ensuite, les autres éléments du graphe (communes, relations NEARLY_TO entre communes et points routes...) peuvent être générés à partir des notebooks qui se situent dans le dossier "notebooks_generation"

Il faut suivre l'ordre des numérotations des titres des notebooks.

Les deux notebooks qui concernent les "NATIONAL_ROAD_POINT" sont optionnels (voire inutiles). (Ce sont des héritages des tentatives d'utilisations du graph de data.gouv avec TMJA.)

Le premier des trois notebooks intitulé "neo4j_generation_graph_communes" qui, comme son nom l'indique, permet de générer les points "communes" (CITY) fait intervenir des fichiers qui ont été préalablement construits par des membres de l'équipe. Ces trois fichiers ont été rassemblés dans le dossier "data_communes" pour éviter de chercher partout ailleurs.

Le deuxième notebook intitulé "neo4j_add_labels_and_index" permet d'élaborer des modifications, apports, ajouts essentiels à l'emploi de l'algorithme de plus court chemin avec Neo4j : ajout de labels, index pour optimisation des calculs, conversion de types, etc...

Le troisième notebook est focalisé sur la connection entre les points routes et les communes, par la génération de relations "NEARLY_TO". Cette construction se fait d'abord sous geopandas (par la jointure entre un fichier des gémoétries des communes et les points routes qui sont ici "gonflées" avec 5km de rayon) avant d'être générées finalement dans le graphe Neo4j. Il utilise notamment une requête url externe ver data.gouv pour récupérer les géométries des communes


