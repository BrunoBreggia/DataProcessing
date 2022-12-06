import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

global_data = pd.read_csv("global_data.csv")
global_data["difference"] = global_data["testing_mean"] - global_data["im_verdadera"]

sns.set_theme()

fig, axs = plt.subplots(1, 3, sharey=True)
tags = ["neuronas", "activacion", "rho"]

for ax, tag in zip(axs.flat, tags):
    sns.catplot(
        data=global_data, x="capas", y="difference", hue=tag, ax=ax
    )

plt.show()
