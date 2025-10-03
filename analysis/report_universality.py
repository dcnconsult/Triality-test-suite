"""
analysis/report_universality.py
Assemble a short universality report (Markdown) comparing JPC and SPDC results.
Generates detuning curves (if available), peak bicoherence and z-scores,
and summarizes lock coherence times.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "out"

DEFAULT_JPC_CSV = OUT_DIR / "jpc_batch_summary.csv"
DEFAULT_SPDC_CSV = OUT_DIR / "spdc_batch_summary.csv"
DEFAULT_REPORT = OUT_DIR / "universality_report.md"
DEFAULT_PLOTS = OUT_DIR / "universality_plots"


def plot_metric(df, x, y, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.plot(df[x], df[y], marker="o")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()


def _to_markdown_path(path):
    path = Path(path)
    try:
        rel = path.relative_to(PROJECT_ROOT)
        return rel.as_posix()
    except ValueError:
        return path.as_posix()


def include_detuning_aggregates(out_dir=DEFAULT_PLOTS, lines=None):
    if lines is None:
        lines = []
    out_dir = Path(out_dir)
    lines.append("\n## Detuning comparison\n")
    jpng = out_dir / "jpc_metrics_vs_detuning.png"
    spng = out_dir / "spdc_metrics_vs_detuning.png"
    if jpng.exists():
        lines.append(f"![JPC metrics vs detuning]({_to_markdown_path(jpng)})\n")
    if spng.exists():
        lines.append(f"![SPDC metrics vs detuning]({_to_markdown_path(spng)})\n")
    return lines


def main(jpc_csv=DEFAULT_JPC_CSV, spdc_csv=DEFAULT_SPDC_CSV,
         out_md=DEFAULT_REPORT, out_dir=DEFAULT_PLOTS,
         run_detuning=True):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Triality Universality Report\n",
        "\n*Auto-generated via detuning aggregate and batch summaries.*\n",
    ]

    jpc_path = Path(jpc_csv)
    spdc_path = Path(spdc_csv)

    jdf = pd.read_csv(jpc_path) if jpc_path.exists() else None
    sdf = pd.read_csv(spdc_path) if spdc_path.exists() else None

    if jdf is not None:
        lines.append("## JPC Summary\n")
        lines.append(f"- Files: {len(jdf)}\n")
        if "detuning" in jdf.columns:
            plot_metric(jdf, "detuning", "b2_peak", out_dir / "jpc_b2_vs_detuning.png")
            lines.append(f"![JPC b2 vs detuning]({_to_markdown_path(out_dir / 'jpc_b2_vs_detuning.png')})\n")
            plot_metric(jdf, "detuning", "peak_z", out_dir / "jpc_z_vs_detuning.png")
            lines.append(f"![JPC z vs detuning]({_to_markdown_path(out_dir / 'jpc_z_vs_detuning.png')})\n")
        lines.append(f"- Max JPC b2_peak: {jdf['b2_peak'].max():.3f}\n")
        lines.append(
            f"- Max JPC coherence time >=0.5: {jdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n"
        )

    if sdf is not None:
        lines.append("\n## SPDC Summary\n")
        lines.append(f"- Files: {len(sdf)}\n")
        if "detuning" in sdf.columns:
            plot_metric(sdf, "detuning", "b2_peak", out_dir / "spdc_b2_vs_detuning.png")
            lines.append(f"![SPDC b2 vs detuning]({_to_markdown_path(out_dir / 'spdc_b2_vs_detuning.png')})\n")
            plot_metric(sdf, "detuning", "peak_z", out_dir / "spdc_z_vs_detuning.png")
            lines.append(f"![SPDC z vs detuning]({_to_markdown_path(out_dir / 'spdc_z_vs_detuning.png')})\n")
        lines.append(f"- Max SPDC b2_peak: {sdf['b2_peak'].max():.3f}\n")
        lines.append(
            f"- Max SPDC coherence time >=0.5: {sdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n"
        )

    if run_detuning:
        try:
            import analysis.detuning_aggregate as dagg

            dagg.main(
                jpc_csv=jpc_path,
                spdc_csv=spdc_path,
                out_csv=OUT_DIR / "detuning_aggregated.csv",
                out_dir=out_dir,
            )
            lines = include_detuning_aggregates(out_dir=out_dir, lines=lines)
        except ImportError:
            print("Skipping detuning aggregate plots: 'analysis.detuning_aggregate' not found.")
        except Exception as exc:
            print(f"Could not run detuning aggregate: {exc}")

    out_md = Path(out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote report:", out_md)


if __name__ == "__main__":
    main()
