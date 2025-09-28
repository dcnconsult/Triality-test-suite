"""
analysis/run_bispec.py
CLI to load time series and compute bicoherence.
"""
import os, argparse, numpy as np, matplotlib.pyplot as plt
from analysis.load_timeseries import load_timeseries
from analysis.bispectrum import bispectrum, cross_bispectrum

def plot_bicoherence(f, b2, outpng):
    plt.figure()
    plt.imshow(b2, origin="lower", extent=[f[0], f[-1], f[0], f[-1]], aspect="auto")
    plt.xlabel("f1 (Hz)")
    plt.ylabel("f2 (Hz)")
    plt.title("Bicoherence b^2(f1,f2)")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(outpng, dpi=160)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--fs", type=float, default=None)
    ap.add_argument("--seglen", type=int, default=2048)
    ap.add_argument("--step", type=int, default=None)
    ap.add_argument("--channels", type=str, default="")
    ap.add_argument("--outdir", type=str, default="/mnt/data/bispec_plots")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    t, X, cols = load_timeseries(args.path)
    if args.fs is None:
        dt = np.median(np.diff(t)); fs = 1.0/dt
    else:
        fs = args.fs

    if args.channels:
        sel = []
        for tok in args.channels.split(","):
            tok = tok.strip()
            if tok.isdigit():
                sel.append(int(tok))
            else:
                sel.append(cols.index(tok))
    else:
        sel = list(range(min(3, X.shape[1])))

    f, S3, b2 = bispectrum(X[:, sel[0]], fs, seglen=args.seglen, step=args.step)
    np.savez(os.path.join(args.outdir, "bispec_uni.npz"), f=f, S3=S3, b2=b2)
    plot_bicoherence(f, b2, os.path.join(args.outdir, "bicoherence_uni.png"))

    if len(sel) >= 3:
        f, Sxyz, b2xyz = cross_bispectrum(X[:, sel[0]], X[:, sel[1]], X[:, sel[2]], fs, seglen=args.seglen, step=args.step)
        np.savez(os.path.join(args.outdir, "bispec_cross.npz"), f=f, Sxyz=Sxyz, b2=b2xyz)
        plot_bicoherence(f, b2xyz, os.path.join(args.outdir, "bicoherence_cross.png"))

    print("Wrote bicoherence outputs to", args.outdir)

if __name__ == "__main__":
    main()
