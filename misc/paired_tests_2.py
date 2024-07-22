import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Función para realizar el emparejamiento por puntaje de propensión
def propensity_matching(X, treat):
    X_subset = X[['age', 'sex']]
    X_subset = pd.get_dummies(X_subset, columns=['sex'])
    model = LogisticRegression()
    model.fit(X_subset, treat)
    prop_scores = model.predict_proba(X_subset)[:, 1]
    print("Propensity scores:", prop_scores)
    return prop_scores

def separate_propensity_scores(data, prop_scores, group1='G1', group2='Control'):
    # Separar los datos en grupos G1 y Control
    g1_data = data[data['group'] == group1]
    g2_data = data[data['group'] == group2]
    
    # Asignar los puntajes de propensión correspondientes a cada grupo
    g1_prop_scores = prop_scores[data['group'] == group1]
    g2_prop_scores = prop_scores[data['group'] == group2]
    
    print(f"Propensity scores for {group1}:", g1_prop_scores)
    print(f"Propensity scores for {group2}:", g2_prop_scores)
    
    return g1_prop_scores, g2_prop_scores

def remove_excess_g1(g1_data, g1_prop_scores, target_g1_count):
    # Obtener los índices ordenados por puntaje de propensión ascendente
    sorted_g1_indices = g1_data.index[g1_prop_scores.argsort()]
    
    # Determinar los índices a eliminar (los más bajos)
    indices_to_remove = sorted_g1_indices[:len(g1_data) - target_g1_count]
    
    # Eliminar las filas no deseadas y restablecer el índice en g1_data
    g1_data = g1_data.drop(indices_to_remove).reset_index(drop=True)
    
    return g1_data

def match_and_optimize(data, group1='G1', group2='Control',ratio=79):
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group'].replace({group1: 'Treat', group2: 'Control'})
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]
    # Separar los datos en X, y, y treat según los grupos especificados
    X = data.drop(columns=['group'])
    treat = (data['group'] == group1).astype(int)
    g2_data = data[data['group'] == group2]
    
    # Realizar el emparejamiento por puntaje de propensión
    prop_scores = propensity_matching(X, treat)
    
    # Separar los puntajes de propensión por grupo
    g1_prop_scores, g2_prop_scores = separate_propensity_scores(data, prop_scores, group1, group2)
    
    # Determinar el objetivo de cuántos sujetos de G1 deben permanecer
    target_g1_count = ratio
    #g2_count = len(g2_prop_scores)

    print("Cantidad de sujetos en el grupo G1 antes de eliminar:", len(g1_prop_scores))
    print("Cantidad de sujetos en el grupo Control:", len(g2_data))
    
    # Eliminar los sujetos de G1 con los puntajes de propensión más bajos para cumplir con el objetivo
    g1_data = data[data['group'] == 'G1']
    g1_data = remove_excess_g1(g1_data, g1_prop_scores, target_g1_count)
    
    # Combinar g1_data con los datos de control
    #g2_data = data[data['group'] == group2].reset_index(drop=True)
    data_MatchIt = pd.concat([g1_data, g2_data]).reset_index(drop=True)
    data_MatchIt = data_MatchIt.drop(['treatG1'], axis=1)

    print("Cantidad de sujetos en el grupo G1 después de eliminar:", len(g1_data))
    print("Cantidad de sujetos en el grupo Control después de eliminar:", len(g2_data))
    
    return data_MatchIt

# Ejemplo de uso (asegúrate de tener tu DataFrame 'data' preparado)
# data_MatchIt = match_and_optimize(data, group1='G1', group2='Control')






