import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')
print(df.head())

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

# Create dataframe only with simulation parameters
param_columns = list(df.columns[:-6])
param_columns.pop(0)  # remove index column
param_columns.remove("last_epoch")

sim_parameters = df[param_columns].drop_duplicates()  # left with 324 entries

# Create dataframe with simulation results
result_columns = list(df.keys())
result_columns.pop(0)  # remove index column
[result_columns.remove(i) for i in param_columns]
sim_results = df[result_columns]

# Separacion de los datos de cada estimador
df_est1 = sim_results[["last_epoch", "estimador1", "estimador1_epoca"]]
df_est2 = sim_results[["last_epoch", "estimador2", "estimador2_epoca"]]
df_est3 = sim_results[["last_epoch", "estimador3", "estimador3_epoca"]]

df_est1.rename(columns={"estimador1_epoca": "epoca_est"}, inplace=True)
df_est2.rename(columns={"estimador2_epoca": "epoca_est"}, inplace=True)
df_est3.rename(columns={"estimador3_epoca": "epoca_est"}, inplace=True)

df_est1 = df_est1.melt(id_vars=["last_epoch", "epoca_est"], var_name="estimador")
df_est2 = df_est2.melt(id_vars=["last_epoch", "epoca_est"], var_name="estimador")
df_est3 = df_est3.melt(id_vars=["last_epoch", "epoca_est"], var_name="estimador")

df_estimations = pd.concat([df_est1, df_est2, df_est3])

# sns.boxplot(data=df_estimations, x='estimador', y='value')
# sns.boxplot(data=df, x='day', y='tip')
# plt.show()
