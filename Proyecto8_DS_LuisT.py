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