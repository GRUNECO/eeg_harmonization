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
# Install R package
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)
#utils.install_packages('MatchIt')
#utils.install_packages('ggplot2')

# Import R libraries
MatchIt = rpackages.importr('MatchIt')
ggplot2 = rpackages.importr('ggplot2')
base = importr('base')


#Abrir base de datos y asignar factoriales a las variables cualitativas

# Convert Python dataframe to R dataframe
def pd_to_R(df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_from_pd_df = ro.conversion.py2rpy(df)
    # Create a variable name in R's global environment
    globalenv['R_data'] = r_from_pd_df

# Convert R dataframe to Python dataframe 
def R_to_pd():
    ro.r('''
    R_data2 <- rapply(EDADG12total, as.character, classes="factor", how="replace")
    ''')

    R_data2 = ro.r['R_data2']
    R_data = pd.DataFrame([dict(R_data2.items())])
    with localconverter(ro.default_converter + pandas2ri.converter):
        pd_from_r_df = ro.conversion.rpy2py(R_data.iloc[0])
        new_pd = pd.DataFrame(dict(pd_from_r_df.items()), columns=R_data.columns.values)   
        return new_pd

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
