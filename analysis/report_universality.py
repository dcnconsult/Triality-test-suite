"""
analysis/report_universality.py
Assemble a short universality report (Markdown) comparing JPC and SPDC results.
Generates detuning curves (if 'detuning' present), peak bicoherence and z-scores,
and summarizes lock coherence times.
"""
import os, pandas as pd, matplotlib.pyplot as plt

def plot_metric(df, x, y, out):
    plt.figure()
    plt.plot(df[x], df[y], marker='o')
    plt.xlabel(x); plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.tight_layout(); plt.savefig(out, dpi=160); plt.close()

def main(jpc_csv="/mnt/data/jpc_batch_summary.csv",
         spdc_csv="/mnt/data/spdc_batch_summary.csv",
         out_md="/mnt/data/universality_report.md",
         out_dir="/mnt/data/universality_plots"):
    os.makedirs(out_dir, exist_ok=True)
    lines = ["# Triality Universality Report\n", "\n*Auto-generated via detuning_aggregate and batch summaries.*\n"]

    jdf = pd.read_csv(jpc_csv) if os.path.exists(jpc_csv) else None
    sdf = pd.read_csv(spdc_csv) if os.path.exists(spdc_csv) else None

    if jdf is not None:
        lines.append("## JPC Summary\n")
        lines.append(f"- Files: {len(jdf)}\n")
        # If detuning present, plot
        if "detuning" in jdf.columns:
            p = os.path.join(out_dir, "jpc_b2_vs_detuning.png")
            plot_metric(jdf, "detuning", "b2_peak", p)
            lines.append(f"![JPC b2 vs detuning]({p})\n")
            pz = os.path.join(out_dir, "jpc_z_vs_detuning.png")
            plot_metric(jdf, "detuning", "peak_z", pz)
            lines.append(f"![JPC z vs detuning]({pz})\n")
        lines.append(f"- Max JPC b2_peak: {jdf['b2_peak'].max():.3f}\n")
        lines.append(f"- Max JPC lock coherence-time ≥0.5: {jdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n")

    if sdf is not None:
        lines.append("\n## SPDC Summary\n")
        lines.append(f"- Files: {len(sdf)}\n")
        if "detuning" in sdf.columns:
            p = os.path.join(out_dir, "spdc_b2_vs_detuning.png")
            plot_metric(sdf, "detuning", "b2_peak", p)
            lines.append(f"![SPDC b2 vs detuning]({p})\n")
            pz = os.path.join(out_dir, "spdc_z_vs_detuning.png")
            plot_metric(sdf, "detuning", "peak_z", pz)
            lines.append(f"![SPDC z vs detuning]({pz})\n")
        lines.append(f"- Max SPDC b2_peak: {sdf['b2_peak'].max():.3f}\n")
        lines.append(f"- Max SPDC lock coherence-time ≥0.5: {sdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n")

    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    print("Wrote report:", out_md)

if __name__ == "__main__":
    main()


def include_detuning_aggregates(out_dir="/mnt/data/universality_plots", lines=None):
    if lines is None: lines = []
    jpng = os.path.join(out_dir, "jpc_metrics_vs_detuning.png")
    spng = os.path.join(out_dir, "spdc_metrics_vs_detuning.png")
    lines.append("\n## Detuning comparison\n")
    if os.path.exists(jpng):
        lines.append(f"![JPC metrics vs detuning]({jpng})\n")
    if os.path.exists(spng):
        lines.append(f"![SPDC metrics vs detuning]({spng})\n")
    return lines

# Rewrap main to call detuning_aggregate and include plots
def main(jpc_csv="/mnt/data/jpc_batch_summary.csv",
         spdc_csv="/mnt/data/spdc_batch_summary.csv",
         out_md="/mnt/data/universality_report.md",
         out_dir="/mnt/data/universality_plots"):
    os.makedirs(out_dir, exist_ok=True)
    lines = ["# Triality Universality Report\n", "\n*Auto-generated via detuning_aggregate and batch summaries.*\n"]
    jdf = pd.read_csv(jpc_csv) if os.path.exists(jpc_csv) else None
    sdf = pd.read_csv(spdc_csv) if os.path.exists(spdc_csv) else None

    if jdf is not None:
        lines.append("## JPC Summary\n")
        lines.append(f"- Files: {len(jdf)}\n")
        if "detuning" in jdf.columns:
            p = os.path.join(out_dir, "jpc_b2_vs_detuning.png")
            plot_metric(jdf, "detuning", "b2_peak", p)
            lines.append(f"![JPC b2 vs detuning]({p})\n")
            pz = os.path.join(out_dir, "jpc_z_vs_detuning.png")
            plot_metric(jdf, "detuning", "peak_z", pz)
            lines.append(f"![JPC z vs detuning]({pz})\n")
        lines.append(f"- Max JPC b2_peak: {jdf['b2_peak'].max():.3f}\n")
        lines.append(f"- Max JPC lock coherence-time ≥0.5: {jdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n")

    if sdf is not None:
        lines.append("\n## SPDC Summary\n")
        lines.append(f"- Files: {len(sdf)}\n")
        if "detuning" in sdf.columns:
            p = os.path.join(out_dir, "spdc_b2_vs_detuning.png")
            plot_metric(sdf, "detuning", "b2_peak", p)
            lines.append(f"![SPDC b2 vs detuning]({p})\n")
            pz = os.path.join(out_dir, "spdc_z_vs_detuning.png")
            plot_metric(sdf, "detuning", "peak_z", pz)
            lines.append(f"![SPDC z vs detuning]({pz})\n")
        lines.append(f"- Max SPDC b2_peak: {sdf['b2_peak'].max():.3f}\n")
        lines.append(f"- Max SPDC lock coherence-time ≥0.5: {sdf.get('coh_time_ge_0.5', pd.Series([0])).max():.2f} s\n")

    # Try to include unified detuning panels
    try:
        import analysis.detuning_aggregate as dagg
        dagg.main(jpc_csv=jpc_csv, spdc_csv=spdc_csv, out_dir=out_dir)
    except Exception as e:
        pass
    lines = include_detuning_aggregates(out_dir, lines)

    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    print("Wrote report:", out_md)
