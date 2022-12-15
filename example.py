import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def filter_df(data_frame: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    for k, v in criteria.items():
        data_frame = data_frame[data_frame[k] == v]
    return data_frame


if __name__ == "__main__":

    global_data = pd.read_csv("global_data.csv")
    global_data["difference"] = global_data["testing_mean"] - global_data["im_verdadera"]

    sns.set_theme()
    # tags = ["batch"] # ["capas", "neuronas", "batch", "rho"]
    tags = ["batch", "capas", "epoca"]

    for mine in global_data["mine"].unique():
        plotting_data = filter_df(global_data,
                                  {
                                      # "epoca": 2048,
                                      # "muestras": 2 ** 14,
                                      "mine": mine,
                                      "activacion": "relu"
                                  })
        for tag in tags:
            sns.catplot(
                data=plotting_data,
                x="muestras",
                y="difference",
                hue=tag,
                col="rho",
                row="neuronas",
            )
            plt.suptitle(f"Red {mine}")

    plt.show()
