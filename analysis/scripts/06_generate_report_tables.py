import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import (  # noqa: E402
    AUTOMATIC_INTERPRETATION_PATH,
    TABLES_DIR,
    ensure_output_dirs,
    format_config,
    load_master_or_raw,
    sort_results,
)


def choose_balanced_configuration(df):
    normalized = df.copy()
    for column in [
        "successful_search_avg_page_accesses",
        "unsuccessful_search_avg_page_accesses",
        "overflow_page_percentage",
    ]:
        min_value = normalized[column].min()
        max_value = normalized[column].max()
        if max_value == min_value:
            normalized[f"{column}_norm"] = 0.0
        else:
            normalized[f"{column}_norm"] = (normalized[column] - min_value) / (max_value - min_value)

    min_util = normalized["real_space_utilization"].min()
    max_util = normalized["real_space_utilization"].max()
    if max_util == min_util:
        normalized["space_loss_norm"] = 0.0
    else:
        normalized["space_loss_norm"] = (
            max_util - normalized["real_space_utilization"]
        ) / (max_util - min_util)

    normalized["balanced_score"] = (
        normalized["successful_search_avg_page_accesses_norm"]
        + normalized["unsuccessful_search_avg_page_accesses_norm"]
        + normalized["overflow_page_percentage_norm"]
        + normalized["space_loss_norm"]
    )
    return normalized.sort_values("balanced_score").iloc[0]


def write_interpretation(df) -> None:
    best_success = df.loc[df["successful_search_avg_page_accesses"].idxmin()]
    best_unsuccess = df.loc[df["unsuccessful_search_avg_page_accesses"].idxmin()]
    best_space = df.loc[df["real_space_utilization"].idxmax()]
    worst_overflow = df.loc[df["overflow_page_percentage"].idxmax()]
    balanced = choose_balanced_configuration(df)

    text = f"""# Interpretacao automatica inicial

Esta analise foi gerada automaticamente a partir dos CSVs consolidados. Ela deve ser revisada pelo aluno antes de entrar no relatorio final.

- Menor custo medio de busca com sucesso: {format_config(best_success)}, com {best_success['successful_search_avg_page_accesses']:.4f} paginas acessadas em media.
- Menor custo medio de busca sem sucesso: {format_config(best_unsuccess)}, com {best_unsuccess['unsuccessful_search_avg_page_accesses']:.4f} paginas acessadas em media.
- Maior utilizacao real de espaco: {format_config(best_space)}, com utilizacao de {best_space['real_space_utilization']:.4f}.
- Maior percentual de paginas de overflow: {format_config(worst_overflow)}, com {worst_overflow['overflow_page_percentage']:.2f}% das paginas em overflow.
- Melhor compromisso automatico entre custo de busca e uso de memoria: {format_config(balanced)}. Esse criterio combina, de forma simples, custos de busca, percentual de overflow e perda relativa de utilizacao de espaco.

Em geral, configuracoes com `alpha_max` mais alto tendem a usar melhor o espaco antes de provocar splits, mas podem acumular mais paginas de overflow e aumentar o custo medio de busca. A conclusao final deve considerar tambem a variabilidade das sementes, o desenho experimental e os objetivos do trabalho.
"""
    AUTOMATIC_INTERPRETATION_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    ensure_output_dirs()
    df = sort_results(load_master_or_raw())

    table_search = df[
        [
            "page_size_P",
            "alpha_max",
            "successful_search_avg_page_accesses",
            "unsuccessful_search_avg_page_accesses",
        ]
    ].rename(
        columns={
            "page_size_P": "P",
            "successful_search_avg_page_accesses": "media_paginas_busca_sucesso",
            "unsuccessful_search_avg_page_accesses": "media_paginas_busca_sem_sucesso",
        }
    )
    table_search.to_csv(TABLES_DIR / "table_search_costs.csv", index=False)

    table_memory = df[
        [
            "page_size_P",
            "alpha_max",
            "real_space_utilization",
            "final_primary_buckets",
            "final_overflow_pages",
            "overflow_page_percentage",
            "final_total_pages",
        ]
    ].rename(
        columns={
            "page_size_P": "P",
            "real_space_utilization": "utilizacao_real",
            "final_primary_buckets": "paginas_primarias",
            "final_overflow_pages": "paginas_overflow",
            "overflow_page_percentage": "percentual_overflow",
            "final_total_pages": "total_paginas",
        }
    )
    table_memory.to_csv(TABLES_DIR / "table_memory.csv", index=False)

    table_splits = df[
        [
            "page_size_P",
            "alpha_max",
            "num_splits",
            "final_level",
            "final_split_pointer",
        ]
    ].rename(
        columns={
            "page_size_P": "P",
            "num_splits": "numero_splits",
            "final_level": "nivel_final",
            "final_split_pointer": "ponteiro_split_final",
        }
    )
    table_splits.to_csv(TABLES_DIR / "table_splits.csv", index=False)

    write_interpretation(df)

    print(f"[OK] Tabelas de relatorio salvas em: {TABLES_DIR}")
    print(f"[OK] Interpretacao automatica salva em: {AUTOMATIC_INTERPRETATION_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
