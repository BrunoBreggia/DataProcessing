import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')
# print(df.head())

"""
sns.boxplot(x=None, y=None,
            hue=None,  # data to use to break your data by break
            data=None,  # DataFrame to use for your data
            order=None,  # how to order your data
            hue_order=None,  # similar to order, represents how to order your data
            orient=None,  # indicates whether data should be horizontal or vertical
            color=None,  # color(s) to use
            palette=None,  # pallette to use
            saturation=0.75,  # saturation of the color
            width=0.8,  # width of an element
            dodge=True,  # hue nesting is used, how to shift categorical data
            fliersize=5,  # size of the markers for outliers
            linewidth=None,  # width of the lines in the graph
            whis=1.5,  # proportion of the interquartile range to extend the plot whiskers
            ax=None  # axes object to draw on
            )
"""

# Read data from sim03 file
df = pd.read_csv("sim03_data.csv")

df["estimator 1"] = df["estimador1"] - df["true_mi"]
df["estimator 2"] = df["estimador2"] - df["true_mi"]
df["estimator 3"] = df["estimador3"] - df["true_mi"]

criterio = ["capas", "neuronas", "rho", "samples", "funcion_activacion"]

# Separacion de los datos de cada estimador
df_est1 = df[["last_epoch", "estimator 1", "estimador1_epoca"] + criterio]
df_est2 = df[["last_epoch", "estimator 2", "estimador2_epoca"] + criterio]
df_est3 = df[["last_epoch", "estimator 3", "estimador3_epoca"] + criterio]

df_est1.rename(columns={"estimador1_epoca": "epoca_est"}, inplace=True)
df_est2.rename(columns={"estimador2_epoca": "epoca_est"}, inplace=True)
df_est3.rename(columns={"estimador3_epoca": "epoca_est"}, inplace=True)

df_est1 = df_est1.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimator", value_name="error")
df_est2 = df_est2.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimator", value_name="error")
df_est3 = df_est3.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimator", value_name="error")

df_estimations = pd.concat([df_est1, df_est2, df_est3])

sns.set_style('darkgrid')
sns.set_palette('Set2')


fig, axs = plt.subplots(1, 1, sharey=True, sharex=True)

capas = df_estimations["capas"].unique()
neuronas = df_estimations["neuronas"].unique()
rhos = df_estimations["rho"].unique()
RHO = rhos[1]

# one graph only
df_aux = df_estimations.loc[df_estimations["rho"] == RHO]
df_aux = df_aux.loc[df_aux["capas"] == 3]
df_aux = df_aux.loc[df_aux["neuronas"] == 50]
sns.boxplot(data=df_aux, x="samples", y='error',
            hue="estimator")

#
# for i, ax in enumerate(axs.flatten()):
#     CAPAS = capas[i % 3]
#     NEURONAS = neuronas[i // 3]
#     df_aux = df_estimations.loc[df_estimations["rho"] == RHO]
#     df_aux = df_aux.loc[df_aux["capas"] == CAPAS]
#     df_aux = df_aux.loc[df_aux["neuronas"] == NEURONAS]
#     sns.boxplot(data=df_aux, x="funcion_activacion", y='error',
#                 hue="estimador",
#                 ax=ax)
#     ax.set_title(f"{CAPAS} capas de {NEURONAS} neuronas")

fig.suptitle(f"Results for Rho {RHO}", fontsize=20)
plt.show()

# sns.boxplot(data=df, x='day', y='tip')
# plt.show()

# Kernel density estimate
# sns.kdeplot(
#     data=df_estimations.loc[df_estimations["estimator"] == "estimador2"],
#     x="error", hue="samples",
#     palette=sns.color_palette("hls", 4)
# )
# plt.title("Desempeño según cantidad de muestras")

