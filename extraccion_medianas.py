import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from df_assembly01 import dataframe_assembly

RUTA_SIM = "../SimulacionMine/sim06_nwEv/"
ARCHI_MEDIANAS = "sim06_data.csv"


def dataframe_from_directory(dirname: str):
    """
    Funcion que recibe el nombre de un directorio con los resultados de la
    simulacion en archivos json, y devuelve un DataFrame con todos los datos
    contenidos en ese directorio.
    :param dirname: nombre el directorio con los archivos de la simulacion
    :return: DataFrame con los datos de todos los archivos en el directorio
    """
    # Creo lista con los nombres de los subdirectorios de la simulacion
    data_subdirs: list = os.listdir(dirname)
    # Ordeno los subdirs antes de leerlos
    data_subdirs = sorted(data_subdirs)
    # print(data_filenames)

    lista_df = []  # lista para contener los dataframes

    for subdir in data_subdirs:

        # Creo lista con los nombres de los archivos json
        data_filenames: list = os.listdir(dirname + "outData/" + subdir)
        # Ordeno los archivos antes de leerlos
        data_filenames = sorted(data_filenames)

        for archi in data_filenames:
            # Creo un dataframe por archivo
            lista_df.append(dataframe_assembly(dirname + archi))

    # Genero un gran dataframe con la informacion de todos los archivos
    total_data = pd.concat(lista_df, ignore_index=True)
    return total_data


# Create sim06 file
df = dataframe_from_directory(RUTA_SIM)
df.to_csv(ARCHI_MEDIANAS)

"""
# Read data from sim06 file
# df = pd.read_csv(ARCHI_MEDIANAS)

# Create one column with foot-angle side combination
df["foot-angle"] = df["foot"] + '-' + df["angle_side"]
df["combination"] = df["foot"] + "toe" + '-' + df["angle_side"] + df["angle_description"]

criterio = ["ciclo", "sujeto", "foot", "angle_description", "angle_side",
            "estimador2", "foot-angle", "combination"]
df = df[criterio]

df.rename(columns={"angle_description": "angle_name",
                   "foot": "foot_side",
                   "estimador2": "estimacion"},
          inplace=True)

df_datos = {
    "sujeto": [],
    "lados": [],
    "angulo": [],
    "combinacion": [],
    "mediana": [],
    "ciclo": []
}

df_datos = pd.DataFrame(df_datos)

sujetos = df["sujeto"].unique()
combinaciones = df["combination"].unique()
ciclos = df["ciclo"].unique()

for suj, comb, cic in product(sujetos, combinaciones, ciclos):
    df_temporal = df[(df["sujeto"] == suj) & (df["combination"] == comb) & (df["ciclo"] == cic)]
    if len(df_temporal) > 0:
        df_datos.loc[len(df_datos)] = [suj,
                                       df_temporal["foot-angle"].unique()[0],
                                       df_temporal["angle_name"].unique()[0],
                                       comb,
                                       df_temporal["estimacion"].median(),
                                       df_temporal["ciclo"].unique()[0]
                                       ]
df_datos.to_csv("sim06_medianas_realizaciones.csv")

# Graficacion particular
fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
CICLO = ["full", "swing", "stance", "nods"][0]  # cambiar este indice para probar con cada ciclo
df_aux = df_datos[df_datos["ciclo"] == CICLO]

# colaterales
sns.boxplot(data=df_aux[(df_aux["lados"] == "R-R") | (df_aux["lados"] == "L-L")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[0])

# contralaterales
sns.boxplot(data=df_aux[(df_aux["lados"] == "R-L") | (df_aux["lados"] == "L-R")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[1])

fig.suptitle(f"Resultados para ciclo {CICLO}", fontsize=20)
axs[0].grid()
axs[1].grid()
plt.show()
"""
