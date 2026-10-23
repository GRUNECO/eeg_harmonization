"""
Synthetic test of the PME (cross-frequency) triangle in sovaharmony/metrics/pme.py.

Output axes of Amplitude_Modulation_Analysis: pme[signal, M_band i, band j] with bands in ASCENDING order
(Delta ... Gamma). i = modulation band, j = carrier sub-band. Valid cells: i <= j (modulation slower than or equal to
the carrier band); the cells with i > j stay at 0.

Run:  python tests/test_pme_triangle.py     (needs numpy, scipy, mne)
"""
import contextlib
import importlib.util
import io
import os
import sys
import types

import numpy as np

try:                                    # pme.py imports sovaflow.utils.createRaw; it is not used by this test
    import sovaflow.utils  # noqa: F401
except Exception:
    _sf, _sfu = types.ModuleType('sovaflow'), types.ModuleType('sovaflow.utils')
    _sfu.createRaw = lambda *a, **k: None
    sys.modules['sovaflow'], sys.modules['sovaflow.utils'] = _sf, _sfu

# load pme.py by path so that the whole package (and its heavy imports) is not needed
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sovaharmony', 'metrics', 'pme.py')
_spec = importlib.util.spec_from_file_location('pme', _path)
pme = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(pme)

BANDS = [(1.5, 6), (6, 8.5), (8.5, 10.5), (10.5, 12.5), (12.5, 18.5), (18.5, 21), (21, 30), (30, 40)]
FS, N_EP, T = 200, 24, 1000


def am_signal(carrier_hz, mod_hz, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(T * N_EP) / FS
    x = rng.standard_normal((1, T * N_EP)) * 0.3
    x += (1 + 0.9 * np.sin(2 * np.pi * mod_hz * t)) * np.sin(2 * np.pi * carrier_hz * t)
    return x.reshape(1, N_EP, T).transpose(0, 2, 1)          # (channels, samples, epochs)


def run(sig, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return np.asarray(pme.Amplitude_Modulation_Analysis(sig, FS, Bands=BANDS, **kw))[0]


def test_gamma_carrier_delta_modulation():
    p = run(am_signal(35, 4))
    assert p[0, 7] > 50                      # modulation Delta (i=0) of the Gamma carrier (j=7)
    assert np.unravel_index(np.argmax(p), p.shape) == (0, 7)


def test_lower_triangle_is_empty_and_sums_to_100():
    p = run(am_signal(11.5, 3))
    assert np.tril(p, -1).sum() == 0
    assert np.count_nonzero(p) == 36
    assert abs(p.sum() - 100) < 1e-6


def test_hamming_method_same_triangle():
    p = run(am_signal(35, 4), Method='hamming')
    assert np.tril(p, -1).sum() == 0 and p[0, 7] > 0


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print('PASS ', name)
