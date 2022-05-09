BIOMARCADORES = {
    'name':'BIOMARCADORES',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE'
}

BIOMARCADORES_test = {
    'name':'BIOMARCADORES',
    'input_path':r'F:\BIOMARCADORES_TEST',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE'
}

SRM_test = {
    'name':'SRM',
    'input_path':r'D:\WEB\backend\filesSaved\SRMPrueba',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE'
}

SRM= {
    'name':'SRM',
    'input_path':r'D:\WEB\backend\filesSaved\SRM',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE'
}
# CHBMP = {
#     'name':'CHBMP',
#     'input_path':r'D:\WEB\backend\filesSaved\CHBMP',
#     'layout':{'extension':'.edf', 'task':'protmap','suffix':'eeg', 'return_type':'filename'},
#     'args':{'line_freqs':[60],},
#     'group_regex':None,
#     'events_to_keep':[65],
#     'run-label':'restCE'
# }

# LEMON = {
#     'name':'LEMON',
#     'input_path':r'D:\WEB\backend\filesSaved\LEMON_BIDS',
#     'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
#     'args':{'resample':1000,'line_freqs':[50],},
#     'group_regex':None,
#     'events_to_keep':[5],
#     'run-label':'restCE'
# }