# ------------- Importacion de librerias

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from matplotlib import pyplot as plt


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

tiendas_gdf["geometry"] = tiendas_gdf.geometry.buffer(120_000)

# 8.	Grafica la intersección de las regiones con los círculos creados a partir de la localización de las sucursales. 

"""df de regiones"""
regiones_gdf = estados[estados["region"].notna()].dissolve(by="region").reset_index()

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_title("cobertura: entregas Costco por region en 120km)")
regiones_gdf.plot(ax=ax,
                  cmap="YlOrRd",
                  alpha=0.6,
                  edgecolor="black",
                  legend=True)
tiendas_gdf.plot(ax=ax,
                 facecolor="none",
                 edgecolor="black",
                 linewidth=1)

plt.show()


# 9.	Identifica las regiones en donde se requiere más cobertura y responde la pregunta: ¿En qué regiones del país (Centro, Centro Oeste, Noreste, Noroeste, Sureste) NO es conveniente abrir una nueva sucursal debido a la falta de cobertura de entregas a domicilio?

union_buffers = tiendas_gdf.geometry.unary_union
for i, row in regiones_gdf.iterrows():
    region = row["region"]
    geometria_region = row["geometry"]
    interseccion = geometria_region.intersection(union_buffers)
    porcentaje = (interseccion.area / geometria_region.area) * 100
    print(region, porcentaje)
    
"""resultados"""
# Centro 81.26916893615125
# Centro Oeste 53.30432018130313
# Noreste 16.372330087428317
# Noroeste 22.995551622572098
# Sureste 22.936762369857096

# en este caso no conviene abrir mas en aquellas zonas donde hay mayor cobertura, en este caso en centro y en centro-oeste. sin embargo, podemos decir que hay 3 zonas de vital importancia que son noreste, noroeste y sureste que estan vacias comparadas con las anteriores. Eso se debe principalmente a que el terreno de esos estados es inmenso entonces abarcar 120 000 km en michoacan es mucho mas completo que en chihuahua por ejemplo. en el sur hay zonas que simplemente no estan muy desarrolladas entonces el envio a domicilio no se ve como algo mas del diario como en zonas mas desarrolladas entonces quizas no haga falta tener en una planificacion a mediano plazo al menos que haya un plan de desarrollo urbano en la zona de interes, sin embargo esos proyectos suelen ser a muy largo plazo, con la llegada de las nuevas generaciones de familias o con el crecimiento de la poblacion y no podemos analizar estas variables por lo que simplemente quedaria la opcion mas segura, de simplemente no tener planes en la zona geografica