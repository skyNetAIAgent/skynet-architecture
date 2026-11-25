<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Verificação «sem força bruta»: o que a matemática oferece em vez do recálculo completo

[English](../../docs/STRATEGY_SEARCH.en.md) · [中文](../zh/STRATEGY_SEARCH.md) · [Español](../es/STRATEGY_SEARCH.md) · [Français](../fr/STRATEGY_SEARCH.md) · [Deutsch](../de/STRATEGY_SEARCH.md) · [Italiano](../it/STRATEGY_SEARCH.md) · [Русский](../../docs/STRATEGY_SEARCH.md) · **Português** · [العربية](../ar/STRATEGY_SEARCH.md)

Situação em 25 de novembro de 2026.

Este documento é o resultado do quinto conselho de modelos. O dono do projeto perguntou literalmente:

> «Talvez faça sentido escolher outra estratégia? Por exemplo, conectar alguma
> matemática? Para não verificar tudo em sequência, mas prever a tentativa de fraude e verificar apenas
> nesse caso? Ou fazer uma análise inteligente do funcionamento da rede skynet e encontrar comportamento
> suspeito? Pensem nessa direção, o que mais existe na ciência que possa ajudar a não resolver de forma direta».

O conselho analisou a teoria dos jogos de inspeção, a verificação por risco, a busca de anomalias, as
armadilhas, a verificação por amostragem, os mecanismos sem verificação, a criptografia e a economia sem
depósitos, e então propôs uma estratégia e redações de decisões.

**Status do documento.** É o resultado de raciocínio e de cálculo por fórmulas, e não uma medição.
Não houve experimentos, execuções da rede nem instalações para ele. Os participantes e os críticos
executaram apenas programas aritméticos curtos e pequenas enumerações no processador. Os números
medidos são tomados apenas dos [resultados do experimento D5](EXPERIMENT_D5.md) (resumo D5_RESULTS em
25 de novembro de 2026) e marcados [medido]; os números obtidos por fórmulas a partir de parâmetros
nomeados explicitamente são marcados [cálculo]. Os trabalhos dos cientistas são citados **de memória**:
não havia rede e os textos das fontes primárias não foram conferidos. **São decisões aceitas apenas as
decisões D1–D25** em [ROADMAP](ROADMAP.md), seção 3. Todo o resto aqui é avaliação e recomendação do
conselho. Onde os críticos divergiram, isso é dito diretamente.

## 1. Resumo curto

1. **«Prever a fraude e verificar apenas os suspeitos» com regras abertas não economiza
   verificações.** As regras de verificação são iguais em todos os nós e conhecidas do trapaceiro
   (D4). Ele apresenta a falsificação apenas onde o detector diz «seguro», e até o momento da fraude
   se comporta como honesto. Está provado de forma rigorosa: o detector eleva a probabilidade de
   verificação da falsificação acima da verificação média do trabalho honesto em não mais que a
   distância entre suas distribuições observáveis (seção 2). Por isso, a previsão, as anomalias, a
   confiança pelo histórico e os grafos podem apenas **adicionar** verificações acima do limite
   inferior, mas não baixar a frequência abaixo dele. Todos os seis trabalhos e todos os três críticos
   concordam com isso.
2. **Há exatamente duas características não falsificáveis:** o resultado do recálculo exato depois
   que a resposta é fixada de forma irrevogável, e o valor pendente que pode ser queimado —
   recompensas ainda não pagas da chave, que desaparecem na detecção. Toda a economia real vem da
   segunda característica, e não da «inteligência».
3. **A melhor estratégia encontrada para as respostas do modelo:** o pagador verifica ele mesmo sua
   resposta em uma única passagem, e decide «verificar ou não» com **sua moeda secreta** após a
   fixação da resposta, com probabilidade não inferior a `R/(R + H_lock)`. Aqui `R` é o preço da
   tarefa, `H_lock` é a parte das recompensas não vencidas do executor que não vencerá até o fim da
   verificação. A resposta de um novato com conta vazia é sempre verificada. Então, sob as condições
   da seção 4, a falsificação não compensa para nenhuma parcela de conluio dos demais, inclusive sob
   conluio total. Dois dos três críticos apoiam esta estratégia; o crítico ChatGPT prefere a
   verificação completa de cada resposta (seção 6).
4. **O preço da própria verificação, nesse caso, é de frações de por cento:** cerca de 0,005–2% do
   trabalho, dependendo do cronograma e da carga da chave; em chaves pouco ativas com limitação do
   dano — até 6,7% [cálculo]. O preço principal passa para o perfil exato: ele é 1,5–1,8 vezes mais
   lento que a geração de 8 bits usual com lote 1 e 2,5–2,8 vezes com lote 8 [medido]. Juntos, isso
   dá +50…+82% sobre a geração usual com lote 1 [cálculo]. A referência de 5% esbarra na velocidade
   do perfil exato, e não na verificação.
5. **O dano não é coberto pela economia.** O sabotador não precisa de lucro: na verificação por
   amostragem, parte de suas falsificações passa (cerca de metade no cronograma mais barato, seção 4).
   Por isso, uma resposta não verificada deve ter a marca «não verificado», e «verificado» só é
   colocado após a verificação completa antes da exibição. Para o passo de treinamento, o conselho
   não encontrou nova garantia.
6. **O usuário sem equipamento** não é protegido por esta estratégia: se nós alheios aleatórios
   verificam em seu lugar, o vazamento é `R·q^k` e, sob conluio total, igual ao preço inteiro
   (seção 5). Isso permanece uma questão aberta D21.
7. **O que o dono precisa decidir:** se permite o pagamento do não verificado pela regra da moeda
   (D21, D11, D7); o que fazer com as falhas honestas gratuitas (D16), que são incompatíveis com a
   verificação por amostragem; se aceita a nova decisão D26 sobre o «bloqueio» do valor pendente e o
   limite de devolução ao prejudicado; a regra de disputas falsas (D23, cálculo M9) continua sendo
   condição de inclusão. As questões estão formuladas na seção 6.

**Notações.** `R` — preço da tarefa; `c` — custo do trabalho honesto; `c_f` — custo da
falsificação (pior caso — quase zero); `H` — valor pendente da chave do executor;
`H_lock` — a parte dele que não vencerá até o resultado final da verificação desta tarefa;
`p` — probabilidade de verificação da tarefa; `q` — parcela de conluio entre os verificadores;
`k` — número de verificadores designados; `n_w` — número de tarefas da chave por janela de
vencimento; `ρ` — tempo de verificação da resposta em uma passagem dividido pelo tempo de sua geração
(0,10–0,40 com lote 1, 0,26–0,64 com lote 8 [medido]); `γ` — desaceleração do perfil exato em relação
ao llama.cpp Q8_0 (1,5–1,8 com lote 1, 2,5–2,8 com lote 8 [medido]); PPS — verificação pelo próprio
pagador. `Δ₀` e `Δч` — diferença esperada de ganho da falsificação contra a inação e contra o trabalho
honesto; D1 e D25 exigem que ambas sejam não maiores que zero.

**Como ler.** A seção 2 — por que a previsão da fraude não funciona. A seção 3 — tabela de todas as
abordagens. A seção 4 — fórmulas que resistiram à crítica e erros encontrados. A seção 5 — estratégia
recomendada, seu preço e risco residual. A seção 6 — questões-decisões. A seção 7 — cálculos e
experimentos. A seção 8 — divergências não resolvidas e referências duvidosas. A seção 9 — quem fez o
quê.

## 2. Por que «prever a fraude» não funciona com regras abertas

### 2.1. Limite pela variação total

Suponha que a decisão de verificação seja tomada por qualquer regra `π(x)` com valor de 0 a 1, onde
`x` é tudo o que a rede ou o pagador veem antes da decisão: tempo de resposta, texto, estatística,
histórico da chave, grafo de conexões. O trabalho honesto dá observações com distribuição `P`, a
falsificação — com distribuição `F`. Então

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

A desigualdade é verdadeira porque `π ≤ 1` onde `F > P`, e `π ≥ 0` onde `F < P`. A grandeza `TV` é a
distância de variação total: o quanto duas distribuições são afinal distinguíveis. Daí (teorema T4 do
trabalho claude2; a mesma desigualdade em gpt1 e gpt2):

1. **A falsificação é verificada não com mais frequência que o trabalho honesto em média, mais
   `TV`.** Se a falsificação é difícil de distinguir pelas observações (`TV ≈ 0`), o detector a
   verifica tão raramente quanto o trabalho honesto.
2. **Contra um adversário informado, é ainda pior.** As regras são abertas (D4), por isso o
   adversário calcula ele mesmo `π` e escolhe a observação em que a verificação é menos provável. A
   probabilidade de detecção de sua melhor falsificação é igual ao menor `π(x)` entre as observações
   que ele pode criar barato.
3. **Consequência para a economia.** Para que a falsificação seja deficitária, ela deve ser
   verificada com probabilidade não inferior a `R/(R + H_lock)` (seção 4). Com `TV ≈ 0`, a mesma
   frequência terá de ser mantida também para o trabalho honesto, ou seja, não há economia. Segundo a
   estimativa de claude2, o ganho da «inteligência» não é maior que o fator `R/(R − c*)`, onde `c*` é
   o preço da falsificação indistinguível mais barata; com um valor plausível `c* ≈ 0,5R`, isso não é mais que
   duas vezes, mas `c*` é escolhido pelo adversário e não foi medido.
4. **O histórico da chave não diz nada sobre o momento da fraude.** Uma chave que decidirá enganar
   na próxima tarefa tem, antes dessa tarefa, o mesmo histórico que uma honesta (razão de
   verossimilhança exatamente 1; teorema T5 de claude2, contraexemplo de gpt1). Por isso, os testes
   sequenciais (SPRT de Wald, CUSUM de Page), os algoritmos de bandit e a «confiança» bayesiana só
   saberão dela depois da fraude. Uma pequena enumeração de claude1 mostrou: se a frequência de
   verificação por confiança for reduzida em 10% abaixo do limiar, surge uma estratégia lucrativa
   «acumular confiança e enganar» (+1,7R…+2,5R em 60 tarefas); com redução pela metade —
   +14,4R…+19,4R [cálculo]. O crítico Claude reproduziu esses números, o crítico DeepSeek no modelo
   mais próximo obteve outra grandeza (+0,085R), mas o mesmo sinal (seção 8).

### 2.2. Exemplo com medições de D5

A falsificação barata mais natural é **o mesmo Qwen executado em llama.cpp Q8_0**. O perfil exato é
1,5–1,8 vezes mais lento que ela com lote 1 e 2,5–2,8 vezes com lote 8 [medido], por isso a
falsificação é sensivelmente mais barata que o trabalho honesto. Além disso, é a resposta do mesmo
modelo: tempo, estilo e perplexidade sob modelo pequeno são os mesmos de uma resposta honesta, e o
executor pode adicionar latência por conta própria. Se a resposta Q8_0 coincidiu com a resposta exata
token a token, isso não é falsificação: por D2, o resultado importa. Se divergiu em pelo menos um
token, apenas o recálculo exato detectará isso, porque os bits do perfil exato coincidem em qualquer
dispositivo testado [medido].

Ressalva do crítico ChatGPT: em D5 mediu-se a proximidade do perfil exato ao modelo oficial (o mesmo
token em 90 de 90 posições, correlação de logits 0,9996 [medido]), mas a proximidade da falsificação
Q8_0 ao perfil exato por características baratas não foi medida. Para a garantia, isso não importa:
basta que ninguém tenha mostrado uma característica que distinga cada falsificação disponível de uma
resposta honesta.

### 2.3. Onde os detectores ainda são úteis

Detectores, armadilhas e análise de rede são admissíveis se **apenas aumentam** a frequência de
verificação:

- como fila de verificações voluntárias adicionais do pagador, que não contam para a garantia, mas
  aumentam a detecção real;
- contra sabotadores descuidados, que não otimizam o comportamento;
- para diagnosticar falhas de equipamento e drivers; o participante pode manter um CUSUM sobre suas
  autoverificações e parar antes de perder o valor pendente;
- em um fluxo de erros não adaptativo, encontram mais erros por hora de verificação. Exemplo de gpt1
  [cálculo]: com parcela de falsificações de 2%, sensibilidade de 90% e 5% de falsos alarmes,
  verificam-se 8,57% das tarefas, detectam-se 90,2% dessa família de falsificações, com preço de
  1,80% contra 18,94% da verificação uniforme. Mas a família de falsificações que o detector não marca
  passa em 98% dos casos.

Há também o ataque inverso (claude2): solicitações cuja resposta honesta parece «anômala» fazem
gastar verificações com honestos. Se a verificação é paga por quem a provocou, isso se limita por si;
se pela rede, é transferência de carga.

## 3. Análise das abordagens

Na tabela, «garante» — o que decorre rigorosamente sob as suposições nomeadas; «com `q`» — o
comportamento com a parcela de conluio dos verificadores; «conta vazia» — o novato com `H = 0` e
muitas chaves gratuitas; «veredito» — o resultado após as três críticas.

| Abordagem | Essência | O que garante | Com `q` e com `q = 1` | Conta vazia, muitas chaves | Preço | Veredito após a crítica |
|---|---|---|---|---|---|---|
| Jogos de inspeção (Dresher, Maschler, revisão de Avenhaus–von Stengel–Zamir; jogos de segurança de Tambe e coautores — de memória) | Verificação aleatória anunciada de antemão, com frequência na qual a fraude não compensa | `Δ₀ ≤ 0` com `p ≥ (R − c_f)/(R + H_lock)`, inclusive para uma leva de falsificações antes da saída (sob as condições da seção 4) | Se o pagador verifica, não depende de `q`, inclusive `q = 1`. Se são verificadores designados — detecção `p·(1 − q^k)`, com `q = 1` zero | `H = 0` ⇒ `p = 1`; cada chave responde com seu próprio valor, Sybil não ajuda | `p·ρ`: centésimos a décimos de por cento em chaves ativas; verificação completa no novato [cálculo] | **Base da estratégia**, se a frequência é executada por quem tem dinheiro em jogo |
| Verificação por risco: SPRT, CUSUM, bandits, confiança bayesiana | Verificar com mais frequência novatos e suspeitos, com menos frequência os antigos | Captura rapidamente um trapaceiro ruidoso constante; contra um estrategista, nada | O veredito por opiniões dos verificadores quebra sob conluio; com `q = 1`, zero | Novas chaves são gratuitas; uma chave «antiga» acumula confiança e engana no final | A economia de 40–70% (ds1) refere-se a um adversário ruidoso, não ao SkyNet | **Não se pode** reduzir a frequência abaixo do limiar (contraexemplo da seção 2.1); pode-se distribuir verificações adicionais |
| Anomalias, grafos, Sybil (tempo, logits, entropia, perplexidade de modelo pequeno, marcas d'água, consistência de repetições, grafos de conluio, SybilGuard/SybilLimit/SybilRank) | Buscar comportamento suspeito e conexões | Contra quem conhece o detector — nada (limite da seção 2.1) | Uma falsificação coordenada parece concordância honesta; com `q = 1` não há proteção | SybilRank exige nós iniciais confiáveis e um número pequeno de conexões «atacantes»; a coalizão compra conexões com trabalho honesto | A perplexidade de modelo pequeno — cerca de 1,3–5% de **cada** resposta segundo a estimativa de claude1 (crítico ChatGPT: nas bordas de ds2, 1,875–9%) [cálculo], mais caro que a verificação pela regra; a marca d'água atesta apenas o amostrador | Apenas **sinal para verificações adicionais** e diagnóstico de falhas |
| Armadilhas, gold questions, modelo Dawid–Skene | Tarefas com resposta conhecida, indistinguíveis das reais | Apenas se a armadilha é indistinguível e a resposta é secreta. Em uma rede pública, só o pagador pode guardar o segredo, e a armadilha coincide com a verificação dele (T9 de claude2) | O conluio compartilha as armadilhas instantaneamente; Dawid–Skene supõe erros independentes | Chaves descartáveis estudam as armadilhas por sondagens; o tipo de tarefa (D22) é visível ao executor | Uma referência nova de texto livre custa uma geração completa, mais caro que a verificação (`ρ < 1`); para o nível `2⁻⁸⁰` com parcela de armadilhas de 10%, são necessárias 526–527 designações [cálculo] | Não é mais barato que a verificação pelo pagador; a forma admissível é a repetição de uma solicitação já verificada do pagador |
| Verificação por amostragem e loteria (parte dos tokens ou camadas após a fixação; BOINC, TrueBit, opML, proof of sampling — de memória) | Verificar uma pequena parte do cálculo; ou pagar apenas pelo escolhido por sorteio (loteria B) | Tokens: um defeito passa com probabilidade `1 − s/N` (99,2% com 8 posições de 1000 [cálculo]). Loteria B com verificação do escolhido pelo pagador: `Δ₀ = −c_f` para qualquer `p` | A loteria com comitê dá ao novato `R·q^k`: 0,001R / 0,027R / 0,125R / R com `q` = 0,1 / 0,3 / 0,5 / 1, `k = 3` [cálculo] | A loteria B com o pagador serve para o novato; a amostragem de tokens — não | Estado do Qwen3.5-4B: 48 MiB + 64 KiB por posição, uma amostra na posição 500/1500/4000 — 79/142/298 MiB [cálculo]; a loteria dá renda irregular e exige pré-pagamento de `R/p` | Tokens e camadas são **piores** que a passagem completa tanto em tráfego quanto em garantia; a loteria B com o pagador é uma variante admissível. Os sistemas externos dependem de depósito ou de «um honesto entre N» |
| Peer prediction (Bayesian Truth Serum de Prelec, peer truth serum, DMI — de memória) | Pagar pela consistência dos relatórios sem verificação | A veracidade é equilíbrio apenas sem conluio; há equilíbrios não informativos | Com `q > 0` o grupo se coordena; com `q = 1` o mecanismo paga por qualquer coisa | Bilhetes gratuitos de cada chave | Não há verificação, mas paga-se por algo desconhecido | **Inaplicáveis** ao cálculo determinístico; o pagamento por coincidência é pagamento por cópia, proibido por D15 |
| Criptografia sem prova completa, TEE, semente | Compromissos e revelações seletivas, disputa por bisseção, sumcheck/GKR, atestação de TEE, geração determinística | A amostragem sem codificação — o mesmo limite `1 − s/N`; a prova completa — sim sob D19, mas pela estimativa da etapa 4 é 16,8 vezes mais cara e também mais cara para a resposta; TEE — confiança no fabricante | A disputa e o determinismo não dependem de `q`; no TEE, uma chave extraída atinge todo o parque | Reduzir a frequência por atestação daria a frequência reduzida a todas as chaves do adversário | Compromisso sobre a resposta — 2–4 KB no registro (D24) | São necessários o compromisso sobre a resposta, a moeda secreta e a disputa pela metade; TEE — apenas para aumentar a verificação ou a privacidade. A proposta de ds1 de reduzir a frequência por TEE foi rejeitada por todos os críticos |
| Economia sem depósitos (pagamentos diferidos, reputação como capital, seguro, preço da chave pelo trabalho) | Punir com a perda de recompensas não vencidas e da renda futura | O valor pendente é a única alavanca compatível com R5. A renda futura ao sair é zero. O seguro indeniza a vítima, mas não reduz o ganho do trapaceiro | Funciona se a frequência é executada pelo pagador | `H = 0` ⇒ verificação completa. A entrada pelo trabalho é um depósito oculto, inútil na saída; com vazamento por comitê `R·q³` e `q = 0,3`, cerca de 370 tentativas pagam o preço de entrada `10R` (ds1) [cálculo] | Atraso do pagamento por uma janela de vencimento | `H_lock` é a parte obrigatória da estratégia; o resto não serve de base para a garantia |

## 4. Limites inferiores e fórmulas que resistiram à crítica

### 4.1. Falsificação isolada: limiar `R/(R + H_lock)`, e não `R/H`

Uma falsificação detectada não é paga e queima o valor pendente (nada mais pode ser debitado por R5).
Então

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

e, com falsificação quase gratuita — `p ≥ R/(R + H_lock)`. Contra o trabalho honesto
`Δч = Δ₀ − (R − c) ≤ Δ₀`, por isso a segunda condição de D25 se cumpre sozinha. No novato
`H_lock = 0`, e `p = 1`. Frequência mínima [cálculo, claude2]: 0,5 com `H_lock = R`; 0,25 com `3R`;
0,0909 com `10R`; 0,01 com `99R`; 0,000231 com `4320R`.

O trabalho claude1 propôs a regra `p = min(1, R/H)` e a chamou de exata. O crítico Claude mostrou por
enumeração que o limiar exato é `R/(R + H)`: com ele, o maior ganho da falsificação é exatamente 0, e
já com `0,99·R/(R + H)` — de +0,225R a +0,299R [cálculo]. A regra `R/H` contém uma margem. O crítico
DeepSeek observou que essa margem é útil para o dano: com `R/H`, o número esperado de falsificações até
a detecção é finito (cerca de `H/R + 1`), com `R/(R + H)` — infinito (seção 4.4). Qual fórmula adotar
no núcleo não está decidido (seção 8).

### 4.2. Condição: o valor não vence até o resultado da verificação

Só se pode queimar o que ainda não foi pago no momento da disputa provada. Se uma parte de `H`
consegue vencer antes, a regra quebra. Contraexemplos [cálculo]:

- claude2: uma chave com `H = 99R`, vencendo antes do resultado, apresenta `n` falsificações com
  `p = 1%`; ganho 0,99R com `n = 1`, 9,04R com 10, 36,6R com 100;
- crítico Claude: uma chave com `H₀ = 100R` interrompe o trabalho honesto e apresenta falsificações,
  e os pagadores verificam tarde; ganho +0,99R, +9,1R, +49,7R, +74,4R com `n` = 1, 10, 100, 300.
  Com o «bloqueio» (tudo é queimado), as mesmas estratégias dão de −0,01R a −0,75R.

Por isso, no denominador da frequência para a tarefa `i` entra apenas a parte do valor que vencerá
**após** o prazo limite da disputa sobre `i`, e o prazo de verificação pelo pagador `δ` deve ser muito
menor que a janela de vencimento `W`; ambos os prazos são contados em tempo ativo (D12). É a suposição
de «verificação tempestiva»; para um telefone que raramente sai à rede, ela é a primeira a ser violada.

### 4.3. Ondas de falsificações antes da saída

A fórmula da falsificação isolada cobre uma leva de falsificações antes da saída apenas com a regra
**«a primeira detecção provada queima todo o valor não vencido da chave, incluindo as recompensas da
mesma onda»**.

- Sem essa regra (gpt1): 10 falsificações paralelas com `R = 1`, `B = 4R`, `d = 0,2`, quando cada
  uma que passa é paga e o valor antigo é perdido uma vez, dão
  `10·0,8 − 4·(1 − 0,8¹⁰) = +4,4295R`, embora uma falsificação dê zero. Se a detecção anula toda a
  onda, a mesma estratégia dá −2,49676R [cálculo; repetido pelos críticos].
- O crítico ChatGPT acrescentou um segundo exemplo: com `H = R`, `p = 1/2`, duas falsificações com
  moedas independentes e um único débito do valor antigo, o ganho é `R/4` [cálculo]. Logo, o
  protocolo deve vincular atomicamente todos os compromissos abertos da chave a toda a sua receita não
  vencida.

Com essa regra, a prova de claude2 (T2) está correta: cada nova falsificação multiplica o resultado
esperado por `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, onde `α_j` é o pagamento pelo não verificado e
`A` é o que já foi acumulado como queimável. A indução pelo número de falsificações dá
`E[resultado] ≤ H_lock` para qualquer leva e qualquer sequência adaptativa. Para uma leva homogênea, o
mesmo decorre de `(1 + R/H)ⁿ ≥ 1 + nR/H`. A verificação em uma grade de frações exatas deu o maior
excesso exatamente 0 [cálculo].

### 4.4. Verificação por comitê: fator `1 − q^k`

Se a detecção deve ser registrada por pelo menos um dos `k` verificadores designados, e cada um com
probabilidade `q` pertence à coalizão, a probabilidade de detecção cai para `p·(1 − q^k)`, e o limiar
se torna `p ≥ R/((R + H_lock)·(1 − q^k))`. Ele é inexequível quando `1 − q^k < R/(R + H_lock)` e
sempre inexequível quando `q = 1`. Na loteria B com comitê, o novato recebe `R·q^k` por tentativa:
0,001R / 0,027R / 0,125R / R com `q` = 0,1 / 0,3 / 0,5 / 1 e `k = 3` [cálculo]. Isso coincide com o
modelo do adversário. A independência das escolhas também é uma suposição: ao escolher `k` diferentes
de `N` participantes, dos quais `C` estão em conluio, a probabilidade de conluio total é
`C(C,k)/C(N,k)`; com indisponibilidade geral dos dados ou emissão seletiva, ela pode chegar a `q` ou a
1 (crítico ChatGPT, segundo o modelo do adversário). Conclusão de todos os trabalhos: **a frequência
deve ser executada por aquele cuja decisão é protegida** — o pagador para o seu dinheiro, cada nó para
a sua contabilidade.

### 4.5. Dano: a parcela não detectada

O sabotador não precisa de lucro, por isso o dano é avaliado pela fração de suas falsificações que
passam sem detecção.

- **O cronograma mais barato torna o dano ilimitado.** Com `p = R/(R + H)`, as falsificações não
  verificadas aumentam `H` por si mesmas, e a frequência cai. A probabilidade de sobreviver a `n`
  falsificações a partir de `h = H/R` é `h/(h + n)`; o número esperado de falsificações até a
  detecção é infinito (T8 de claude2). A estimativa de claude1 «`e^{−m}`» subestima a passagem: com
  `H₀ = 4320R` e 4320 falsificações, a passagem exata é 0,50 em vez de 0,37 com frequência `m·R/H` e
  `m = 1`; 0,125 em vez de 0,050 com `m = 3`; 0,0078 em vez de 0,0009 com `m = 7` [cálculo, crítico
  Claude].
- **Uma falsificação direcionada** passa com probabilidade `1 − p`: em uma chave madura com
  `n_w = 4320`, cerca de 99,977% (crítico ChatGPT) [cálculo].
- **A correção pela parte verificada do valor não resistiu.** claude2 propôs calcular a frequência por
  `H_ver` — recompensas apenas pelas tarefas verificadas; então, em uma chave honesta, `p ≈ 1/√n_w`
  (ponto fixo `p²·n_w + p − 1 = 0`) e a fração de falsificações do sabotador é cerca de `p`: 5,6% com
  `n_w = 300`, 1,8% com 3000, 0,58% com 30 000 [cálculo]. O crítico Claude mostrou que `H_ver` é
  inflado por solicitações autopagas da coalizão; o crítico ChatGPT — que um sabotador com nova chave,
  após uma resposta verificada com `p = 1/2`, consegue que cerca de metade de suas respostas entregues
  seja falsa. Nenhum trabalho encontrou um limite econômico de dano que resista ao autopagamento e a
  novas chaves.

Conclusão: com qualquer `p < 1`, parte das respostas do sabotador é falsa. Para solicitações, isso é
admissível apenas com a marca «não verificado» (texto D6); para o passo de treinamento, não.

### 4.6. Outras fórmulas que resistiram à crítica

- **Falhas gratuitas são incompatíveis com a verificação por amostragem** (claude1). Se uma falha
  honesta não queima o valor (D16), o trapaceiro detectado chama a falsificação de falha, e
  `Δ₀ = (1 − p)·R − c_f > 0`. Com `b` falhas gratuitas por janela, o vazamento é da ordem de `b·H` por
  janela [cálculo].
- **Pagadores preguiçosos** (claude2). Se a parcela `λ` dos pagadores não verifica e o executor não os
  distingue, é preciso `p·(1 − λ) ≥ R/(R + H_lock)`. Se os distingue — a falsificação contra eles
  rende até `R` sem risco. A dissuasão é um bem comum: o pagador que desliga a verificação economiza
  frações de por cento e não perde nada. É a suposição «os pagadores em média executam a moeda do
  núcleo».
- **Preço e irregularidade da loteria B** (claude2, T7, com correção do crítico ChatGPT). O pagamento
  de `R/p` com probabilidade `p` dá um coeficiente de variação da renda de até `√((1 − p)/(pT))` em
  `T` tarefas. Para uma dispersão dada `v`, é preciso `p ≥ 1/(1 + T·v²)`; com `T = 6000`, `v = 10%`,
  `ρ = 0,21`, o preço mínimo da verificação é 0,3443% [cálculo]. Na verificação «por cada um dos 1000
  nós», o mesmo preço é multiplicado pelo número de nós; por isso, a loteria com verificação por todos
  os nós é inadequada para a emissão de créditos.
- **Conluio entre pagador e executor** reduz-se a transferir seu próprio dinheiro dentro da coalizão,
  desde que a solicitação paga não crie emissão de créditos, peso nem direito a indenização do caixa
  comum.

### 4.7. Erros nas fórmulas dos trabalhos (brevemente)

| Trabalho | Erro | Correção |
|---|---|---|
| ds2 | O segundo limiar está escrito como `(c − c_f)/R` | Deve ser `(c − c_f)/(R + H)`; esse limiar nunca é restritivo. Passar aos mini-agentes apenas o corrigido |
| ds1 | No jogo, a perda foi tomada como `L = H + V` sem considerar a `c_f` já gasta | Limiar `(R − c_f)/(R + H + V)`; com `H = 0`, `c_f = 0,1R` — 90%, e não 100% |
| claude1 | Equilíbrio do jogo de inspeção com `L = H + R` (contagem dupla de `R`) | Ponto de indiferença `(R − c_f)/(R + H)`: com `H = R`, `c_f = 0` — 1/2, e não 1/3 |
| claude1 | «A regra `R/H` é exata»; dano `e^{−m}` | Limiar exato `R/(R + H)`; a passagem é maior (seção 4.5) |
| claude1 | Geração especulativa «cerca de `1 + ρ·s`» | Não deduzido; segundo o crítico DeepSeek — contagem dupla; com lote 8 resulta 1,65–2,79 |
| claude2 | T7: «`κ·CV²` não depende de `p`» | Há um fator `1 − p`; limiar exato `p ≥ 1/(1 + T·v²)` |
| claude2 | O preço agregado de 0,2–1,2% foi tomado com `n_w = 3000` | Com `n_w = 300` — 0,56–2,24% (até 3,6% com lote 8), com `n_w = 30` — 1,7–6,7% [cálculo] |
| claude2 | Instantâneos de estado de 0,33 e 2,9 GiB por resposta | Com cache de atenção de 0,651 GiB (500/500, passo 64) e 12,38 GiB (2000/1000, passo 16) [cálculo, crítico ChatGPT] |
| claude2 | Em S1, o pagamento do não verificado `α` sob a regra por `H_ver` é sempre igual a `R` | Não há transição suave A/B em S1; o farol comum para a decisão de verificação não é necessário |
| ds1, gpt1, gpt2 | Estimativas de estratégias sem a desaceleração do perfil exato | O preço total é 1,5–1,8 vezes maior já com lote 1 (seção 5.2) |
| ds1 | «A verificação de `k` tokens não é mais barata que a passagem completa» | Em termos de cálculo, é mais barata; perde em tráfego de estado e em garantia |
| gpt2 | Certificado por limites de logits: 6,25% | Os limites exigem o estado verdadeiro da última camada; a cabeça é cerca de 15% das multiplicações, e a economia não é maior que sua fração |
| ds2 | Fração estável de fraude contra CUSUM `θ = d_h/(d_h + d_f)` | É uma aproximação pelo desvio médio, e não um teorema |
| ds1 | SPRT: 65 e 133 observações | Recálculo exato do crítico ChatGPT: 132,73 e 76,70, teste fixo — 229 [cálculo]; não se aplica ao adversário estratégico |

## 5. Estratégia recomendada

### 5.1. Respostas do modelo: «pagador-inspetor com aposta»

O núcleo foi tomado dos trabalhos claude1 e claude2, as correções — de gpt1 e das três críticas.

1. **Perfil exato.** Cada resposta paga é gerada no perfil exato v2 (escolha gulosa ou Gumbel-max
   canônico), e o texto cifrado da resposta é gravado no registro em uma única entrada com a aceitação
   (D24).
2. **Moeda secreta do pagador.** Depois que a resposta é fixada de forma irrevogável, o programa do
   pagador decide, com sua aleatoriedade secreta, se a verifica em uma única passagem, com
   probabilidade `p_i = max(p_usuário, R_i/(R_i + H_lock))`. `p_usuário` é escolhido pelo próprio
   usuário; com `p_usuário = 1` ele vê apenas respostas verificadas. Com `H_lock = 0` (novato) a
   verificação é sempre. Um farol comum não é necessário para isso, enquanto o pagamento não depende
   do resultado da moeda; a decisão não espera um bloco público.
3. **Bloqueio do valor.** `H_lock` para a tarefa `i` — recompensas não vencidas da chave que vencerão
   depois do prazo limite da disputa sobre `i`; o prazo de verificação `δ` é muito menor que a janela
   de vencimento (seção 4.2).
4. **Queima.** Qualquer erro provado queima **todo** o valor não vencido da chave, incluindo
   as recompensas da mesma onda. Ao prejudicado é devolvido não mais que o seu pagamento `R`, o resto
   é destruído. Caso contrário, é possível o ataque de «autodisputa»: a coalizão detecta com sua
   chave-pagador uma solicitação autopaga deliberadamente falsificada e toma valores alheios
   contornando a janela de vencimento (crítico Claude).
5. **Marcas.** «Verificado» — apenas a resposta verificada por completo antes da exibição. Todo o
   resto é, por padrão, «não verificado». A marca «verificado por amostragem» (claude1) foi rejeitada
   por todos os críticos como enganosa.
6. **Sinais apenas para cima.** Anomalias, perplexidade, grafos e repetições de solicitações
   verificadas (armadilhas) disparam apenas verificações voluntárias adicionais. É proibido reduzir a
   frequência por histórico, reputação, anomalias, atestação ou número de chaves.
7. **Disputas** — apenas por prova de erro, que cada nó verifica ele mesmo (I8). A estratégia
   não é incluída sem a regra de disputas falsas (D23, cálculo M9).
8. **Variante para chaves com valor pequeno.** Onde a verificação frequente é cara para o pagador, é
   admissível a loteria B: paga-se apenas a resposta escolhida por sorteio, e o pagador a
   verifica por inteiro (gpt1, claude2). Nela, a falha honesta gratuita (D16) se mantém sem
   alterações, mas a renda do executor é irregular, e o pagador mantém um pré-pagamento de `R/p`.

A estratégia exige alterar D16 e D21 (seção 6). Todos os zeros da garantia são condicionais:
coincidência de bits nos dispositivos testados, e não em quaisquer dispositivos; verificação
tempestiva; vivacidade do registro e ausência de censura da prova; correção do núcleo; execução
honesta da moeda pelo programa do pagador; regra de disputas falsas.

### 5.2. Preço

Parâmetros: `p = R/(R + H)` com `H ≈ n_w·R` em regime; `ρ` = 0,10 / 0,21 / 0,40 (lote 1);
`γ` = 1,5–1,8 (lote 1) e 2,5–2,8 (lote 8). O preço total contra Q8_0 — `γ·(1 + p·ρ) − 1`.
Tabela do crítico Claude [cálculo]:

| `n_w` (tarefas da chave por janela) | `p` estável | Verificação com `ρ` = 0,10 / 0,21 / 0,40 | Total contra Q8_0, lote 1 | Total, lote 8 | Verificações na primeira janela da nova chave |
|---|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5% … +82,3% | +152% … +186% | cerca de 4,0 |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0% … +80,2% | +150% … +181% | cerca de 6,3 |
| 4320 | 0,023% | 0,002% / 0,005% / 0,009% | +50,0% … +80,0% | +150% … +180% | cerca de 9,0 |

Outros cronogramas [cálculo]: na frequência mínima em termos de dinheiro
`p ≈ t_task/t_lock ≈ 2,3·10⁻⁴`, a verificação custa cerca de 0,005% do trabalho (crítico DeepSeek);
na frequência com limitação do dano `p ≈ 1/√n_w` — 0,18–0,72% com `n_w = 3000` e 0,56–2,2% com
`n_w = 300`; na loteria B com `p = 5%` — 0,5–2,0% com lote 1. Se à regra monetária se acrescentar um
piso contra o dano por `H_ver`, a verificação cresce até 0,15–2,2% com `n_w` = 300–4320 e até 6,7%
com `n_w = 30` (crítico Claude). A primeira tarefa do novato custa uma verificação completa, 10–40%
de sua geração.

Para comparação: a verificação completa de cada resposta (contrato principal de gpt1, gpt2, ds2)
custa `γ·(1 + ρ) − 1` = +65…+152% contra Q8_0; com `γ = 1,65`, `ρ = 0,21` — +99,65% [cálculo].

Não foram calculados: a gravação de 2–4 KB por cada resposta no registro, as disputas falsas (M9), a
energia, a verificação nos dispositivos dos pagadores. **O gargalo da referência de 5% é a
desaceleração do perfil exato, e não a verificação.** Podem reduzi-la núcleos rápidos bit a bit iguais
e a decodificação especulativa exata: o rascunho é gerado pelo Q8_0 rápido, e o perfil exato aceita o
prefixo até a primeira divergência. A estimativa de claude2 com coincidência de 99% dos tokens e bloco
32 — cerca de 0,78 do tempo do token exato, ou seja, +28% sobre o Q8_0 em vez de +65%; com
coincidência de 95% — 1,33 do tempo do token exato, pior que a geração direta (crítico Claude)
[cálculo; a coincidência não foi medida].

### 5.3. Risco residual

Ganho esperado por falsificação; «dano» — a fração de falsificações não detectadas do sabotador,
todas com a marca «não verificado». Resumo do crítico Claude e do crítico DeepSeek [cálculo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novato, `H = 0` |
|---|---|---|---|---|---|
| Dinheiro, o pagador verifica ele mesmo | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verificação sempre) |
| Resposta falsa exibida como «verificado» | 0 | 0 | 0 | 0 | 0 |
| Dano com `p = R/(R + H)`: não detectado após `n_w` falsificações | cerca de 50% | cerca de 50% | cerca de 50% | cerca de 50% | 0 (as primeiras são verificadas) |
| O mesmo com `p = 3R/(R + H)` | cerca de 12,5% | o mesmo | o mesmo | o mesmo | 0 |
| Pagador sem equipamento delega a verificação a um trio aleatório | +0,001R | +0,027R | +0,125R | +R | o mesmo |
| O pagador não verifica, o executor o distingue | até +R | até +R | até +R | até +R | 0 |
| Treinamento, há auditor honesto de frequência completa | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Treinamento, não há auditor honesto | até +R | até +R | até +R | até +R | até +R |

As linhas «o pagador verifica ele mesmo» não dependem de `q`. É este o principal resultado do
conselho: a verificação que não depende da parcela de conluio é barata no pagador, se ele verifica por
amostragem, e o valor queimável do executor está bloqueado até o fim da verificação.

### 5.4. Novato

Uma chave com conta vazia é sempre verificada, por isso a falsificação nela dá `−c_f`. À medida que o
valor bloqueado se acumula, a frequência cai: com a regra `R/(R + H)`, na primeira janela há cerca de
4,0 / 6,3 / 9,0 verificações completas com `n_w` = 30 / 300 / 4320 (crítico Claude); com a regra
`R/H` — 5,0 / 7,3 / 10,0 (claude1) [cálculo]. O preço da primeira janela com `n_w = 30` — 1,7 / 3,5 /
6,6% com `ρ` = 0,10 / 0,21 / 0,40 (claude1) [cálculo]. O «preço de entrada» é o trabalho útil
verificado por completo, e não uma contribuição inicial. O outro lado é a carga: a coalizão de novas
chaves obriga os pagadores a verificar cada resposta delas. Isso pesa no preço (R6), mas não em D1; a
grandeza precisa ser calculada (seção 7).

### 5.5. Usuário sem equipamento

A estratégia não o protege. Se ele delega a verificação a um trio aleatório de nós alheios, o
vazamento esperado é `R·q³`: 0,001R / 0,027R / 0,125R / R com `q` = 0,1 / 0,3 / 0,5 / 1 [cálculo]. Se
ele a delega ao seu dispositivo ou a um nó conhecido, essa é sua suposição por D21; sob conluio do
auxiliar com o executor, uma confirmação falsa é possível com probabilidade 1. O crítico Claude
propõe verificar por experimento quanto custa a verificação em uma passagem no processador de um
notebook e de um telefone: com frequência de cerca de uma verificação por janela da chave, uma
verificação lenta rara pode ser aceitável. A garantia para esse usuário permanece uma questão aberta
D21.

### 5.6. Treinamento

Para o passo de treinamento, o conselho não encontrou nova garantia. O passo não tem um pagador cujo
dinheiro está em jogo, por isso a verificação por amostragem deve ser executada por cada nó que
precisa da garantia, e o preço é multiplicado pelo número desses nós. Variantes:

- **Repetição completa do passo** a partir do pai aceito — cerca de 100% do trabalho do passo para
  cada nó verificador. Exemplo do crítico ChatGPT: se a inferência é 80% do trabalho base, `ρ = 0,21`
  e cada passo é repetido uma vez, resulta 0,8·0,21 + 0,2·1 = 36,8% acima do trabalho base [cálculo];
  com `N` nós que verificam por conta própria, a segunda parcela é multiplicada por `N`.
- **Verificação por amostragem do passo por todos os nós completos** (claude2, S2): apenas para o
  dinheiro com janela de 3 dias — 0,23% / 2,3% / 23% do trabalho da rede com 10 / 100 / 1000 nós
  verificadores; com limitação do dano de 10% — 10 vezes mais caro [cálculo; a coluna do dano não foi
  deduzida rigorosamente]. Exige treinamento inteiro exato, que não foi construído nem medido.
- **Auditoria «um honesto entre N»** (claude1, S2) — é uma suposição que a etapa 4 já rejeitou para o
  treinamento; sem auditoria paga, o equilíbrio é «não há auditores».
- **Pagamento pela melhoria comprovada (D18)** — não é verificação do passo; o cálculo M12 já mostrou
  que a duplicata exata da solicitação aumenta a atribuição do dono por todas as três regras de
  atribuição (cálculo dos mini-agentes, resumo D5_RESULTS).

A agregação robusta de contribuições (Krum, mediana, média truncada — de memória) limita o dano da
parcela não detectada, mas não protege contra sabotadores coordenados com parcela de peso notável e
não cumpre D1. Um passo não verificado não deve entrar na versão lançada do modelo (D6).

## 6. Decisões que precisam ser alteradas ou aceitas

As formulações abaixo são **recomendações do conselho**, e não decisões aceitas. Cada questão precisa
ser aceita ou rejeitada explicitamente. Os requisitos imutáveis R1–R6 não mudam com a edição de uma
linha do roteiro (lembrete de gpt1).

**Questão 1 (D21, e também D11 e D2). Permitir que o pagador pague do seu pré-pagamento a resposta que
seu programa, pela regra do núcleo, não verificou?** Hoje D21 diz: «A rede não paga por uma
resposta sem verificação», e D11 — «só se paga o verificado».
*Recomendação (crítico Claude, pelos trabalhos claude1 e claude2):* sim. A segunda frase proposta de
D21: «O pagador paga do seu pré-pagamento a resposta que ele verificou ou pulou pela regra D7 com sua
moeda secreta; a resposta pulada tem a marca «não verificado». Não há emissão de créditos nem peso pela
solicitação paga». Ao mesmo tempo, é preciso precisar D11 (e, conforme a observação do crítico
DeepSeek, D2), caso contrário as edições se contradizem.
*Onde divergiram:* crítico DeepSeek — não alterar D21 por enquanto (a estratégia já está bloqueada por
D23) e usar a loteria B (`α = 0`, pagamento de `R/p` ao escolhido), compatível com as atuais D2, D11,
D21. Crítico ChatGPT — deixar como contrato principal a verificação completa de cada resposta pelo
pagador, e introduzir o pagamento dos escolhidos de um lote por contrato separado; sem verificação
própria, não há pagamento pela rede.

**Questão 2 (D7). Como registrar qual verificação é admissível para o pagamento?**
*Recomendação (crítico Claude):* «A verificação que não depende da parcela de conluio é obrigatória
para a marca «verificado», para a emissão de créditos e para o peso. O pagamento da solicitação com
recursos do pagador é admitido após a verificação pelo pagador ou após a dispensa da verificação pela
regra do núcleo: moeda secreta do pagador, lançada após a fixação da resposta, probabilidade não
inferior a `R_i/(R_i + H_lock)`. É proibido reduzir essa probabilidade por histórico, reputação,
anomalias, atestação ou número de chaves; aumentar é permitido. A verificação por verificadores
designados não serve de base para o pagamento. D1 não é enfraquecido até `q < q*`». Separadamente, é
preciso escolher `R/(R + H_lock)` (limiar exato) ou `R/H` (com margem, número finito de falsificações
do sabotador até a detecção).
*Onde divergiram:* os críticos DeepSeek e ChatGPT propõem não alterar o texto de D7, mas acrescentar
seu âmbito: a garantia para a parte que executa ela mesma a verificação não depende de `q`; a parte
que delegou a verificação é protegida apenas se a parcela de conluio dos designados for inferior a
`q*`, e isso lhe é mostrado (crítico DeepSeek). O crítico ChatGPT acrescenta: classificação, quórum,
expiração de prazo e a suposição `q_eff < q*` não dão direito a status independente.

**Questão 3 (D6). Esclarecer as marcas do resultado?**
*Recomendação (comum aos críticos, formulação por ds1):* «Uma resposta falsa não é entregue como
«verificado». As marcas são duas: «verificado» — verificação completa antes da exibição por um método
que não depende da parcela de conluio (para a solicitação — pelo próprio pagador, ou por prova aceita
pelo núcleo); «não verificado» — por padrão, colocada automaticamente, e só tal verificação pode
retirá-la. A entrega em fluxo — em blocos verificados ou com essa marca. Um passo de treinamento não
verificado não entra na versão lançada do modelo». O crítico ChatGPT esclarece: o passo não verificado e
seus descendentes podem existir apenas em um ramo de pesquisa isolado, sem pagamento pela transição.
*Onde divergiram:* no essencial não divergiram; claude1 propôs uma terceira marca, «verificado por
amostragem» — ela foi rejeitada por todos os três críticos.

**Questão 4 (D16). O que fazer com uma falha honesta de hardware?** Hoje a falha não é punida, e o
valor pendente não é queimado. Na verificação por amostragem com pagamento do não verificado, isso é
vazamento direto (seção 4.6).
*Recomendação (críticos Claude e DeepSeek, por claude1):* «Na verificação completa ou na loteria B, a
falha honesta não é punida (regra anterior). Na verificação por amostragem com pagamento do não
verificado, qualquer divergência provada queima o `H_lock` da chave independentemente da causa, pois a
causa não pode ser estabelecida a partir de uma saída errada idêntica. A perda esperada do honesto (cerca de
`P_f·R` por tarefa, onde `P_f` é a probabilidade de falha silenciosa) é indenizada por um acréscimo
incondicional da taxa da rede. A regra só é ativada após a medição de `P_f`».
*Onde divergiram:* crítico ChatGPT — preservar a proteção contra a falha honesta: a falha deixa o
resultado sem pagamento, as recompensas anteriores são preservadas, o número de falhas por chave é
limitado, e a confiabilidade do cálculo não deve depender do débito de recompensas anteriores. Ele
também observa que o acréscimo da taxa alheia por cada tarefa aumenta o pagamento também para a
falsificação e muda o limiar. O crítico Claude acrescenta: queimar a janela de renda por uma
instabilidade não medida atinge os nós fracos (R6), e o acréscimo indeniza a média, não o risco de
ruína. A disputa é resolvida pela escolha da estrutura de pagamento (a loteria B preserva D16, o
pagamento do não verificado — não) e pela medição de `P_f`.

**Questão 5 (D8). Como organizar o prazo e os direitos de disputa?**
*Recomendação (crítico Claude):* «O pagador apresenta a prova de erro não depois do prazo `δ`
de tempo ativo após receber a resposta; a disputa é decidida apenas por prova, que cada nó verifica ele
mesmo». *Complemento (crítico ChatGPT):* o executor tem o direito de exigir o cálculo pelo seu pedido
fixado em caso de recusa infundada ou silêncio do comprador; ambas as partes disputam a partir de uma
conta zerada, sem depósito; a duplicata não dispara uma nova verificação cara; até a decisão, o valor
em disputa permanece pendente. Aqui há uma bifurcação aberta: se se paga após o prazo sem objeção, a
ausência do pagador paga a falsificação; se se recusa por silêncio, o pagador desonesto recebe a
resposta correta de graça.
*Onde divergiram:* claude2 e o crítico DeepSeek propõem, após M9, permitir a disputa a qualquer nó
sobre a tarefa escolhida pelo farol, com cota de disputas falsas; o crítico Claude considera isso
vazio para uma solicitação privada (um nó estranho não tem a solicitação) e útil apenas para o
treinamento.

**Questão 6 (D23). Manter o bloqueio até o cálculo M9?**
*Recomendação (todos os três críticos):* manter. Complemento (crítico Claude): «M9 é calculado para a
regra D7: as disputas são raras em equilíbrio, mas a coalizão «pagador = executor» pode apresentá-las
à vontade por solicitações autopagas; o valor queimado é destruído, e ao prejudicado é devolvido não
mais que o seu pagamento». O crítico ChatGPT propõe registrar o critério de remoção do bloqueio:
limites superiores de bytes, cálculos, mensagens e prazos por processo, limite de processos abertos
simultaneamente, fonte de cobertura da carga, verificação de formato e unicidade antes do recálculo
caro, resistência a solicitações autopagas, ao conluio de ambas as partes, à recusa falsa do
comprador, à partição da rede e à indisponibilidade dos dados.

**Questão 7 (nova D26). Aceitar a decisão sobre o bloqueio do valor pendente e o limite de devolução?**
*Recomendação (crítico Claude, com correções da seção 4):* «`H_lock` da tarefa `i` — recompensas não
vencidas da chave que vencerão após o prazo limite da disputa sobre `i`; o prazo de verificação pelo
pagador é muito menor que a janela de vencimento. Um erro provado queima todo o valor não
vencido da chave, incluindo as recompensas das tarefas entregues depois da contestada e na mesma onda.
Ao pagador prejudicado é devolvido não mais que o seu pagamento pela resposta contestada; o resto é
destruído; a primeira disputa não toma valores devidos a outros pagadores». Sem essa regra, a
estratégia das seções 5.1–5.3 não se sustenta (contraexemplos +4,4295R e até +74,4R nas seções
4.2–4.3).
*Onde divergiram:* o crítico ChatGPT não discute o bloqueio nessa forma, pois não apoia o pagamento do
não verificado; mas ele mesmo exige vincular atomicamente os compromissos abertos a toda a receita não
vencida.

**Questão 8 (D1). É preciso alterar D1?**
*Recomendação (todos os três críticos):* não enfraquecer o texto. As variantes «D1 com parcela de
conluio menor que `q*`» e «vazamento não maior que `ε` do volume» (claude1, ds1, ds2, gpt1) foram
rejeitadas: com `q = 1` elas entregam à coalizão toda a emissão não verificada, contradizem D19 e o
imutável R4, e o «volume» é inflado por autotransações. O crítico Claude propõe uma nota: para a
resposta do modelo, D1 é garantido em relação ao pagador que executa a verificação do núcleo; a
verificação por amostragem com sua moeda secreta cumpre D1 como expectativa e é registrada como
suposição sobre um adversário racional (por R4, a amostragem estatística é uma suposição); para o
consumidor que não verifica, a rede não promete D1. O crítico DeepSeek — uma nota de que a garantia D1
se refere a cada resultado com a marca «verificado» e a cada emissão de créditos.

## 7. O que calcular com mini-agentes e o que verificar por experimento

### 7.1. Cálculos exatos (frações, hash de controle, repetição em um segundo dispositivo)

1. Enumeração completa da regra D7 com vencimento do valor, ondas, várias chaves, preços diferentes
   na onda e verificações retroativas. Valores de referência: `κ = 1` → 0; `κ = 0,9` com `H₀ = 0` →
   +1,734R (reproduzido pelo crítico Claude, não reproduzido pelo crítico DeepSeek — a enumeração deve
   decidir); `0,99·R/(R + H)` → +0,225R; contraexemplo de vencimento +0,99R / +9,08R / +49,7R /
   +74,4R.
2. Fórmula da onda de gpt1: +4,4295R com débito separado e −2,49676R com a queima de toda a onda.
3. Ataque de «autodisputa»: com que parcela de devolução ao prejudicado o ganho se torna positivo.
4. Vazamento de falhas gratuitas (`b` por janela) e acréscimo `P_f·R` com dispersão das perdas do
   honesto.
5. Dano nos cronogramas `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` com autopagamento e novas chaves;
   referências 0,50 / 0,125 / 0,0078 com `n_w = 4320`.
6. Pagadores preguiçosos: parcela `λ` e distinguibilidade com que a dissuasão desaparece.
7. Carga da coalizão de novas chaves sobre os pagadores com `p = 1` para novatos.
8. M9 (disputas falsas) para a regra D7 — condição de D23.
9. Preço agregado `γ·(1 + p·ρ)` em uma grade de `γ`, `ρ` medidos e distribuições de `n_w`.
10. Probabilidade de conluio total na escolha sem reposição (`C(C,k)/C(N,k)`) e em rodadas de sorteio.
11. Tamanhos dos instantâneos de estado pela configuração fixada do modelo (M1) — disputa sobre o
    preço dos tokens amostrados e dos instantâneos.
12. Limiar corrigido de ds2 e script de controle de gpt2 (SHA-256 começa com `58aec3b0` e termina em
    `cd07ba`; coincidiu nos críticos Claude e DeepSeek).
13. Cadeias exatas de SPRT e CUSUM em grades finitas, incluindo a mudança de comportamento após um bom
    histórico.
14. Tabelas de armadilhas `(1 − g·θ·d)^m` para os níveis `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Apenas por experimento

O experimento D5 permite o trabalho com o Qwen3.5-4B inteiro no volume O1–O5 de seu protocolo. **Todo
o resto — apenas com autorização separada do dono.**

1. No âmbito de D5: núcleos rápidos bit a bit iguais (O3, O4) — o único caminho para se aproximar de
   5%; a parcela de verificação nos dispositivos dos pagadores e com lotes 1, 8, 32; O5 — qualidade em
   320 tarefas.
2. Fora de D5: decodificação especulativa exata — distribuição do comprimento do prefixo coincidente
   do Q8_0 e do perfil exato em respostas longas.
3. Fora de D5: frequência de divergências silenciosas `P_f` em trabalho longo em dispositivos
   voluntários — antes de qualquer alteração de D16.
4. Fora de D5: tempo e memória da verificação em uma passagem no processador de um notebook e de um
   telefone.
5. Coincidência de bits em entradas de borda (overflow, empates, término antecipado da resposta) e em
   novos drivers; na RX 580, a passagem longa sobre uma resposta pronta era interrompida pelo driver
   [medido].
6. Fora de D5: O9 (energia), O6 (ruído da melhoria do LoRA), O7 (preço da prova do bloco), treinamento
   inteiro — pré-requisito de qualquer esquema de verificação do passo.
7. Fora de D5, opcionalmente: até que ponto as falsificações baratas são distinguíveis por
   características. Isso não dá garantia em nenhum resultado, apenas especifica o teto da seção 2.1.

## 8. Divergências não resolvidas e referências duvidosas

### 8.1. Divergências

1. **A verificação por amostragem pelo pagador cumpre o D1 literal.** claude1, claude2, os críticos
   Claude e DeepSeek — sim para o dinheiro, não para o dano. ds1 e ds2 — é necessária a verificação
   completa (os críticos consideram que eles não notaram a verificação pelo pagador com frequência
   baseada no valor bloqueado). gpt1, gpt2 e o crítico ChatGPT — verificação completa de cada resposta, e o
   pagamento dos escolhidos — apenas por contrato separado para lotes. A decisão sobre se o ganho
   esperado basta na primeira frase de R4 é do dono.
2. **`R/(R + H_lock)` ou `R/H`.** O primeiro é exato para o dinheiro; o segundo dá margem e um número
   esperado finito de falsificações até a detecção; a diferença de preço é de cerca de duas vezes com
   valor pequeno.
3. **Pagar o não verificado** (`α = R` ou o G(α) suave de claude2) **ou apenas o escolhido**
   (`α = 0`, loteria B). Depende da edição de D2, D11, D21 e da irregularidade não medida da renda.
4. **Farol ou moeda secreta.** claude2 — farol comum (D20); claude1 e os críticos Claude e DeepSeek —
   moeda secreta do pagador; o farol é necessário apenas com `α < R` e para disputas de terceiros. O
   crítico ChatGPT: a moeda secreta serve para a verificação pessoal, mas não pode dispor de um prêmio
   comum; ao escolher o resultado conveniente entre dois resultados independentes do farol, a detecção cai de
   `p` para `p²`.
5. **D16** — seção 6, questão 4.
6. **Limite do dano** — nenhum esquema resistiu ao autopagamento e a novas chaves.
7. **Treinamento** — auditoria «um entre N» (claude1), verificação por cada nó completo com reversão
   do ramo (claude2), D18 ou repetição completa (ds1, ds2, gpt1, gpt2); nenhum esquema cumpre D7 com
   `q = 1`.
8. **Grandezas da enumeração de claude1** (+1,73R com `κ = 0,9`): reproduzidas pelo crítico Claude,
   não reproduzidas pelo crítico DeepSeek (+0,085R no modelo mais próximo); o sinal é igual nos dois.
9. **Decodificação especulativa:** 1,15–1,38 (claude1) contra cerca de 0,78 do tempo do token exato
   (claude2); ambos não medidos.
10. **Armadilhas:** ds2 calcula o número necessário de armadilhas; claude1 e claude2 provam que, em
    uma rede pública, a armadilha coincide com a verificação pelo pagador. As conclusões são
    compatíveis.

### 8.2. Referências bibliográficas marcadas pelos críticos como duvidosas

Todas as referências são dadas de memória, sem conferência dos textos.

- SybilGuard e SybilRank sob o rótulo comum «Yu e coautores» (ds1): segundo a memória dos críticos,
  SybilGuard e SybilLimit — Yu e coautores (2006, 2008), SybilRank — Cao e coautores (2012); o ano do
  SybilRank em si foi marcado pelo crítico Claude como incerto.
- «Proof of Sampling (2024)» e «Verde (Gensyn, 2025)» (claude1, claude2) — os próprios trabalhos
  escrevem «não tenho certeza»; o funcionamento do mecanismo não está confirmado.
- Peer Truth Serum como trabalho de Witkowski e Parks (2012) (ds2): o crítico Claude considera isso
  duvidoso (segundo sua memória, eles têm a «BTS robusta», e o nome pertence a Radanovic e Faltings);
  o crítico DeepSeek — correto. Divergência.
- DMI como trabalho de Kong e Schönbeck (2019) (ds1, ds2): duvidoso segundo a memória dos críticos
  Claude e ChatGPT (DMI é um trabalho de Kong por volta de 2020); o crítico DeepSeek considera a
  atribuição correta.
- «Ataques de autopredição ao BTS em Radanovic e Faltings» (ds1) — duvidoso.
- «Gao, Wright e Layton-Brown (2016)» sobre a superioridade da verificação por amostragem sobre peer
  prediction (claude2) — o ano não está confirmado (crítico DeepSeek), e a validade incondicional da
  conclusão é duvidosa (crítico ChatGPT).
- Kreps e Wilson (1982) como fundamento de «a reputação funciona apenas em horizonte longo»
  (claude1) — duvidoso (crítico ChatGPT).
- DetectGPT como justificativa do limiar de perplexidade de modelo pequeno (ds1) — incorreto: ele
  estuda outra propriedade (crítico ChatGPT).
- A fórmula geral de passagem `(1 − f)^s` como propriedade de BOINC, TrueBit, opML (ds1, ds2) — não
  decorre de seus protocolos.
- As referências de ds1 e ds2 a «0,3–0,7% / 0,33–0,66% dos tokens do exame» e «cerca de 2,4 horas por
  candidato» não foram encontradas nos documentos de entrada.

## 9. Quem fez o quê

O conselho de modelos trabalhou com os materiais do projeto, sem acesso à rede e sem experimentos.

- **Seis trabalhos independentes:** dois trabalhos ChatGPT (gpt1, gpt2), dois trabalhos DeepSeek
  (ds1, ds2), dois trabalhos Claude (claude1, claude2). Cada um analisou as sete direções da
  tarefa atribuída, acrescentou as suas, comparou-as com as decisões D1, D6, D7 e propôs estratégias com
  preço e risco residual. Programas aritméticos curtos e pequenas enumerações foram executados por
  claude1 (enumeração de estratégias contra a regra de frequência), claude2 (grade de frações exatas),
  gpt1 e gpt2 (gpt2 anexou um script de controle com hash).
- **Três críticas:** uma de ChatGPT, uma de DeepSeek e uma de Claude. Cada crítico leu todos os seis
  trabalhos, procurou erros e contraexemplos e recalculou os números principais. Os críticos Claude e
  DeepSeek repetiram o script de controle de gpt2, e o hash coincidiu; o crítico Claude repetiu a
  enumeração de claude1, o crítico DeepSeek não reproduziu suas grandezas.
- **Consolidação:** este documento foi elaborado por Claude a partir dos trabalhos e das críticas. Não
  foram acrescentadas novas avaliações nem números além dos trabalhos, das críticas e das medições D5;
  onde os críticos divergiram, isso está indicado.
