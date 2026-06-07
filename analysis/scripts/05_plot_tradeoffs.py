import sys
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib"))

import matplotlib.pyplot as plt


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import FIGURES_DIR, ensure_output_dirs, load_master_or_raw, save_figure, sort_results  # noqa: E402


ALPHA_MARKERS = {
    0.60: "o",
    0.75: "s",
    0.90: "^",
}


def marker_for(alpha: float) -> str:
    return ALPHA_MARKERS.get(round(float(alpha), 2), "o")


def plot_space_vs_success(df) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for row in df.itertuples():
        ax.scatter(
            row.real_space_utilization,
            row.successful_search_avg_page_accesses,
            marker=marker_for(row.alpha_max),
            s=90,
            label=f"alpha={row.alpha_max:.2f}" if int(row.page_size_P) == df["page_size_P"].min() else None,
        )
        ax.annotate(f"P={int(row.page_size_P)}", (row.real_space_utilization, row.successful_search_avg_page_accesses),
                    textcoords="offset points", xytext=(5, 5), fontsize=9)

    ax.set_title("Trade-off: espaco usado vs custo de busca com sucesso")
    ax.set_xlabel("Utilizacao real do espaco")
    ax.set_ylabel("Paginas acessadas em busca com sucesso")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Marcador")
    save_figure(fig, "tradeoff_space_vs_success_cost")
    plt.close(fig)


def plot_overflow_vs_unsuccess(df) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for row in df.itertuples():
        ax.scatter(
            row.overflow_page_percentage,
            row.unsuccessful_search_avg_page_accesses,
            marker=marker_for(row.alpha_max),
            s=90,
            label=f"alpha={row.alpha_max:.2f}" if int(row.page_size_P) == df["page_size_P"].min() else None,
        )
        ax.annotate(f"P={int(row.page_size_P)}", (row.overflow_page_percentage, row.unsuccessful_search_avg_page_accesses),
                    textcoords="offset points", xytext=(5, 5), fontsize=9)

    ax.set_title("Trade-off: overflow vs custo de busca sem sucesso")
    ax.set_xlabel("Paginas de overflow (%)")
    ax.set_ylabel("Paginas acessadas em busca sem sucesso")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Marcador")
    save_figure(fig, "tradeoff_overflow_vs_unsuccess_cost")
    plt.close(fig)


def plot_alpha_space_overflow(df) -> None:
    page_sizes = sorted(df["page_size_P"].unique())
    fig, axes = plt.subplots(1, len(page_sizes), figsize=(5.5 * len(page_sizes), 4.8), sharex=True)
    if len(page_sizes) == 1:
        axes = [axes]

    for ax, page_size in zip(axes, page_sizes):
        group = df[df["page_size_P"] == page_size].sort_values("alpha_max")
        ax2 = ax.twinx()

        line1 = ax.plot(
            group["alpha_max"],
            group["real_space_utilization"],
            marker="o",
            color="tab:blue",
            label="Utilizacao real",
        )
        line2 = ax2.plot(
            group["alpha_max"],
            group["overflow_page_percentage"],
            marker="s",
            color="tab:red",
            label="Overflow (%)",
        )

        ax.set_title(f"P={int(page_size)}")
        ax.set_xlabel("alpha_max")
        ax.set_ylabel("Utilizacao real", color="tab:blue")
        ax2.set_ylabel("Overflow (%)", color="tab:red")
        ax.grid(True, linestyle="--", alpha=0.35)

        lines = line1 + line2
        labels = [line.get_label() for line in lines]
        ax.legend(lines, labels, loc="best")

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
        ax.annotate(
            f"P={int(row.page_size_P)}",
            (row.real_space_utilization, row.successful_search_avg_page_accesses),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9,
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
