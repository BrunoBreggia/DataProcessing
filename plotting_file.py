import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def eliminate_columns(data_frame: pd.DataFrame, columns: list):
    data_frame = data_frame.copy()
    for col in columns:
        del data_frame[col]
    return data_frame


def filter_df(data_frame: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    for k, v in criteria.items():
        data_frame = data_frame[data_frame[k] == v]
    return data_frame


def melting(original_df: pd.DataFrame, melting_fields: list,
            var_name=None, value_name=None) -> pd.DataFrame:

    remaining_keys = list(original_df.keys())
    for field in melting_fields:
        remaining_keys.remove(field)

    return pd.melt(original_df, id_vars=remaining_keys, value_vars=melting_fields,
                   var_name=var_name, value_name=value_name)


estadisticos = {
        "training_mean", "testing_mean",
        "training_med", "testing_med",
        "training_var", "testing_var",
        "training_std", "testing_std",
        "training_max", "testing_max",
        "training_min", "testing_min",
}


def plot_data_1(global_data, criteria, ax):

    # a continuacion descomentar lo que se desea graficar
    plotting_fields = {
        "training_mean", "testing_mean",
        # "training_med", "testing_med",
        # "training_var", "testing_var",
        # "training_std", "testing_std",
        # "training_max", "testing_max",
        # "training_min", "testing_min",
    }
    plotting_data = eliminate_columns(global_data, list(estadisticos.difference(plotting_fields)))

    plotting_data = filter_df(plotting_data, criteria)
    plotting_data = melting(plotting_data, list(plotting_fields),
                            "phase", "mean")
    plotting_data = plotting_data.replace(to_replace="training_mean", value="training")
    plotting_data = plotting_data.replace(to_replace="testing_mean", value="testing")
    plotting_data["mean_difference"] = plotting_data["mean"] - plotting_data["im_verdadera"]

    palette = sns.color_palette("hls", 8)
    parameters_dict = {
        "data": plotting_data,
        "x": "epoca",
        "y": "mean_difference",
        "hue": "phase",
        "ax": ax,
        'palette': palette,
    }
    sns.boxplot(**parameters_dict)

    ax.set_xlabel("epocas")
    ax.set_ylabel(f"Diferencia con la IM real")
    ax.set_title(f"{muestras} muestras")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2])


if __name__ == "__main__":
    global_data = pd.read_csv("global_data.csv")

    for rho in global_data["rho"].unique():
        fig, axs = plt.subplots(2, 3, sharey=True, sharex=True)

        # rho = 0
        for ax, muestras in zip(axs.flat, global_data["muestras"].unique()):
            criteria = {
                "rho": rho,
                "muestras": muestras,
            }
            plot_data_1(global_data, criteria, ax)
            ax.grid()

        fig.suptitle(f"Rho = {rho}")
    plt.show()






