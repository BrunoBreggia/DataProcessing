import json
import pandas as pd
import numpy as np
import os


def dataframe_assembly(filename: str) -> pd.DataFrame:
    """
    Funcion que recibe nombre de archivo json y devuelve dataframe con
    los datos de las simulaciones y los parametros estadisticos del conjunto de
    sus realizaciones

    :param filename: nombre del archivo json
    :return: DataFrame
    """

    with open(filename, 'r') as jsonFile:
        content = json.load(jsonFile)
        # content is a dictionary

    # create pandas dataframes
    params_df = pd.DataFrame.from_dict([content['params']])
    data_df = pd.DataFrame.from_dict(content['data'])

    # Agrego datos del json de parametros
    data_df['capas'] = params_df['capa'].get(0)
    data_df['tipo'] = params_df['tipo'].get(0)
    data_df['realizaciones'] = params_df['realizaciones'].get(0)
    data_df['seed'] = params_df['seed'].get(0)
    data_df['data_mu'] = [params_df['data_mu'].get(0)] * len(data_df)

    # Agrego datos de tendencia central de las realizaciones
    data_df['training_mean'] = [np.mean(values) for values in data_df['im_entrenamiento']]
    data_df['testing_mean'] = [np.mean(values) for values in data_df['im_testeo']]
    data_df['training_med'] = [np.median(values) for values in data_df['im_entrenamiento']]
    data_df['testing_med'] = [np.median(values) for values in data_df['im_testeo']]

    # Agrego datos de dispersion de las realizaciones
    data_df['training_var'] = [np.var(values) for values in data_df['im_entrenamiento']]
    data_df['testing_var'] = [np.var(values) for values in data_df['im_testeo']]
    data_df['training_std'] = np.sqrt(data_df['training_var'])
    data_df['testing_std'] = np.sqrt(data_df['testing_var'])
    data_df['training_max'] = [np.max(values) for values in data_df['im_entrenamiento']]
    data_df['testing_max'] = [np.max(values) for values in data_df['im_testeo']]
    data_df['training_min'] = [np.min(values) for values in data_df['im_entrenamiento']]
    data_df['testing_min'] = [np.min(values) for values in data_df['im_testeo']]

    # Extraidos los datos estadisticos de las realizaciones, las elimino
    del data_df['im_entrenamiento']
    del data_df['im_testeo']

    return data_df


def dataframe_from_directory(dirname:str):
    """
    Funcion que recibe el nombre de un directorio con los resultados de la
    simulacion en archivos json, y devuelve un DataFrame con todos los datos
    contenidos en ese directorio.
    :param dirname: nombre el directorio con los archivos de la simulacion
    :return: DataFrame con los datos de todos los archivos en el directorio
    """
    # Creo lista con los nombres de los archivos json
    data_filenames: list = os.listdir(dirname)
    # Ordeno los archivos antes de leerlos
    data_filenames = sorted(data_filenames)
    # print(data_filenames)

    lista_df = []  # lista para contener los dataframes

    for archi in data_filenames:
        # Creo un dataframe por archivo
        lista_df.append(dataframe_assembly(dirname + archi))

    # Genero un gran dataframe con la informacion de todos los archivos
    total_data = pd.concat(lista_df, ignore_index=True)
    return total_data


if __name__ == '__main__':
    # data = dataframe_assembly("ResultadoSimulacion/sim01/sim01_C0_T0_R0.json")
    global_data = dataframe_from_directory("ResultadoSimulacion/sim01/")
    global_data.to_csv("global_data.csv")









