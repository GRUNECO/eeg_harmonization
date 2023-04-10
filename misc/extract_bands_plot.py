# Import numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Import the FOOOF object
from fooof import FOOOF

# Import simulation, utility, and plotting tools
from fooof.bands import Bands
from fooof.utils import trim_spectrum
from fooof.analysis import get_band_peak_fm
from fooof.sim.gen import gen_power_spectrum
from fooof.sim.utils import set_random_seed
from fooof.plts.spectra import plot_spectra_shading

def compare_exp(fm1, fm2):
    """Compare exponent values."""

    exp1 = fm1.get_params('aperiodic_params', 'exponent')
    exp2 = fm2.get_params('aperiodic_params', 'exponent')

    return exp1 - exp2

def compare_peak_pw(fm1, fm2, band_def):
    """Compare the power of detected peaks."""

    pw1 = get_band_peak_fm(fm1, band_def)[1]
    pw2 = get_band_peak_fm(fm2, band_def)[1]

    return pw1 - pw2

def compare_band_pw(fm1, fm2, band_def):
    """Compare the power of frequency band ranges."""

    pw1 = np.mean(trim_spectrum(fm1.freqs, fm1.power_spectrum, band_def)[1])
    pw2 = np.mean(trim_spectrum(fm1.freqs, fm2.power_spectrum, band_def)[1])

    return pw1 - pw2

# Set consistent aperiodic parameters
ap_params = [1, 1]

# Set periodic parameters, defined to vary between groups
#   All parameters are set to match, except for systematic power differences
pe_g1 = [[2, 0.25, 1], [6, 0.2, 1], [10, 0.5, 1.5], [20, 0.2, 3], [40, 0.25, 3.5]]
pe_g2 = [[2, 0.5, 1], [6, 0.3, 1], [10, 0.5, 1.5], [20, 0.15, 3], [40, 0.15, 3.5]]

# Set random seed, for consistency generating simulated data
set_random_seed(21)
bands =Bands({'delta':[1.5,6],
        'theta':[6,8.5],
        'alpha-1':[8.5,10.5],
        'alpha-2':[10.5,12.5],
        'beta1':[12.5,18.5],
        'beta2':[18.5,21],
        'beta3':[21,30],
        'gamma':[30,45]})

# Define plot settings
t_settings = {'fontsize' : 24, 'fontweight' : 'bold'}
shade_cols = ['#e8dc35', '#46b870', '#1882d9', '#a218d9', '#e60026']
labels = ['Group-1', 'Group-2']

# General simulation settings
f_range = [1, 50]
nlv = 0
# Simulate example power spectra for each group
freqs, g1_spectrum_bands = gen_power_spectrum(f_range, ap_params, pe_g1, nlv)
freqs, g2_spectrum_bands = gen_power_spectrum(f_range, ap_params, pe_g2, nlv)

# Define some template strings for reporting
exp_template = "The difference of aperiodic exponent is: \t {:1.2f}"
pw_template = ("The difference of {:5} power is  {: 1.2f}\t"
               "with peaks or  {: 1.2f}\t with bands.")

# Plot the power spectra differences, representing the 'band-by-band' idea
plot_spectra_shading(freqs, [g1_spectrum_bands, g2_spectrum_bands],
                     log_powers=True, linewidth=3,
                     shades=bands.definitions, shade_colors=shade_cols,
                     labels=labels)
plt.xlim(f_range);
plt.title('Band-by-Band', t_settings);
plt.xlim(1.5,45)
plt.show()

# Initialize FOOOF objects
fm_bands_g1 = FOOOF(verbose=False)
fm_bands_g2 = FOOOF(verbose=False)

# Fit power spectrum models
fm_bands_g1.fit(freqs, g1_spectrum_bands)
fm_bands_g2.fit(freqs, g2_spectrum_bands)

# Plot the power spectra differences
plot_spectra_shading(freqs, [fm_bands_g1._spectrum_flat, fm_bands_g2._spectrum_flat],
                     log_powers=False, linewidth=3,
                     shades=bands.definitions, shade_colors=shade_cols,
                     labels=labels)
plt.xlim(f_range);
plt.title('Band-by-Band - Flattened', t_settings);
plt.xlim(1.5,45)
plt.show()