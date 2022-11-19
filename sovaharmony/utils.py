import numpy as np
def _verify_epochs_axes(epochs_spaces_times,spaces_times_epochs,max_epochs=None):
    """
    """
    epochs,spaces,times = epochs_spaces_times.shape
    if max_epochs is None:
        max_epochs = epochs
    for e in range(np.max([epochs,max_epochs])):
        for c in range(spaces):
            assert np.all(epochs_spaces_times[e,c,:] == spaces_times_epochs[c,:,e])
    return True

def _verify_epoch_continuous(data,spaces_times,data_axes,max_epochs=None):
    epochs_idx = data_axes.index('epochs')
    spaces_idx = data_axes.index('spaces')
    times_idx = data_axes.index('times')
    epochs,spaces,times = data.shape[epochs_idx],data.shape[spaces_idx],data.shape[times_idx]
    if not epochs_idx in [0,2]:
        raise ValueError('Axes should be either epochs,spaces,times or spaces,times,epochs')
    if max_epochs is None:
        max_epochs = epochs
    for e in range(np.max([epochs,max_epochs])):
        for c in range(spaces):
            if epochs_idx==0:
                assert np.all(data[e,c,:] == spaces_times[c,e*times:(e+1)*times])
            elif epochs_idx==2:
                assert np.all(data[c,:,e] == spaces_times[c,e*times:(e+1)*times])
    return True
