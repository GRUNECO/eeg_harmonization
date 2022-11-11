"""
@autor: Luisa María Zapata Saldarriaga, Universidad de Antioquia, luisazapatasaldarriaga@gmail.com
@autor: Yorguin José Mantilla Ramos, Universidad de Antioquia, yjmantilla@gmail.com
@autor: Verónica Henao Isaza, Universidad de Antioquia, 
@autor: Valeria Cadavid Castro, Universidad de Antioquia, 

"""

from requests import session
import json
import numpy as np
import pandas as pd 
import itertools

def load_txt(file):
  '''
  Function that reads txt files

  Parameters
  ----------
    file: extend .txt 

  Returns
  -------
    data: 
      Contains the information that was stored in the txt file
  '''
  with open(file, 'r') as f:
    data=json.load(f)
  return data

def feather2xlsx(path,name_file):
  file_feather=pd.read_feather(path+name_file+'.feather')
  print(type(file_feather))
  path_xlsx=path+name_file+'.xlsx'
  file_feather.to_excel(path_xlsx)
  return 

def get_metrics_prep(files,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None):
  '''

  Parameters
  ----------
    file: extend .txt 
    list_studies: None
    list_subjects: None
    list_groups: None
    list_sessions: None

  Returns
  -------
    df: dataframe
      Contains the information that was stored in the txt file in format dataframe
  '''

  if list_studies is None:
    list_studies=["None"]*len(files)
  if list_subjects is None:
    list_subjects=["None"]*len(files) 
  if list_groups is None:
    list_groups=["None"]*len(files)
  if list_sessions is None:
    list_sessions=["None"]*len(files)
  # 3 state (Original, after and before) *9 (different metrics)
  metrics=3*9
  df_prep={}
  df_prep['Study']=list_studies*metrics
  df_prep['Subject']=list_subjects*metrics
  df_prep['Group']=list_groups*metrics
  df_prep['Session']=list_sessions*metrics
  df_prep['Metric']=[]
  df_prep['Metric_value']=[]
  df_prep['State']=[]
  

  for file in files:
    dataFile=load_txt(file)
    noisy_channels_original=dataFile['noisy_channels_original']
    df_prep['Metric']+=[key for key,val in noisy_channels_original.items()]
    df_prep['Metric_value']+=[len(val) for key,val in noisy_channels_original.items()]
    df_prep['State']+=['original']*len(dataFile['noisy_channels_original'])
   
    noisy_channels_before_interpolation=dataFile['noisy_channels_before_interpolation']
    df_prep['Metric']+=[key for key,val in noisy_channels_before_interpolation.items()]
    df_prep['Metric_value']+=[len(val) for key,val in noisy_channels_before_interpolation.items()]
    df_prep['State']+=['before_interpolation']*len(dataFile['noisy_channels_before_interpolation'])
    
    noisy_channels_after_interpolation= dataFile['noisy_channels_after_interpolation']
    df_prep['Metric']+=[key for key,val in noisy_channels_after_interpolation.items()]
    df_prep['Metric_value']+=[len(val) for key,val in noisy_channels_after_interpolation.items()]
    df_prep['State']+=['after_interpolation']*len(dataFile['noisy_channels_after_interpolation'])

  df=pd.DataFrame((df_prep))
  return df

def get_metrics_wica(files,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None):
  '''
  Parameters
  ----------
    files: extend '.txt'
    list_studies:None
    list_subjects: None
    list_groups: None
    list_sessions: None 

  Returns
  -------
    dfstats_wica: dataframe 
      dataframe containing information of all subjects
  '''
  if list_studies is None:
    list_studies=["None"]*len(files)
  if list_subjects is None:
    list_subjects=["None"]*len(files) 
  if list_groups is None:
    list_groups=["None"]*len(files)
  if list_sessions is None:
    list_sessions=["None"]*len(files)   

  sums=[]
  for file in files:
    dataFile=load_txt(file)
    mat=np.array(dataFile)
    sum=np.sum(mat.flatten())
    sums.append(sum/mat.size)

  dfstats_wica=pd.DataFrame({'Study':list_studies,'Subject':list_subjects,'Group':list_groups,'Session':list_sessions,'Components':sums})
  return dfstats_wica

def channelsPowers(data,name_study="None",subject="None",group="None",session="None",stage="None"):
  '''
  Function to return the power bands

  Parameters
  ----------
    data:
    name_study: str
      Database study name
    subject: str
      Name with which the subject was encoded
    group:  str
      Name with which the group was encoded. This refers to the condition of a group of patients.
    session: str
      Name with which the session was encoded. This refers to the visit of a subject. 
    stage: str 

  Returns
  -------
    powers: dataframe 
      Dataframe containing unique information about a subject
  '''

  df_powers={}
  df_powers['Powers']=[]
  df_powers['bands']=[]
  df_powers['Channels']=[]
  df_powers['Study']=[]
  df_powers['Session']=[]
  df_powers['Subject']=[]
  df_powers['Group']=[]
  df_powers['Stage']=[]

  for i,key in enumerate(data['bands']):
    df_powers['Study']+=[name_study]*len(data['channels'])
    df_powers['Subject']+=[subject]*len(data['channels'])
    df_powers['Group']+=[group]*len(data['channels'])
    df_powers['Session']+=[session]*len(data['channels'])
    df_powers['Powers']+=data['channel_power'][i]
    df_powers['bands']+=[key]*len(data['channels'])
    df_powers['Channels']+=data['channels']
    df_powers['Stage']+=[stage]*len(data['channels'])
  
  powers=pd.DataFrame(df_powers)
  return powers 

def get_powers_channels(powersFiles,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None,list_stage=None):
  '''

  Parameters
  ----------
    powersFiles
    list_studies:None
    list_subjects:None
    list_groups:None
    list_sessions:None
    list_stage:None

  Returns
  -------
  
  '''
  dataframesPowers=[]
  if list_studies is None:
    list_studies=["None"]*len(powersFiles)
  if list_subjects is None:
    list_subjects=["None"]*len(powersFiles) 
  if list_groups is None:
    list_groups=["None"]*len(powersFiles)
  if list_sessions is None:
    list_sessions=["None"]*len(powersFiles) 
  if list_stage is None:
    list_stage=['Preprocessed data']*len(powersFiles)
  for power,name_study,subject,group,session,stage in zip(powersFiles,list_studies,list_subjects,list_groups,list_sessions,list_stage):
    dataFile=load_txt(power)
    statsPowers=channelsPowers(dataFile,name_study,subject,group,session,stage)
    dataframesPowers.append(statsPowers)
  datosPowers=pd.concat((dataframesPowers))
  return datosPowers 

def reject_thresholds(data,name_study="None",subject="None",group="None",session="None"):
  '''
  Function to extract the thresholds from the reject metric

  Parameters
  ----------
    data:
    name_study:"None"
    subject:"None"
    group:"None"
    session:"None"

  Returns
  -------
    df= dataframe 

  '''
  df= pd.DataFrame({
  'Study':[name_study]*len(data['final_thresholds']['spectrum'][1]),
  'Subject':[subject]*len(data['final_thresholds']['spectrum'][1]),
  'Group':[group]*len(data['final_thresholds']['spectrum'][1]),
  'Session':[session]*len(data['final_thresholds']['spectrum'][1]),
  'i_kurtosis_min':data['initial_thresholds']['kurtosis'][0],
  'i_kurtosis_max':data['initial_thresholds']['kurtosis'][1],
  'i_amplitude_min': data['initial_thresholds']['amplitude'][0],
  'i_amplitude_max':data['initial_thresholds']['amplitude'][1],
  'i_trend':data['initial_thresholds']['trend'][0],
  'f_kurtosis_min':data['final_thresholds']['kurtosis'][0],
  'f_kurtosis_max':data['final_thresholds']['kurtosis'][1],
  'f_amplitude_min': data['final_thresholds']['amplitude'][0],
  'f_amplitude_max':data['final_thresholds']['amplitude'][1],
  'f_trend':data['final_thresholds']['trend'][0],
  'f_spectrum_min':data['final_thresholds']['spectrum'][0],
  'f_spectrum_max':data['final_thresholds']['spectrum'][1]
  
  })
  return df

def reject_thresholds_format_long(data,name_study="None",subject="None",group="None",session="None"):
  '''
  Function to extract the thresholds from the reject metric

  Parameters
  ----------
    data:
    name_study:"None"
    subject:"None"
    group:"None"
    session:"None"

  Returns
  -------
    df= dataframe 

  '''
  metrics=['i_kurtosis_min','i_kurtosis_max','i_amplitude_min','i_amplitude_max','i_trend','f_kurtosis_min','f_kurtosis_max','f_amplitude_min','f_amplitude_max','f_trend','f_spectrum_min','f_spectrum_max']
  metrics_value=[*data['initial_thresholds']['kurtosis'][0],*data['initial_thresholds']['kurtosis'][1],*data['initial_thresholds']['amplitude'][0],*data['initial_thresholds']['amplitude'][1],*data['initial_thresholds']['trend'][0],*data['final_thresholds']['kurtosis'][0],*data['final_thresholds']['kurtosis'][1],*data['final_thresholds']['amplitude'][0],*data['final_thresholds']['amplitude'][1],*data['final_thresholds']['trend'][0],*data['final_thresholds']['spectrum'][0],*data['final_thresholds']['spectrum'][1]]
  metrics_value_=[data['initial_thresholds']['kurtosis'][0],data['initial_thresholds']['kurtosis'][1],data['initial_thresholds']['amplitude'][0],data['initial_thresholds']['amplitude'][1],data['initial_thresholds']['trend'][0],data['final_thresholds']['kurtosis'][0],data['final_thresholds']['kurtosis'][1],data['final_thresholds']['amplitude'][0],data['final_thresholds']['amplitude'][1],data['final_thresholds']['trend'][0],data['final_thresholds']['spectrum'][0],data['final_thresholds']['spectrum'][1]]

  df= pd.DataFrame({
  'Study':[name_study]*len(data['final_thresholds']['spectrum'][1])*len(metrics),
  'Subject':[subject]*len(data['final_thresholds']['spectrum'][1])*len(metrics),
  'Group':[group]*len(data['final_thresholds']['spectrum'][1])*len(metrics),
  'Session':[session]*len(data['final_thresholds']['spectrum'][1])*len(metrics)
   })
  list_metrics=[]
  for pos,metric in enumerate(metrics):
    # 58 porque es la longitud de los canales 
    list_metrics.extend([metric]*len(metrics_value_[pos]))
  df['Metric']=list_metrics
  df['Metric_Value']=metrics_value
  return df 

def get_metrics_reject(files,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None):
  '''
  
  Parameters
  ----------
    files
    list_studies:None
    list_subjects:None
    list_groups:None
    list_sessions:None

  Returns
  -------
  '''
  if list_studies is None:
    list_studies=["None"]*len(files)
  if list_subjects is None:
    list_subjects=["None"]*len(files) 
  if list_groups is None:
    list_groups=["None"]*len(files)
  if list_sessions is None:
    list_sessions=["None"]*len(files)  
  dataframesReject=[]
  for file,name_study,subject,group,session in zip(files,list_studies,list_subjects,list_groups,list_sessions):
    dataFile=load_txt(file)
    statsReject=reject_thresholds_format_long(dataFile,name_study,subject,group,session)
    dataframesReject.append(statsReject)
  dataReject=pd.concat((dataframesReject))
  return dataReject

def component_power(data,name_study="None",subject="None",group="None",session="None",stage="None"):
  '''

  Parameters
  ----------
    data
    name_study:str
    subject:str
    group:str
    session:str
    stage:str

  Returns
  -------
    powers: dataframe
      Dataframe containing unique information about a subject
  '''
  df_powers={}
  df_powers['Powers']=[]
  df_powers['Bands']=[]
  df_powers['Components']=[]
  df_powers['Study']=[]
  df_powers['Session']=[]
  df_powers['Subject']=[]
  df_powers['Group']=[]
  df_powers['Stage']=[]

  for i,key in enumerate(data['bands']):
    ncomps = np.array(data['ics_power']).shape[1]
    comp_labels = ['C'+str(i+1) for i in range(ncomps)]
    df_powers['Study']+=[name_study]*len(comp_labels)
    df_powers['Subject']+=[subject]*len(comp_labels)
    df_powers['Group']+=[group]*len(comp_labels)
    df_powers['Session']+=[session]*len(comp_labels)
    df_powers['Powers']+=data['ics_power'][i]
    df_powers['Bands']+=[key]*len(comp_labels)
    df_powers['Components']+= comp_labels
    df_powers['Stage']+=[stage]*len(comp_labels)
  powers=pd.DataFrame(df_powers)
  return powers 

def get_powers_components(powersFiles,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None,list_stage=None):
  '''

  Parameters
  ----------
    powersFiles
    list_studies=None
    list_subjects=None
    list_groups=None
    list_sessions=None
    list_stage=None
  
  Returns
  -------
    datosPowers:dataframe
  '''
  dataframesPowers=[]
  if list_studies is None:
    list_studies=["None"]*len(powersFiles)
  if list_subjects is None:
    list_subjects=["None"]*len(powersFiles) 
  if list_groups is None:
    list_groups=["None"]*len(powersFiles)
  if list_sessions is None:
    list_sessions=["None"]*len(powersFiles) 
  if list_stage is None:
    list_stage=['Preprocessed data']*len(powersFiles)
  for power,name_study,subject,group,session,stage in zip(powersFiles,list_studies,list_subjects,list_groups,list_sessions,list_stage):
    dataFile=load_txt(power)
    statsPowers=component_power(dataFile,name_study,subject,group,session,stage)
    dataframesPowers.append(statsPowers)
  datosPowers=pd.concat((dataframesPowers))
  return datosPowers 

def get_data_sl_format_long(files,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None):
  '''
  Parameters
  ----------
    file: extend .txt 
    list_studies: None
    list_subjects: None
    list_groups: None
    list_sessions: None

  Returns
  -------
    df: dataframe
      Contains the information that was stored in the txt file in format dataframe
  '''

  if list_studies is None:
    list_studies=["None"]*len(files)
  if list_subjects is None:
    list_subjects=["None"]*len(files) 
  if list_groups is None:
    list_groups=["None"]*len(files)
  if list_sessions is None:
    list_sessions=["None"]*len(files)

  df_sl={}
  df_sl['Study']=[]
  df_sl['Subject']=[]
  df_sl['Group']=[]
  df_sl['Session']=[]
  df_sl['bands']=[]
  df_sl['sl_values']=[]
  df_sl['channel']=[]
  for f,file in enumerate(files):
    dataFile=load_txt(file)
    for i,key in enumerate(dataFile['bands']):
      df_sl['Study']+=[list_studies[f]]*len(dataFile['sl'][key])*len(dataFile['channels'])
      df_sl['Subject']+=[list_subjects[f]]*len(dataFile['sl'][key])*len(dataFile['channels'])
      df_sl['Group']+=[list_groups[f]]*len(dataFile['sl'][key])*len(dataFile['channels'])
      df_sl['Session']+=[list_sessions[f]]*len(dataFile['sl'][key])*len(dataFile['channels'])
      df_sl['channel']+=list(itertools.chain(*[[f'{y}:{x}' for y in dataFile['channels'] for x in dataFile['channels']]]))
      df_sl['bands']+=[key]*len(dataFile['sl'][key])*len(dataFile['channels'])
      df_sl['sl_values']+=itertools.chain(*dataFile['sl'][key])
  df=pd.DataFrame(df_sl)
  return df

def get_data_mean_roi_sl_format_long(files,list_studies=None,list_subjects=None,list_groups=None,list_sessions=None,ROIs=None):
  if list_studies is None:
    list_studies=["None"]*len(files)
  if list_subjects is None:
    list_subjects=["None"]*len(files) 
  if list_groups is None:
    list_groups=["None"]*len(files)
  if list_sessions is None:
    list_sessions=["None"]*len(files)
  if ROIs is None:
    F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
    T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
    C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
    PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
    ROIs = [F,C,PO,T]
      

  df_sl={}
  df_sl['sl_values']=[]
  df_sl['Study']=[]
  df_sl['Subject']=[]
  df_sl['Group']=[]
  df_sl['Session']=[]
  df_sl['bands']=[]
  df_sl['ROI']=[]
  
  roi_labels = ['F','C','PO','T']
  
  for f,file in enumerate(files):
    dataFile=load_txt(file)
    df_sl['Study']+=[list_studies[f]]*len(roi_labels)*len(dataFile['bands'])
    df_sl['Group']+=[list_groups[f]]*len(roi_labels)*len(dataFile['bands'])
    df_sl['Session']+=[list_sessions[f]]*len(roi_labels)*len(dataFile['bands'])
    df_sl['Subject']+=[list_subjects[f]]*len(roi_labels)*len(dataFile['bands'])
    new_rois = []
    for roi in ROIs:
      channels = set(dataFile['channels']).intersection(roi)
      new_roi=[dataFile['channels'].index(channel) for channel in channels]
      new_rois.append(new_roi)

    for i,key in enumerate(dataFile['bands']):
      for r,roi in enumerate(new_rois):
        df_sl['bands']+=[key]
        df_sl['ROI']+=[roi_labels[r]]
        df_sl['sl_values']+=[np.average(np.array(dataFile['sl'][key])[roi])]

  df=pd.DataFrame(df_sl)
  return df
    
def get_data_columns_ROI_sl(ROIs): 
  '''Obtain data frames with SL of ROIs in different columns''' 
  for f,file in enumerate(files):
    dataFile=load_txt(file)
    total_channels=np.array(dataFile['channels'])
    bandas = dataFile['bands']
    new_rois = []
    potencias_roi_banda=[]

    for roi in ROIs:
        channels = set(dataFile['channels']).intersection(roi)
        new_roi=[dataFile['channels'].index(channel) for channel in channels]
        new_rois.append(new_roi)

    for b,band in enumerate(bandas):
      for r,roi in enumerate(new_rois):
          datos_1_sujeto[f'SL_ROI_{roi_labels[r]}_{band.title()}']=np.average(np.array(dataFile['sl'][band])[roi])
    list_subjects.append(datos_1_sujeto)
  df = pd.DataFrame(list_subjects)
  return df



def get_data_coherence():
  return

# FILTROS
def filter_nS_nG_1M(superdata,group_dict):
    """
    superdata
    group_dict={
        'BIOMARCADORES':[CTR,DCL],
        'SRM':['SRM'] # assume datasets with no groups have Group=Study
    }
    """
    fil=superdata
    list_df=[]
    for dataset,group_list in group_dict.items():
        for group in group_list:
            auxfil = fil[fil['Group']==group]
            list_df.append(auxfil)
    df=pd.concat((list_df))
    return df

#no_relative_path = 'D:/TDG/filesSaved/BIOMARCADORES/derivatives/'
# task_path = 'CE'
# no_relative_path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives/'
# feather2xlsx(no_relative_path,'data_'+task_path+'_wICA')
# feather2xlsx(no_relative_path,'data_'+task_path+'_reject')
# feather2xlsx(no_relative_path,'longitudinal_data_powers_long_'+task_path+'_channels')
# feather2xlsx(no_relative_path,'longitudinal_data_powers_long_'+task_path+'_components')
# feather2xlsx(no_relative_path,'longitudinal_data_powers_long_'+task_path+'_norm_channels')
# feather2xlsx(no_relative_path,'longitudinal_data_powers_long_'+task_path+'_norm_components')