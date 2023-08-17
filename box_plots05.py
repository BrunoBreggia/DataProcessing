import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

# Read data from sim04 file
df = pd.read_csv("sim05_data.csv")

# Create one columns with foot-angle side combination
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
