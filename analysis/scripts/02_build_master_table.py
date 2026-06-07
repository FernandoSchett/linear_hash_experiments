import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import (  # noqa: E402
    EXPECTED_COLUMNS,
    MASTER_RESULTS_PATH,
    SUMMARY_COLUMNS,
    SUMMARY_METRICS_PATH,
    ensure_output_dirs,
    load_raw_results,
    sort_results,
)


def main() -> int:
    ensure_output_dirs()
    df = load_raw_results()

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        print(f"[ERRO] Colunas ausentes: {missing_columns}")
        return 1

    master = sort_results(df[EXPECTED_COLUMNS].copy())
    master.to_csv(MASTER_RESULTS_PATH, index=False)

    summary = master[SUMMARY_COLUMNS].copy()
    summary.to_csv(SUMMARY_METRICS_PATH, index=False)

    print(f"[OK] Tabela mestre salva em: {MASTER_RESULTS_PATH}")
    print(f"[OK] Tabela resumida salva em: {SUMMARY_METRICS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
