#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 18:25:43 2021

@author: singaresekou et gueyelamine
"""

#### Importation des librairies

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

import configparser

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

import numpy as np
import folium

#### 1- Instancier le client Spark Session."
# Instantiation
spark = SparkSession.builder\
                    .master("local")\
                    .appName("Spark_k-means")\
                    .getOrCreate()

#### 2- Créer un fichier properties.conf contenant les informations relatives à vos paramètres du programme en dur."

# Utiliser le fichier de configuration pour récupérer les path.
config = configparser.ConfigParser()
config.read('properties.conf')

path_to_input_data = config['Bristol-City-bike']['Input-data']
path_to_output_data = config['Bristol-City-bike']['Output-data']
num_partition_kmeans = config.getint('Bristol-City-bike', 'Kmeans_level') # conversion en numérique 

#### 3-Importer le json avec spark "

bristol = spark.read.json(path_to_input_data)
bristol.show(5)

#### 4-créer un nouveau data frame Kmeans-df contenant seulement les variables latitude et longitude."

Kmeans_df = bristol.select("latitude", "longitude")
Kmeans_df.show(5)

#### 5- L'algorithme du k-means.

features = ('longitude','latitude')
kmeans = KMeans().setK(num_partition_kmeans).setSeed(1)
assembler = VectorAssembler(inputCols=features, outputCol="features")
dataset=assembler.transform(Kmeans_df)
model = kmeans.fit(dataset)
fitted = model.transform(dataset)

#### 6- quels sont les noms des colonnes de fitted ? vérifier qu’il s’agit de longitude, latitude, features, predictions."

fitted.columns
 
#Il s’agit bien de longitude, latitude, features, prediction

#### 7- Déterminer les longitudes et latitudes moyennes pour chaque groupe en utilisant spark DSL et SQL. comparer les résultats"

#spark DSL
fitted.groupBy("prediction")\
      .agg(F.mean("latitude").alias("latitude"), F.mean("longitude").alias("longitude"))\
      .show()

#spark SQL
fitted.createOrReplaceTempView("fittedSQL")

spark.sql("""select prediction ,mean(latitude) as latitude,
                    mean(longitude) as longitude  from fittedSQL group by prediction""").show()

# Nous obtenons les mêmes resultats avec spark DSL et spark SQL.

#### 8- Bonus:  Faire une visualisation dans une map avec le package leaflet"

data = fitted.toPandas()
data['name'] = bristol.select("name").toPandas()
data.head(5)

# Définition des coordonnées pour centrer la carte
meanlat = data['latitude'].mean()
meanlong = data['longitude'].mean()

# Colorier les vélos en fonction de leur classe
def couleur(prediction):
    if prediction == 0:
        col = 'green'
    elif prediction == 1:
        col = 'blue'
    else:
        col = 'orange'
    return col

map_velo = folium.Map(location = [meanlat, meanlong], zoom_start = 14)

for latitude, longitude, name, prediction in zip(data['latitude'], data['longitude'], data['name'], data['prediction']):
    folium.Marker(location=[latitude, longitude], popup=name,
                  icon=folium.Icon(color=couleur(prediction),
                                   icon_color='yellow', icon='bicycle', prefix='fa')).add_to(map_velo)
    
output_map = path_to_output_data + "carte_velo_brisbane.html"
map_velo.save(output_map)

# Visualisation
map_velo

#Ajout des centres des clusters sur la carte
folium.Marker([-27.460240636363633, 153.04186302272726], popup = 'centre cluster 3', 
              icon=folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(map_velo)

folium.Marker([-27.47255990624999, 153.02594553125], popup = 'centre cluster 2',
             icon=folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(map_velo)

folium.Marker([-27.481218536585374, 153.00572882926832], popup = 'centre cluster 1',
             icon=folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(map_velo)

#Display the map
map_velo

#### 9- Exporter la data frame fitted après élimination de la colonne  features, dans le répertoire path-to-output-data"

fitted.drop("features")\
      .toPandas().to_csv(path_to_output_data + "fitted.csv")

# Fermeture de spark
spark.stop()
