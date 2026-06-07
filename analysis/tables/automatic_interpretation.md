# Interpretacao automatica inicial

Esta analise foi gerada automaticamente a partir dos CSVs consolidados. Ela deve ser revisada pelo aluno antes de entrar no relatorio final.

- Menor custo medio de busca com sucesso: P=100, alpha=0.60, com 1.0158 paginas acessadas em media.
- Menor custo medio de busca sem sucesso: P=10, alpha=0.60, com 1.1444 paginas acessadas em media.
- Maior utilizacao real de espaco: P=10, alpha=0.90, com utilizacao de 0.8998.
- Maior percentual de paginas de overflow: P=10, alpha=0.90, com 77.81% das paginas em overflow.
- Melhor compromisso automatico entre custo de busca e uso de memoria: P=10, alpha=0.60. Esse criterio combina, de forma simples, custos de busca, percentual de overflow e perda relativa de utilizacao de espaco.

Em geral, configuracoes com `alpha_max` mais alto tendem a usar melhor o espaco antes de provocar splits, mas podem acumular mais paginas de overflow e aumentar o custo medio de busca. A conclusao final deve considerar tambem a variabilidade das sementes, o desenho experimental e os objetivos do trabalho.
