# PROJET_SPARK_K-MEANS_CLUSTERING
L'objectif principal de ce projet est de proposer un k-means clustering de Brisbane City Bike en fonction de l'emplacement des stations vélos en utilisant spark.

## Lancer le programme.
Assurez - Vous d'étre dans le bon fichier <br>
-  Lancement du porgramme : ouvrir un invité de commande et taper la commande suivante :

```spark-submit k-means.py```

-----------------------------------------------------------------------

## Description de la base de données
Le fichier Brisbane-city-bike.json (notre base de données) contient des informations concernant l’emplacement de chaque vélo. Il est composé des variables suivantes :

  - Adresse
  - Latitude
  - Longitude
  - name
  - number
  
Les 5 premières observations sont données dans le tableau suivant :

|             address|  latitude| longitude|                name|number|
|:-------------------|:---------|:---------|:-------------------|:----:|
|Lower River Tce /...|-27.482279|153.028723|122 - LOWER RIVER...|   122|
|Main St / Darragh St| -27.47059|153.036046|91 - MAIN ST / DA...|    91|
|Sydney St Ferry T...|-27.474531|153.042728|88 - SYDNEY ST FE...|    88|
|Browne St / James St|-27.461881|153.046986|75 - BROWNE ST / ...|    75|
|Kurilpa Point / M...|-27.469658|153.016696|98 - KURILPA POIN...|    98|

-----------------------------------------------------------------------

### Résultat du K-mean

Nous nous sommes basés sur la latitude et la longitude comme variables d'entrées pour la réalisation du K-means.
Il a été demandé de réaliser 3 groupe de cluster par la méthode des K-means sous spark.
Le k-means a permis d'avoir 3 cluster (groupe suivant l'emplacement des vélos) qui sont disposés de la façon suivante :

- un premier groupe se placant à l'est de la ville
- un second groupe étant au centre de la ville
- un dernier groupe à l'ouest de ville. 

Les longitudes et latitudes moyennes de chaque groupe sont données par le tableaux ci-dessous.

|   Longitude moyen|      Latitude Moyen|Groupe      |
|:-----------------|:------------------ |:---------: |
|153.04186302272726|-27.46024+0636363633|     Est    |
|   153.02594553125| -27.47255990624999 |      Centre|
|153.00572882926832|-27.481218536585374 |      Ouest |

-----------------------------------------------------------------------
## Visualisation

Sur l'image ci-dessous nous avons la cartographie de l'emplacement des vélos en fonction de leur groupe.

![Visualisation](https://user-images.githubusercontent.com/56762162/105491924-6e0c4300-5cb7-11eb-89eb-6f1c29b23d09.jpg)

Sur la carte, on voit bien l'emplacement des vélos en fonction de leur groupe d'appartenance obtenu via la méthode des K-means. Vous pouvez consulter la version interactive de la carte est disponible en <a href="https://ghcdn.rawgit.org/sing0019/PROJET_SPARK_K-MEANS_CLUSTERING/master/exported/carte_velo_brisbane.html" target="_blank">cliquant ici</a>.
