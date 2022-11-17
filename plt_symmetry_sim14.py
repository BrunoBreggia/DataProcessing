#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import product

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import colors
from statannotations.Annotator import Annotator

sns.set_theme(style="ticks", palette="tab10", context='notebook')
# sns.set_theme(style="ticks", palette="tab10")
DATA_PATH = "/media/Datos/toeMine/sims/sim14"
DATA_PATH_ZEUS = "/media/jrestrepo/Datos/toeMine/sims/sim14"
ROOT_SIMDIR = '/home/jrestrepo/Dropbox/inv/toeMine/sims/sim14'
CVS_ROOT_PATH = f'{ROOT_SIMDIR}/jamovi_sim14/mixed_stat_test'
df_columns = [
    'protesis', 'cycle', 'subject', 'plane', 'angle', 'foot_angle', 'mi'
]
yLim = [-0.01, 1.6]


def read_df_():

    fname = f"{DATA_PATH}/sim14_compiledData.json"
    # fname = f"{DATA_PATH_ZEUS}/sim14_compiledData.json"
    df = pd.read_json(fname, orient="index")

    # filtrar datos
    df = df[df_columns]

    return df


def parse_pvals(cvs_file, pairs):

    # angles = list(df['angle'].unique())
    # pairs = [((f'{an}', 'A-A'), (f'{an}', 'S-S')) for an in angles]
    csv_df = pd.read_csv(cvs_file, delimiter='\t')

    keys = list(csv_df.keys())
    keys.remove(" ")
    new_keys = [
        'angle1', 'foot_angle1', 'angle2', 'foot_angle2', 'Difference', 'SE',
        't', 'df', 'pbonferroni', 'pholm'
    ]

    for old_key, new_key in zip(keys, new_keys):
        csv_df = csv_df.rename(columns={old_key: new_key})

    csv_df['angle1'] = csv_df['angle1'].str.strip()
    csv_df['foot_angle1'] = csv_df['foot_angle1'].str.strip()
    csv_df['angle2'] = csv_df['angle2'].str.strip()
    csv_df['foot_angle2'] = csv_df['foot_angle2'].str.strip()
    try:
        csv_df['pholm'] = csv_df['pholm'].str.strip()
        csv_df.loc[csv_df['pholm'].isin(['< .001']), 'pholm'] = '0.0009'
    except:
        pass

    csv_df['pholm'] = pd.to_numeric(csv_df['pholm'])

    pvals = []
    for pair in pairs:
        (a1, fa1), (a2, fa2) = pair

        temp = csv_df[(csv_df['angle1'] == a2) & (csv_df['angle2'] == a1) &
                      (csv_df['foot_angle1'] == fa1) &
                      (csv_df['foot_angle2'] == fa2)]

        pvals.append(temp['pholm'].to_numpy()[0])
        pass

    return pvals


def plot_simetry(df, protesis, cycle, plane, side, ax):

    df = df[(df['protesis'] == protesis) & (df['cycle'] == cycle) &
            (df['plane'] == plane)]
    angles = list(df['angle'].unique())
    if side == 'same':
        side = ['A-A', 'S-S']
        pairs = [((f'{an}', 'A-A'), (f'{an}', 'S-S')) for an in angles]
        # palette = sns.color_palette("cubehelix", 4)[0:2]
        palette = sns.color_palette()[0:2]
    else:
        side = ['A-S', 'S-A']
        pairs = [((f'{an}', 'A-S'), (f'{an}', 'S-A')) for an in angles]
        palette = sns.color_palette()[2:4]

    df = df[df['foot_angle'].isin(side)]

    plot_parameters = {
        "data": df,
        "x": "angle",
        "y": "mi",
        "hue": "foot_angle",
        "hue_order": side,
        # "hue_order": side,
        "ax": ax,
        # 'boxprops': {
        #     'alpha': 0.4
        # }
        # "palette": palette,
        # "width": 0.5,
        'palette': palette,
    }
    sns.boxplot(**plot_parameters)
    sns.stripplot(
        **plot_parameters,
        # palette=sns.color_palette(),
        dodge=True,
        alpha=0.6,
        ec='k',
        linewidth=1,
    )

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2])

    pvals_file = f'{CVS_ROOT_PATH}/{protesis.lower()}/{cycle}/mixed_{protesis.lower()}_{cycle}_{plane}.txt'
    pvals = parse_pvals(pvals_file, pairs)

    annotator = (
        Annotator(pairs=pairs, **plot_parameters).configure(
            test=None,
            # comparisons_correction="Holm-Bonferroni",
            # text_format="simple",
            text_format="star",
            loc="inside",
        ).set_pvalues(pvalues=pvals).annotate())
    ax.set_ylim(yLim)


if __name__ == "__main__":
    df = read_df_()

    protesis = 'Ech'
    cycle = ['stance_nods', 'stance', 'swing', 'full']
    for c in cycle:
        fig, axs = plt.subplots(2, 2, sharey=True)
        plot_simetry(df, protesis, c, 'frontal', 'same', axs[0, 0])
        plot_simetry(df, protesis, c, 'sagital', 'same', axs[1, 0])
        plot_simetry(df, protesis, c, 'frontal', 'contra', axs[0, 1])
        plot_simetry(df, protesis, c, 'sagital', 'contra', axs[1, 1])
        axs[0, 0].set_title("Same side")
        axs[0, 1].set_title("Contralateral side")
        axs[0, 0].set(xlabel="", ylabel="mi - frontal")
        axs[0, 1].set(xlabel="", ylabel="")
        axs[1, 1].set(ylabel="")
        axs[1, 0].set(ylabel="mi - sagital")
        axs[1, 0].legend([], [], frameon=False)
        axs[1, 1].legend([], [], frameon=False)
        fig.suptitle(f"All subjects- Ech - {c} cycle")
        plt.gcf().set_size_inches(10, 10)
        plt.tight_layout()
        fname = f'{ROOT_SIMDIR}/symmetry/symmetry-{protesis.lower()}-{c}.pdf'
        # fig.savefig(fname, dpi=350)
    plt.show()
    pass
