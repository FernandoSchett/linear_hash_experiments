#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[ERRO] Python nao encontrado no PATH."
    exit 1
fi

if ! compgen -G "resultados/csv/generated/*.csv" >/dev/null; then
    echo "[ERRO] Nenhum CSV encontrado em resultados/csv/generated/."
    echo "Rode os experimentos antes da analise."
    exit 1
fi

echo "[1/6] Validando CSVs"
"${PYTHON_BIN}" analysis/scripts/01_load_and_validate.py

echo "[2/6] Gerando tabela mestre"
"${PYTHON_BIN}" analysis/scripts/02_build_master_table.py

echo "[3/6] Gerando graficos de busca"
"${PYTHON_BIN}" analysis/scripts/03_plot_search_costs.py

echo "[4/6] Gerando graficos de memoria e overflow"
"${PYTHON_BIN}" analysis/scripts/04_plot_memory_overflow.py

echo "[5/6] Gerando graficos de trade-off"
"${PYTHON_BIN}" analysis/scripts/05_plot_tradeoffs.py

echo "[6/6] Gerando tabelas do relatorio"
"${PYTHON_BIN}" analysis/scripts/06_generate_report_tables.py

echo "[OK] Analise concluida."
echo "[OK] Saidas: analysis/data/processed, analysis/tables, analysis/figures"
