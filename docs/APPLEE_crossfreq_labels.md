# Using APPLEE with the corrected PME (cross-frequency)

APPLEE (https://github.com/GNACo/APPLEE) imports `_get_pme` from this package. Two things to take into account until APPLEE is updated:

1. **Install `sovaharmony` from this repository, not from the commit pinned by APPLEE.** APPLEE's `requirements.txt` pins `sovaharmony` at commit `ff023b89`, which contains the inverted loops. After installing APPLEE's requirements, run:

   ```bash
   pip install --force-reinstall --no-deps "git+https://github.com/GRUNECO/eeg_harmonization.git@main#egg=sovaharmony"
   ```

2. **Column names.** `Amplitude_Modulation_Analysis` returns `pme[signal, i, j]` with `i` = modulation band and `j` = carrier sub-band (bands in ascending order, Delta ... Gamma). In the unmodified `APPLEE/ld_postprocessing.py` (about lines 221-230) the first axis is written as `Band` and the second as `M<band>`. Therefore, with the unmodified APPLEE, a column `Sensor_X/MY` means **X = modulation band, Y = carrier band**, and the corrected PME only exists for X at or below Y in frequency (for example `O2_Delta/MGamma`). Before the correction the columns had the opposite order (`Sensor_Gamma/MDelta`), and their values were the ones computed for the wrong triangle.

   To name the columns with the carrier first (`Sensor_Carrier/MModulation`), change in `ld_postprocessing.py`:

   ```python
   # before
   'Band': band,
   'Mband': f'M{band1}',
   # after
   'Band': band1,        # carrier sub-band (j)
   'Mband': f'M{band}',  # modulation band (i)
   ```

If you used the cross-frequency features from the previous version in a study, re-run the feature extraction after updating.
