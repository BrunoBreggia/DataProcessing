import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def read_dataframe_simulacion(datafile):
    # Read data from sim03 file
    df = pd.read_csv(datafile)

    df.rename(columns={"samples": "muestras"}, inplace=True)

    df["estimador 1"] = df["estimador1"] - df["true_mi"]
    df["estimador 2"] = df["estimador2"] - df["true_mi"]
    df["estimador 3"] = df["estimador3"] - df["true_mi"]

    criterio = ["capas", "neuronas", "rho", "muestras", "funcion_activacion"]

    # Separacion de los datos de cada estimador
    df_est1 = df[["last_epoch", "estimador 1", "estimador1_epoca"] + criterio]
    df_est2 = df[["last_epoch", "estimador 2", "estimador2_epoca"] + criterio]
    df_est3 = df[["last_epoch", "estimador 3", "estimador3_epoca"] + criterio]

    df_est1.rename(columns={"estimador1_epoca": "epoca"}, inplace=True)
    df_est2.rename(columns={"estimador2_epoca": "epoca"}, inplace=True)
    df_est3.rename(columns={"estimador3_epoca": "epoca"}, inplace=True)

    df_est1 = df_est1.melt(id_vars=["last_epoch", "epoca"] + criterio, var_name="estimador", value_name="error")
    df_est2 = df_est2.melt(id_vars=["last_epoch", "epoca"] + criterio, var_name="estimador", value_name="error")
    df_est3 = df_est3.melt(id_vars=["last_epoch", "epoca"] + criterio, var_name="estimador", value_name="error")

    df_estimations = pd.concat([df_est1, df_est2, df_est3])

    return df_estimations


def boxplots_simulacion(datafile, rho, outfile=None):

    df_estimations = read_dataframe_simulacion(datafile)

    sns.set_style('darkgrid')
    sns.set_palette('Set2')

    plt.rcParams.update({'font.size': 10})
    fig, axs = plt.subplots(3, 3, sharey=True, sharex=True)
    fig.set_size_inches((12, 8))
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.95,
                        top=0.95,
                        wspace=0.2,
                        hspace=0.2)

    capas = df_estimations["capas"].unique()
    neuronas = df_estimations["neuronas"].unique()
    # rhos = df_estimations["rho"].unique()
    # RHO = rhos[0]

    # one graph only
    # df_aux = df_estimations.loc[df_estimations["rho"] == RHO]
    # df_aux = df_aux.loc[df_aux["capas"] == 3]
    # df_aux = df_aux.loc[df_aux["neuronas"] == 50]
    # sns.boxplot(data=df_aux, x="samples", y='error',
    #             hue="estimator")
    # plt.legend(loc="upper right", prop={'size': 14})
    # plt.setp(axs.get_xticklabels(), fontsize=14)
    # plt.setp(axs.get_yticklabels(), fontsize=14)
    plt.subplots_adjust(left=0.15)

    for i, ax in enumerate(axs.flatten()):
        fil = i // 3
        col = i % 3

        CAPAS = capas[col]
        NEURONAS = neuronas[fil]
        df_aux = df_estimations.loc[df_estimations["rho"] == rho]
        df_aux = df_aux.loc[df_aux["capas"] == CAPAS]
        df_aux = df_aux.loc[df_aux["neuronas"] == NEURONAS]
        sns.boxplot(data=df_aux, x="muestras", y='error',
                    hue="estimador",
                    ax=ax)
        ax.set_title(f"{CAPAS} capas de {NEURONAS} neuronas")

        if fil != 2:
            ax.set(xlabel=None)

        if col != 0:
            ax.set(ylabel=None)

        if not (fil == 2 and col == 2):
            ax.get_legend().set_visible(False)

    # fig.suptitle(f"Results for Rho {RHO}", fontsize=20)
    plt.tight_layout()

    if outfile:
        plt.savefig(outfile)
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":

    filename = "sim03_data.csv"
    RHO = 0.0
    outputfile = f"../Documento Final/figuras resultados/simulacion_rho_{RHO}.pdf"
    boxplots_simulacion(filename, RHO, outputfile)
