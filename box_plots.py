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

df["estimador1"] = df["estimador1"] - df["true_mi"]
df["estimador2"] = df["estimador2"] - df["true_mi"]
df["estimador3"] = df["estimador3"] - df["true_mi"]

criterio = ["capas", "neuronas", "rho", "samples"]

# Separacion de los datos de cada estimador
df_est1 = df[["last_epoch", "estimador1", "estimador1_epoca"] + criterio]
df_est2 = df[["last_epoch", "estimador2", "estimador2_epoca"] + criterio]
df_est3 = df[["last_epoch", "estimador3", "estimador3_epoca"] + criterio]

df_est1.rename(columns={"estimador1_epoca": "epoca_est"}, inplace=True)
df_est2.rename(columns={"estimador2_epoca": "epoca_est"}, inplace=True)
df_est3.rename(columns={"estimador3_epoca": "epoca_est"}, inplace=True)

df_est1 = df_est1.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="error")
df_est2 = df_est2.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="error")
df_est3 = df_est3.melt(id_vars=["last_epoch", "epoca_est"] + criterio, var_name="estimador", value_name="error")

df_estimations = pd.concat([df_est1, df_est2, df_est3])

sns.set_style('darkgrid')
sns.set_palette('Set2')


fig, axs = plt.subplots(3, 3, sharey=True, sharex=True)

capas = df_estimations["capas"].unique()
neuronas = df_estimations["neuronas"].unique()
rhos = df_estimations["rho"].unique()
RHO = rhos[2]


for i, ax in enumerate(axs.flatten()):
    CAPAS = capas[i % 3]
    NEURONAS = neuronas[i // 3]
    df_aux = df_estimations.loc[df_estimations["rho"] == RHO]
    df_aux = df_aux.loc[df_aux["capas"] == CAPAS]
    df_aux = df_aux.loc[df_aux["neuronas"] == NEURONAS]
    sns.boxplot(data=df_aux, x="samples", y='error',
                hue="estimador",
                ax=ax)
    ax.set_title(f"{CAPAS} capas de {NEURONAS} neuronas")
fig.suptitle(f"Resultados para Rho {RHO}", fontsize=20)
plt.show()

# sns.boxplot(data=df, x='day', y='tip')
# plt.show()

# Kernel density estimate
sns.kdeplot(
    data=df_estimations, x="error", hue="estimador",
    palette=sns.color_palette("hls", 3)
)
plt.title("Desempeño según estimador")

