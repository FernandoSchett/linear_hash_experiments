import itertools
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import (  # noqa: E402
    EXPECTED_ALPHA_MAX,
    EXPECTED_COLUMNS,
    EXPECTED_CONFIG_COUNT,
    EXPECTED_NUM_RECORDS,
    EXPECTED_PAGE_SIZES,
    EXPECTED_RESULT_ROWS,
    EXPECTED_RUNS_PER_CONFIG,
    EXPECTED_SEEDS,
    EXPECTED_SUCCESSFUL_SEARCHES,
    EXPECTED_UNSUCCESSFUL_SEARCHES,
    RAW_CSV_DIR,
    load_raw_results,
)


def main() -> int:
    problems = []

    try:
        df = load_raw_results()
    except FileNotFoundError as exc:
        print(f"[ERRO] {exc}")
        return 1

    print("Validacao dos resultados experimentais")
    print(f"Diretorio de entrada: {RAW_CSV_DIR}")
    print(f"Linhas carregadas: {len(df)}")

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        problems.append(f"Colunas ausentes: {missing_columns}")

    if df[EXPECTED_COLUMNS].isna().any().any() if not missing_columns else df.isna().any().any():
        missing_summary = df.isna().sum()
        missing_summary = missing_summary[missing_summary > 0]
        problems.append(f"Valores ausentes encontrados: {missing_summary.to_dict()}")

    found_triplets = {
        (int(row.page_size_P), round(float(row.alpha_max), 2), int(row.seed))
        for row in df.itertuples(index=False)
        if hasattr(row, "page_size_P") and hasattr(row, "alpha_max") and hasattr(row, "seed")
    }
    expected_triplets = set(itertools.product(EXPECTED_PAGE_SIZES, EXPECTED_ALPHA_MAX, EXPECTED_SEEDS))
    expected_triplets = {(p, round(alpha, 2), seed) for p, alpha, seed in expected_triplets}

    missing_triplets = sorted(expected_triplets - found_triplets)
    extra_triplets = sorted(found_triplets - expected_triplets)
    if missing_triplets:
        problems.append(f"Combinacoes P/alpha/seed ausentes: {missing_triplets}")
    if extra_triplets:
        problems.append(f"Combinacoes P/alpha/seed inesperadas: {extra_triplets}")

    if len(df) != EXPECTED_RESULT_ROWS:
        problems.append(f"Quantidade de linhas esperada: {EXPECTED_RESULT_ROWS}; encontrada: {len(df)}")

    if {"page_size_P", "alpha_max", "seed"}.issubset(df.columns):
        duplicated = df[df.duplicated(["page_size_P", "alpha_max", "seed"], keep=False)]
        if not duplicated.empty:
            duplicates = duplicated[["page_size_P", "alpha_max", "seed", "source_file"]].to_dict("records")
            problems.append(f"Execucoes duplicadas por P/alpha/seed: {duplicates}")

        runs_per_config = df.groupby(["page_size_P", "alpha_max"])["seed"].nunique()
        invalid_runs = runs_per_config[runs_per_config != EXPECTED_RUNS_PER_CONFIG]
        if not invalid_runs.empty:
            problems.append(f"Configs sem {EXPECTED_RUNS_PER_CONFIG} seeds: {invalid_runs.to_dict()}")

    checks = [
        ("num_inserted_records", EXPECTED_NUM_RECORDS),
        ("num_successful_searches", EXPECTED_SUCCESSFUL_SEARCHES),
        ("num_unsuccessful_searches", EXPECTED_UNSUCCESSFUL_SEARCHES),
    ]
    for column, expected_value in checks:
        if column in df.columns:
            invalid = df[df[column] != expected_value]
            if not invalid.empty:
                ids = invalid["experiment_id"].tolist() if "experiment_id" in invalid else invalid.index.tolist()
                problems.append(f"{column} diferente de {expected_value} em: {ids}")

    found_pairs = {
        (page_size, alpha)
        for page_size, alpha, _seed in found_triplets
    }
    print("\nResumo encontrado:")
    print(f"- Configuracoes P/alpha: {len(found_pairs)} de {EXPECTED_CONFIG_COUNT}")
    print(f"- Seeds esperadas por configuracao: {sorted(EXPECTED_SEEDS)}")
    for page_size, alpha in sorted(found_pairs):
        seeds = sorted(seed for p, a, seed in found_triplets if p == page_size and a == alpha)
        print(f"- P={page_size}, alpha_max={alpha:.2f}, seeds={seeds}")

    if problems:
        print("\n[AVISO] A validacao encontrou problemas:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("\n[OK] Todos os CSVs possuem as colunas, combinacoes e tamanhos esperados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
