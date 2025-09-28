"""
analysis/plot_bispec_with_peak.py
Plot bicoherence heatmap with peak annotation and sum-frequency line.
"""
import os, numpy as np, matplotlib.pyplot as plt

def plot(f, b2, peak, f3_est=None, outpng="bicoherence_annotated.png"):
    plt.figure()
    plt.imshow(b2, origin="lower", extent=[f[0], f[-1], f[0], f[-1]], aspect="auto")
    plt.xlabel("f1 (Hz)"); plt.ylabel("f2 (Hz)"); plt.title("Bicoherence with peak")
    cbar = plt.colorbar(); cbar.set_label("b^2")
    # Peak
    plt.scatter([peak["f1"]], [peak["f2"]], s=60, marker="x")
    plt.text(peak["f1"], peak["f2"], f'  peak={peak["b2_peak"]:.3f}', color="white")
    # Sum line (optional): f1+f2 = f3_est
    if f3_est is not None:
        xs = np.linspace(f[0], f[-1], 400)
        ys = f3_est - xs
        plt.plot(xs, ys, linestyle="--")
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpng), exist_ok=True)
    plt.savefig(outpng, dpi=160); plt.close()
