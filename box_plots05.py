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

fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
CICLO = "swing"
df_datos = df_datos[df_datos["ciclo"] == CICLO]

# colaterales
sns.boxplot(data=df_datos[(df_datos["lados"] == "R-R") | (df_datos["lados"] == "L-L")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[0])

# contralaterales
sns.boxplot(data=df_datos[(df_datos["lados"] == "R-L") | (df_datos["lados"] == "L-R")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[1])

fig.suptitle(f"Resultados para ciclo {CICLO}", fontsize=20)
axs[0].grid()
axs[1].grid()
plt.show()
