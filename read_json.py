import json
import pandas as pd
import numpy as np

# Lectura de prueba de un archivo json

filename = 'sim01_C0_T0_R0.json'

with open(filename, 'r') as jsonFile:
    content = json.load(jsonFile)
    # content is a dictionary

params_df = pd.DataFrame.from_dict([content['params']])
data_df = pd.DataFrame.from_dict(content['data'])
# create pandas dataframes

# print(  data_df)
# print(params_df)

# data_df['training_mean'] = 0
# data_df['testing_mean'] = 0

# Agrego datos del json de parametros
data_df['capas'] = params_df['capa'].get(0)
data_df['tipo'] = params_df['tipo'].get(0)
# data_df['data_rho'] = params_df['data_rho'].get(0)
data_df['realizaciones'] = params_df['realizaciones'].get(0)
data_df['seed'] = params_df['seed'].get(0)
data_df['data_mu'] = [params_df['data_mu'].get(0)]*len(data_df)

# Agrego datos de tendencia central de las realizaciones
data_df['training_mean'] = [np.mean(values) for values in data_df['im_entrenamiento']]
data_df['testing_mean'] = [np.mean(values) for values in data_df['im_testeo']]
data_df['training_median'] = [np.median(values) for values in data_df['im_entrenamiento']]
data_df['testing_median'] = [np.median(values) for values in data_df['im_testeo']]

# Agrego datos de dispersion de las realizaciones
data_df['training_variance'] = [np.var(values) for values in data_df['im_entrenamiento']]
data_df['testing_variance'] = [np.var(values) for values in data_df['im_testeo']]
data_df['training_max'] = [np.max(values) for values in data_df['im_entrenamiento']]
data_df['testing_max'] = [np.max(values) for values in data_df['im_testeo']]
data_df['training_min'] = [np.min(values) for values in data_df['im_entrenamiento']]
data_df['testing_min'] = [np.min(values) for values in data_df['im_testeo']]

# Extraidos los datos estadisticos de las realizaciones, las elimino
del data_df['im_entrenamiento']
del data_df['im_testeo']

