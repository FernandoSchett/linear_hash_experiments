## 1. Uso de IA na escrita do relatório técnico e neste relatório

O texto do relatório foi inicialmente escrito por mim, incluindo a organização das seções, a descrição da fundamentação teórica, a metodologia experimental, a apresentação dos resultados e as conclusões.

Após a escrita inicial, utilizei o ChatGPT como ferramenta auxiliar de revisão textual. O uso foi feito seção por seção, com prompts voltados a melhorar a clareza, a fluidez e a objetividade do texto, além de corrigir problemas gramaticais.

Um exemplo do tipo de prompt utilizado foi:

> Revise o texto abaixo mantendo o conteúdo técnico original, mas melhorando a fluidez, a objetividade e a correção gramatical. Não adicione resultados novos, não altere a interpretação técnica e mantenha o estilo adequado para um relatório acadêmico.

Esse processo foi aplicado em seções como introdução, fundamentação teórica, metodologia, resultados e conclusão.

Após as sugestões geradas pela ferramenta, revisei manualmente o texto para verificar se o conteúdo técnico continuava correto.

## 2. Uso de IA na implementação

Na parte de implementação, utilizei o ChatGPT como apoio para gerar rascunhos iniciais de código e para organizar a estrutura do repositório.

Primeiro, defini a estrutura geral que o projeto deveria ter (src,main,cpp,libs...), separando a implementação da estrutura de dados, os arquivos de execução dos experimentos, os scripts de análise e os arquivos de saída. A partir dessa organização, utilizei prompts específicos para gerar código arquivo por arquivo, descrevendo a finalidade esperada de cada componente.

Exemplos do tipo de prompt utilizado foram:

> Gere uma classe em C++ responsável por escrever em CSV o resultado de um experimento. A classe deve receber um caminho de saída e uma estrutura ExperimentResult, criar o diretório caso necessário e salvar métricas como tamanho da página, fator de carga máximo, número de registros inseridos, número de páginas primárias, páginas de overflow, fator de carga final, utilização real de espaço, número de splits, acessos totais e médios em inserções e buscas, além dos tempos de execução.

> Gere uma classe em C++ responsável por executar um experimento com Hash Linear. A classe deve receber uma configuração com número de registros, tamanho da página, fator de carga máximo, número de buscas com sucesso e sem sucesso, gerar chaves aleatórias únicas, inserir as chaves na estrutura, executar buscas por chaves existentes e inexistentes, contabilizar acessos simulados a páginas, medir tempos de execução e salvar os resultados em CSV.

Os códigos gerados pela ferramenta não foram utilizados diretamente como versão final. Em vários casos, os arquivos precisaram ser corrigidos, adaptados e integrados manualmente. Fiz alterações na lógica de implementação, nos parâmetros dos experimentos, na organização dos dados, na geração dos CSVs e nos scripts de análise.

**A ferramenta de IA foi usada como apoio para acelerar a escrita de rascunhos e sugerir estruturas iniciais de código, mas a integração, adaptação, execução dos experimentos, validação dos resultados e versão final do projeto foram realizadas e revisadas por mim. Oquê está alinhado com às diretrizes da Universidade Federal da Bahia para o uso ético e responsável de inteligência artificial generativa.[1]**

[1] UNIVERSIDADE FEDERAL DA BAHIA. Guia para uso ético e responsável da inteligência artificial generativa na Universidade Federal da Bahia. Salvador: UFBA, 2025.