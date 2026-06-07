from pathlib import Path

import pandas as pd


ANALYSIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ANALYSIS_DIR.parent

RAW_CSV_DIR = PROJECT_ROOT / "resultados" / "csv" / "generated"
PROCESSED_DIR = ANALYSIS_DIR / "data" / "processed"
FIGURES_DIR = ANALYSIS_DIR / "figures"
TABLES_DIR = ANALYSIS_DIR / "tables"

RAW_RESULTS_PATH = PROCESSED_DIR / "raw_results.csv"
MASTER_RESULTS_PATH = PROCESSED_DIR / "master_results.csv"
SUMMARY_METRICS_PATH = TABLES_DIR / "summary_metrics.csv"
AUTOMATIC_INTERPRETATION_PATH = TABLES_DIR / "automatic_interpretation.md"

EXPECTED_PAGE_SIZES = set(range(10, 101, 10))
EXPECTED_ALPHA_MAX = {0.40, 0.50, 0.60, 0.75, 0.80, 0.90, 0.95}
EXPECTED_SEEDS = {42, 43, 44, 45, 46}
EXPECTED_RUNS_PER_CONFIG = len(EXPECTED_SEEDS)
EXPECTED_CONFIG_COUNT = len(EXPECTED_PAGE_SIZES) * len(EXPECTED_ALPHA_MAX)
EXPECTED_RESULT_ROWS = EXPECTED_CONFIG_COUNT * EXPECTED_RUNS_PER_CONFIG
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

GROUP_COLUMNS = [
    "page_size_P",
    "alpha_max",
]

CONSTANT_COLUMNS = [
    "num_inserted_records",
    "num_successful_searches",
    "num_unsuccessful_searches",
    "initial_buckets",
    "final_total_records",
]

MEASURE_COLUMNS = [
    "final_primary_buckets",
    "final_overflow_pages",
    "final_total_pages",
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
    "num_runs",
    "successful_search_avg_page_accesses",
    "successful_search_avg_page_accesses_std",
    "unsuccessful_search_avg_page_accesses",
    "unsuccessful_search_avg_page_accesses_std",
    "real_space_utilization",
    "real_space_utilization_std",
    "overflow_page_percentage",
    "overflow_page_percentage_std",
    "final_primary_buckets",
    "final_primary_buckets_std",
    "final_overflow_pages",
    "final_overflow_pages_std",
    "final_total_pages",
    "final_total_pages_std",
    "num_splits",
    "num_splits_std",
    "insert_runtime_ms",
    "insert_runtime_ms_std",
    "total_runtime_ms",
    "total_runtime_ms_std",
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


def alpha_tag(alpha: float) -> str:
    return f"a{int(round(float(alpha) * 100)):03d}"


def aggregate_results(raw: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (page_size, alpha), group in raw.groupby(GROUP_COLUMNS, sort=True):
        group = group.sort_values("seed")
        row = {
            "experiment_id": f"p{int(page_size)}_{alpha_tag(float(alpha))}",
            "page_size_P": int(page_size),
            "alpha_max": round(float(alpha), 2),
            "num_runs": int(len(group)),
            "seeds": ";".join(str(int(seed)) for seed in sorted(group["seed"].unique())),
        }

        for column in CONSTANT_COLUMNS:
            row[column] = group[column].iloc[0]

        for column in MEASURE_COLUMNS:
            row[column] = group[column].mean()
            row[f"{column}_std"] = group[column].std(ddof=1) if len(group) > 1 else 0.0

        rows.append(row)

    return sort_results(pd.DataFrame(rows))


def load_master_or_raw() -> pd.DataFrame:
    if MASTER_RESULTS_PATH.exists():
        master = pd.read_csv(MASTER_RESULTS_PATH)
        if "num_runs" in master.columns:
            return master
        try:
            return aggregate_results(load_raw_results())
        except FileNotFoundError:
            return master
    return aggregate_results(load_raw_results())


def sort_results(df: pd.DataFrame) -> pd.DataFrame:
    sort_columns = [column for column in ["page_size_P", "alpha_max", "seed"] if column in df.columns]
    return df.sort_values(sort_columns).reset_index(drop=True)


def save_figure(fig, name: str) -> None:
    ensure_output_dirs()
    png_path = FIGURES_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(png_path, dpi=200)
    pdf_path = FIGURES_DIR / f"{name}.pdf"
    if pdf_path.exists():
        pdf_path.unlink()


def format_config(row: pd.Series) -> str:
    return f"P={int(row['page_size_P'])}, alpha={row['alpha_max']:.2f}"


def format_mean_std(row: pd.Series, column: str, decimals: int = 4) -> str:
    std_column = f"{column}_std"
    std = row[std_column] if std_column in row and pd.notna(row[std_column]) else 0.0
    return f"{row[column]:.{decimals}f} \u00b1 {std:.{decimals}f}"
