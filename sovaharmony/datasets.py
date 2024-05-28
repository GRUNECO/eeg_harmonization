BIOMARCADORES_OE = {
    'name':'BIOMARCADORES',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename', 'session':'V0'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restOE',
    'session':'V'
}

BIOMARCADORES_CE = {
    'name':'BIOMARCADORES',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename', 'session':'V0'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
   
}

BIOMARCADORESMini = {
    'name':'BIOMARCADORES',
    'input_path':r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\Datos MsC Verónica\biomarcadoresprueba',
     #"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\biomarcadoresprueba",
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}

BIOMARCADORESYorguin = {
    'name':'BIOMARCADORES',
    'input_path':r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\biomarcadorespruebaICAYorguin",
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}


CHBMP = {
    'name':'CHBMP',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\CHBMP',
    'layout':{'extension':'.edf', 'task':'protmap','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60],},
    'group_regex':None,
    'events_to_keep':[65],
    'run-label':'restCE',
    'session':None
}

LEMON = {
    'name':'LEMON',
    'input_path':r'D:\BASESDEDATOS\LEMON_BIDS',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'resample':1000,'line_freqs':[50],},
    'group_regex':None,
    'events_to_keep':[5],
    'run-label':'restEC',
    'session':None
}


SRM = {
    'name':'SRM',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\SRM',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename', 'session':'t1'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
    }

DUQUE = {
    'name':'DUQUE',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\DUQUE',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':None
}

Estudiantes2021_OE={
    'name':'Estudiantes2021',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes2021',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'OE',
    'session':'V'
}

Estudiantes2021_CE={
    'name':'Estudiantes2021',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes2021',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'CE',
    'session':'V'
}

Estudiantes2021_T1={
    'name':'Estudiantes2021',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes2021',
    'layout':{'extension':'.vhdr', 'task':'T1','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T1',
    'session':'V'
}

Estudiantes2021_T2={
    'name':'Estudiantes2021',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes2021',
    'layout':{'extension':'.vhdr', 'task':'T2','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T2',
    'session':'V'
}



Estudiantes_OE={
    'name':'Estudiantes',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'OE',
    'session':'V'
}

Estudiantes_CE={
    'name':'Estudiantes',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'CE',
    'session':'V'
}

Estudiantes_T1={
    'name':'Estudiantes',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes',
    'layout':{'extension':'.vhdr', 'task':'T1','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T1',
    'session':'V'
}

Estudiantes_T2={
    'name':'Estudiantes',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes',
    'layout':{'extension':'.vhdr', 'task':'T2','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T2',
    'session':'V'
}

Estudiantes_T3={
    'name':'Estudiantes',
    'input_path':r'D:\XIMENA\BIDS\Estudiantes',
    'layout':{'extension':'.vhdr', 'task':'T3','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T3',
    'session':'V'
}

Residentes_CE={
    'name':'Residentes',
    'input_path':r'D:\XIMENA\BIDS\Residentes',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'CE',
    'session':'V'
}


Residentes_OE={
    'name':'Residentes',
    'input_path':r'D:\XIMENA\BIDS\Residentes',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'OE',
    'session':'V'
}

Residentes_T1={
    'name':'Residentes',
    'input_path':r'D:\XIMENA\BIDS\Residentes',
    'layout':{'extension':'.vhdr', 'task':'T1','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T1',
    'session':'V'
}


Residentes_T2={
    'name':'Residentes',
    'input_path':r'D:\XIMENA\BIDS\Residentes',
    'layout':{'extension':'.vhdr', 'task':'T2','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T2',
    'session':'V'
}


Residentes_T3={
    'name':'Residentes',
    'input_path':r'D:\XIMENA\BIDS\Residentes',
    'layout':{'extension':'.vhdr', 'task':'T3','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'T3',
    'session':'V'
}

BIOMARCADORES_CE_54X10 = {
    'name':'BIOMARCADORES',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASEDEDATOS147\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename', 'session':'V0'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
   
}

CHBMP_54X10 = {
    'name':'CHBMP',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASEDEDATOS147\CHBMP',
    'layout':{'extension':'.edf', 'task':'protmap','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60],},
    'group_regex':None,
    'events_to_keep':[65],
    'run-label':'restCE',
    'session':None
}

SRM_54X10 = {
    'name':'SRM',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASEDEDATOS147\SRM',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename', 'session':'t1'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
    }

DUQUE_54X10 = {
    'name':'DUQUE',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASEDEDATOS147\DUQUE',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':None
}