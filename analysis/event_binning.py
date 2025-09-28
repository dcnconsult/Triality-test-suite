"""
analysis/event_binning.py
Utilities to convert photon time-tag event lists into binned time series suitable
for bispectral analysis.

Supported inputs:
- CSV/JSON/NPZ with arrays/lists of event times (seconds) per channel.
  * JSON: {"ch1":[t...], "ch2":[...], "ch3":[...]}
  * NPZ: arrays "ch1","ch2","ch3" with event times (float seconds)
  * CSV: columns ch1, ch2, ch3 with event times per row (NaNs allowed)

Output:
- time vector t (centers), and counts per bin for each channel (shape N x C)
"""
import os, json
import numpy as np
import pandas as pd

def load_event_times(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r") as f:
            obj = json.load(f)
        # Accept both ch1/ch2/ch3 and ch_signal/ch_idler/ch_sum
        keys = []
        lowered = {k.lower(): k for k in obj.keys()}
        for want in ["ch1","ch2","ch3","ch_signal","ch_idler","ch_sum"]:
            if want in lowered:
                keys.append(lowered[want])
        if not keys:
            # fallback: any keys starting with ch
            keys = [k for k in obj if k.lower().startswith("ch")]
        chs = [obj[k] for k in keys]
        return [np.asarray(ch, dtype=float) for ch in chs]
    elif ext == ".npz":
        npz = np.load(path)
        chs = []
        for k in ["ch1","ch2","ch3"]:
            if k in npz:
                chs.append(np.asarray(npz[k], dtype=float))
        if not chs:
            raise ValueError("NPZ must contain ch1/ch2/ch3 arrays of event times.")
        return chs
    elif ext == ".csv":
        df = pd.read_csv(path)
        chs = []
        for k in ["ch1","ch2","ch3"]:
            if k in df.columns:
                chs.append(df[k].dropna().to_numpy(dtype=float))
        if not chs:
            raise ValueError("CSV must have ch1/ch2/ch3 columns with event times.")
        return chs
    else:
        raise ValueError(f"Unsupported extension: {ext}")

def bin_events(ch_times, fs=1e6, T=None, t0=None):
    """
    Bin event times into counts per bin.
    fs: sampling rate for bins (Hz); default 1 MHz bins
    T: total duration (seconds); if None, deduced from max event
    t0: start time; default min event
    Returns t (N,), X (N,C)
    """
    if not ch_times:
        raise ValueError("No channels provided")
    all_times = np.concatenate(ch_times)
    if t0 is None:
        t0 = float(np.nanmin(all_times))
    if T is None:
        T = float(np.nanmax(all_times) - t0)
    N = int(np.ceil(T * fs))
    edges = t0 + np.arange(N+1)/fs
    X = []
    for arr in ch_times:
        idx = np.clip(((arr - t0) * fs).astype(int), 0, N-1)
        counts = np.bincount(idx, minlength=N)
        X.append(counts.astype(float))
    X = np.stack(X, axis=1)  # (N,C)
    t = 0.5*(edges[:-1] + edges[1:])
    return t, X
