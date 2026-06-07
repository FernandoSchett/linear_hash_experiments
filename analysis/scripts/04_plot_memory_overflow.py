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


def plot_bars(df, column: str, title: str, ylabel: str, output_name: str) -> None:
    labels = [f"P={int(row.page_size_P)}\na={row.alpha_max:.2f}" for row in df.itertuples()]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(x, df[column])
    ax.set_title(title)
    ax.set_xlabel("Configuracao")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    save_figure(fig, output_name)
    plt.close(fig)


def main() -> int:
    ensure_output_dirs()
    df = sort_results(load_master_or_raw())

    plot_lines(
        df,
        "real_space_utilization",
        "Utilizacao real do espaco",
        "Registros / capacidade total",
        "real_space_utilization",
    )
    plot_lines(
        df,
        "overflow_page_percentage",
        "Percentual de paginas de overflow",
        "Paginas de overflow (%)",
        "overflow_page_percentage",
    )
    plot_bars(
        df,
        "final_overflow_pages",
        "Paginas de overflow por configuracao",
        "Numero de paginas",
        "final_overflow_pages",
    )
    plot_bars(
        df,
        "final_total_pages",
        "Total de paginas alocadas por configuracao",
        "Numero de paginas",
        "final_total_pages",
    )

    print(f"[OK] Graficos de memoria e overflow salvos em: {FIGURES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
