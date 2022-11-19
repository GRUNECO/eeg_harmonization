Opcion 1
dict
    values:
        alpha:
            c1: 23
            c2: 212
        beta:
            c1: 23
            c2: 123
    axes = {bands:lista de bandas,canal:lista canales}
    metadata: anyother info useful to describe 
        type: power
        bands: (the bands dict)
    dict[values][banda][canal]

Opcion 2
dict
    values : [[23,212],[23,123]]
    axes = {bands:lista de bandas,canal:lista canales}
    metadata: anyother info useful to describe 
        type: power
        bands: (the bands dict)

    idx_banda = axes_keys[bands].index(banda)
    idx_canal = axes_keys[canales].index(canal)
    dict[values][idx_banda,idx_canal]

Opcion 3
    values : [{band:band_label,canal:canal_label,value:x}]
    axes = {bands:lista de bandas,canal:lista canales}
    metadata: anyother info useful to describe 
        type: power
        bands: (the bands dict)

    idx_banda = axes[band].index(banda)
    idx_canal = axes[canal].index(canal)
    dict[values][idx_banda,idx_canal]
