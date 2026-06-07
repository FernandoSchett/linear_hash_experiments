import sys
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib"))

import matplotlib.pyplot as plt
import numpy as np


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import FIGURES_DIR, ensure_output_dirs, load_master_or_raw, save_figure, sort_results  # noqa: E402


def plot_lines(df, column: str, title: str, ylabel: str, output_name: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    for page_size, group in df.groupby("page_size_P"):
        group = group.sort_values("alpha_max")
        ax.plot(group["alpha_max"], group[column], marker="o", linewidth=2, label=f"P={page_size}")

    ax.set_title(title)
    ax.set_xlabel("alpha_max")
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(title="Tamanho da pagina")
    save_figure(fig, output_name)
    plt.close(fig)


def plot_success_vs_unsuccess(df) -> None:
    labels = [f"P={int(row.page_size_P)}\na={row.alpha_max:.2f}" for row in df.itertuples()]
    x = np.arange(len(labels))
    width = 0.38

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(
        x - width / 2,
        df["successful_search_avg_page_accesses"],
        width,
        label="Busca com sucesso",
    )
    ax.bar(
        x + width / 2,
        df["unsuccessful_search_avg_page_accesses"],
        width,
        label="Busca sem sucesso",
    )

    ax.set_title("Comparacao do custo medio de busca por configuracao")
    ax.set_xlabel("Configuracao")
    ax.set_ylabel("Paginas acessadas em media")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    save_figure(fig, "search_success_vs_unsuccess")
    plt.close(fig)


def plot_heatmap(df, column: str, title: str, output_name: str) -> None:
    pivot = df.pivot(index="page_size_P", columns="alpha_max", values=column).sort_index()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    image = ax.imshow(pivot.values, aspect="auto", cmap="viridis")

    ax.set_title(title)
    ax.set_xlabel("alpha_max")
    ax.set_ylabel("P")
    ax.set_xticks(np.arange(len(pivot.columns)))
    ax.set_xticklabels([f"{alpha:.2f}" for alpha in pivot.columns])
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_yticklabels([str(p) for p in pivot.index])

    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, f"{pivot.values[i, j]:.2f}", ha="center", va="center", color="white")

    fig.colorbar(image, ax=ax, label="Paginas acessadas em media")
    save_figure(fig, output_name)
    plt.close(fig)


def main() -> int:
    ensure_output_dirs()
    df = sort_results(load_master_or_raw())

    plot_lines(
        df,
        "successful_search_avg_page_accesses",
        "Custo medio de buscas com sucesso",
        "Paginas acessadas em media",
        "search_success_avg_pages",
    )
    plot_lines(
        df,
        "unsuccessful_search_avg_page_accesses",
        "Custo medio de buscas sem sucesso",
        "Paginas acessadas em media",
        "search_unsuccess_avg_pages",
    )
    plot_success_vs_unsuccess(df)
    plot_heatmap(
        df,
        "successful_search_avg_page_accesses",
        "Heatmap: buscas com sucesso",
        "heatmap_search_success_avg_pages",
    )
    plot_heatmap(
        df,
        "unsuccessful_search_avg_page_accesses",
        "Heatmap: buscas sem sucesso",
        "heatmap_search_unsuccess_avg_pages",
    )

    print(f"[OK] Graficos de custo de busca salvos em: {FIGURES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
