### Generation du graph routier national sous NEO4J

##### Lancer le container Neo4J

Depuis ce même dossier, lancer le container Neo4j avec docker-compose

``` docker compose up ```

Au moment de la compilation et du lancement du container, les dossiers conf, data, import, logs et plugins sont automatiquement créés.

Vérifier que les deux fichiers de plugins en .jar (apoc et graph-data-science) ont bien été générés le dossier plugins.

##### Interface Neo4J et première connexion

Visualisation :

Deux interfaces de visualisations sont possibles:

Pour "dialoguer" avec le graph de manière simple et rapide, une interface web browser existe à l'adresse http://localhost:7474

- Utiliser "Neo4j Desktop" si le logiciel est présent sur l'ordinateur. Une fois le logiciel lancé, "Add" => "Remote connection". Nommer la nouvelle base de données.

À la première visite, il est demandé de définir les idientifiants et mots de passe.

Par défaut, Initialement, l'id_user par défaut est : neo4j
Et le mot de passe est : neo4j

À la première connexion, il est possible de redéfinir ce user et  mot de passe.


#### Reqêtes en langage Cypher

Toutes les requêtes d'écritures et de consultation du graph se font grâce au langage Cypher, qui est un langage déclaratif qui peu ressembler, très souvent au SQL.

Il peut être bon de s'y familiariser pour pouvoir checker ce qui se passe du côtès du graph, et vérifier, par exemple, sa bonne génération.

Exemple :

Visualiser toutes les villes qui ont des points d'intérêts touristiques (visit_score) au-delà de 10, et limiter le résultat à 25 villes.

``` MATCH (c:CITY) WHERE c.visit_score > 10 RETURN c LIMIT 25 ```

LE c utilisé ici est une variable qui sert d' "alias" et peut se ré-employer dans la suite de la requête

(La requête ressemble en effet, dans sa logique, à "SELECT cities AS c FROM cities WHERE c.visit_score > 10 LIMIT 25; " en SQL ...)

Pour apprendre facilement (et rapidement) le langage Cypher c'est ici -> https://graphacademy.neo4j.com/categories/beginners/



#### Génération du graph routier

##### Génération du graph de points routiers :

- Tout d'abord, il faut importer le fichier de Micka du graph généré à partir des données d'Open Street Map.
Comme le fichier est voluminieux pour Git, il faut demander à Micka ce fichier par WeTransfer, par exemple.

Le fichier .graphml est à mettre dans le dossier "import".

Ensuite, se rendre sur l'interface simple à l'adresse http://localhost:7474.

Lancer la requête suivante :

```CALL apoc.import.graphml("[france]graph.graphml", {readLabels: true})```

Après quelques minutes, le graph des points routes est généré.

On peut vérifier avec la requête :

```MATCH (p:) RETURN p LIMIT 25```

- Ensuite, les autres éléments du graphe (communes, relations NEARLY_TO entre communes et points routes...) peuvent être générés à partir des notebooks qui se situent dans le dossier "notebooks_generation"

Il faut suivre l'ordre des numérotations des titres des notebooks.

Les deux notebooks qui concernent les "NATIONAL_ROAD_POINT" sont optionnels (voire inutiles). (Ce sont des héritages des tentatives d'utilisations du graph de data.gouv avec TMJA.)

Le premier des trois notebooks intitulé "neo4j_generation_graph_communes" qui, comme son nom l'indique, permet de générer les points "communes" (CITY) fait intervenir des fichiers qui ont été préalablement construits par des membres de l'équipe. Ces trois fichiers ont été rassemblés dans le dossier "data_communes" pour éviter de chercher partout ailleurs.

