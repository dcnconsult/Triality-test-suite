"""
analysis/run_jpc.py
Load a JPC config (JSON) and invoke the bispectrum CLI with correct columns.
"""
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"
DEFAULT_CFG = PROJECT_ROOT / "analysis" / "configs" / "jpc_run_15.json"
DEFAULT_OUTDIR = OUT_DIR / "jpc_plots"


def _resolve_path(value):
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def main(cfg_path=DEFAULT_CFG):
    cfg_path = _resolve_path(cfg_path)
    with open(cfg_path, "r") as f:
        cfg = json.load(f)

    data_path = _resolve_path(cfg["path"])
    channels = ",".join(cfg.get("channels", []))
    seglen = str(cfg.get("seglen", 4096))
    step = cfg.get("step", None)
    outdir = _resolve_path(cfg.get("outdir", DEFAULT_OUTDIR))
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "analysis.run_bispec",
        "--path",
        str(data_path),
        "--seglen",
        seglen,
        "--outdir",
        str(outdir),
    ]
    if channels:
        cmd += ["--channels", channels]
    if step is not None:
        cmd += ["--step", str(step)]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CFG
    main(cfg)
