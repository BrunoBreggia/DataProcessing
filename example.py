import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def filter_df(data_frame: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    for k, v in criteria.items():
        data_frame = data_frame[data_frame[k] == v]
    return data_frame


global_data = pd.read_csv("global_data.csv")
global_data["difference"] = global_data["testing_mean"] - global_data["im_verdadera"]
global_data = filter_df(global_data, {"epoca": 2048, "muestras": 2**14})

sns.set_theme()

tags = ["capas", "neuronas", "batch", "mine", "rho"]

for tag in tags:
    sns.catplot(
        data=global_data, x="activacion", y="difference", hue=tag,
    )


plt.show()
