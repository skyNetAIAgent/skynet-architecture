<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Etapa 4. Contrato byte a byte dos cálculos integrados

[English](../../docs/STAGE4_KERNELS.en.md) · [中文](../zh/STAGE4_KERNELS.md) · [Español](../es/STAGE4_KERNELS.md) · [Français](../fr/STAGE4_KERNELS.md) · [Deutsch](../de/STAGE4_KERNELS.md) · [Italiano](../it/STAGE4_KERNELS.md) · [Русский](../../docs/STAGE4_KERNELS.md) · **Português** · [العربية](../ar/STAGE4_KERNELS.md)

Estado em 24 de novembro de 2026. O documento define as regras exatas de quatro novos cálculos integrados do mini-agente (desde a versão 1.2.0 do agente) para os cálculos M8, M10, M12 e M14 de [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), seção 5.3. A especificação e a implementação em Go foram escritas por ChatGPT; DeepSeek verificou a especificação de forma independente pelos trabalhos de origem do conselho e, apenas com base nela, escreveu uma segunda implementação em Python ([tools/reference_stage4.py](../../tools/reference_stage4.py)); todos os 73 resultados das tarefas coincidiram byte a byte; Claude verificou o código e a conferência. Referências como «claude1, §5.4» apontam para os trabalhos do conselho de modelos, reunidos em VERIFICATION_SEARCH. É uma contagem exata por fórmulas, não uma medição: a coincidência confirma a aritmética, mas não as suposições dos modelos. Os cálculos M5, M7 e M18 foram adiados: faltam regras nos trabalhos para determiná-los de forma inequívoca (seção «Cálculos adiados»).

| Cálculo da §5.3 | Núcleo da versão 1 | O que se pode saber de uma unidade |
|---|---|---|
| M8 | `t4-scale` | Quantos tokens de treinamento por nó são necessários para um dado número de proponentes e quantos proponentes o orçamento admite |
| M10 | `exam-thresholds` | Em que intervalo racional está cada um dos dois limiares do exame |
| M12 | `merge-attribution` | Como muda a soma das atribuições ao participante ao acrescentar duplicatas exatas ou com ruído |
| M14 | `verification-enumerations` | Quais casos passaram ou falharam de forma exaustiva na verificação de empacotamento, cadeia ou igualdade de corpo |

A escolha decorre da tabela do conselho na §5.3. Por D18, o pagamento pela melhoria continua sendo uma hipótese de pesquisa. Para reproduzir todos os quatro cálculos, bastam os parâmetros de entrada. [Resultado do conselho](VERIFICATION_SEARCH.md) · [Decisões D18–D20](ROADMAP.md)

## Regras gerais da versão 1

Na tarefa assinada, o nome do núcleo e o inteiro `kernel_version: 1` são armazenados separadamente. A entrada `params` é um objeto com todos os campos enumerados para o núcleo. Campos extras ou ausentes, repetição de chave JSON, valores fora da faixa e tipos incorretos levam a erro. Um inteiro é escrito como literal inteiro JSON, sem ponto decimal nem expoente. Strings e valores booleanos no lugar de números são proibidos. Os limites são inclusivos. Os eixos da grade preservam a ordem de entrada. O número de unidades é exatamente igual ao tamanho da grade indicado para o núcleo, de 1 a 1 000 000. A numeração das unidades começa em zero. No produto cartesiano, o último eixo varia mais rápido.

Para a conferência, toma-se o objeto de resultado inteiro. Em Python, os bytes canônicos são iguais a `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, sem nova linha final. O hash do resultado é o SHA-256 desses bytes, 64 dígitos hexadecimais minúsculos. A ordem dos elementos dos arrays é significativa. Uma fração em string é escrita no sistema decimal como `p/q` com denominador positivo após a redução, incluindo `0/1` e inteiros com `/1`. Não há sinais de mais nem zeros à esquerda. Para M14, define-se separadamente o hash dos bytes *dentro* do resultado do empacotamento. [Codificador canônico do agente](../../agent-go/canon/canon.go)

## M8. Escala de T4 com uma atualização de cada participante

`t4-scale@1` calcula o número inteiro mínimo de tokens de treinamento próprio por rodada com o qual o exame acrescenta no máximo 20% de computação. Para um dado orçamento de tokens, o núcleo também encontra o número limite de proponentes. No modelo, cada nó verifica todas as `K=N` atualizações. A base custa uma passagem direta por posição, cada atualização das camadas superiores custa a fração `a=L_a/L` de uma passagem, e o treinamento de um token custa três passagens. Essas relações são dadas pela proposta. claude1, §5.4 «Preço» e §7.5, item 4 · critic_claude, §1.8 e §10.4, item 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.md)

| Campo `params` | Valores admissíveis |
|---|---|
| `N` | Eixo de inteiros de 1 a 1 000 000. Número de proponentes na rodada |
| `n` | Eixo de inteiros de 1 a 1 000 000. Número de posições do exame |
| `a` | Eixo de pares de inteiros `[p,q]`, onde `1 ≤ p ≤ q ≤ 1 000 000`. Fração de uma passagem por atualização |
| `D_budget` | Eixo de inteiros de 1 a 1 000 000 000 000. Orçamento de tokens de treinamento por nó por rodada |
| `epsilon_bits` | Um inteiro de 1 a 256. Define `ε=1/2^epsilon_bits` para um exame fixado. Para um dado `n`, o custo é o mesmo para todos os `ε` |

Todos os cinco campos são obrigatórios. Cada eixo é um array de comprimento 1…32, os valores são únicos considerando a redução das frações, e a ordem do array de entrada é preservada. O número de unidades é igual ao produto dos comprimentos dos eixos e não excede 1 000 000. Numeração a partir de zero no produto cartesiano `N, n, a, D_budget` na ordem de laços aninhados, com o orçamento variando mais rápido. Uma unidade produz um objeto.

Para o ponto escolhido, ponhamos `D=D_budget`, e reduzamos `a=p/q`. Meçamos a computação em unidades de `1/q` de uma passagem direta por posição. Então o exame exige `E=n(q+Np)`, o treinamento exige `W=3Dq`, e a fração de custos indiretos é `E/W`. A divisão pelo volume do treinamento próprio decorre da formulação «acréscimo» na §5.4. A condição de 20% é equivalente a `5E ≤ W`.

| Campo do resultado | Valor |
|---|---|
| `kernel` | String `t4-scale@1` |
| `N`, `n`, `D_budget` | Inteiros do ponto de entrada |
| `a`, `epsilon` | Strings reduzidas `p/q`; `epsilon` é escrito como `1/q`, onde `q = 2^epsilon_bits` é um inteiro decimal (por exemplo, `"1/4"` com `epsilon_bits = 2`) |
| `D_min` | Inteiro `(5E + 3q − 1) // (3q)`, onde `//` é a divisão inteira para baixo. É o arredondamento do limiar para cima até um token inteiro |
| `fits` | Valor booleano `D_budget ≥ D_min`. A igualdade conta |
| `N_max` | `null` se `W < 5nq` e mesmo a passagem base excede o orçamento. Caso contrário, o inteiro `(W − 5nq) // (5np)`. Zero significa que só a base cabe. O limite pode sair fora do eixo de entrada `N` |
| `overhead` | `E/W` como string reduzida `numerator/denominator` |

A fronteira inversa decorre da desigualdade linear `5npN ≤ W − 5nq` com `p` positivo. Com os parâmetros permitidos, `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. Os denominadores são positivos. Bastam inteiros de 64 bits com sinal e a redução da fração pelo MDC. Em Go, para `overhead` usa-se `big.Rat`, e para `2^epsilon_bits`, `big.Int`. Por unidade, há o parsing de no máximo 128 elementos dos eixos e um número constante de operações aritméticas.

Para `n=3, N=4, a=1/2`, o exame custa 9 passagens; com 15 tokens de treinamento, ele ocupa exatamente um quinto. Com 14 tokens, o limite cai para três proponentes. Com `epsilon_bits=2`, obtêm-se os seguintes bytes canônicos.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

Como referência, na §5.4, com `n=100000, N=10000, a=4/36`, o mínimo exato é 185 351 852 tokens. O preço físico depende da reutilização de prefixos, do volume de cache, da cabeça de saída, da normalização, do tráfego e do preço efetivo do treinamento das camadas superiores. A fórmula cobre apenas a contagem de passagens descrita na §5.4. Para estimar o limiar estatístico quando `ε` muda, serve M10. A tarefa proposta define `ε=2^-80` conforme a referência numérica D19. critic_gpt, seção sobre claude1, «Preço oculto de T4» · [ROADMAP, D18–D19](ROADMAP.md)

## M10. Limiar do exame T4 — `exam-thresholds@1`

M10 determina quão grande deve ser a melhoria média observada no exame para que supere o limiar estatístico. Para um único candidato fixado de antemão, tomam-se `n` posições independentes com reposição. A diferença de perdas em cada posição é truncada para `[−B/2, B/2]`. A entrada `V` é a variância amostral das diferenças truncadas com divisor `n−1` (o quadrado do desvio padrão). Os limites em nats por posição são tirados do passo 6 da descrição de T4. claude1, §5.4 · crítico Claude, §1.8

| Método | Limiar exato `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Bernstein empírico | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Parâmetros e unidades.** Cinco campos são obrigatórios. Os campos `n`, `epsilon_bits`, `B`, `variance` são eixos de comprimento de 1 a 32, cada um na ordem do array de entrada. Os valores no eixo são distintos; frações são comparadas após a redução.

| Campo | Valores admissíveis |
|---|---|
| `n` | Número de posições, inteiro de 2 a 1 000 000 |
| `epsilon_bits` | Inteiro `k` de 1 a 128, `ε = 2⁻ᵏ` por comparação |
| `B` | Largura da faixa de truncamento, inteiro de 1 a 64 |
| `variance` | Fração `[p,q]`, inteiros `0 ≤ p ≤ 10⁶` e `1 ≤ q ≤ 10⁶`. Em todos os pontos da grade, `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | Um inteiro `d` de 1 a 9. A largura absoluta garantida de cada intervalo é menor que `10⁻ᵈ` |

O máximo da variância é atingido nas extremidades da faixa, pois a variância é convexa em cada observação. Com `j` valores em uma extremidade, seu numerador é proporcional a `j(n−j)`, o que dá o limite indicado. O número de unidades é igual ao produto dos comprimentos dos quatro eixos e não excede 1 000 000. A numeração coincide com `itertools.product(n, epsilon_bits, B, variance)`, começando em zero.

**Algoritmo de reprodução byte a byte.** Para ambos os métodos, escrever `t = √(A·ln 2) + C·ln 2`. Em Hoeffding, `A=B²k/(2n), C=0`. Em Bernstein, `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. Todas as divisões aqui são racionais.

1. Tomar `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸`.
2. O limite inferior é `(floor(√(S²Al)) + floor(SCl))/S`. O superior é `(ceil(√(S²Ah)) + ceil(SCh))/S`. Ambos os termos são arredondados **separadamente**.
3. Para uma fração não negativa `x=p/q`, calcular `r=isqrt(p//q)`. Isto é `floor(√x)`. Para o limite superior, somar um a `r` exatamente quando `r²q < p`. Os `floor` e `ceil` usuais também são realizados por divisão inteira. Todas as frações obtidas são reduzidas.

**Certificado de precisão.** Da série para `2·atanh(1/3)=ln 2`, tomamos `T=2·Σ 1/(j·3ʲ)` nos ímpares `j=1,3,…,39`. A cauda é positiva e limitada pelo primeiro termo omitido multiplicado por `1/(1−1/9)`. Por comparação inteira, obtemos `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. A monotonicidade de ambos os termos e o arredondamento direcionado garantem a inclusão do limiar verdadeiro. Na faixa dada, `A ≤ 264192` e `C ≤ 19264`. Como `√h+√l > 1`, substituir `l` por `h` muda o limiar não arredondado em menos de `(515+19264)·10⁻¹⁸`. O arredondamento amplia o intervalo em menos de `4/S`. A soma é menor que `10⁻ᵈ` mesmo com `d=9`. Por unidade, bastam quatro raízes quadradas inteiras e um número constante de operações sobre inteiros e frações de algumas centenas de bits, independentemente de `n`.

**Resposta.** Os campos `n`, `epsilon_bits`, `B` e `digits` são coordenadas inteiras e a precisão. `variance` é uma string com a fração reduzida. `hoeffding` e `bernstein` são arrays de duas dessas strings, com o limite inferior primeiro. Para `n=2, k=1, B=2, V=0, d=1`, o núcleo produz os seguintes bytes canônicos.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

Para um limiar limite dado `τ`, o tamanho mínimo do exame **na grade** fica estabelecido quando, no ponto escolhido, o limite superior é `≤ τ` e, para todos os `n` menores com os mesmos parâmetros, o limite inferior é `> τ`. Se o intervalo cruza o alvo, pode ser necessária maior precisão. Os números caracterizam uma comparação unilateral da média truncada com fixação até um farol externo. A correção pela escolha entre vários candidatos, a qualidade fora do exame, a escolha de `τ` e a magnitude do efeito real exigem dados ou regras separados. O pagamento pela melhoria continua sendo uma variante de pesquisa por D18. [ROADMAP, D18–D20](ROADMAP.md) · crítico GPT, avaliação de T4

## M12. Como muda a atribuição do dono das duplicatas na fusão por soma

No trabalho para M12, indicam-se perdas linear-quadráticas com gradiente e hessiano conhecidos, três regras de atribuição, duplicatas exatas e duplicatas com ruído. Escolhemos a variante explicitamente analisada na §5.4, `merge = sum`. O crítico apresenta um caso em que até a repetição do mesmo passo melhora a função de perdas. O núcleo `merge-attribution@1` verifica isso com coeficientes de entrada explícitos. claude1, §5.4, passos 6–7 e item 2 «Atribuição e duplicatas», §7.5, item 7 · critic_gpt, tabela sobre claude1, linha T4

| Campo `params` | Significado e limites inclusivos |
|---|---|
| `scale` | Denominador comum `s`, inteiro 1…10 000 |
| `g` | Vetor de numeradores do gradiente no ponto base. Seu comprimento define a dimensão `d`, 1…8 |
| `hessian` | Matriz simétrica de numeradores do hessiano, array de `d` linhas com `d` componentes |
| `updates` | Array de `b=1…8` vetores de numeradores originais de comprimento `d`, na ordem de submissão. Vetores iguais são permitidos |
| `owner` | Índice inteiro da submissão original do participante verificado, de 0 a `b−1`. As outras submissões originais pertencem a outros participantes |
| `copies` | Eixo de 1…8 inteiros distintos de 1…8. O `c` escolhido define o número de submissões adicionadas do mesmo participante |
| `noise` | Eixo de 1…32 vetores de numeradores de comprimento `d` dois a dois distintos. O vetor nulo dá uma duplicata exata |
| `threshold` | Numerador inteiro 0…10 000 para a dedução `t=threshold/s` da estimativa de cada submissão |

Cada componente de `g`, `hessian`, `updates` e `noise` é um inteiro de −10 000 a 10 000. Para obter o valor matemático de cada componente, dividi-la por `s` **uma vez**, inclusive para a matriz. A versão suporta coeficientes racionais com denominador comum na faixa indicada. A simetria é obrigatória; o sinal da curvatura é arbitrário. Os eixos de entrada `copies, noise` formam a grade. Para a unidade `u`, tomar os índices `divmod(u,len(noise))` respectivamente. Após as `b` submissões originais, acrescentar `c` vetores, cada um igual a `updates[owner] + noise[j]` nos numeradores. Os vetores originais são preservados. Os conjuntos de submissões antes e depois do acréscimo são considerados separadamente.

**Cálculo.** Seja `U` o conjunto de índices das submissões de um mesmo conjunto, e `x(S)` a soma dos seus vetores **matemáticos** de atualizações sobre o subconjunto `S`. O ganho em perdas é definido como a redução em relação à base comum,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

Para cada índice `i`, calcular três estimativas **com sinal**. `separate[i]=v({i})`. A regra de exclusão de um, `loo[i]=v(U)−v(U без i)`. A estimativa `shapley[i]` é igual ao aumento médio `v(S∪{i})−v(S)` sobre todas as permutações de índices, onde `S` consiste nos predecessores de `i`. Essa regra é aplicada à função completa de redução de perdas. Para o cálculo sem busca fatorial, ponhamos `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. A simetria dá `v(S)=Σ q_i + Σ_{i<j} h_ij` sobre os participantes `S`. Ao excluir um participante, todos os seus termos pareados desaparecem. Em uma permutação uniforme, cada outro participante o precede exatamente em metade dos casos. Portanto

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Em seguida, separadamente para cada regra, a estimativa `z` é convertida na atribuição `max(0,z−t)` em unidades de melhoria (o coeficiente de pagamento κ é tomado como um). Primeiro atribui-se por cada submissão, depois somam-se as atribuições do dono. `gain` é a atribuição ao dono pela sua submissão original e por todas as adicionadas após o acréscimo menos a atribuição pela sua única submissão antes do acréscimo. O sinal positivo significa ganho com submissões adicionais neste exemplo.

**Formato da resposta.** As chaves `kernel` (string `merge-attribution@1`), `owner`, `scale`, `copies` (o inteiro escolhido do eixo), `noise` (o vetor escolhido de inteiros numeradores), `baseline`, `with_copies` e `gain`. Cada um dos objetos `baseline` e `with_copies` contém `value` — a fração `v(U)` — e os campos `separate`, `loo`, `shapley` — arrays de frações na ordem dos índices das submissões. O objeto `gain` contém uma fração sob cada um dos três nomes de regras. Todas as frações de saída são strings canônicas.

**Aritmética e limites.** O denominador comum das estimativas intermediárias é `2s³`. Se `G, A, z_i` são os numeradores inteiros de entrada do gradiente, do hessiano e do passo, o numerador `q_i` é igual a `−2s Gᵀz_i−z_iᵀAz_i`. À metade do termo pareado corresponde o numerador inteiro `−z_iᵀAz_j`. O numerador da dedução é `2s²·threshold`. Após o acréscimo, há até 16 submissões e `|z_ij| ≤ 20 000`. Daí `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, e a parte linear em módulo não passa de `3,2·10¹³`. Mesmo a soma de 16 estimativas completas de LOO e deduções em módulo é menor que `1,3·10¹⁷`. Todas as multiplicações e somas parciais cabem em 64 bits com sinal. A implementação reduz frações com `big.Rat`. Tempo `O(k d²+k²d)` com `k ≤ 16`, sem tabela de subconjuntos. A memória é limitada pelos vetores de entrada, pela matriz, por três estimativas por submissão e pelo resultado.

**Verificação manual.** Com `v(x)=3x−x²/2`, uma submissão `x=1` e limiar zero, a estimativa original é igual a `5/2` por todas as regras. Após a duplicata exata, `v(2)=4`. As regras dão, por cada submissão, `5/2` separadamente, `3/2` ao excluir e `2/1` por Shapley. O ganho total do dono é, respectivamente, `5/2`, `1/2`, `3/2`. Só esse exemplo basta para refutar a ausência de ganho para cada uma das três regras em toda a família de tais modelos com limiar zero.

**Âmbito da conclusão.** O conjunto de participantes da comparação é fixado. O ruído é dado por um vetor explícito, o limiar é dado pela entrada. A aceitação, a nova seleção da composição após a dedução do limiar, os custos de submissão, o treinamento de parâmetros, os efeitos externos e o exame empírico estão fora deste modelo. O ganho numérico refere-se à soma das atribuições pela regra escolhida. A verificação completa de D1 exige comparar as utilidades da coalizão também com o trabalho honesto e com a inação. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.md) · [ROADMAP, D18 e D25](ROADMAP.md)

## M14. Verificação de fórmulas por enumeração finita

O núcleo `verification-enumerations@1` repete três pequenos experimentos. Ele permite verificar se o empacotamento preserva a distinção entre vetores admissíveis, e quantos erros deixam passar dois tipos de verificação por amostragem. Os dados de origem, a ordem de enumeração e os hashes de referência estão publicados em GPT2, §6.2 e «Código de controle para a primeira repetição». A cadeia é dada na tabela «O que entregar aos mini-agentes», e a condição de passagem no corpo está na §6.1. Trabalho GPT2 · [Resumo, §5.3](VERIFICATION_SEARCH.md)

O único parâmetro `cases` é um array de 1–4 strings distintas da tabela abaixo. `units = len(cases)`. Numeração a partir de zero; a unidade `u` calcula o experimento inteiro `cases[u]`. A chave `case` do resultado contém essa mesma string, e `kernel` é igual a `"verification-enumerations@1"`. O formato dos demais campos depende do experimento.

| `case` | Campos do resultado além de `case` e `kernel` | Valores de controle |
|---|---|---|
| `packing-8` | Inteiros `total`, `true_accepts`, `false_accepts`, string `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | Os mesmos campos | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Inteiros `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Inteiros `total`, `caught`, `missed` | 25, 20, 5 |

**Empacotamento posicional.** Tomar a base `B` da etiqueta do experimento. Enumerar `(x,y,c,d)` lexicograficamente em ordem crescente, com `x,y ∈ {−1,0,1}`, `c,d ∈ {−3,…,3}`. O laço interno varia `d`. O resultado verdadeiro é `(s,t)=(2x−y,−x−y)`. O critério de aceitação é a divisibilidade de `(c−s)+B(d−t)` por `B²` sobre os inteiros. Quando `(c,d)=(s,t)`, a aceitação incrementa `true_accepts`; nos demais casos de aceitação, incrementa `false_accepts`. Registrar, na ordem de enumeração, exatamente 441 bytes, cada um com valor 1 em caso de aceitação e 0 em caso de recusa. `verdict_sha256` é o SHA-256 desses bytes brutos na forma de 64 dígitos hexadecimais minúsculos. O hash usual do resultado da unidade é calculado separadamente de todo o JSON canônico. Para a verificação manual com `B=4`, `x=−1`, `y=1`, a resposta verdadeira `(−3,0)` e a declaração `(1,−1)` dão diferença 0.

**Cadeia.** Para cada defeito único `h=0,…,7`, enumerar todos os pares não ordenados sem reposição como `0 ≤ i < j < 8`. Incrementar `total` em 1 por cada tripla, e `caught` se `h=i` ou `h=j`. O número de omissões é `missed=total−caught`. Para cada `h`, há 28 pares, dos quais exatamente 7 contêm `h`.

**Corpo.** Enumerar os vetores `(x,y)∈{0,…,4}²`, incluindo o nulo. O erro `(1,−1)` é omitido exatamente quando `(x−y) mod 5 = 0`. `total` conta todos os vetores, `missed` conta as omissões, `caught=total−missed`. Cinco pares diagonais dão cinco omissões.

A unidade mais longa verifica 441 combinações e armazena 441 bytes de veredictos para um único SHA-256. Os contadores não excedem 441, o módulo da expressão de empacotamento não excede 46, e o maior módulo de divisão é 64. Bastam inteiros de 32 bits com sinal. Os resultados referem-se às faixas indicadas, a um único erro fixado e à enumeração completa de variantes equiprováveis. A generalização para um protocolo real exigiria justificar a distribuição das chamadas e a independência das verificações.

## Cálculos adiados


| Cálculo | O que já está definido | Quais dados permitirão obter um resultado inequívoco |
|---|---|---|
| M5. Ondas de falsificações | Para uma única falsificação barata com custos nulos, `π=m_s/(L+1)` e `H*=R(1/π−1)`. Por exemplo, com `L=36, m_s=2`, o limiar é igual a 17,5R | Para uma onda, é preciso fixar a distribuição conjunta das verificações e a transição do saldo em vários descobrimentos simultâneos, incluindo o momento do débito e a disponibilidade das recompensas da onda anterior. Com `π=1/2`, a amostra comum para dois erros iguais omite ambos com probabilidade 1/2; amostras independentes, com probabilidade 1/4. A analogia proposta com `exit-scam-a` exige também esclarecer se a sua probabilidade separada de designação para verificação se conserva. (claude1, §1.3, §4.2 e §7.5, item 3) (THREAT_MODEL, §1.8) |
| M7. Economia da revelação | Para um pagamento fixo R e o pagamento da prova apenas no ramo de sucesso, conhece-se a receita de uma tentativa `p(R−Pe)−c_view−c_commit` | Para o limite geral ε, são necessários o preço da tentativa descartada, a regra de pagamento em vários sucessos e a lei conjunta dos resultados dos candidatos no exame comum. O número de chaves por si só não determina essas grandezas. A ODU com prova obrigatória de cada tentativa dá outro orçamento, e em T4 o pagamento depende ainda da magnitude da melhoria. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, análise da ODU) |
| M18. Pagamentos e recuperação | Estão definidos a atomicidade da aceitação, o resgate único do direito no histórico canônico e a lista de cenários | Para a contagem dos caminhos, é necessária uma tabela de transições na mudança de ramo, um critério de finalidade, regras de recuperação quando os dados desaparecem e retornam, e um limite finito do número de reapresentações. Autômatos diferentes podem satisfazer os mesmos invariantes e dar números diferentes de pagamentos em históricos intermediários. (gpt1, §1 e §7) (critic_gpt, «Completude, recuperação e preço») |
