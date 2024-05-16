from mne.viz import plot_topomap
import mne
from mne.preprocessing import ICA
import numpy as np
from mne.io.pick import (pick_types, _picks_by_type, pick_info, pick_channels,
                       _pick_data_channels, _picks_to_idx, _get_channel_types,
                       _MEG_CH_TYPES_SPLIT)
from mne.utils import (_clean_names, _time_mask, verbose, logger, warn, fill_doc,
                     _validate_type, _check_sphere, _check_option, _is_numeric)
from mne.viz.utils import (tight_layout, _setup_vmin_vmax, _prepare_trellis,
                    _check_delayed_ssp, _draw_proj_checkbox, figure_nobar,
                    plt_show, _process_times, DraggableColorbar,
                    _validate_if_list_of_axes, _setup_cmap, _check_time_unit)
from mne.viz.topomap import _prepare_topomap_plot,_make_head_outlines,_add_colorbar,_hide_frame
from mne.channels.channels import _get_ch_type
from mne.channels.layout import (
    _find_topomap_coords, find_layout, _pair_grad_sensors, _merge_ch_data)
from mne.io import BaseRaw
from mne.epochs import BaseEpochs
import copy

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_matrix(array,ylabels=None,xlabels=None,cmap='plasma',show=True,figsize=(10,20),clim=None,fontsize=12,sort=False,incell_fontsize=12):
    numbers = list(range(array.shape[0]))
    if ylabels is not None:
        ylabels = [ylabels[i]+'-'+str(numbers[i]) for i in range(len(numbers))]
    else:
        ylabels = [str(i) for i in range(array.shape[0])]

    
    if xlabels is None:
        xlabels = [str(i) for i in range(array.shape[1])]

    if sort:
        ind = array.argsort(axis=0)[::-1]
        array = np.take_along_axis(array, ind, axis=0)
        labels_array = np.array([numbers]*array.shape[1]).transpose()
        labels_array = np.take_along_axis(labels_array,ind,axis=0)

    #fig = plt.figure()
    #fig.set_size_inches()
    fig, ax = plt.subplots(1, 1, figsize=figsize)  
    #ax = axes#fig.add_subplot(111)
    ax.set_aspect('auto')
    if clim is None:
        cax = ax.matshow(array, cmap=plt.get_cmap(cmap),aspect='auto')
    else:
        cax = ax.matshow(array, cmap=plt.get_cmap(cmap),aspect='auto',vmin=clim[0],vmax=clim[1])

    cb = fig.colorbar(cax)
    cb.ax.tick_params(labelsize=fontsize)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    #ax.set_xticklabels(['']+labels_df['aka'])
    #https://stackoverflow.com/questions/28885279/matplotlibs-matshow-not-aligned-with-grid
    if True:#not sort:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.set_yticks(np.arange(len(ylabels)),minor='true')
        ax.set_yticklabels(['']+ylabels,fontsize=fontsize)
        ax.get_yaxis().set_minor_locator(ticker.AutoMinorLocator(n=2))
    ax.set_xticks(np.arange(len(xlabels)),minor='true')
    ax.set_xticklabels(['']+xlabels,fontsize=fontsize)
    ax.get_xaxis().set_minor_locator(ticker.AutoMinorLocator(n=2))
    ax.grid(b=True,color='k',which='minor',linewidth=fontsize/10)
    #ax.minorticks_on()
    if sort:
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                ax.text(j, i, str(labels_array[i,j]), va='center', ha='center',fontsize=incell_fontsize)
    plt.tight_layout()
    if show:
        plt.show()
    return fig


def plot_ica_components(ica, picks=None, ch_type=None, res=64,
                        vmin=None, vmax=None, cmap='RdBu_r',
                        sensors=True, colorbar=False, title=None,
                        show=False, outlines='head', contours=6,
                        image_interp='bilinear',
                        inst=None, plot_std=True, topomap_args=None,
                        image_args=None, psd_args=None, reject='auto',
                        sphere=None,p=20,ncols=5):
    """
    Copy of the mne.viz.plot_ica_components function but with 2 additional parameters: p,ncols
    This allows the control of the distribution of topomaps in the plot.
    _____________________________________________________________________
    Project unmixing matrix on interpolated sensor topography.
    Parameters
    ----------
    ica : instance of mne.preprocessing.ICA
        The ICA solution.
        If None all are plotted in batches of 20.
    ch_type : 'mag' | 'grad' | 'planar1' | 'planar2' | 'eeg' | None
        The channel type to plot. For 'grad', the gradiometers are
        collected in pairs and the RMS for each pair is plotted.
        If None, then channels are chosen in the order given above.
    res : int
        The resolution of the topomap image (n pixels along each side).
    vmin : float | callable | None
        The value specifying the lower bound of the color range.
        If None, and vmax is None, -vmax is used. Else np.min(data).
        If callable, the output equals vmin(data). Defaults to None.
    vmax : float | callable | None
        The value specifying the upper bound of the color range.
        If None, the maximum absolute value is used. If callable, the output
        equals vmax(data). Defaults to None.
    cmap : matplotlib colormap | (colormap, bool) | 'interactive' | None
        Colormap to use. If tuple, the first value indicates the colormap to
        use and the second value is a boolean defining interactivity. In
        interactive mode the colors are adjustable by clicking and dragging the
        colorbar with left and right mouse button. Left mouse button moves the
        scale up and down and right mouse button adjusts the range. Hitting
        space bar resets the range. Up and down arrows can be used to change
        the colormap. If None, 'Reds' is used for all positive data,
        otherwise defaults to 'RdBu_r'. If 'interactive', translates to
        (None, True). Defaults to 'RdBu_r'.
        .. warning::  Interactive mode works smoothly only for a small amount
                      of topomaps.
    sensors : bool | str
        Add markers for sensor locations to the plot. Accepts matplotlib
        plot format string (e.g., 'r+' for red plusses). If True (default),
        circles  will be used.
    colorbar : bool
        Plot a colorbar.
    title : str | None
        Title to use.
    show : bool
        Show figure if True.
    contours : int | array of float
        The number of contour lines to draw. If 0, no contours will be drawn.
        When an integer, matplotlib ticker locator is used to find suitable
        values for the contour thresholds (may sometimes be inaccurate, use
        array for accuracy). If an array, the values represent the levels for
        the contours. Defaults to 6.
    image_interp : str
        The image interpolation to be used. All matplotlib options are
        accepted.
    inst : Raw | Epochs | None
        To be able to see component properties after clicking on component
        topomap you need to pass relevant data - instances of Raw or Epochs
        (for example the data that ICA was trained on). This takes effect
        only when running matplotlib in interactive mode.
    plot_std : bool | float
        Whether to plot standard deviation in ERP/ERF and spectrum plots.
        Defaults to True, which plots one standard deviation above/below.
        If set to float allows to control how many standard deviations are
        plotted. For example 2.5 will plot 2.5 standard deviation above/below.
    topomap_args : dict | None
        Dictionary of arguments to ``plot_topomap``. If None, doesn't pass any
        additional arguments. Defaults to None.
    image_args : dict | None
        Dictionary of arguments to ``plot_epochs_image``. If None, doesn't pass
        any additional arguments. Defaults to None.
    psd_args : dict | None
        Dictionary of arguments to ``psd_multitaper``. If None, doesn't pass
        any additional arguments. Defaults to None.
    reject : 'auto' | dict | None
        Allows to specify rejection parameters used to drop epochs
        (or segments if continuous signal is passed as inst).
        If None, no rejection is applied. The default is 'auto',
        which applies the rejection parameters used when fitting
        the ICA object.
    p : int
        Number of topomaps per plot figure
    ncols: int
        Number of columns for topomaps in a figure
    
    Returns
    -------
    fig : instance of matplotlib.figure.Figure or list
        The figure object(s).
    Notes
    -----
    When run in interactive mode, ``plot_ica_components`` allows to reject
    components by clicking on their title label. The state of each component
    is indicated by its label color (gray: rejected; black: retained). It is
    also possible to open component properties by clicking on the component
    topomap (this option is only available when the ``inst`` argument is
    supplied).
    """

    if ica.info is None:
        raise RuntimeError('The ICA\'s measurement info is missing. Please '
                           'fit the ICA or add the corresponding info object.')

    topomap_args = dict() if topomap_args is None else topomap_args
    topomap_args = copy.copy(topomap_args)
    if 'sphere' not in topomap_args:
        topomap_args['sphere'] = sphere
    if picks is None:  # plot components by sets of p
        ch_type = _get_ch_type(ica, ch_type)
        n_components = ica.mixing_matrix_.shape[1]
        figs = []
        for k in range(0, n_components, p):
            picks = range(k, min(k + p, n_components))
            fig = plot_ica_components(ica, picks=picks, ch_type=ch_type,
                                      res=res, vmax=vmax,
                                      cmap=cmap, sensors=sensors,
                                      colorbar=colorbar, title=title,
                                      show=show, outlines=outlines,
                                      contours=contours,
                                      image_interp=image_interp, inst=inst,
                                      plot_std=plot_std,
                                      topomap_args=topomap_args,
                                      image_args=image_args,
                                      psd_args=psd_args, reject=reject,
                                      sphere=sphere,ncols=ncols)
            figs.append(fig)
        return figs
    else:
        picks = _picks_to_idx(ica.info, picks)
    ch_type = _get_ch_type(ica, ch_type)

    cmap = _setup_cmap(cmap, n_axes=len(picks))
    data = np.dot(ica.mixing_matrix_[:, picks].T,
                  ica.pca_components_[:ica.n_components_])

    data_picks, pos, merge_channels, names, _, sphere, clip_origin = \
        _prepare_topomap_plot(ica, ch_type, sphere=sphere)
    outlines = _make_head_outlines(sphere, pos, outlines, clip_origin)

    data = np.atleast_2d(data)
    data = data[:, data_picks]

    # prepare data for iteration
    fig, axes, _, _ = _prepare_trellis(len(data), ncols=ncols)
    if title is None:
        title = 'Components'
    fig.suptitle(title)

    titles = list()
    for ii, data_, ax in zip(picks, data, axes):
        kwargs = dict(color='gray') if ii in ica.exclude else dict()
        titles.append(ax.set_title(ica._ica_names[ii], fontsize=12, **kwargs))
        if merge_channels:
            data_, names_ = _merge_ch_data(data_, ch_type, names.copy())
        vmin_, vmax_ = _setup_vmin_vmax(data_, vmin, vmax)
        im = plot_topomap(
            data_.flatten(), pos, vmin=vmin_, vmax=vmax_, res=res, axes=ax,
            cmap=cmap[0], outlines=outlines, contours=contours,
            image_interp=image_interp, show=False, sensors=sensors)[0]
        im.axes.set_label(ica._ica_names[ii])
        if colorbar:
            cbar, cax = _add_colorbar(ax, im, cmap, title="AU",
                                      side="right", pad=.05, format='%3.2f')
            cbar.ax.tick_params(labelsize=12)
            cbar.set_ticks((vmin_, vmax_))
        _hide_frame(ax)
    del pos
    tight_layout(fig=fig)
    fig.subplots_adjust(top=0.88, bottom=0.)
    fig.canvas.draw()
    # add title selection interactivity
    def onclick_title(event, ica=ica, titles=titles):
        # check if any title was pressed
        title_pressed = None
        for title in titles:
            if title.contains(event)[0]:
                title_pressed = title
                break
        # title was pressed -> identify the IC
        if title_pressed is not None:
            label = title_pressed.get_text()
            ic = int(label[-3:])
            # add or remove IC from exclude depending on current state
            if ic in ica.exclude:
                ica.exclude.remove(ic)
                title_pressed.set_color('k')
            else:
                ica.exclude.append(ic)
                title_pressed.set_color('gray')
            fig.canvas.draw()
    fig.canvas.mpl_connect('button_press_event', onclick_title)

    # add plot_properties interactivity only if inst was passed
    if isinstance(inst, (BaseRaw, BaseEpochs)):
        def onclick_topo(event, ica=ica, inst=inst):
            # check which component to plot
            if event.inaxes is not None:
                label = event.inaxes.get_label()
                if label.startswith('ICA'):
                    ic = int(label[-3:])
                    ica.plot_properties(inst, picks=ic, show=True,
                                        plot_std=plot_std,
                                        topomap_args=topomap_args,
                                        image_args=image_args,
                                        psd_args=psd_args, reject=reject)
        fig.canvas.mpl_connect('button_press_event', onclick_topo)

    plt_show(show)
    return fig


def createRaw(signal,sfreq,ch_types='eeg',ch_names=None):
    """Creates an mne.io.raw object given some parameters.
    Parameters
    ----------
    signal : np.ndarray
        Signal with the shape of (channels,samples)
    sfreq : float
        The sampling frequency of the signal.
    ch_types: str or list of strings, default='eeg'
        The types of all or each of the channels.
        See mne.create_info documentation.
    ch_names : list of str, default=None
        The names of the sensors/channels.
    Returns
    -------
    signals : mne.io.raw instance of the signal
    """
    if signal.ndim == 1:
        signal = np.reshape(signal,(1,len(signal)),order='F')
    if ch_names is None:
        ch_names = signal.shape[0]
    signals = mne.io.RawArray(signal, mne.create_info(ch_names=ch_names, ch_types=ch_types,sfreq=sfreq),verbose=False)
    return signals

def chn_name_mapping(ch_name):
    """
    Map channel names to fit standard naming convention.
    This code is from NeuroDataDesign Standford pyprep Implementation

    Parameters:
        ch_name: string
            channel name to fit

    Returns_
        ch_name: string
            channel name fitted
    """
    ch_name = ch_name.strip('.')
    ch_name = ch_name.upper()
    if 'Z' in ch_name:
        ch_name = ch_name.replace('Z', 'z')
    
    if 'FP' in ch_name:
        ch_name = ch_name.replace('FP', 'Fp')
    
    return ch_name

def topomap(A,W,n_components,info,cmap='plasma',show=False,title=None,labels=None):
    """Gets the topomap of all the components in
    a given spatial filter.
    Parameters
    ----------
    A : np.ndarray
        The mixing matrix of the spatial filter.
    W : np.ndarray
        The unmixing matrix of the spatial filter.
    n_components: int
        Number of components of the spatial filter.
        Ie A.shape[0]
    info : mne.Info instance
        The metadata of the eeg recording needed
        to create a mne.io.raw objetct.
    cmap: string, default='plasma'
        String of the colormap to use to plot
        the topomap.
        See matplotlib colormaps documentation.
    show: bool, default=False
        Whether to plot or not.
    title: string, default=None
        The desired title of the topomap.
    labels: list of strings, default=None
        The labels of each of the components.
        If None components will be numbered
        from 1 and labeled as compX.
    Returns
    -------
    figs : matplotlib.pyplot.figure or list of it
        The figure(s) with the topomap required

    Note:
        You may or may not need to tranpose A and W,
        just check which gets the obvious correct result
    Example:
    >>>import models.eegflow.utils as us
    >>>import matplotlib.pyplot as plt
    >>>ch_names = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8', 'FC5', 'FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'FC6', 'T7', 'C5', 'C3', 'C1', 'CZ', 'C2', 'C4', 'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4', 'CP6', 'TP8', 'P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'O1', 'OZ', 'O2']
    >>>ch_names = [us.chn_name_mapping(x) for x in ch_names]
    >>>dummy = np.zeros((len(ch_names),1000))
    >>>sfreq = 250
    >>>montage_kind = 'standard_1020'
    >>>raw = us.createRaw(dummy,sfreq,'eeg',ch_names)
    >>>raw.set_montage(montage_kind)
    >>>A,W = us.get_spatial_filter()
    >>>comp = 25
    >>>A_ = np.expand_dims(A[:,comp-1],axis=-1)
    >>>W_ = np.expand_dims(W[comp-1,:],axis=0)
    >>>figSingle = us.topomap(A_,W_,A_.shape[0],raw.info,cmap='seismic',show=True)
    >>>figMany = us.topomap(A,W,A.shape[0],raw.info,cmap='seismic',show=True)
    """
    ica = ICA(random_state=97, method = 'fastica')
    ica.info = info
    ica.n_components_= n_components
    ica.unmixing_matrix_ = W
    ica.pca_components_ = np.eye(n_components) #transformer.whitening_#np.linalg.pinv(transformer.whitening_)
    ica.mixing_matrix_ = A
    ica._update_ica_names()

    if labels is None:
        labels = [str('comp'+str(i+1)) for i in range(A.shape[1])]

    ica._ica_names = labels
    #figs = ica.plot_components(cmap=cmap,show=False)
    ncols = int(np.floor(np.sqrt(A.shape[1])))
    
    figs = plot_ica_components(ica,p=A.shape[1],ncols=ncols,cmap=cmap)
    if title is not None:
        for fig in figs:
            fig.suptitle(title)
    else:
        for fig in figs:
            fig.suptitle('')

    # Reverse labels and pop consecutively
    
    # labels.reverse()
    # for fig in figs:
    #     for ax in fig.axes:
    #         #ax.set_label(labels.pop())
    #         idx0 = figs.index(fig)
    #         idx = fig.axes.index(ax)
    #         figs[idx0].axes[idx].set_title(labels.pop(),y=1.08)
    #     fig.subplots_adjust(top=0.88, bottom=0.)
    #     fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    #     fig.canvas.draw()
    if show:
        plt.show()
    return figs



def our_topomap(A,W,ch_names,comp=None,colormap='seismic'):
    """Gets the topomap of a component or a set
    of components given by the default spatial
    filter.
    Parameters
    ----------
    comp : string of list of string
        Components required in the following notation
        compX where X is the number of the component
        counting from 1.
    colormap: string, default='seismic'
        String of the colormap to use to plot
        the topomap.
        See matplotlib colormaps documentation.
    Returns
    -------
    figs : matplotlib.pyplot.figure or list of it
        The figure(s) with the topomap required
    """

    ch_names = [chn_name_mapping(x) for x in ch_names]
    dummy = np.zeros((len(ch_names),1))
    sfreq = 250
    montage_kind = 'standard_1020'
    raw = createRaw(dummy,sfreq,'eeg',ch_names)
    raw.set_montage(montage_kind)
    if comp is not None and type(comp) != list:
        label = comp
        comp = comp.replace('comp','')
        comp = int(comp)
        A_ = np.expand_dims(A[:,comp-1],axis=-1)
        W_ = np.expand_dims(W[comp-1,:],axis=0)
        figs = topomap(A_,W_,A_.shape[0],raw.info,cmap=colormap,show=False,labels=as_list(label))
    elif type(comp) == list :
        if len(comp) == 0:
            return None
        labels = comp
        comp = [int(c.replace('comp','')) -1  for c in labels]
        if len(comp)==1:
            comp = comp[0]
            A_ = np.expand_dims(A[:,comp-1],axis=-1)
            W_ = np.expand_dims(W[comp-1,:],axis=0)
        else:
            A_ = A[:,comp]
            W_ = W[comp,:]
        figs = topomap(A_,W_,A_.shape[0],raw.info,cmap=colormap,show=False,labels=as_list(labels))
    else:
        labels = ['comp'+str(i) for i in range(A.shape[1])]
        figs = topomap(A,W,A.shape[0],raw.info,cmap=colormap,show=False,labels=labels)

    return figs


