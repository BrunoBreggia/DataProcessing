import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def eliminate_columns(data_frame: pd.DataFrame, columns: list):
    data_frame = data_frame.copy()
    for col in columns:
        del data_frame[col]
    return data_frame


def filter_df(data_frame: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    for k, v in criteria.items():
        data_frame = data_frame[data_frame[k] == v]
    return data_frame


if __name__ == "__main__":
    global_data = pd.read_csv("global_data.csv")

    ##############

    estadisticos = {
            "training_mean", "testing_mean",
            "training_med", "testing_med",
            "training_var", "testing_var",
            "training_std", "testing_std",
            "training_max", "testing_max",
            "training_min", "testing_min",
    }

    fields_of_interest = {
        "testing_mean", "testing_std",
    }

    for mine in global_data["mine"].unique():
        plotting_data = eliminate_columns(global_data, list(estadisticos.difference(fields_of_interest)))

        plotting_data.rename(columns={'testing_mean': 'mean', "testing_std": "std"}, inplace=True)
        plotting_data["difference"] = plotting_data["mean"] - plotting_data["im_verdadera"]

        ################

        sns.set_theme()

        # for rho in plotting_data["rho"].unique():
        plotting_data = filter_df(plotting_data,
                                  {"epoca": 2048,
                                   "muestras": 2 ** 14,
                                   # "capas": 5,
                                   "neuronas": 200,
                                   # "rho": rho,
                                   "mine": mine,
                                   })

        sns.relplot(
            data=plotting_data, x="difference", y="std", hue="activacion", size="batch"
        )

        plt.title(f"Red con {mine}")

    plt.show()
