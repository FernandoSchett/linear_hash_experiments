# Avaliacao Experimental do Hash Linear

Trabalho pratico da disciplina IC0004 - Algoritmos e Estruturas de Dados, UFBA, 2026.1.

O projeto implementa Hash Linear em memoria principal, simulando paginas/buckets de disco. Cada acesso a pagina primaria ou de overflow incrementa uma metrica de acesso a disco simulada. Os experimentos inserem chaves aleatorias unicas, executam buscas com sucesso e sem sucesso, e exportam os resultados em CSV.

## Estrutura

```text
.
|-- CMakeLists.txt
|-- .gitignore
|-- README.md
|-- main.cpp
|-- experiments/
|-- scripts/
|-- resultados/csv/
|-- src/
`-- libs/
```

`libs` contem a estrutura generica de Hash Linear. `src` contem configuracao, geracao de chaves, execucao dos experimentos e escrita dos CSVs. `main.cpp` apenas recebe o caminho do JSON e dispara a execucao.

## Como compilar

```bash
cmake -S . -B build
cmake --build build
```

## Como executar um experimento

```bash
./build/hash_linear_experiment experiments/p10_a060.json
```

Para executar todos:

```bash
bash scripts/run_all_experiments.sh
```

O script gera automaticamente as configuracoes em `build/generated_experiments/` e executa:

- `P = 10, 20, ..., 100`
- `alpha_max = 0.40, 0.50, 0.60, 0.75, 0.80, 0.90, 0.95`
- `seed = 42, 43, 44, 45, 46`

No total, sao 350 execucoes. Os arquivos CSV serao criados em `resultados/csv/generated/`.

## Teste pequeno recomendado

Crie um arquivo, por exemplo `experiments/teste_pequeno.json`, com:

```json
{
  "experiment_id": "teste_pequeno",
  "page_size": 3,
  "alpha_max": 0.75,
  "initial_buckets": 2,
  "num_records": 20,
  "num_successful_searches": 5,
  "num_unsuccessful_searches": 5,
  "seed": 7,
  "output_csv": "resultados/csv/teste_pequeno.csv"
}
```

Execute:

```bash
./build/hash_linear_experiment experiments/teste_pequeno.json
cat resultados/csv/teste_pequeno.csv
```

Verificacoes esperadas:

- `final_total_records` deve ser 20.
- `num_splits` deve ser maior que zero para indicar crescimento dinamico.
- As buscas com sucesso sao validadas pelo proprio programa; se alguma chave inserida nao for encontrada, a execucao termina com erro.
- As buscas sem sucesso tambem sao validadas; se uma chave inexistente for encontrada, a execucao termina com erro.
- `final_load_factor_global` deve ficar proximo ou abaixo de `alpha_max`, exceto por pequenas variacoes causadas pela granularidade de paginas e splits.

## Metricas exportadas

O CSV inclui: identificador do experimento, tamanho de pagina, alpha maximo, seed, quantidade de insercoes e buscas, buckets iniciais e finais, paginas de overflow, paginas totais, registros totais, fator de carga, utilizacao real de espaco, percentual de overflow, numero de splits, nivel final, ponteiro de split, acessos totais e medios a paginas, e tempos de execucao em milissegundos.

## Uso de IA

IA foi usada como apoio para estruturar a versao inicial do projeto e acelerar a escrita do codigo. A execucao dos testes, validacao dos resultados, interpretacao das metricas e analise final continuam sendo responsabilidade do aluno.
