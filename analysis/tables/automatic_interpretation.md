# Interpretacao automatica inicial

Esta analise foi gerada automaticamente a partir dos CSVs consolidados. Ela deve ser revisada pelo aluno antes de entrar no relatorio final.

- Menor custo medio de busca com sucesso: P=30, alpha=0.40, com 1.0000 ± 0.0000 paginas acessadas.
- Menor custo medio de busca sem sucesso: P=30, alpha=0.40, com 1.0000 ± 0.0000 paginas acessadas.
- Maior utilizacao real de espaco: P=10, alpha=0.95, com utilizacao de 0.9496 ± 0.0006.
- Maior percentual de paginas de overflow: P=70, alpha=0.95, com 89.34 ± 0.14% das paginas em overflow.
- Melhor compromisso automatico entre custo de busca e uso de memoria: P=60, alpha=0.75. Esse criterio combina, de forma simples, custos de busca, percentual de overflow e perda relativa de utilizacao de espaco.

Os valores acima usam media ± desvio padrao sobre 5 seeds por configuracao.

Em geral, configuracoes com `alpha_max` mais alto tendem a usar melhor o espaco antes de provocar splits, mas podem acumular mais paginas de overflow e aumentar o custo medio de busca. A conclusao final deve considerar tambem a variabilidade das sementes, o desenho experimental e os objetivos do trabalho.
