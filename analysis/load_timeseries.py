"""
analysis/load_timeseries.py
Generic loader for time-series datasets in CSV/JSON/NPZ.
"""
from __future__ import annotations
import json, os
import numpy as np
import pandas as pd
from typing import Tuple, List

def load_timeseries(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(path)
        cols = list(df.columns)
        tcol = None
        for cand in ["time","t","Time","TIME","timestamp","Timestamp"]:
            if cand in cols:
                tcol = cand
                break
        if tcol is None:
            raise ValueError("CSV must include a time column (e.g., 'time').")
        t = df[tcol].to_numpy(dtype=float)
        xcols = [c for c in cols if c != tcol]
        if not xcols:
            raise ValueError("CSV must contain at least one data column besides time.")
        X = df[xcols].to_numpy(dtype=float)
        return t, X, xcols
    elif ext == ".json":
        with open(path, "r") as f:
            obj = json.load(f)
        t = np.asarray(obj["time"], dtype=float)
        X = np.asarray(obj["data"], dtype=float)
        if X.ndim == 1:
            X = X[:,None]
        colnames = obj.get("colnames", [f"ch{i+1}" for i in range(X.shape[1])])
        return t, X, colnames
    elif ext == ".npz":
        npz = np.load(path)
        t = np.asarray(npz["time"], dtype=float)
        X = np.asarray(npz["data"], dtype=float)
        if X.ndim == 1:
            X = X[:,None]
        colnames = [f"ch{i+1}" for i in range(X.shape[1])]
        return t, X, colnames
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
