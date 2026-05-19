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

regiones = {
    "Tlaxcala": "Centro",
    "Puebla": "Centro",
    "Ciudad de México": "Centro",
    "Morelos": "Centro",
    "México": "Centro",
    "Hidalgo": "Centro",
    "Jalisco": "Centro Oeste",
    "Michoacán de Ocampo": "Centro Oeste",
    "Colima": "Centro Oeste",
    "Aguascalientes": "Centro Oeste",
    "Nayarit": "Centro Oeste",
    "Zacatecas": "Centro Oeste",
    "San Luis Potosí": "Centro Oeste",
    "Guanajuato": "Centro Oeste",
    "Querétaro": "Centro Oeste",
    "Chihuahua": "Noreste",
    "Coahuila de Zaragoza": "Noreste",
    "Nuevo León": "Noreste",
    "Tamaulipas": "Noreste",
    "Durango": "Noreste",
    "Baja California": "Noroeste",
    "Baja California Sur": "Noroeste",
    "Sonora": "Noroeste",
    "Sinaloa": "Noroeste",
    "Guerrero": "Sureste",
    "Veracruz de Ignacio de la Llave": "Sureste",
    "Oaxaca": "Sureste",
    "Tabasco": "Sureste",
    "Chiapas": "Sureste",
    "Campeche": "Sureste",
    "Yucatán": "Sureste",
    "Quintana Roo": "Sureste"
}

"""para extraer los nombres exactos"""
print(estados["name"].unique())

"""incorporamos la nueva columna"""
estados["region"] = estados["name"].map(regiones)

# 6.	Asegura que ambos GeoDataFrames utilicen el CRS epsg=3395 que usa metros como medida de distancia

"""aseguramos que el crs sea el esperado"""
print(estados.crs)
print(tiendas_gdf.crs)

"""como no lo anterior es falso, debemos cambiar al que piden CRS epsg=3395"""
estados = estados.to_crs("EPSG:3395")
tiendas_gdf = tiendas_gdf.to_crs("EPSG:3395")

#confirmo
print(estados.crs)
print(tiendas_gdf.crs)

# 7.	Crea un buffer de 120 km alrededor de los puntos de localización de cada sucursal. 

tiendas_gdf["geometry"] = tiendas_gdf.geometry.buffer(120_000)  # 120,000 metros
