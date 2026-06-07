import itertools
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import (  # noqa: E402
    EXPECTED_ALPHA_MAX,
    EXPECTED_COLUMNS,
    EXPECTED_NUM_RECORDS,
    EXPECTED_PAGE_SIZES,
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

    found_pairs = {
        (int(row.page_size_P), round(float(row.alpha_max), 2))
        for row in df.itertuples(index=False)
        if hasattr(row, "page_size_P") and hasattr(row, "alpha_max")
    }
    expected_pairs = set(itertools.product(EXPECTED_PAGE_SIZES, EXPECTED_ALPHA_MAX))
    expected_pairs = {(p, round(alpha, 2)) for p, alpha in expected_pairs}

    missing_pairs = sorted(expected_pairs - found_pairs)
    extra_pairs = sorted(found_pairs - expected_pairs)
    if missing_pairs:
        problems.append(f"Combinacoes P/alpha ausentes: {missing_pairs}")
    if extra_pairs:
        problems.append(f"Combinacoes P/alpha inesperadas: {extra_pairs}")

    if len(df) != len(expected_pairs):
        problems.append(f"Quantidade de linhas esperada: 9; encontrada: {len(df)}")

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

    print("\nCombinacoes encontradas:")
    for page_size, alpha in sorted(found_pairs):
        print(f"- P={page_size}, alpha_max={alpha:.2f}")

    if problems:
        print("\n[AVISO] A validacao encontrou problemas:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("\n[OK] Todos os CSVs possuem as colunas, combinacoes e tamanhos esperados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
