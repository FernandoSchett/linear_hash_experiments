import sys
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib"))

import matplotlib.pyplot as plt
import numpy as np


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import FIGURES_DIR, ensure_output_dirs, load_master_or_raw, save_figure, sort_results  # noqa: E402


ALPHA_MARKERS = {
    0.40: "o",
    0.50: "s",
    0.60: "^",
    0.75: "D",
    0.80: "P",
    0.90: "X",
    0.95: "*",
}


def marker_for(alpha: float) -> str:
    return ALPHA_MARKERS.get(round(float(alpha), 2), "o")


def std_value(row, column: str) -> float:
    std_column = f"{column}_std"
    return getattr(row, std_column, 0.0)


def plot_space_vs_success(df) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    labeled_alphas = set()
    for row in df.itertuples():
        alpha = round(float(row.alpha_max), 2)
        label = f"alpha={row.alpha_max:.2f}" if alpha not in labeled_alphas else None
        labeled_alphas.add(alpha)
        ax.errorbar(
            row.real_space_utilization,
            row.successful_search_avg_page_accesses,
            xerr=std_value(row, "real_space_utilization"),
            yerr=std_value(row, "successful_search_avg_page_accesses"),
            fmt=marker_for(row.alpha_max),
            markersize=7,
            capsize=2,
            alpha=0.8,
            label=label,
        )

    ax.set_title("Trade-off: espaco usado vs custo de busca com sucesso")
    ax.set_xlabel("Utilizacao real do espaco")
    ax.set_ylabel("Paginas acessadas em busca com sucesso")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Marcador")
    save_figure(fig, "tradeoff_space_vs_success_cost")
    plt.close(fig)


def plot_overflow_vs_unsuccess(df) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    labeled_alphas = set()
    for row in df.itertuples():
        alpha = round(float(row.alpha_max), 2)
        label = f"alpha={row.alpha_max:.2f}" if alpha not in labeled_alphas else None
        labeled_alphas.add(alpha)
        ax.errorbar(
            row.overflow_page_percentage,
            row.unsuccessful_search_avg_page_accesses,
            xerr=std_value(row, "overflow_page_percentage"),
            yerr=std_value(row, "unsuccessful_search_avg_page_accesses"),
            fmt=marker_for(row.alpha_max),
            markersize=7,
            capsize=2,
            alpha=0.8,
            label=label,
        )

    ax.set_title("Trade-off: overflow vs custo de busca sem sucesso")
    ax.set_xlabel("Paginas de overflow (%)")
    ax.set_ylabel("Paginas acessadas em busca sem sucesso")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Marcador")
    save_figure(fig, "tradeoff_overflow_vs_unsuccess_cost")
    plt.close(fig)


def plot_alpha_space_overflow(df) -> None:
    page_sizes = sorted(df["page_size_P"].unique())
    cols = min(5, len(page_sizes))
    rows = int(np.ceil(len(page_sizes) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4.5 * rows), sharex=True)
    axes = np.atleast_1d(axes).ravel()

    for ax, page_size in zip(axes, page_sizes):
        group = df[df["page_size_P"] == page_size].sort_values("alpha_max")
        ax2 = ax.twinx()

        line1 = ax.errorbar(
            group["alpha_max"],
            group["real_space_utilization"],
            yerr=group["real_space_utilization_std"] if "real_space_utilization_std" in group else None,
            fmt="-o",
            color="tab:blue",
            label="Utilizacao real",
            capsize=3,
        )
        line2 = ax2.errorbar(
            group["alpha_max"],
            group["overflow_page_percentage"],
            yerr=group["overflow_page_percentage_std"] if "overflow_page_percentage_std" in group else None,
            fmt="-s",
            color="tab:red",
            label="Overflow (%)",
            capsize=3,
        )

        ax.set_title(f"P={int(page_size)}")
        ax.set_xlabel("alpha_max")
        ax.set_ylabel("Utilizacao real", color="tab:blue")
        ax2.set_ylabel("Overflow (%)", color="tab:red")
        ax.grid(True, linestyle="--", alpha=0.35)

        lines = [line1.lines[0], line2.lines[0]]
        labels = ["Utilizacao real", "Overflow (%)"]
        ax.legend(lines, labels, loc="best", fontsize=8)

    for ax in axes[len(page_sizes):]:
        ax.axis("off")

    fig.suptitle("Alpha maximo, utilizacao real e overflow")
    save_figure(fig, "tradeoff_alpha_space_overflow")
    plt.close(fig)


def plot_final_discussion(df) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    size_scale = 40 + df["overflow_page_percentage"] * 8
    scatter = ax.scatter(
        df["real_space_utilization"],
        df["successful_search_avg_page_accesses"],
        s=size_scale,
        c=df["alpha_max"],
        cmap="viridis",
        edgecolor="black",
        alpha=0.85,
    )

    for row in df.itertuples():
        ax.errorbar(
            row.real_space_utilization,
            row.successful_search_avg_page_accesses,
            xerr=std_value(row, "real_space_utilization"),
            yerr=std_value(row, "successful_search_avg_page_accesses"),
            fmt="none",
            ecolor="gray",
            alpha=0.25,
            capsize=2,
        )

    ax.set_title("Alpha alto: economia de espaco, overflow e custo de busca")
    ax.set_xlabel("Utilizacao real do espaco")
    ax.set_ylabel("Custo medio de busca com sucesso")
    ax.grid(True, linestyle="--", alpha=0.35)
    colorbar = fig.colorbar(scatter, ax=ax)
    colorbar.set_label("alpha_max")
    save_figure(fig, "tradeoff_alpha_high_discussion")
    plt.close(fig)


def main() -> int:
    ensure_output_dirs()
    df = sort_results(load_master_or_raw())

    plot_space_vs_success(df)
    plot_overflow_vs_unsuccess(df)
    plot_alpha_space_overflow(df)
    plot_final_discussion(df)

    print(f"[OK] Graficos de trade-off salvos em: {FIGURES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
