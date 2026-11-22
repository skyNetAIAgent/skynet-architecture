<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# O que foi verificado no piloto

[English](../../docs/PILOT_RESULTS.en.md) · [中文](../zh/PILOT_RESULTS.md) · [Español](../es/PILOT_RESULTS.md) · [Français](../fr/PILOT_RESULTS.md) · [Deutsch](../de/PILOT_RESULTS.md) · [Italiano](../it/PILOT_RESULTS.md) · [Русский](../../docs/PILOT_RESULTS.md) · **Português** · [العربية](../ar/PILOT_RESULTS.md)

Antes de escolher a arquitetura sem coordenadores, o projeto montou um **piloto de confiança** com um servidor central
e vários protótipos de pesquisa de verificação. Abaixo, o que foi realmente executado e medido,
e onde ficam os limites desses resultados. O código-fonte do piloto não faz parte deste repositório.

O piloto é um sistema fechado com um operador de confiança. Ele não está protegido contra fraude em uma rede aberta
e não implementa a arquitetura alvo. Todos os pagamentos nele são de treinamento (TEST_CREDIT, sem saque).

## Inferência e contabilização

| O quê | Resultado |
|---|---|
| Circuito do servidor | API, fila, PostgreSQL, agente, verificação separada do resultado e crédito de treinamento em uma única transação. O reenvio não gera um segundo crédito; a locação expirada da tarefa é rejeitada |
| GPU fraca | Qwen2.5-0.5B-Instruct Q4_K_M via llama.cpp (Vulkan) na Intel Arrow Lake-P integrada: tarefa aceita, substituição de resposta rejeitada |
| Segunda GPU | Qwen3-4B-Instruct-2507 Q4_K_M na RTX 2060 de 6 GB: todas as camadas na GPU, cerca de 2,4 GiB de VRAM, mediana de 73,8 tokens/s em um perfil curto |
| Modelo em vários computadores | As camadas do Qwen3-4B eram distribuídas pela rede local entre a RTX 2060 e a GPU do participante (RTX 4070 Laptop, depois Intel Arrow Lake-P). O participante recebia na memória apenas a parte designada dos pesos. O par RTX 2060 + RTX 4070 Laptop rendeu cerca de 38–40 tokens/s contra 69,5 em uma única RTX 2060: memória adicional não garante aceleração |
| Recuperação | Pausa, retomada e recuperação automática do grupo após a queda do túnel |

A verificação no piloto é a repetição da geração na **mesma GPU de confiança**. Isso não é prova da honestidade
de um nó desconhecido.

## Protótipos de verificação de cálculos

| O quê | Resultado | Limite |
|---|---|---|
| Groth16 para duas matmul inteiras + verificador Solidity | Provas reais e pagamento único em uma EVM local | Tarefa pequena na CPU |
| RISC Zero para uma linha Q4_K da projeção Qwen em dados reais | Prova de 22 min 10 s, verificação de 117 ms, entradas de 11,7 KB | Uma linha, não o grafo inteiro; muito acima do orçamento |
| Pacote de oito linhas na zkVM | 350 ms de execução contra 19,8 µs nativamente (~17 700×) | Sem a construção da prova |
| Cartesi: disputa sobre o resultado Qwen | Substituição de um bit encontrada; disputa de 93 transações, 5,8–6,3 milhões de gas | Exige um contestador honesto em tempo hábil |
| Repetição completa da aritmética da linha na EVM | 14,1 milhões de gas por submissão | Uma linha |
| Auditores automáticos | Um auditor externo refutou o vetor falso apesar de dois que concordaram | Sem observador, o erro passou pela regra otimista |
| Conluio entre o executor e o verificador | Receberam pagamento por um resultado incorreto | Mostra por que a votação dos verificadores não é uma garantia |

## O que não houve

- Treinamento distribuído.
- Cotas rígidas de hardware de CPU/GPU/RAM/VRAM.
- Pagamentos reais em dinheiro.
- Verificação em hardware independente em rede aberta.
- Medição de energia.
- Experimentos com a nova arquitetura sem coordenadores: ela, por enquanto, está apenas projetada.
