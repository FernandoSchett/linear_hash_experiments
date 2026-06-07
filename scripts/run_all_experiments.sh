#!/usr/bin/env bash
set -euo pipefail

mkdir -p build
cmake -S . -B build
cmake --build build
mkdir -p resultados/csv/generated

python3 scripts/generate_experiments.py \
    --output-dir build/generated_experiments \
    --csv-dir resultados/csv/generated

for experiment in build/generated_experiments/*.json; do
    echo "Executando ${experiment}"
    ./build/hash_linear_experiment "${experiment}"
done
