BIOMARCADORES_OE = {
    'name':'BIOMARCADORES',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restOE',
    'session':'V'
}

BIOMARCADORES_CE = {
    'name':'BIOMARCADORES',
    'input_path':r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}

BIOMARCADORESMini = {
    'name':'BIOMARCADORES',
    'input_path':r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\biomarcadoresprueba",
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
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}

DUQUE = {
    'name':'DUQUE',
    'input_path':r'C:\Users\valec\OneDrive - Universidad de Antioquia\Datos MsC Verónica\DUQUE',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}