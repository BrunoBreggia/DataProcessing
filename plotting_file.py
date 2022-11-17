import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def eliminate_columns(data_frame: pd.DataFrame, columns: list):
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


def plot_data(df, ax):
    palette = sns.color_palette("hls", 8)
    parameters_dict = {
        "data": df,
        "x": "epoca",
        "y": "mean",
        "hue": "phase",
        "ax": ax,
        'palette': palette,
    }
    sns.boxplot(**parameters_dict)
    # sns.stripplot(
    #     **parameters_dict,
    #     # palette=sns.color_palette(),
    #     dodge=True,
    #     alpha=0.6,
    #     ec='k',
    #     linewidth=1,
    # )
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2])


if __name__ == "__main__":
    global_data = pd.read_csv("global_data.csv")

    estadisticos = {
        "training_mean",
        "testing_mean",
        "training_med",
        "testing_med",
        "training_var",
        "testing_var",
        "training_std",
        "testing_std",
        "training_max",
        "testing_max",
        "training_min",
        "testing_min",
    }

    # a continuacion descomentar lo que se desea graficar
    plotting_fields = {
        "training_mean",
        "testing_mean",
        # "training_med",
        # "testing_med",
        # "training_var",
        # "testing_var",
        # "training_std",
        # "testing_std",
        # "training_max",
        # "testing_max",
        # "training_min",
        # "testing_min",
    }
    global_data = eliminate_columns(global_data, list(estadisticos.difference(plotting_fields)))

    fig, axs = plt.subplots(2, 3, sharey=True, sharex=True)

    for ax, muestras in zip(axs.flat, global_data["muestras"].unique()):
        criteria = {
            "rho": 0,
            "muestras": muestras,
        }
        plotting_data = filter_df(global_data, criteria)
        plotting_data = melting(plotting_data, list(plotting_fields),
                              "phase", "mean")
        plot_data(plotting_data, ax)

    plt.show()





