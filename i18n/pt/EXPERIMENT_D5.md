<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 8c74b11b335ebd7a0797e908c40ed9e4c2b98395835bb319e3272b464224875d -->

# Experimento D5: Qwen3.5-4B inteiro

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · [Français](../fr/EXPERIMENT_D5.md) · [Deutsch](../de/EXPERIMENT_D5.md) · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · **Português** · [العربية](../ar/EXPERIMENT_D5.md)

Situação em 24 de novembro de 2026: **plano do experimento, ainda não há medições.** O experimento é autorizado pela decisão D5 ([ROADMAP](ROADMAP.md), seção 3) e faz parte da etapa 5 do mapa. Ele verifica a principal suposição não medida do melhor candidato da etapa 4 — a verificação da resposta pelo próprio pagador (PPS, [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), seções 3.2 e 5.2).

## 1. O que se verifica

O pagador que possui o modelo deve, em uma única passagem, recalcular a solicitação e a resposta obtida e obter **os mesmos bits** que o executor na geração. Isso só é possível se toda a aritmética do modelo for definida em números inteiros com arredondamento fixado: a soma de inteiros não depende da ordem da adição, desde que não haja estouro. O experimento responde a cinco perguntas; os critérios de refutação são fixados antes da execução:

| Experimento | Pergunta | O que o refuta |
|---|---|---|
| O1 | Os bits coincidem em placas de vídeo diferentes e no processador | Pelo menos um bit diferente dos logits, do token escolhido, do motivo de parada ou dos hashes de controle com a mesma entrada. Antes da conclusão — busca da primeira divergência e repetição na entrada mais curta. A conclusão refere-se apenas aos dispositivos testados e à versão da implementação |
| O2 | Os bits coincidem entre a geração token a token e uma única passagem pela sequência pronta em uma mesma placa | Qualquer bit diferente, incluindo o hash do estado recorrente das camadas Gated DeltaNet nos pontos de controle |
| O3 | Quanto custa a verificação da resposta em comparação com a sua geração | Mediana da fração `ρ(1)` maior que 5% para pelo menos um dos quatro pares de comprimentos de solicitação e resposta nomeados de antemão com lote 1. Os lotes 8 e 32 são medidos separadamente |
| O4 | Quanto o perfil inteiro é mais lento que o usual de 8 bits na mesma placa | Mediana da desaceleração maior que 1,25 vez na célula comparável (limiar diagnóstico: decidem O3 e O5) |
| O5 | Quanta qualidade se perde | Perda de acurácia maior que 3 pontos percentuais em 320 tarefas escolhidas de antemão (64 de cada uma das quatro seções do MMLU e do MGSM russo) em comparação com o perfil usual de 8 bits do mesmo modelo |

Os 1,2–3,8% calculados da etapa 4 não são considerados resultado de O3: somente este experimento os confirma ou refuta.

## 2. Modelo e equipamento

- **Modelo:** repositório oficial Qwen/Qwen3.5-4B no Hugging Face, revisão fixada `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Dois arquivos de pesos de 5 329 398 688 e 3 990 429 408 bytes, no total cerca de 9,3 GB. Após o download, os valores SHA-256 são conferidos com o inventário do repositório.
- **Arquitetura** (conforme o `config.json` publicado): 32 blocos, vetor oculto 2560, MLP 9216. Cada quarto bloco (índices 3, 7, …, 31) — atenção completa: 16 cabeças de consulta, 4 cabeças de chaves e valores, tamanho da cabeça 256, portão de saída, rotação das primeiras 64 coordenadas. Os outros 24 blocos — Gated DeltaNet: estado recorrente 32 × 128 × 128 por bloco, convolução causal de profundidade 4. Vocabulário 248 320, matrizes de entrada e saída compartilhadas. O «INT-canônico» transformer usual da etapa 4 é insuficiente para ela; o perfil é definido de novo (seção 3).
- **Dispositivos:** RTX 2060 6 GB (Turing) no Linux doméstico do mantenedor; RTX 4070 Laptop 8 GB (Ada) no computador do dono; o processador como terceiro executor independente. Com consentimento — dispositivos de outros participantes por meio de mini-agente.
- **Memória** [cálculo]: os pesos principais de 8 bits — 4010 MiB. Com lote 1 e comprimento de até 3000 tokens, tudo cabe em 6 GB; o lote 32 com comprimento 3000 exige cerca de 7064 MiB antes mesmo dos buffers de trabalho e, na RTX 2060, só é possível com a transferência do histórico para a memória RAM.

## 3. Perfil inteiro

O perfil recebe um nome e uma versão separados e é congelado até O1–O5. A base é o grafo numérico do projeto ChatGPT com as correções de ambos os críticos:

1. **Pesos e ativações.** Pesos de 8 bits por linha, escala da linha — número binário exato. Ativações de 16 bits com ponto fixo (1024 = unidade). O arredondamento é o mesmo para todas as operações: para o mais próximo, a metade — para o par, em valor absoluto com retorno do sinal.
2. **Normalizações e não linearidades** (RMSNorm, L2, SiLU, sigmoide, softplus, exponencial) — fórmulas inteiras com raiz quadrada inteira e tabelas. As tabelas são construídas fora do programa com arredondamento correto comprovado (MPFR) e publicadas com SHA-256.
3. **Atenção completa.** Pontuações, exponencial por tabela, frações em 16 bits. O crítico ChatGPT encontrou um erro no projeto original: com valores iguais, a adição de mais uma chave igual mudava a saída de 1365 para 683. Correção: dividir a soma ponderada pela soma das próprias frações arredondadas; assim, o valor constante é preservado exatamente.
4. **Gated DeltaNet.** Decaimento, correção e atualização do estado — cinco atribuições inteiras para cada token em uma única ordem canônica no tempo. A fórmula do projeto DeepSeek descrevia outra recorrência e foi rejeitada. A forma «em blocos» acelerada só é admitida se reproduzir os mesmos bits em cada token.
5. **Escolha do token.** Máximo pelo par (pontuação, −número) em todo o vocabulário, de forma gulosa. Modo separado — Gumbel-max canônico com pseudorrandomicidade HMAC-SHA256 a partir da semente da solicitação (D22). Parada — o primeiro motivo: EOS ou o limite.
6. **Limites de estouro** são definidos para cada acumulador; onde 32 bits são poucos, usam-se 64. Testes separados verificam os valores extremos.

Todos os pontos ambíguos («bifurcações») são resolvidos antes da primeira execução pela leitura do código-fonte do modelo da versão fixada do Transformers; o hash desse código-fonte entra no manifesto do perfil.

## 4. Ordem dos trabalhos

1. **P0, preparação (2–4 dias).** Download e conferência do modelo; inventário de todos os tensores; fechamento das bifurcações pelo código-fonte; tabelas; vetores de controle com valores manuais.
2. **Etapa reduzida (1–1,5 semana).** Referência no processador para o modelo inteiro em entradas curtas; conferência com o cálculo usual em ponto flutuante (apenas para detectar erro de importação, não para O1/O2). Versão simples para placa de vídeo sem núcleos tensoriais. Respostas de O2 em uma única placa e de O1 «processador contra RTX 2060» em contexto curto. Em seguida, o mesmo lote na RTX 4070 Laptop — a primeira resposta de O1 para duas placas de vídeo diferentes.
3. **Etapa completa (3–4 semanas).** Multiplicações rápidas de 8 bits, núcleo fundido da recorrência DeltaNet, lotes 1/8/32, experimentos O3, O4, O5, repetição em um segundo dispositivo.

Todo o trabalho ocorre em um diretório separado no Linux doméstico, com um ambiente Python próprio (CuPy com bibliotecas CUDA 12 dos pacotes pip, sem instalação no sistema). Os serviços em operação e os diretórios de outros experimentos não são afetados. A estimativa total — 4–6 semanas de trabalho de um desenvolvedor; os principais riscos — o preço da recorrência DeltaNet (O3 o mostrará), as ambiguidades até P0 e o suporte ao Qwen3.5 nos motores usuais para O4/O5.

## 5. O que será publicado

Para cada execução: manifesto do perfil e das versões, entradas, hashes dos logits e dos estados por camada, tempos brutos e condições de medição, falhas iniciais junto com as correções. A coincidência de bits refere-se apenas aos dispositivos e às versões testados. O resultado de cada experimento é registrado no mapa (etapa 5) e neste documento; o experimento é considerado concluído quando um segundo participante o repetiu.

## 6. Quem fez o quê

- **Projetos do experimento:** dois projetos independentes — ChatGPT e DeepSeek.
- **Crítica cruzada:** o ChatGPT analisou os dois projetos, o DeepSeek analisou os dois projetos; recálculos de memória e de limites, verificação da recorrência curta e da correção da atenção em pequenas enumerações.
- **Consolidação e decisões sobre o plano:** Claude.
