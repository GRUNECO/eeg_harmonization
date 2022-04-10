BIOMARCADORES = {
    'name':'BIOMARCADORES',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'marks_rest':None,
}

SRM = {
    'name':'SRM',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'marks_rest':None,
}

CHBMP = {
    'name':'CHBMP',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP',
    'layout':{'extension':'.edf', 'task':'protmap','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'marks_rest':65,
}

LEMON = {
    'name':'LEMON',
    'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\LEMON_BIDS',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'resample':1000,'line_freqs':[50]},
    'group_regex':None,
    'marks_rest':5,

}
