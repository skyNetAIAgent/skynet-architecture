<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 3aaab08790ed9745e86dcaed1c7bbebd15df48ba863df50aac4f965c117afbe1 -->

# Experimento D5: Qwen3.5-4B inteiro

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · [Français](../fr/EXPERIMENT_D5.md) · [Deutsch](../de/EXPERIMENT_D5.md) · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · **Português** · [العربية](../ar/EXPERIMENT_D5.md)

Situação em 25 de novembro de 2026: **primeiros resultados em entradas curtas (seção 7); contexto longo, velocidade e qualidade ainda não medidos.** O experimento é autorizado pela decisão D5 ([ROADMAP](ROADMAP.md), seção 3) e faz parte da etapa 5 do mapa. Ele verifica a principal suposição não medida do melhor candidato da etapa 4 — a verificação da resposta pelo próprio pagador (PPS, [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), seções 3.2 e 5.2).

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
- **Preparação, perfis v1 e v2, referência no processador e versão para placa de vídeo:** ChatGPT.
- **Verificações independentes:** DeepSeek — importação do modelo pelo forward oficial, unicidade e limites de estouro do perfil v2.
- **Execuções nas placas de vídeo e verificação dos resultados:** Claude (a partir da sandbox dos modelos, a placa de vídeo não está acessível).

## 7. Resultados

**24 de novembro de 2026, entradas curtas.** Entradas: duas histórias de 8 + 8 tokens e seis textos curtos (russo, inglês, chinês, aritmética, código, receita), profundidade 4 e 32 blocos; lote 1.

- **Importação do modelo.** O cálculo usual em ponto flutuante, escrito a partir do código-fonte, coincidiu com o forward oficial do Transformers 5.24.0: o mesmo token escolhido em 130 de 130 posições, desvio dos logits não maior que 3,6·10⁻⁵ (verificaram o ChatGPT e, de forma independente, o DeepSeek).
- **Perfil v1 rejeitado.** Ele era reproduzido bit a bit, mas a escala 1/1024 era grosseira demais: a saída da recorrência DeltaNet era quase toda arredondada para zero, a coincidência do token escolhido com o modelo — 5 de 8, a correlação dos logits cerca de 0,8.
- **Perfil v2** (ativações com expoente binário por vetor e mantissa de 16 bits, resto e estado da recorrência com passo 2⁻²⁰, chaves e valores da atenção em 32 bits): o mesmo token que o do modelo oficial em 90 de 90 posições, correlação média dos logits 0,9996, mínima 0,998. O estado e o cache ocupam 238 MiB em 3000 posições, contra 95 no v1; o número de multiplicações por token é o mesmo — 4,2 bilhões.
- **O2 (um dispositivo).** A geração token a token e a passagem pela resposta pronta com divisão em 1, 3 e 8 posições dão os mesmos bits de todos os logits, dos tokens escolhidos e dos hashes dos estados.
- **O1 (dispositivos diferentes).** Processador (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) e RTX 4070 Laptop (Ada, Windows, CuPy): 88 comparações em cada placa, 242 360 320 logits, 976 tokens escolhidos e 37 152 hashes de estados — **nenhuma diferença**.

**25 de novembro de 2026, outra arquitetura e outra linguagem de núcleos.** A terceira implementação em OpenCL (ChatGPT), as mesmas entradas e 88 comparações: o processador via pocl, a RTX 2060 via NVIDIA OpenCL e a **AMD Radeon RX 580** (Polaris, Mesa rusticl, Linux) — novamente nenhuma diferença em nenhum dos 242 360 320 logits, 976 tokens e 37 152 hashes. No total, os mesmos bits em seis executores: processador (NumPy), processador (pocl), RTX 2060 (CUDA e OpenCL), RTX 4070 Laptop (CUDA), RX 580 (OpenCL).

**25 de novembro de 2026, contexto longo.** Solicitação + resposta: 512 + 64, 2048 + 256 e 4096 + 64 tokens (textos reais), todos os 32 blocos; foram comparados os hashes dos logits de cada posição, os tokens escolhidos e os hashes dos estados a cada 64 posições. A RTX 2060 (CUDA), a RTX 2060 (OpenCL) e a RTX 4070 Laptop (CUDA) coincidiram entre si nos três casos, e em cada placa a geração token a token coincidiu com a passagem pela resposta pronta em blocos de 64 e 512 posições. Para 512 + 64, o mesmo deram a referência independente no processador e a RX 580. Na RX 580, a geração token a token coincidiu com as demais placas também para 2048 + 256 e 4096 + 64, mas a passagem pela resposta pronta em entradas longas é interrompida pelo driver (reset de uma tarefa da placa de vídeo demasiado longa); é preciso dividir o núcleo de atenção em partes. Esta é uma limitação de execução, não uma divergência de bits.

Limitações: entradas curtas e lote 1; núcleos inteiros simples sem blocos tensoriais; o tempo dessas execuções não é uma medição de O3 e O4. A seguir — contexto longo de até milhares de tokens, núcleos rápidos com a mesma aritmética e, depois, O3–O5.
