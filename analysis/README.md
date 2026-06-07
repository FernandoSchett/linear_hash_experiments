# Analise dos Experimentos de Hash Linear

Este modulo Python consolida os CSVs produzidos pelo experimento em C++, valida os dados, gera tabelas para relatorio e cria graficos em PNG.

## Instalar dependencias

```bash
cd analysis
pip install -r requirements.txt
```

## Executar

A partir da raiz do projeto, use o script unico:

```bash
bash scripts/run_analysis.sh
```

A partir da pasta `analysis/`:

```bash
python3 scripts/01_load_and_validate.py
python3 scripts/02_build_master_table.py
python3 scripts/03_plot_search_costs.py
python3 scripts/04_plot_memory_overflow.py
python3 scripts/05_plot_tradeoffs.py
python3 scripts/06_generate_report_tables.py
```

Tambem e possivel executar a partir da raiz do projeto:

```bash
python3 analysis/scripts/01_load_and_validate.py
python3 analysis/scripts/02_build_master_table.py
python3 analysis/scripts/03_plot_search_costs.py
python3 analysis/scripts/04_plot_memory_overflow.py
python3 analysis/scripts/05_plot_tradeoffs.py
python3 analysis/scripts/06_generate_report_tables.py
```

## Saidas geradas

- `analysis/data/processed/raw_results.csv`: tabela bruta com uma linha por seed.
- `analysis/data/processed/master_results.csv`: tabela mestre agregada por `P` e `alpha_max`, com medias e colunas `_std`.
- `analysis/tables/summary_metrics.csv`: tabela resumida com as metricas principais, medias e desvios.
- `analysis/tables/table_search_costs.csv`: tabela de custo medio de busca em formato `media +/- desvio`.
- `analysis/tables/table_memory.csv`: tabela de memoria, utilizacao e overflow em formato `media +/- desvio`.
- `analysis/tables/table_splits.csv`: tabela com splits, nivel final e ponteiro final em formato `media +/- desvio`.
- `analysis/tables/automatic_interpretation.md`: interpretacao automatica inicial em portugues.

## Figuras

O script `03_plot_search_costs.py` gera:

- `search_success_avg_pages`: custo medio de buscas com sucesso.
- `search_unsuccess_avg_pages`: custo medio de buscas sem sucesso.
- `search_success_vs_unsuccess`: comparacao lado a lado entre buscas com e sem sucesso.
- `heatmap_search_success_avg_pages`: heatmap opcional de busca com sucesso.
- `heatmap_search_unsuccess_avg_pages`: heatmap opcional de busca sem sucesso.

O script `04_plot_memory_overflow.py` gera:

- `real_space_utilization`: utilizacao real do espaco por `alpha_max`.
- `overflow_page_percentage`: percentual de paginas de overflow.
- `final_overflow_pages`: numero absoluto de paginas de overflow.
- `final_total_pages`: total de paginas alocadas.

O script `05_plot_tradeoffs.py` gera:

- `tradeoff_space_vs_success_cost`: relacao entre utilizacao real e custo de busca com sucesso.
- `tradeoff_overflow_vs_unsuccess_cost`: relacao entre overflow e custo de busca sem sucesso.
- `tradeoff_alpha_space_overflow`: comparacao entre utilizacao real e overflow por `alpha_max`.
- `tradeoff_alpha_high_discussion`: grafico de apoio para discutir se `alpha_max` alto economiza espaco, mas aumenta overflow e custo.

Cada figura e salva apenas em `.png` dentro de `analysis/figures/`.