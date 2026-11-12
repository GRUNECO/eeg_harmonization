"""
Regression test: band filters in permutation entropy and synchronization likelihood must not be applied in place.

mne's Epochs/Raw.filter() modifies the object it is called on. get_entropy_freq (p_entropy.py) and get_sl_1band (sl.py)
used to call signal.filter(fmin, fmax) directly, and features._get_entropy / features._get_sl call them once per band on
the same object. The band filters therefore accumulated: Delta was correct, but every later band was computed on the
residual left by the previous filters (variance about 1e-10 of the original after eight bands).

Checks:
  1. the signal passed in is not modified;
  2. the value of a band does not depend on which bands were computed before it.

Run:  python tests/test_band_filter_not_in_place.py     (needs numpy, scipy, mne and the sovaharmony dependencies)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import mne  # noqa: E402

from sovaharmony.metrics.p_entropy import get_entropy_freq  # noqa: E402
from sovaharmony.metrics.sl import get_sl_1band  # noqa: E402

mne.set_log_level('ERROR')

BANDS = {'Delta': (1.5, 6), 'Theta': (6, 8.5), 'Alpha-1': (8.5, 10.5), 'Alpha-2': (10.5, 12.5),
         'Beta1': (12.5, 18.5), 'Beta2': (18.5, 21), 'Beta3': (21, 30), 'Gamma': (30, 40)}
SF = 200.0


def make_epochs(seed=0, n_epochs=6, n_ch=4, seconds=5):
    rng = np.random.default_rng(seed)
    n = int(SF * seconds)
    t = np.arange(n) / SF
    data = np.zeros((n_epochs, n_ch, n))
    for e in range(n_epochs):
        for c in range(n_ch):
            data[e, c] = (rng.standard_normal(n)
                          + 2.0 * np.sin(2 * np.pi * 4 * t + rng.uniform(0, 6.28))
                          + 1.5 * np.sin(2 * np.pi * 10 * t + rng.uniform(0, 6.28))
                          + 1.0 * np.sin(2 * np.pi * 16 * t + rng.uniform(0, 6.28))
                          + 0.5 * np.sin(2 * np.pi * 35 * t + rng.uniform(0, 6.28)))
    data *= 1e-5
    return mne.EpochsArray(data, mne.create_info([f'ch{i}' for i in range(n_ch)], SF, 'eeg'), verbose=False)


def sl_value(m):
    return float(np.mean([np.mean(m[i]) for i in range(m.shape[0])]))


def test_input_not_modified():
    for name, fn in (('entropy', lambda s, lo, hi: get_entropy_freq(s, fmin=lo, fmax=hi, D=3)),
                     ('sl', lambda s, lo, hi: get_sl_1band(s, lo, hi))):
        ep = make_epochs()
        before = ep.get_data().copy()
        fn(ep, 6, 8.5)
        assert np.array_equal(before, ep.get_data()), f'{name}: the input signal was modified in place'
    print('PASS  test_input_not_modified')


def test_band_value_independent_of_previous_bands():
    base = make_epochs()
    # entropy
    shared = base.copy()
    cumulative = {b: float(np.mean(get_entropy_freq(shared, fmin=lo, fmax=hi, D=3))) for b, (lo, hi) in BANDS.items()}
    for b, (lo, hi) in BANDS.items():
        alone = float(np.mean(get_entropy_freq(base.copy(), fmin=lo, fmax=hi, D=3)))
        assert abs(alone - cumulative[b]) < 1e-12, f'entropy {b}: {alone} (alone) vs {cumulative[b]} (after other bands)'
    # synchronization likelihood
    shared = base.copy()
    cumulative = {b: sl_value(get_sl_1band(shared, lo, hi)) for b, (lo, hi) in BANDS.items()}
    for b, (lo, hi) in BANDS.items():
        alone = sl_value(get_sl_1band(base.copy(), lo, hi))
        assert abs(alone - cumulative[b]) < 1e-9, f'sl {b}: {alone} (alone) vs {cumulative[b]} (after other bands)'
    print('PASS  test_band_value_independent_of_previous_bands')


if __name__ == '__main__':
    test_input_not_modified()
    test_band_value_independent_of_previous_bands()
