from pathlib import Path

import pandas as pd


ANALYSIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ANALYSIS_DIR.parent

RAW_CSV_DIR = PROJECT_ROOT / "resultados" / "csv"
PROCESSED_DIR = ANALYSIS_DIR / "data" / "processed"
FIGURES_DIR = ANALYSIS_DIR / "figures"
TABLES_DIR = ANALYSIS_DIR / "tables"

MASTER_RESULTS_PATH = PROCESSED_DIR / "master_results.csv"
SUMMARY_METRICS_PATH = TABLES_DIR / "summary_metrics.csv"
AUTOMATIC_INTERPRETATION_PATH = TABLES_DIR / "automatic_interpretation.md"

EXPECTED_PAGE_SIZES = {10, 50, 100}
EXPECTED_ALPHA_MAX = {0.60, 0.75, 0.90}
EXPECTED_NUM_RECORDS = 100000
EXPECTED_SUCCESSFUL_SEARCHES = 5000
EXPECTED_UNSUCCESSFUL_SEARCHES = 5000

EXPECTED_COLUMNS = [
    "experiment_id",
    "page_size_P",
    "alpha_max",
    "seed",
    "num_inserted_records",
    "num_successful_searches",
    "num_unsuccessful_searches",
    "initial_buckets",
    "final_primary_buckets",
    "final_overflow_pages",
    "final_total_pages",
    "final_total_records",
    "final_load_factor_global",
    "real_space_utilization",
    "overflow_page_percentage",
    "num_splits",
    "final_level",
    "final_split_pointer",
    "insert_total_page_accesses",
    "insert_avg_page_accesses",
    "successful_search_total_page_accesses",
    "successful_search_avg_page_accesses",
    "unsuccessful_search_total_page_accesses",
    "unsuccessful_search_avg_page_accesses",
    "insert_runtime_ms",
    "successful_search_runtime_ms",
    "unsuccessful_search_runtime_ms",
    "total_runtime_ms",
]

SUMMARY_COLUMNS = [
    "experiment_id",
    "page_size_P",
    "alpha_max",
    "successful_search_avg_page_accesses",
    "unsuccessful_search_avg_page_accesses",
    "real_space_utilization",
    "overflow_page_percentage",
    "final_primary_buckets",
    "final_overflow_pages",
    "final_total_pages",
    "num_splits",
    "insert_runtime_ms",
    "total_runtime_ms",
]


def ensure_output_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_results() -> pd.DataFrame:
    csv_files = sorted(RAW_CSV_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {RAW_CSV_DIR}")

    frames = []
    for path in csv_files:
        frame = pd.read_csv(path)
        frame["source_file"] = path.name
        frames.append(frame)

    return pd.concat(frames, ignore_index=True)


def load_master_or_raw() -> pd.DataFrame:
    if MASTER_RESULTS_PATH.exists():
        return pd.read_csv(MASTER_RESULTS_PATH)
    return load_raw_results()


def sort_results(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(["page_size_P", "alpha_max"]).reset_index(drop=True)


def save_figure(fig, name: str) -> None:
    ensure_output_dirs()
    png_path = FIGURES_DIR / f"{name}.png"
    pdf_path = FIGURES_DIR / f"{name}.pdf"
    fig.tight_layout()
    fig.savefig(png_path, dpi=200)
    fig.savefig(pdf_path)


def format_config(row: pd.Series) -> str:
    return f"P={int(row['page_size_P'])}, alpha={row['alpha_max']:.2f}"
