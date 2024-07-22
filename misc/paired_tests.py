'''
2023

Authors:
    - Verónica Henao Isaza, veronica.henao@udea.edu.co
    - Jan Karlo Rodas Marín, jan.rodas@udea.edu.co
    - Luisa María Zapata Saldarriaga, luisazapatasaldarriaga@gmail.com
'''

# Data processing
import pandas as pd
import numpy as np
# Python to R conversion
import subprocess
import rpy2.robjects as robjects
# Configurar la página de códigos en UTF-8
subprocess.call('chcp 65001', shell=True)

# Configurar la codificación de caracteres en UTF-8 en R
robjects.r('Sys.setlocale("LC_ALL", "en_US.UTF-8")')

# Ahora puedes continuar con tu código para interactuar con R a través de rpy2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects.packages as rpackages
from rpy2.robjects import r
import rpy2.robjects as ro
from rpy2.robjects import globalenv
from rpy2.robjects.conversion import get_conversion
from rpy2 import rinterface as ri
from rpy2.robjects.vectors import StrVector

# Activar las conversiones automáticas entre pandas DataFrame y R DataFrame
pandas2ri.activate()

# Instalar paquetes necesarios en R
#utils = importr('utils')
#utils.chooseCRANmirror(ind=1)  # Seleccionar el espejo CRAN
#utils.install_packages(StrVector(['MatchIt', 'lmtest', 'sandwich','Matching']))

# Importar paquetes necesarios en R
MatchIt = importr('MatchIt')
Matching = importr('Matching')
lmtest = importr('lmtest')
sandwich = importr('sandwich')
optmatch = importr('optmatch')
ggplot2 = importr('ggplot2')
nnet = importr('nnet')
base = importr('base')
# Importar paquetes R necesarios
pandas2ri.activate()



#Abrir base de datos y asignar factoriales a las variables cualitativas

# Convert Python dataframe to R dataframe
def pd_to_R_V1(df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd_df = ro.conversion.py2rpy(df)
    # Create a variable name in R's global environment
    globalenv['R_data'] = r_from_pd_df

# Convert R dataframe to Python dataframe 
def R_to_pd_V1():
    R_data2 = r('''R_data2 <- rapply(EDADG12total, as.character, classes="factor", how="replace")''')
    R_data = pd.DataFrame([dict(R_data2.items())]) 
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r_df = ro.conversion.rpy2py(R_data.iloc[0])
        new_pd = pd.DataFrame(dict(pd_from_r_df.items()), columns=R_data.columns.values)   
        return new_pd

def R_to_pd_V2():
    # Obtener el objeto EDADG12total desde el espacio de R
    EDADG12total = ro.globalenv['EDADG12total']
    
    # Convertir objeto de datos de R a DataFrame de pandas
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_df = ro.conversion.rpy2py(EDADG12total)
    
    return pd_df

def R_to_pd_V3():
    # Obtener el objeto EDADG12total desde el espacio de R
    EDADG12total = ro.globalenv['matched_data']
    
    # Convertir objeto de datos de R a DataFrame de pandas
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_df = ro.conversion.rpy2py(EDADG12total)
    
    return pd_df
 
# Función para pasar datos de Pandas a R --------------------------------------------------------------- 25/05/24
def pd_to_R(data):
    r_data = pandas2ri.py2rpy(data)
    r.assign('R_data', r_data)

# Función para extraer datos de R a Pandas ------------------------------------------------------------- 25/05/24
def R_to_pd(variable_name):
    return pandas2ri.rpy2py(r(variable_name))

def MatchIt_R(data,group1 = 'G1', group2 = 'Control' ):
    if (group1  == 'Control' or group2  == 'Control'):
        data['group'] = data['group'].replace('CTR', 'Control')
    filtered_data = data[(data['group'] == group1) | (data['group'] == group2)]
    filtered_data['treatG1'] = filtered_data['group']
    filtered_data['treatG1'] = filtered_data.treatG1.replace(group1,'Treat') 
    filtered_data['treatG1'] = filtered_data.treatG1.replace(group2,'Control') 
    dataTreat = filtered_data[filtered_data['treatG1'] == 'Treat']
    dataCTR = filtered_data[filtered_data['treatG1'] == 'Control']
    filtered_data = pd.concat([dataTreat, dataCTR])
    data = filtered_data[(filtered_data['visit'] == 'V0') | (filtered_data['visit'] == 't1')]

    # Eliminar columnas con al menos una celda con valor None
    columnas_con_none = data.columns[data.isna().any()].tolist()
    data.drop(columnas_con_none, axis=1,inplace=True)
    
    pd_to_R(data)
    
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')
    
    r('''
    EDADG12 <- matchit(treatG1 ~ age+sex, data = R_data, 
        method = "nearest", ratio = 2)
    ''')

    r('''summary(EDADG12, un=FALSE)''')
    #r('''plot(summary(EDADG12))''')
    #r('''plot(EDADG12, type='jitter')''')
    #r('''plot(EDADG12, type='hist')''')
    #r('''plot(EDADG12, type = "qq")''')
    
    r('''
    EDADG12treat <- match.data(EDADG12, group = "treated")
    EDADG12control <- match.data(EDADG12, group = "control")
    ''')
    
    r('''
    EDADG12total <- rbind(EDADG12treat,EDADG12control)
    ''')

    data_MatchIt =R_to_pd()
    r('''
    head(EDADG12total)
    ''')
    #ggplot(EDADG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
    r('''
    t.test(EDADG12total$age~EDADG12total$treatG1)
    ''')

    data_MatchIt = data_MatchIt.drop(['treatG1', 'distance', 'weights','subclass'],axis=1)
    return data_MatchIt

def MatchIt_G1G2(data,group1 = 'G1', group2 = 'G2' ):
    data['treatG1'] = data['group']
    data['treatG1'] = data.treatG1.replace(group1,'Treat') 
    data['treatG1'] = data.treatG1.replace(group2,'G2')
    dataTreat = data[data['treatG1'] == 'Treat']
    dataCTR = data[data['treatG1'] == 'G2']
    data = pd.concat([dataTreat, dataCTR])
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]


    pd_to_R(data)
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')
    r('''
    EDADG12 <- matchit(treatG1 ~ age+sex, data = R_data, 
        method = "nearest", ratio = 1)
    ''')

    r('''summary(EDADG12, un=FALSE)''')
    #r('''plot(summary(EDADG12))''')
    #r('''plot(EDADG12, type='jitter')''')
    #r('''plot(EDADG12, type='hist')''')
    #r('''plot(EDADG12, type = "qq")''')
    r('''
    EDADG12treat <- match.data(EDADG12, group = "treated")
    EDADG12control <- match.data(EDADG12, group = "control")
    ''')
    r('''
    EDADG12total <- rbind(EDADG12treat,EDADG12control)
    ''')

    data_MatchIt =R_to_pd()
    r('''
    head(EDADG12total)
    ''')
    #ggplot(EDADG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
    r('''
    t.test(EDADG12total$age~EDADG12total$treatG1)
    ''')

    data_MatchIt = data_MatchIt.drop(['treatG1', 'distance', 'weights','subclass'],axis=1)
    return data_MatchIt

def get_max_ratio(data):
    # Bucle para encontrar el máximo ratio posible
    max_ratio = None
    for ratio in range(1, len(data) + 1):
        try:
            r(f'''
            EDADG12 <- matchit(treatG1 ~ age + sex, data = R_data, 
                method = "nearest", ratio = {ratio})
            ''')
            r(f'print(summary(EDADG12, un=FALSE))')
            max_ratio = ratio
        except Exception as e:
            break

    return max_ratio

def MatchIt_R_15(data,group1 = 'G1', group2 = 'Control' ):
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group']
    data['treatG1'] = data['treatG1'].replace(group1, 'Treat')
    data['treatG1'] = data['treatG1'].replace(group2, 'Control')

    dataTreat = data[data['treatG1'] == 'Treat']
    dataCTR = data[data['treatG1'] == 'Control']
    # Seleccionar un subconjunto de 31 G1 al azar
    dataTreat_sub = dataTreat.sample(n=31, random_state=42)
    
    # Combinar el subconjunto de G1 con todos los controles
    data = pd.concat([dataTreat_sub, dataCTR])
    
    #data = pd.concat([dataTreat, dataCTR])
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]

    pd_to_R(data)

    # Ajustar factores en R
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')

    # Seleccionar un subconjunto de 31 G1 al azar
    dataTreat_sub = dataTreat.sample(n=31, random_state=42)
    
    # Combinar el subconjunto de G1 con todos los controles
    data = pd.concat([dataTreat_sub, dataCTR])
    
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]

    pd_to_R(data)
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')

    # Realizar el emparejamiento con ratio = 5
    r('''
    EDADG12 <- matchit(treatG1 ~ age + sex, data = R_data, method = "nearest", ratio = 5)
    ''')

    r('''summary(EDADG12, un=FALSE)''')
    #r('''plot(summary(EDADG12))''')
    #r('''plot(EDADG12, type='jitter')''')
    #r('''plot(EDADG12, type='hist')''')
    #r('''plot(EDADG12, type = "qq")''')
    r('''
    EDADG12treat <- match.data(EDADG12, group = "treated")
    EDADG12control <- match.data(EDADG12, group = "control")
    ''')
    r('''
    EDADG12total <- rbind(EDADG12treat,EDADG12control)
    EDADG12total <- na.omit(EDADG12total)
    ''')

    data_MatchIt =R_to_pd_V2()
    r('''
    head(EDADG12total)
    ''')
    #ggplot(EDADG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
    r('''
    t.test(EDADG12total$age~EDADG12total$treatG1)
    ''')

    data_MatchIt = data_MatchIt.drop(['treatG1', 'distance', 'weights','subclass'],axis=1)
    data_MatchIt = data_MatchIt.dropna()
    return data_MatchIt

def MatchIt_R_10(data,group1 = 'G1', group2 = 'Control' ):
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group']
    data['treatG1'] = data['treatG1'].replace(group1, 'Treat')
    data['treatG1'] = data['treatG1'].replace(group2, 'Control')

    dataTreat = data[data['treatG1'] == 'Treat']
    dataCTR = data[data['treatG1'] == 'Control']
    # Seleccionar un subconjunto de 15 G1 al azar
    dataTreat_sub = dataTreat.sample(n=15, random_state=42)
    
    # Combinar el subconjunto de G1 con todos los controles
    data = pd.concat([dataTreat_sub, dataCTR])
    
    #data = pd.concat([dataTreat, dataCTR])
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]

    pd_to_R(data)

    # Ajustar factores en R
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')

    # Seleccionar un subconjunto de 31 G1 al azar
    dataTreat_sub = dataTreat.sample(n=31, random_state=42)
    
    # Combinar el subconjunto de G1 con todos los controles
    data = pd.concat([dataTreat_sub, dataCTR])
    
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]

    pd_to_R(data)
    r('''
    R_data$treatG1 <- factor(R_data$treatG1)
    R_data$sex <- factor(R_data$sex)
    R_data$group <- factor(R_data$group)
    R_data$participant_id <- factor(R_data$participant_id)
    ''')

    # Realizar el emparejamiento con ratio = 5
    r('''
    EDADG12 <- matchit(treatG1 ~ age + sex, data = R_data, method = "nearest", ratio = 10)
    ''')

    r('''summary(EDADG12, un=FALSE)''')
    #r('''plot(summary(EDADG12))''')
    #r('''plot(EDADG12, type='jitter')''')
    #r('''plot(EDADG12, type='hist')''')
    #r('''plot(EDADG12, type = "qq")''')
    r('''
    EDADG12treat <- match.data(EDADG12, group = "treated")
    EDADG12control <- match.data(EDADG12, group = "control")
    ''')
    r('''
    EDADG12total <- rbind(EDADG12treat,EDADG12control)
    EDADG12total <- na.omit(EDADG12total)
    ''')

    data_MatchIt =R_to_pd_V2()
    r('''
    head(EDADG12total)
    ''')
    #ggplot(EDADG12total, aes(x=treatG1, y=age, fill=treatG1)) + geom_violin(show.legend = FALSE, alpha=0.5, colour="navyblue", fill = "white", size=1) + geom_boxplot(show.legend = FALSE, alpha=0.5, width=0.2, colour="purple4", fill = "purple4") + stat_summary (fun=median, show.legend = FALSE, geom = "crossbar") + geom_dotplot(binaxis = "y",binwidth = 0.8, stackdir = "center", show.legend = FALSE, colour="black", fill="darkblue")
    r('''
    t.test(EDADG12total$age~EDADG12total$treatG1)
    ''')

    data_MatchIt = data_MatchIt.drop(['treatG1', 'distance', 'weights','subclass'],axis=1)
    data_MatchIt = data_MatchIt.dropna()
    return data_MatchIt

# Función para realizar el emparejamiento basado en el puntaje de propensión
def MatchIt_R_Propensity_5_1(data, group1='G1', group2='Control'):
    # Reemplazar los valores de grupo según corresponda
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group'].replace({group1: 'Treat', group2: 'Control'})
    
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]
    
    # Pasar los datos de Pandas a R
    pd_to_R(data)
    
    # Ajustar el modelo de regresión logística binomial para calcular el puntaje de propensión
    r('''
    library(MatchIt)
    R_data$treatG1 <- as.factor(R_data$treatG1)
    R_data$sex <- as.factor(R_data$sex)
    R_data$group <- as.factor(R_data$group)
    R_data$participant_id <- as.factor(R_data$participant_id)
    
    # Calcular el puntaje de propensión usando regresión logística binomial
    ps_model <- glm(treatG1 ~ age + sex, data = R_data, family = binomial())
    R_data$ps <- predict(ps_model, type = "response")
    ''')
    
    # Verificar el puntaje de propensión calculado
    r('print(head(R_data$ps))')
    
    # Realizar el emparejamiento usando `MatchIt` con ratio de 5:1
    r('''
    match_obj <- matchit(treatG1 ~ ps, data=R_data, method="nearest", ratio=5, caliper=0.2)
    matched_data <- match.data(match_obj)
    ''')
    
    # Extraer los datos emparejados de R a Pandas
    data_MatchIt = R_to_pd('matched_data')
    
    # Filtrar para eliminar cualquier tratado sin pareja adecuada
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]
    
    if treated_count * 5 > control_count:
        excess_treats = treated_count - control_count // 5
        excess_treat_ids = data_MatchIt[data_MatchIt['treatG1'] == 'Treat']['participant_id'].unique()[:excess_treats]
        data_MatchIt = data_MatchIt[~data_MatchIt['participant_id'].isin(excess_treat_ids)]
    
    # Verificar la cantidad de controles por cada tratado después del filtrado
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]
    print(f'Total tratados: {treated_count}, Total controles: {control_count}')
    
    # Realizar una prueba t de los datos emparejados
    r('''
    t_test_result <- t.test(matched_data$age ~ matched_data$treatG1)
    print(t_test_result)
    ''')
    
    # Limpiar los datos emparejados y reasignar los nombres de los grupos
    data_MatchIt = data_MatchIt.drop(['distance', 'weights', 'subclass'], axis=1)
    data_MatchIt = data_MatchIt.dropna()

    # Reasignar nombres de grupos para mayor claridad
    data_MatchIt['group'] = data_MatchIt['group'].replace({1: group1, 2: group2})
    data_MatchIt = data_MatchIt.drop(['treatG1'], axis=1)
    
    return data_MatchIt


# Función para realizar el emparejamiento basado en el puntaje de propensión
def MatchIt_R_Propensity_10_1(data, group1='G1', group2='Control'):
    # Reemplazar los valores de grupo según corresponda
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group'].replace({group1: 'Treat', group2: 'Control'})
    
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]
    
    # Pasar los datos de Pandas a R
    pd_to_R(data)
    
    # Ajustar el modelo de regresión logística binomial para calcular el puntaje de propensión
    r('''
    library(MatchIt)
    R_data$treatG1 <- as.factor(R_data$treatG1)
    R_data$sex <- as.factor(R_data$sex)
    R_data$group <- as.factor(R_data$group)
    R_data$participant_id <- as.factor(R_data$participant_id)
    
    # Calcular el puntaje de propensión usando regresión logística binomial
    ps_model <- glm(treatG1 ~ age + sex, data = R_data, family = binomial())
    R_data$ps <- predict(ps_model, type = "response")
    ''')
    
    # Verificar el puntaje de propensión calculado
    r('print(head(R_data$ps))')
    
    # Realizar el emparejamiento usando `MatchIt` con ratio de 10:1
    r('''
    match_obj <- matchit(treatG1 ~ ps, data=R_data, method="nearest", ratio=10, caliper=0.2)
    matched_data <- match.data(match_obj)
    ''')
    
    # Extraer los datos emparejados de R a Pandas
    data_MatchIt = R_to_pd('matched_data')
    
    # Filtrar para eliminar cualquier tratado sin pareja adecuada
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]
    
    if treated_count * 10 > control_count:
        excess_treats = treated_count - control_count // 10
        excess_treat_ids = data_MatchIt[data_MatchIt['treatG1'] == 'Treat']['participant_id'].unique()[:excess_treats]
        data_MatchIt = data_MatchIt[~data_MatchIt['participant_id'].isin(excess_treat_ids)]
    
    # Verificar la cantidad de controles por cada tratado después del filtrado
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]
    print(f'Total tratados: {treated_count}, Total controles: {control_count}')
    
    # Realizar una prueba t de los datos emparejados
    r('''
    t_test_result <- t.test(matched_data$age ~ matched_data$treatG1)
    print(t_test_result)
    ''')
    
    # Limpiar los datos emparejados y reasignar los nombres de los grupos
    data_MatchIt = data_MatchIt.drop(['distance', 'weights', 'subclass'], axis=1)
    data_MatchIt = data_MatchIt.dropna()

    # Reasignar nombres de grupos para mayor claridad
    data_MatchIt['group'] = data_MatchIt['group'].replace({1: group1, 2: group2})
    data_MatchIt = data_MatchIt.drop(['treatG1'], axis=1)
    
    return data_MatchIt

# Función para realizar el emparejamiento basado en el puntaje de propensión
def MatchIt_R_Propensity_2_1(data, group1='G1', group2='Control'):
    # Reemplazar los valores de grupo según corresponda
    data['group'] = data['group'].replace('G2', 'Control')
    data['treatG1'] = data['group'].replace({group1: 'Treat', group2: 'Control'})
    
    # Filtrar por las visitas necesarias
    data = data[(data['visit'] == 'V0') | (data['visit'] == 't1')]
    
    # Pasar los datos de Pandas a R
    pd_to_R(data)
    
    # Ajustar el modelo de regresión logística binomial para calcular el puntaje de propensión
    r('''
    library(MatchIt)
    R_data$treatG1 <- as.factor(R_data$treatG1)
    R_data$sex <- as.factor(R_data$sex)
    R_data$group <- as.factor(R_data$group)
    R_data$participant_id <- as.factor(R_data$participant_id)
    
    # Calcular el puntaje de propensión usando regresión logística binomial
    ps_model <- glm(treatG1 ~ age + sex, data = R_data, family = binomial())
    R_data$ps <- predict(ps_model, type = "response")
    ''')
    
    # Verificar el puntaje de propensión calculado
    r('print(head(R_data$ps))')
    
    # Realizar el emparejamiento usando `MatchIt` con ratio de 2:1
    r('''
    match_obj <- matchit(treatG1 ~ ps, data=R_data, method="nearest", ratio=2, caliper=0.2)
    matched_data <- match.data(match_obj)
    ''')
    
    # Extraer los datos emparejados de R a Pandas
    data_MatchIt = R_to_pd('matched_data')
    
    # Filtrar para eliminar cualquier tratado sin pareja adecuada
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]

    if treated_count * 2 > control_count:
        excess_treats = treated_count - control_count // 2
        excess_treat_ids = data_MatchIt[data_MatchIt['treatG1'] == 'Treat']['participant_id'].unique()[:excess_treats]
        data_MatchIt = data_MatchIt[~data_MatchIt['participant_id'].isin(excess_treat_ids)]
    
    # Verificar la cantidad de controles por cada tratado después del filtrado
    treated_count = data_MatchIt[data_MatchIt['treatG1'] == 'Treat'].shape[0]
    control_count = data_MatchIt[data_MatchIt['treatG1'] == 'Control'].shape[0]
    print(f'Total tratados: {treated_count}, Total controles: {control_count}')
    
    # Realizar una prueba t de los datos emparejados
    r('''
    t_test_result <- t.test(matched_data$age ~ matched_data$treatG1)
    print(t_test_result)
    ''')
    
    # Limpiar los datos emparejados y reasignar los nombres de los grupos
    data_MatchIt = data_MatchIt.drop(['distance', 'weights', 'subclass'], axis=1)
    data_MatchIt = data_MatchIt.dropna()

    # Reasignar nombres de grupos para mayor claridad
    data_MatchIt['group'] = data_MatchIt['group'].replace({1: group1, 2: group2})
    data_MatchIt = data_MatchIt.drop(['treatG1'], axis=1)
    
    return data_MatchIt