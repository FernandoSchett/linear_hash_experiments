#!/usr/bin/env bash
set -euo pipefail

mkdir -p build
cmake -S . -B build
cmake --build build
mkdir -p resultados/csv

for experiment in experiments/*.json; do
    echo "Executando ${experiment}"
    ./build/hash_linear_experiment "${experiment}"
done
