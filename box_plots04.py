import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})

# Read data from sim04 file
df = pd.read_csv("sim04_data.csv")

# Create one columns with foot-angle side combination
df["foot-angle"] = df["foot"] + '-' + df["angle_side"]

criterio = ["capas", "neuronas", "ciclo", "foot-angle", "angle_description"]

# Separacion de los datos de cada estimador
df_est1 = df[["last_epoch", "estimador1", "estimador1_epoca"] + criterio]
df_est2 = df[["last_epoch", "estimador2", "estimador2_epoca"] + criterio]
df_est3 = df[["last_epoch", "estimador3", "estimador3_epoca"] + criterio]

df_est1.rename(columns={"estimador1_epoca": "epoca_est"}, inplace=True)
df_est2.rename(columns={"estimador2_epoca": "epoca_est"}, inplace=True)
df_est3.rename(columns={"estimador3_epoca": "epoca_est"}, inplace=True)

df_est1 = df_est1.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="estimacion")
df_est2 = df_est2.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="estimacion")
df_est3 = df_est3.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="estimacion")

df_estimations = pd.concat([df_est1, df_est2, df_est3])

sns.set_style('darkgrid')
# sns.set_palette('Set2')

fig, axs = plt.subplots(1, 1, sharey=True, sharex=True)

capas = df_estimations["capas"].unique()
neuronas = df_estimations["neuronas"].unique()
CICLO = "full"

# one graph only
df_aux = df_estimations.loc[df_estimations["ciclo"] == CICLO]
df_aux = df_aux.loc[df_aux["capas"] == 3]
df_aux = df_aux.loc[df_aux["neuronas"] == 50]
df_aux["estimator 2"] = df_aux[df_aux["estimador"] == "estimador2"]["estimacion"]
sns.boxplot(data=df_aux, x="foot-angle", y='estimator 2', color=sns.color_palette("Set2", 2)[1])
plt.grid()

# for i, ax in enumerate(axs.flatten()):
#     CAPAS = capas[i % 3]
#     NEURONAS = neuronas[i // 3]
#     df_aux = df_estimations.loc[df_estimations["ciclo"] == CICLO]
#     df_aux = df_aux.loc[df_aux["capas"] == CAPAS]
#     df_aux = df_aux.loc[df_aux["neuronas"] == NEURONAS]
#     sns.boxplot(data=df_aux, x="foot-angle", y='estimacion',
#                 hue="estimador",
#                 ax=ax)
#     ax.set_title(f"{CAPAS} capas de {NEURONAS} neuronas")
#     ax.grid()

fig.suptitle(f"Resultados para ciclo {CICLO}", fontsize=20)
plt.subplots_adjust(left=0.15)
plt.show()




