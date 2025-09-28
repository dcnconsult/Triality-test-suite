"""
analysis/run_jpc.py
Load a JPC config (JSON) and invoke the bispectrum CLI with correct columns.
"""
import os, json, subprocess, sys

def main(cfg_path="analysis/configs/jpc_run_15.json"):
    with open(cfg_path, "r") as f:
        cfg = json.load(f)
    path = cfg["path"]
    channels = ",".join(cfg.get("channels", []))
    seglen = str(cfg.get("seglen", 4096))
    step = cfg.get("step", None)
    outdir = cfg.get("outdir", "/mnt/data/jpc_plots")
    cmd = ["python", "-m", "analysis.run_bispec", "--path", path, "--seglen", seglen, "--outdir", outdir]
    if channels:
        cmd += ["--channels", channels]
    if step is not None:
        cmd += ["--step", str(step)]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)

if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "analysis/configs/jpc_run_15.json"
    main(cfg)
