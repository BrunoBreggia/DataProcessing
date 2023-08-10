import pandas as pd
import csv
import os


def dataframe_from_directory(dirname: str) -> pd.DataFrame:
    """
    Funcion que recibe el nombre de un directorio con los resultados de la
    simulacion en archivos csv, y devuelve un DataFrame con todos los datos
    contenidos en ese directorio.
    :param dirname: nombre el directorio con los archivos de la simulacion
    :return: DataFrame con los datos de todos los archivos en el directorio
    """
    # Creo lista con los nombres de los archivos csv
    data_filenames = os.listdir(dirname)
    # Ordeno los archivos antes de leerlos
    data_filenames = sorted(data_filenames)
    # print(data_filenames)

    lista_df = []  # lista para contener los dataframes

    for archi in data_filenames:
        # Creo un dataframe por archivo
        lista_df.append(pd.read_csv(dirname + archi))

    # Genero un gran dataframe con la informacion de todos los archivos
    total_data = pd.concat(lista_df, ignore_index=True)
    return total_data


if __name__ == '__main__':
    global_data = dataframe_from_directory("ResultadoSimulacion/sim04/")
    global_data.to_csv("sim04_data.csv")




