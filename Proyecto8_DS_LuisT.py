# ------------- Importacion de librerias

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# ------------- Finalizacion de las Importacion de librerias

"""se carga el archivo a usar .shp y el .csv"""

estados = gpd.read_file(r"C:\\Users\\sasor\\Desktop\\Tec de mty\\3. Visualizacion de datos con python\\2. Geovisualizacion\\reto\\mexican-states\\mexican-states\\mexican-states.shp")

tiendas = pd.read_csv("tiendaCostco.csv")

"""con esto se hace la correccino de cualquier desigualdad en los textos de las columnas del df"""
tiendas.columns = (tiendas.columns.str.strip().str.lower().str.replace(" ", "_"))

# 4.	Convierte los datos de la localización de las sucursales de Costco® en un GeoDataFrame, creando puntos a partir de la longitud y latitud de cada sucursal. 

tiendas_gdf = gpd.GeoDataFrame(tiendas, geometry=gpd.points_from_xy(tiendas.longitud, tiendas.latitud, crs="EPSG:4326"))

# 5.	Agrega una columna a los estados que indique la región a la que pertenecen y separa el GeoDataFrame por regiones en lugar de por estados:

