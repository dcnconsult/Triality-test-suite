"""
analysis/run_timetags.py
Convert time-tag event lists to binned time series and compute bicoherence.
"""
import os, argparse, numpy as np
from analysis.event_binning import load_event_times, bin_events
from analysis.bispectrum import cross_bispectrum
from analysis.plot_bispec_with_peak import plot as plot_annot
from analysis.bispec_peaks import find_bicoherence_peak

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="JSON/CSV/NPZ with ch1/ch2/ch3 event times (s)")
    ap.add_argument("--fs", type=float, default=1e6, help="binning sample rate (Hz)")
    ap.add_argument("--T", type=float, default=None, help="duration seconds; if omitted, derived")
    ap.add_argument("--seglen", type=int, default=131072, help="FFT length for bispectrum")
    ap.add_argument("--outdir", type=str, default="/mnt/data/timetag_bispec")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    ch_times = load_event_times(args.path)
    t, X = bin_events(ch_times, fs=args.fs, T=args.T)
    fs = args.fs

    # Compute cross-bispectrum on three channels
    f, Sxyz, b2 = cross_bispectrum(X[:,0], X[:,1], X[:,2], fs, seglen=args.seglen, step=None)
    peak = find_bicoherence_peak(b2, f)
    np.savez(os.path.join(args.outdir, "timetag_bispec.npz"), f=f, b2=b2, peak=list(peak.items()))
    plot_annot(f, b2, peak, f3_est=None, outpng=os.path.join(args.outdir, "timetag_bicoherence.png"))
    print("Peak:", peak)

if __name__ == "__main__":
    main()
