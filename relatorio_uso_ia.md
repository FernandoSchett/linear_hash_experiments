## 1. Uso de IA na escrita do relatório técnico e neste relatório

O texto do relatório foi inicialmente escrito por mim, incluindo a organização das seções, a descrição da fundamentação teórica, a metodologia experimental, a apresentação dos resultados e as conclusões.

Após a escrita inicial, utilizei o ChatGPT como ferramenta auxiliar de revisão textual. O uso foi feito seção por seção, com prompts voltados a melhorar a clareza, a fluidez e a objetividade do texto, além de corrigir problemas gramaticais.

Um exemplo do tipo de prompt utilizado foi:

> Revise o texto abaixo mantendo o conteúdo técnico original, mas melhorando a fluidez, a objetividade e a correção gramatical. Não adicione resultados novos, não altere a interpretação técnica e mantenha o estilo adequado para um relatório acadêmico.

Esse processo foi aplicado em seções como introdução, fundamentação teórica, metodologia, resultados e conclusão.

Após as sugestões geradas pela ferramenta, revisei manualmente o texto para verificar se o conteúdo técnico continuava correto, se os resultados apresentados correspondiam aos experimentos executados e se nenhuma informação incorreta havia sido adicionada. A versão final do relatório foi, portanto, revisada e validada por mim.

## 2. Uso de IA na implementação

Na parte de implementação, utilizei o ChatGPT como apoio para gerar rascunhos iniciais de código e para organizar a estrutura do repositório.

Primeiro, defini a estrutura geral que o projeto deveria ter (src,main,cpp,libs...), separando a implementação da estrutura de dados, os arquivos de execução dos experimentos, os scripts de análise e os arquivos de saída. A partir dessa organização, utilizei prompts específicos para gerar código arquivo por arquivo, descrevendo a finalidade esperada de cada componente.

Exemplos do tipo de prompt utilizado foram:

> Gere um arquivo C++ para implementar a estrutura principal de Hash Linear, considerando páginas primárias, páginas de overflow, inserção de chaves, busca e contabilização de acessos simulados a disco.

> Gere um script Python para ler os arquivos CSV produzidos pelos experimentos, consolidar as métricas e gerar gráficos comparando custo de busca, utilização de espaço e páginas de overflow.

Os códigos gerados pela ferramenta não foram utilizados diretamente como versão final. Em vários casos, os arquivos precisaram ser corrigidos, adaptados e integrados manualmente. Fiz alterações na lógica de implementação, nos parâmetros dos experimentos, na organização dos dados, na geração dos CSVs e nos scripts de análise.

Também revisei os resultados produzidos, executei os experimentos, verifiquei os arquivos de saída e ajustei o código quando os resultados não estavam coerentes com o comportamento esperado da estrutura de Hash Linear.

Assim, a ferramenta de IA foi usada como apoio para acelerar a escrita de rascunhos e sugerir estruturas iniciais de código, mas a integração, adaptação, execução dos experimentos, validação dos resultados e versão final do projeto foram realizadas e revisadas por mim.
