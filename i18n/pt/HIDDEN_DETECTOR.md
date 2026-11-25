<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# Detector oculto e mutável: o que o segredo das regras oferece

[English](../../docs/HIDDEN_DETECTOR.en.md) · [中文](../zh/HIDDEN_DETECTOR.md) · [Español](../es/HIDDEN_DETECTOR.md) · [Français](../fr/HIDDEN_DETECTOR.md) · [Deutsch](../de/HIDDEN_DETECTOR.md) · [Italiano](../it/HIDDEN_DETECTOR.md) · [Русский](../../docs/HIDDEN_DETECTOR.md) · **Português** · [العربية](../ar/HIDDEN_DETECTOR.md)

Situação em 25 de novembro de 2026. Resultado do sexto conselho de modelos.

## 1. Pergunta e resumo curto

O dono do projeto perguntou textualmente:

> «Com regras abertas (D4), o trapaceiro conhece o detector e falsifica exatamente onde ele está
> tranquilo. E se escondermos o detector? Por exemplo, a rede, em momento aleatório, gerará
> aleatoriamente novas regras de verificação de honestidade, e os agentes verificarão por elas.
> Dada a arquitetura distribuída e aberta da rede skynet, ninguém deve conhecer as regras de
> verificação, e elas devem ser criptografadas, com a chave de cifra mudando. Pensem nessa direção
> em um conselho de modelos. Antes eu levantei a questão do uso de blockchain — há uma variante de
> fazer um detector dinâmico com base em blockchain? Talvez, além do blockchain, existam outras
> tecnologias ou algoritmos?»

**Status do documento.** É raciocínio e cálculo, não medição. Não havia rede durante o trabalho do
conselho, não foram realizados experimentos; os trabalhos científicos são citados de memória e não
foram conferidos. As medições são tomadas apenas dos resultados do experimento D5 em 25 de novembro
([EXPERIMENT_D5](EXPERIMENT_D5.md), seção 7) e da síntese anterior
[STRATEGY_SEARCH](STRATEGY_SEARCH.md). As únicas decisões aceitas do projeto continuam sendo D1–D25
([ROADMAP](ROADMAP.md)); tudo o que abaixo é chamado de «recomendação» deve ser aceito ou rejeitado
explicitamente pelo dono. Marcações: [medido] — medido em D5; [cálculo] — decorre de fórmula com
parâmetros nomeados; [suposição] — valor tomado para estimativa e não medido.

Notações que aparecem abaixo: `R` — pagamento de uma tarefa; `H_lock` — valor não vencido do
executor que é queimado em caso de falsificação comprovada; `c_f` — custos da falsificação; `p` —
probabilidade de verificação completa da tarefa; `ρ` — tempo de verificação de uma resposta pronta em
uma passagem dividido pelo tempo de geração; `γ` — quantas vezes o perfil exato de inteiros é mais lento
que a geração usual do llama.cpp Q8_0; `q` — parcela de conluio; `n_w` — número de tarefas da chave
por janela de vencimento.

**Resumo curto.**

1. **Um detector oculto não oferece mais do que uma verificação aberta com aleatoriedade secreta do
   mesmo custo.** Se o trapaceiro conhece a lei segundo a qual as regras são escolhidas (e, por D4,
   o código do agente é aberto, logo ele a conhece), então a probabilidade de detectar qualquer
   falsificação dele com uma regra oculta é igual à probabilidade de detecção com o programa aberto
   «após a fixação da resposta, lançar uma moeda e aplicar a regra sorteada». Todos os onze trabalhos
   chegaram a isso independentemente, e os quatro críticos confirmaram. Portanto, a ocultação não
   permite baixar a frequência de verificação abaixo do limiar anterior `R/(R + H_lock)`.
2. **Uma regra que vive mais que uma tarefa é pior que uma moeda fresca.** O trapaceiro aprende com
   seus próprios resultados («detectado / não detectado»), testa o detector com chaves novas
   gratuitas, descobre a regra por qualquer cúmplice a quem ela foi dada para aplicar. Mesmo sem
   nenhum vazamento, uma regra comum à época é mais perigosa: no exemplo do ChatGPT, uma onda de dez
   falsificações dá `+8,1R` contra `−2,38R` com moedas independentes [cálculo]. «Mudar as regras em
   momento aleatório» é, por isso, pior que mudar a escolha a cada tarefa.
3. **Exatamente uma forma de ocultação é útil:** o segredo da escolha aleatória *antes* de o executor
   fixar irrevogavelmente a resposta, e o segredo do *papel* — se um dado pagador verifica e quem foi
   designado verificador. As regras, a família de verificações e a lei de escolha permanecem abertas.
   Essa forma já existe na estratégia do conselho anterior («moeda secreta do pagador»).
4. **O que tirar do blockchain e da criptografia.** O blockchain é um registro de fixações, ordem,
   revelações e queima de valores; segredos não há nele e não pode haver. Um farol externo de
   aleatoriedade com limiar e o atraso VDF a partir do bloco final são fontes de aleatoriedade para
   amostras comuns segundo D20 (auditoria do treinamento, exame, designação de verificadores),
   misturadas por hash. VRF e compromisso com sal antes da fixação — onde o resultado da moeda afeta
   dinheiro de terceiros. Um «detector dinâmico no blockchain», na forma correta, é **um gerador
   aberto de regras no núcleo mais aleatoriedade fresca após a fixação**, e não regras cifradas.
5. **O que rejeitar como fundamento de garantia.** Armazenamento de limiar de regras secretas pelos
   participantes (revela-se ou é bloqueado por conluio; com `q = 1` não há proteção — violação de
   D7), ambientes de execução confiáveis TEE (confiança no fabricante, nas placas do experimento D5
   eles não existem), criptografia homomórfica FHE (segundo a estimativa dos críticos, de 19 horas a
   15 dias de computação por resposta), computação multipartidária MPC (centenas de megabytes e mais
   tráfego por token e, de novo, dependência de `q`), ofuscação indistinguível iO (impraticável e
   ainda deixa ao trapaceiro um «ensaio»), criptografia funcional e PIR (resolvem outras tarefas).
   Armadilhas, limiares secretos e estatística são admissíveis apenas como sinal para uma
   verificação *adicional*.
6. **Encontrado um erro nas tabelas anteriores.** Em STRATEGY_SEARCH 5.3 e na maioria dos trabalhos
   deste conselho, a célula «pagador preguiçoso, o executor o distingue» × «novato» contém 0. O
   correto é **até `+R`**: a regra «o novato é sempre verificado» é executada pelo programa do
   pagador, e o pagador preguiçoso não a executa. Pior ainda, as novas chaves permitem descobrir
   gratuitamente qual pagador é preguiçoso. Só a não vinculabilidade dos pagadores entre solicitações
   protege disso, e ela ainda precisa ser construída.
7. **O conselho não propõe novas decisões sobre a garantia.** Propõem-se um esclarecimento de D4 («o
   núcleo aceita aleatoriedade futura, mas não um segredo de longa duração») e um esclarecimento de
   D20 («as fontes são misturadas por hash, e não por escolha; o farol é para decisões comuns, não
   para o dinheiro do pagador»). O custo da verificação não muda por causa da ocultação: o principal
   item continua sendo a desaceleração do perfil exato `γ` (+50…+82% sobre Q8_0 com lote 1 [medido
   γ, cálculo]), e não a verificação em si.

---

## 2. Por que o segredo das regras não ajuda: afirmações e contraexemplos

### 2.1. Regra oculta é igual a regra aberta com moeda secreta

**Modelo.** O defensor escolhe a regra de verificação `r` de uma distribuição `D`. A regra `r`
detecta a falsificação `x` com probabilidade `π_r(x)`. O trapaceiro conhece a distribuição `D` (por
D4, o gerador de regras faz parte do núcleo aberto), mas não conhece o `r` sorteado, e escolhe a
falsificação antes de `r` ser sorteado.

**Afirmação 1 (equivalência).** A probabilidade de detecção da falsificação `x` é
`π̄(x) = E_{r~D}[π_r(x)]`, o custo médio da verificação é igual ao custo médio das regras. O programa
aberto «após a fixação irrevogável da resposta, tomar aleatoriedade fresca, escolher `r` segundo a
lei `D` e aplicá-lo» dá, para **cada** falsificação, a mesma probabilidade de detecção e o mesmo
custo. Portanto, a ocultação da implementação acrescenta zero à proteção.

A prova é a média sobre `r`: os resultados dos dois experimentos coincidem para cada valor de
aleatoriedade. Ela foi realizada independentemente por gpt1, gpt2, ds1, ds2, claude1, claude2,
mm1–mm5; os críticos ChatGPT, DeepSeek, Claude e MiniMax a confirmaram. É o mesmo resultado que o
limite do conselho anterior `E_F[π] − E_P[π] ≤ TV(F, P)`
([STRATEGY_SEARCH](STRATEGY_SEARCH.md), seção 2.1): a grandeza `π̄` é uma função comum das
observações com valores de 0 a 1, e o segredo não a altera.

**Afirmação 2 (informações sobre o segredo só prejudicam o defensor).** Se o trapaceiro, antes da
falsificação, recebe qualquer sinal `Z` sobre a regra sorteada — por uma disputa anterior, por
sondagem, por uma fração da chave, por vazamento do enclave —, seu melhor resultado não piora:
`E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`. Ele sempre pode ignorar o sinal (claude1, claude2;
confirmado pelos críticos).

O crítico ChatGPT precisou o limite desta afirmação: a desigualdade é não estrita. Se todas as regras
têm a mesma falsificação «pior para o defensor», a revelação da regra pode não mudar nada. Portanto, a
frase de claude1 «qualquer vazamento piora estritamente» é falsa; o correto é «nunca melhora».

**Como isso difere da randomização.** Vários trabalhos (ds1, ds2, mm2) registraram a consequência como
«o detector oculto é igual à verificação de toda a resposta com probabilidade `p`». Isso é impreciso.
O equivalente do detector oculto é uma *mistura das mesmas regras*. A mistura de verificações
parciais às vezes é mais forte que a verificação completa com o mesmo custo, mas o ganho vem da
randomização, não do segredo, e ele se mantém com o algoritmo aberto:

- **Contraexemplo de gpt1.** O resultado tem três partes verificáveis independentemente de um mesmo
  custo, e, pela natureza da tarefa, qualquer falsificação admissível estraga ao menos duas. A
  verificação de uma parte aleatória por um terço do custo completo detecta não menos que 2/3 das
  falsificações; o recálculo completo com probabilidade 1/3 — apenas 1/3.
- **Variante de gpt2.** Três testes por metade do custo do recálculo completo, cada um detecta duas
  classes de erro de três: a mistura detecta 2/3, o recálculo completo de metade das tarefas — 1/2.
  Se acrescentarmos uma quarta classe, que nenhum teste detecta, a garantia da mistura cai para 0.

Para o Qwen, essa cobertura de classes de erro não está provada: uma única posição errada da resposta
já é uma falsificação, e para ela qualquer verificação parcial detecta no máximo a sua fração. Por
isso, o ganho prático da mistura atualmente é nulo (críticos Claude e ChatGPT). A afirmação de mm2 «a
mistura é sempre mais cara que o tipo decisivo» é falsa em geral; além disso, na sua fórmula há um
fator extra (os números 0,2111 / 0,22 / 0,2333 foram calculados pela fórmula correta, mas está
escrita a incorreta — críticos Claude e DeepSeek).

**Onde o segredo não se reduz a uma moeda.** É um rótulo privado do defensor, ligado à resposta
correta: a referência da armadilha, que só o pagador conhece (gpt1, gpt2). Ela não pode ser
substituída por um bit aleatório. Mas, como mostrado na seção 3, ela custa não menos que uma geração
e, portanto, não torna a verificação mais barata.

**Contra uma regra «fixa», a oculta é realmente melhor.** claude1 dá um exemplo: se a regra aberta
sempre olha as posições 1–8, uma falsificação na posição 9 nunca é detectada. Mas o mesmo ganho é
dado pela regra aberta «escolher 8 posições uniformemente após a fixação» (mm3, teorema 2: uma
posição fresca detecta `e/N` falsificações, onde `e` é o número de posições corrompidas de `N`,
independentemente de o trapaceiro conhecer a regra). O crítico MiniMax chamou isso de principal erro
da rodada: muitos trabalhos compararam o detector oculto com uma regra aberta fixa e atribuíram ao
segredo um ganho que pertence à aleatoriedade.

### 2.2. Aprendizado do trapaceiro pelos resultados e sondagens com novas chaves

Um segredo usado mais de uma vez é aprendido. Para isso, o adversário não precisa conhecer a regra
inteira — basta encontrar um lugar seguro.

- **Duas posições de dez (claude1).** A regra oculta verifica 2 posições de 10; a detecção de uma
  falsificação de uma posição — 1/5. Depois que uma disputa revela uma posição verificável, a
  detecção cai para 1/9; após a revelação da segunda — para 0. Se a regra é revelada já na primeira
  disputa, o número esperado de detecções entre 100 falsificações é `1 − 0,8¹⁰⁰ = 0,9999999998`, ou
  seja, praticamente uma, enquanto uma moeda fresca detectaria em média 20 [cálculo, confirmado pelos
  críticos]. O crítico ChatGPT observou que isso vale para uma ordem concreta de sondagens e para a
  revelação completa na primeira detecção; no caso geral, uma disputa revela ao menos a posição
  verificada, mas não necessariamente todo o conjunto.
- **Oito posições de mil (ds2).** Com um subconjunto oculto constante de 8 posições de 1000, a
  primeira falsificação de uma posição passa com probabilidade 0,992, assim como com uma amostra
  fresca pública da mesma fração. A diferença é que, com um subconjunto oculto constante, a posição
  que passou permanece segura para sempre. O número de ds2 «≈ 2718 tentativas para reconstruir todo o
  conjunto» foi calculado por um modelo incorreto (com reposição); sem reposição são necessárias
  cerca de 890 tentativas e, o mais importante, ao adversário basta uma posição segura (críticos
  Claude, DeepSeek e ChatGPT).
- **Regra de época e chave madura (claude2).** Uma regra determinística por época de 100 tarefas,
  `p = 1%`, `H_lock = 99R`: o trapaceiro que encontrou por sondagem uma área segura recebe cerca de
  `0,99·100R − 0,01·99R = 98,01R` por época, contra `≤ 0` com moeda fresca [cálculo, confirmado].
- **Bit comum da época (gpt2).** `R = 1`, bloqueado `9R`, dez falsificações de uma onda, a primeira
  falsificação comprovada anula a onda e `9R`, frequência de verificação de uma solicitação individual
  1/10. Se um único bit oculto da época decide «verificar tudo» ou «pular tudo», o ganho da onda é
  `0,9·10R − 0,1·9R = +8,1R` — violação de D1 **antes de qualquer vazamento**. Com dez moedas
  independentes e os mesmos custos, `(0,9¹⁰·10 − (1 − 0,9¹⁰)·9)R = −2,3751096381R` [cálculo,
  repetido por todos os críticos]. Analogamente no crítico ChatGPT: com `R = 1`, `H = 4`, `p = 0,2` e
  dez falsificações, uma moeda comum para toda a onda dá `+7,2R` mesmo com o cancelamento de toda a
  onda.

**Chaves Sybil.** As novas chaves são gratuitas. Uma chave com conta vazia não perde nada ao ser
detectada, então as sondagens do detector a partir dela quase não custam nada. A proteção só se
sustenta onde o novato é de fato sempre verificado (`p = 1`). O crítico ChatGPT ressalvou que a
gratuidade das chaves não implica adaptação instantânea: cada resultado informativo exige uma tarefa
paga e tempo, e, com feedback ruidoso, várias tentativas. A conclusão não muda: um segredo que dura
muito cedo ou tarde é aprendido, e uma moeda fresca não ensina nada, porque o próximo lançamento é
independente dos anteriores.

**Conclusão.** A escolha deve ser feita de novo a cada tarefa, e não por cronograma. É exatamente por
isso que «a rede gera novas regras em momento aleatório» é pior que «uma moeda fresca a cada tarefa»,
que se regenera sozinha e gratuitamente (ds1).

### 2.3. A regra vaza por aqueles que a aplicam

«Uma regra que ninguém conhece, mas que todos executam» é impossível em uma rede aberta. O nó que
aplica a regra a conhece no momento da aplicação: o código e as chaves ficam na memória da máquina, e
o dono da máquina, segundo o modelo de adversário, pode lê-los ([THREAT_MODEL](THREAT_MODEL.md),
seção 1.3). claude1 formulou a lista completa de portadores do segredo:

1. a regra ainda não existe — ela será derivada de aleatoriedade futura (farol, VDF);
2. a regra é executada em hardware que o dono não pode abrir (TEE) — então a confiança é transferida
   ao fabricante, e R4 chama isso de suposição;
3. a regra é cifrada de modo que possa ser executada sem ser conhecida (iO, FHE, MPC) — ver seção 3;
4. a regra é conhecida por um comitê de participantes — então o conluio a revela ou a bloqueia.

O crítico ChatGPT complementou a lista: MPC sobre frações e o cálculo de um esquema aberto sobre um
parâmetro cifrado permitem ao operador não ver o resultado de modo algum. Isso não muda a conclusão,
porque tais esquemas novamente dependem da fração de participantes honestos ou do detentor da chave.

**A chave de limiar protege o armazenamento, mas não a aplicação** (claude2, o argumento mais forte do
conselho contra uma regra secreta no comitê). Mesmo que a chave seja dividida de forma confiável, a
regra de época decifrada é executada por um nó concreto. Com `m` aplicações independentes, a
probabilidade de que ao menos um nó aplicador seja da coalizão é `1 − (1 − q)^m`: em 10 aplicações,
isso é 0,65 / 0,97 / 0,999 com `q` = 0,1 / 0,3 / 0,5. A probabilidade de que a regra de época *não*
seja conhecida pela coalizão em 100 aplicações com `q = 0,1` é `0,9¹⁰⁰ ≈ 2,7·10⁻⁵` [cálculo,
confirmado pelos críticos].

**Esconder do verificador não faz sentido** (claude2, corolário 4.2). Um verificador em conluio pode
simplesmente não verificar e dizer «limpo»; o honesto não tem nada a esconder. O único de quem a
decisão precisa ser escondida é o executor, antes da fixação da resposta. claude2 acrescentou o
teorema 4: se o verificador não deve saber quais posições verifica, ele precisa «tocar» todas as
posições, e a economia da amostragem desaparece. O crítico ChatGPT observou que essa conclusão é
válida em um modelo especial (um servidor, sem pré-processamento) e pode mudar com outros modelos de
acesso à memória; o crítico Claude — que o teorema refuta uma variante que ninguém defendia.

**Um segredo oculto não fornece um veredito verificável.** mm2 observou que a afirmação «existe uma
regra secreta que aceitou o resultado» é sempre verdadeira para a regra «aceitar tudo». Os críticos
Claude e ChatGPT esclareceram: uma prova de conhecimento zero pode atestar a afirmação substantiva «a
regra foi derivada de um compromisso registrado antes da fixação, e ela aceitou o resultado». Mas tal
prova exige uma relação aberta no núcleo, ou seja, nos leva de volta ao gerador aberto, e seu custo
para o Qwen não foi calculado.

### 2.4. Chave de limiar com parcela de conluio q

Suponha que a chave seja dividida entre `n` detentores; para decifrar são necessárias `t` frações.
Então a coalizão descobre o segredo antecipadamente se tiver `t` ou mais lugares, e pode parar o
trabalho se tiver `n − t + 1` ou mais lugares. Se os lugares são escolhidos independentemente e cada
um pertence à coalizão com probabilidade `q`, são caudas binomiais. Tabela do crítico Claude,
conferida pelos críticos ChatGPT e DeepSeek; em cada célula, «revelação / parada» [cálculo]:

| `n`, `t` | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0,856% / 0,856% | 16,3% / 16,3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0,0177% / 2,57% | 2,88% / 35,3% | 22,7% / 77,3% | 1 / 1 |
| 16, 11 | 2,7·10⁻⁸ / 0,33% | 0,157% / 34,0% | 10,5% / 89,5% | 1 / 1 |
| 30, 16 | 3,66·10⁻⁹ / 3,56·10⁻⁸ | 0,637% / 1,69% | 42,8% / 57,2% | 1 / 1 |
| 64, 43 | 4,75·10⁻²⁸ / 1,20·10⁻⁷ | 9,43·10⁻¹⁰ / 26,2% | 0,41% / 99,6% | 1 / 1 |
| 100, 51 | 6,3·10⁻²⁵ / 5,8·10⁻²⁴ | 9,0·10⁻⁶ / 2,2·10⁻⁵ | 46,0% / 54,0% | 1 / 1 |
| 100, 67 | 9,6·10⁻⁴³ / 7,0·10⁻¹¹ | 2,7·10⁻¹⁴ / 22,1% | 0,044% / ≈1 | 1 / 1 |

O que dela decorre:

1. **Nenhuma linha oferece proteção com `q = 1`.** D7 exige uma verificação independente da parcela de
   conluio, portanto o segredo no comitê não cumpre D7 com nenhum limiar.
2. **Um limiar alto guarda bem o segredo, mas é facilmente bloqueado.** Linha 16/11: com `q = 0,3`,
   revelação 0,157%, mas com probabilidade 34% a coalizão paralisa a emissão simplesmente não enviando
   as frações.
3. **As épocas se acumulam.** Com probabilidade de revelação de 0,856% por época (3 de 5, `q = 0,1`),
   em 30 épocas independentes ao menos uma revelação ocorrerá com probabilidade 22,7% (gpt1) [cálculo].
4. **A tabela é otimista.** A escolha independente dos lugares é uma suposição. Ela se rompe se os
   detentores são selecionados por peso, e o peso pode ser acumulado com solicitações verificadas
   autopagas; se, num modelo raro, a parcela de conluio é acima da média; com suborno após a
   designação; com proprietários comuns dos lugares. Em [THREAT_MODEL](THREAT_MODEL.md) (seção 1.7) já
   há um exemplo: 42,1% do peso total dão `q_eff = 88,9%` entre os admitidos à tarefa (o crítico
   MiniMax chamou atenção para isso).
5. **Erros nos trabalhos.** claude1 registrou a condição «`q < min(t/n, 1 − t/n) ≤ 1/2`» como teorema;
   não é teorema: com `t = n`, o segredo se mantém enquanto houver ao menos um honesto no comitê, e o
   bloqueio pode ter uma saída alternativa segura (crítico Claude). mm4 confundiu os limiares de
   revelação e de bloqueio; mm2 erroneamente considerava que a decifração de limiar exige todos os
   detentores; ds1 registrou de forma contraditória «reconstroem com `t + 1` frações». A afirmação de
   mm3 «com `q ≥ t` a coalizão falsifica a regra» só é verdadeira onde o veredito é uma assinatura de
   limiar sem conteúdo verificável; se o que se decifra é um texto cifrado fixado antecipadamente, a
   coalizão descobre a regra, mas não pode substituí-la.

**Como ler os requisitos R2/R3.** ds1, mm1, mm3 e mm4 escreveram que o requisito de recuperação após
uma parada total «proíbe por princípio» segredos comuns. Os críticos Claude e ChatGPT consideram isso
exagero: as frações dos detentores podem sobreviver à parada em seus discos; R2/R3 proíbem depender
do endereço de um coordenador vivo, e não do retorno de parte dos participantes. A fronteira exata
(claude2): um segredo sem o qual não se pode verificar o fundamento de uma decisão **passada** é
incompatível com a verificabilidade após reinício. Logo, qualquer regra secreta deve ser revelada não
depois do pagamento, e seu segredo vive não mais que o segredo da moeda. A conclusão sobre a
inadequação das regras secretas é a mesma; o fundamento de ds1, mm1, mm3 foi exagerado.

### 2.5. Princípio de Kerckhoffs, jogos de segurança, bancos e CAPTCHA

**Kerckhoffs.** O princípio de Kerckhoffs (de memória) admite um algoritmo aberto com chave fechada.
Neste jogo, a «chave» fechada deve ser a realização, imprevisível antes da fixação, da chamada de
verificação, e não o algoritmo. A troca de uma chave de longa duração é útil após o comprometimento,
mas não apaga o que o trapaceiro já aprendeu sobre a função que essa chave decifrava (crítico
ChatGPT).

**Jogos de segurança.** O defensor com orçamento limitado randomiza — isso é clássico dos jogos de
Stackelberg e dos jogos de inspeção (de memória). Mas ali a distribuição do defensor geralmente é
considerada conhecida do atacante, e todo o benefício vem da aleatoriedade, e não do segredo da
distribuição. O crítico DeepSeek corrigiu mm3: o desconhecimento da distribuição pelo trapaceiro não
pode elevar seu ganho acima da melhor resposta à distribuição verdadeira, e, por D4, ele de qualquer
modo é obrigado a conhecer essa distribuição. Para a mistura de testes diferentes, gpt1 escreveu um
problema de programação linear: maximizar a menor probabilidade de detecção entre as falsificações
`min_f Σ w_j D(j,f)` com orçamento `Σ w_j c_j ≤ B`.

**«Alvo móvel».** A ideia de moving target defense (de memória) é valiosa quando o observador precisa
de tempo para se adaptar à nova configuração. No SkyNet, o melhor «alvo móvel» é uma nova configuração
a cada tarefa, ou seja, uma moeda fresca (mm4, mm5).

**Por que a ocultação funciona no banco e no CAPTCHA, mas não no SkyNet.** Os trabalhos e os críticos
concordaram nas seguintes diferenças (claude2, ds2, mm3, mm5, crítico ChatGPT):

| | Antifraude bancário, CAPTCHA | SkyNet |
|---|---|---|
| Quem detém o modelo de verificação | Uma organização em seu próprio servidor | Não há centro; o código do agente é aberto (D4) |
| Feedback ao atacante | Frequentemente não atribuível, com atraso | O resultado é visto imediatamente e vinculado à tarefa |
| Custo da tentativa | Abertura de conta, documentos, limitação de repetições | A chave é gratuita (Sybil) |
| Sanções | Não monetárias: bloqueio, tribunal, informações externas | Apenas a queima do valor não vencido (R5) |
| Objetivo da proteção | Reduzir as perdas em média | O ganho esperado de qualquer coalizão não é maior que zero (D1) |
| Verificabilidade da decisão | Não é exigida por terceiros | Cada nó verifica o fundamento por si mesmo |

O banco tem rótulos privados de resultados, custo de abertura de conta e limitação de repetições; o
CAPTCHA tem um verificador externo. São informações adicionais e custos do atacante. Eles não
aparecem no SkyNet pela troca de um arquivo cifrado de regras. ds2 e mm5 nomearam com precisão a
essência: onde a ocultação funciona, o segredo é de fato descartável, ou seja, é a mesma moeda.

**A premissa principal da pergunta no SkyNet é em parte falsa** (mm3). A verificação principal do
projeto é a comparação bit a bit com o recálculo exato. Ela não tem um «lugar onde o detector está
tranquilo»: a resposta honesta coincide em toda parte, a falsificação diverge onde foi falsificada.
«Zonas silenciosas» existem apenas nos detectores estatísticos e nas verificações parciais. Os
detectores estatísticos contra a principal falsificação (geração comum Q8_0 em vez do perfil exato)
são quase inúteis, e para as verificações parciais ajuda uma escolha fresca após a fixação.

---

## 3. Análise das tecnologias

Os preços abaixo são [cálculo] por parâmetros explicitamente nomeados e [suposição] sobre a velocidade
da criptografia estimada segundo a memória; nenhuma dessas tecnologias foi medida no projeto. Medições básicas:
`ρ = 0,10–0,40` com lote 1 e `0,26–0,64` com lote 8; `γ = 1,5–1,8` com lote 1 e `2,5–2,8` com lote 8
[medido, O3 e O4]. Modelo D5: 32 blocos, tamanho oculto 2560, MLP 9216, 24 blocos Gated DeltaNet com
estado `32×128×128`, vocabulário 248 320, cerca de 4,2·10⁹ multiplicações-adições por token.

| Tecnologia | O que oferece | O que não oferece | Preço [cálculo / suposição] | Veredito |
|---|---|---|---|---|
| **Registro blockchain** | Ordem, fixação final da resposta (D24, 2–4 KB de texto cifrado), compromissos, revelações, cálculo único, queima | Confidencialidade: todos veem tudo no bloco. Aleatoriedade não enviesável: o produtor do bloco pode segurar um bloco inconveniente (N13) | Disputa piloto: 93 transações, 5,8–6,3 milhões de gas, com 1 gwei e 3000 $/ETH — 17,4–18,9 $, com 20 gwei — 348–378 $ (crítico ChatGPT segundo THREAT_MODEL, N3) | **Adotar como registro** |
| **Contrato inteligente como detector** | Cálculo automático sobre um fundamento já verificado | Nem armazenamento de segredo, nem computação do modelo | Recálculo de um token dentro do contrato: `4,2·10⁹ × 3 gas ≈ 1,26·10¹⁰ gas` ≈ 37 800 $ por token com 1 gwei e 3000 $/ETH (ds1, confirmado). Crítico Claude: isso é cerca de 420 blocos de 30 milhões de gas (limite segundo a memória). Crítico ChatGPT: uma operação MUL simples, segundo a memória, custa 5 gas, portanto isso é um cenário, e não um limite inferior rigoroso | **Rejeitar como detector** |
| **Farol externo de limiar** (classe drand, de memória) | Aleatoriedade pública que ninguém conhece antecipadamente, se o limiar do seu comitê for honesto | Segredo: a rodada é publicada para todos. Uma coalizão dentro do comitê do farol descobre a rodada antes ou pode não liberá-la | Centenas de bytes por rodada por lote e espera de uma rodada (de memória, 30 s na cadeia principal e cerca de 3 s na rápida) | **Adotar como uma das duas fontes de D20** para amostras comuns |
| **VDF a partir do bloco final** | Atraso durante o qual o produtor do bloco não consegue escolher um bloco conveniente | Entropia independente: o VDF do mesmo bloco não é uma segunda fonte independente (crítico ChatGPT) | Trabalho sequencial do computador; verificação rápida | **Adotar como complemento ao farol**, registrar a suposição sobre a superioridade de hardware rápido |
| **Criptografia timelock via farol** | Revelação postergada de referências comuns, tarefas de exame | Segredo por mais de uma rodada; herda o limiar do farol | Como no farol | **Apenas para revelação postergada de dados comuns**; não revelar dados privados assim |
| **Quebra-cabeça com bloqueio temporal** (Rivest–Shamir–Wagner, de memória) | Atraso na revelação | O criador conhece a resposta imediatamente; a moeda é mais simples | Trabalho sequencial | **Rejeitar** |
| **VRF** | Valor unívoco e verificável para uma chave e uma entrada registradas antecipadamente | Segredo em relação ao dono da chave: ele calcula o valor quando quiser. A verificação da prova VRF revela o valor (erro de mm4). Não prova o fato do recálculo | Uma chamada e centenas de bytes por resposta | **Adotar**: para a designação de verificadores (contra suborno após a designação) e como moeda do pagador onde o resultado dela afeta o pagamento de terceiros; a chave é registrada para o pedido antes da fixação |
| **Commit–reveal** | Vinculação do sal a um único pedido antes da fixação da resposta | Proteção contra o «último a revelar», que pode ficar calado | gpt2: 448 bytes por esquema | **Adotar de forma restrita**: compromisso antes da fixação, sem direito de escolher o resultado |
| **Criptografia de limiar** (Shamir, DKG, decifração de limiar) | Armazenamento da chave sem um único detentor | Independência de `q` (seção 2.4); proteção na aplicação da regra (seção 2.3) | DKG com `n = 7`, `t = 5`: `7·6·32 + 7·5·48 = 3024` bytes de carga útil (gpt2), assinatura de limiar BLS — 288 bytes; sem replicação e reclamações | **Rejeitar para regras secretas**; o farol de limiar interno dos participantes — apenas como uma das fontes, não a única |
| **TEE** (SGX, SEV, TDX, GPUs protegidas) | Execução de código oculto do dono da máquina, com confiança no fabricante | Independência do fabricante e da sua cadeia de atestação; não há GPUs protegidas no parque D5 (RTX 2060, RTX 4070 Laptop, RX 580) | Cenário do crítico ChatGPT: verificação protegida 1,2 vezes mais longa que a aberta, `p = 0,1` — cerca de 3,20% do tempo de geração com carregamento de pesos; modelo na CPU — cerca de 50–100 ms por token contra 15–50 ms na GPU (crítico Claude) [suposição]. Crítico MiniMax: o dono pode usar o enclave como oráculo; o segredo depende da limitação do número de solicitações | **Apenas como modo de privacidade à escolha do usuário**, não fundamento de garantia |
| **FHE** | Computação sobre dados cifrados e, por um esquema universal, sobre um programa cifrado | Verificação da correção da computação; o resultado é aberto pelo detentor da chave (de novo `q`). O esquema aproximado CKKS não reproduz os bits do perfil v2 | 1,4·10⁷–2,6·10⁷ bootstraps por token, com 10⁴–10⁵ bootstraps por segundo [suposição] — 140–2600 s por token, de 19 horas a 15 dias por resposta de 500 tokens; multiplicador em relação à verificação aberta `Φ ≈ 3·10³…2·10⁵` (claude2, críticos Claude, ChatGPT, MiniMax). Acréscimo `p·ρ·Φ` com `n_w = 300`: de 2,1 a 139 gerações por resposta | **Rejeitar para verificação**; estudar apenas para privacidade |
| **MPC** | Computação sem reunir o segredo em um único lugar | Independência de `q`: a proteção depende da maioria honesta ou de «ao menos um honesto» com direito de arruinar o trabalho; com `q = 1` não há proteção | Para esconder a *escolha* da verificação, é preciso processar tudo — `1/p` = 31 / 303 / 4329 vezes mais caro que a moeda com `n_w` = 30 / 300 / 4320 (crítico Claude). Esconder a *solicitação*: crítico Claude — de 151 MB por token como limite inferior a 0,15–1 GB, 10–67 minutos por resposta a 1 Gbit/s; crítico ChatGPT — 448 MB por posição, 224 GB para 500 posições; crítico MiniMax — até 180 TB por resposta (as estimativas divergem em ordens de grandeza, ver seção 7) | **Rejeitar para verificação** |
| **iO** (ofuscação indistinguível) | Em teoria — execução de um programa sem revelar seu funcionamento | Não há implementação prática para o modelo; mesmo a iO ideal deixa ao trapaceiro um «ensaio» da sua falsificação pelo detector | Não é avaliado | **Rejeitar** |
| **Ofuscação de funções pontuais** | Verificação «coincidiu com a referência» sem revelar a referência | Proteção com espaço pequeno de respostas: força bruta; é a mesma armadilha | Hash | Apenas como parte da armadilha |
| **Criptografia funcional** | Obtenção do valor da função pelo dono da chave funcional | Ocultação da função do dono da chave (é necessário um esquema separado); é necessário um emissor de chaves | Não é avaliado | **Rejeitar** para esta tarefa |
| **PIR, ORAM** | Ocultação do índice de leitura do servidor | Ocultação da regra; evidência da origem dos dados | Crítico ChatGPT: em PIR de dois servidores com 10 000 registros de 32 bytes — uma consulta de cerca de 320 KB por servidor e ausência de conluio entre os servidores | **Rejeitar** para esta tarefa |
| **Armadilhas** (solicitação com resposta conhecida antecipadamente) | Novas informações: referência correlacionada com a verdade | Barateamento. Uma armadilha da mesma força que a moeda custa o trabalho do executor (≈ uma geração, paga e inútil para todos) e o da referência (uma geração, se for fresca). A coalizão reconhece a repetição de uma solicitação antiga | Razão entre o preço da armadilha e o preço da moeda `≥ 1/((1 − σ)ρ)`, onde `σ` é a probabilidade de reconhecer a armadilha: com `ρ = 0,21` — 5,3 / 6,8 / 9,5 / ∞ vezes com `σ = q` = 0,1 / 0,3 / 0,5 / 1; com `ρ = 0,40` — 2,8 / 3,6 / 5,0 / ∞ (claude2). gpt2: armadilhas descartáveis em 1% dos trabalhos com duas gerações acrescentam 2,02% | **Apenas «sinal para cima»**, sem reduzir a frequência e sem a marca «verificado» |
| **Testes estatísticos e limiares secretos** | Diagnóstico de falhas em massa e erros de implementação | Redução da frequência: limite `TV`; o limiar é aprendido por sondagens | Pouco | **Apenas «sinal para cima»** |
| **Verificador oculto, pagadores não vinculáveis** | Contra suborno após a designação (designação por VRF) e contra a distinção de pagadores preguiçosos (chaves descartáveis do pagador, claude1) | Independência de `q` na verificação por comitê. Para o pagamento não vinculável é necessário um emissor ou outro mecanismo sem privilégios especiais — não construído | Quilobytes e segundos (claude1), não avaliado por completo | **Adotar a designação por VRF; estudar os pagadores não vinculáveis** |
| **Prova ZK de computação** | O único caminho para um veredito publicamente verificável com base em uma testemunha fechada | Não trata do segredo das regras; o custo para o Qwen não foi calculado. Experiência do piloto: execução em zkVM 17 700 vezes mais lenta mesmo sem construir a prova | Não é avaliado | **Estudar** separadamente |
| **«Moving target defense»** | Valor da troca de configuração enquanto o observador não se adaptou | No SkyNet, a melhor troca é a cada tarefa, ou seja, uma moeda fresca | Zero além da moeda | Reduzir à moeda fresca |
| **Antifraude bancário, CAPTCHA** | Funcionam graças ao servidor fechado, ao custo da tentativa, às sanções não monetárias e às chamadas descartáveis | Nada disso aparece no SkyNet pela troca do arquivo de regras (seção 2.5) | — | Não transplantar |

**Achado separado de claude1 (não sobre sigilo): a verificação de Freivalds.** Verificar a multiplicação
de uma matriz por um vetor por projeção aleatória pode ser mais barato que a própria multiplicação:
razão de cerca de 1740 por token e bloco [cálculo, confirmado pelo crítico Claude]. Mas o crítico
ChatGPT observou que isso não é uma aceleração da resposta: é preciso transmitir as ativações
intermediárias, considerar as não linearidades, os arredondamentos do perfil v2 e a atualidade do vetor
a cada solicitação. A conclusão de claude1 «o tráfego de ativações torna isso pior que uma passagem
completa» é correta. Não se pode declarar todo o Qwen verificado com base em uma única multiplicação.

---

## 4. Estratégia recomendada

### 4.1. Etapas

Esta é a estratégia do conselho anterior («pagador-inspetor»), refinada pelos trabalhos e críticos deste
conselho. Nenhuma etapa exige regras secretas. As etapas 3, 4 e 9 dependem de decisões ainda não
aceitas (seção 5).

1. **Núcleo aberto.** O gerador da instância de verificação, a família de verificações admissíveis e a
   lei de escolha — parte aberta do núcleo com impressão digital fixada (D4). «Novas regras em momento
   aleatório» são novos valores de aleatoriedade, e não novos algoritmos.
2. **Fixação.** O executor calcula no perfil exato v2 e, em uma única entrada com aceite, deposita no
   registro o texto cifrado da resposta (D24). Até esse momento, nenhuma escolha de verificação é
   feita.
3. **Moeda secreta do pagador.** Após a fixação irrevogável, o programa do pagador toma aleatoriedade
   fresca e decide se verifica a resposta, com probabilidade
   `p = max(p_user, (R − c_f)/(R + H_lock))`; com `c_f ≈ 0`, isso é `R/(R + H_lock)`; com `H_lock = 0`
   (novato) — sempre. Para o dinheiro do próprio pagador, o farol não é necessário.
4. **Moeda verificável onde o dinheiro de terceiros depende dela.** Se o pagamento de terceiros depende
   do resultado da moeda (loteria com prêmio comum, disputas de nós terceiros), a moeda deve ser
   verificável: VRF de uma chave registrada para o pedido antes da fixação, ou um compromisso com sal
   publicado antes da fixação (gpt2, claude2). Um compromisso feito após a fixação é inútil: o pagador
   escolhe o resultado já vendo a resposta (erro de mm5 na proposta D28).
5. **Bloqueio do valor.** `H_lock` é apenas o valor que vence após o prazo de disputa; o prazo de
   verificação `δ` é muito menor que a janela de vencimento `W` (em tempo ativo, D12). A primeira
   falsificação comprovada queima atomicamente todo o valor não vencido da chave, incluindo as
   recompensas da mesma onda; ao prejudicado é devolvido não mais que o seu pagamento (candidato D26).
   Sem atomicidade, as fórmulas não resistem à onda: 10 falsificações paralelas com `R = 1`, `H = 4`,
   `p = 0,2` dão `+4,4295R` em vez de `−2,49676R` [cálculo].
6. **Marcas.** «Verificado» — apenas a resposta completamente verificada antes da exibição; todo o
   resto é «não verificado» por padrão. Uma etapa de treinamento não verificada não entra no modelo
   lançado (D6).
7. **Amostras comuns segundo D20.** A auditoria do treinamento, o exame, a loteria com prêmio comum e a
   designação de verificadores tomam aleatoriedade de não menos que duas fontes independentes (farol
   externo de limiar e VDF a partir do bloco final), misturadas por hash; a rodada é designada antes da
   fixação e ocorre depois dela. Os nós designados descobrem a escolha por VRF.
8. **Sinais apenas para cima.** Armadilhas, anomalias e testes estatísticos podem designar uma
   verificação adicional, mas não reduzem a frequência e não dão a marca «verificado».
9. **Não vinculabilidade do pagador** (elemento de pesquisa). Chaves descartáveis do pagador e um
   retransmissor, para que o executor não possa distinguir um pagador verificador de um preguiçoso
   (claude1). Enquanto o mecanismo não estiver construído, a tabela de risco contém a linha «os
   preguiçosos são distinguíveis: até `+R`, inclusive para o novato».
10. **O que não há no fundamento.** Regras secretas, chaves de verificação de rede, comitês de limiar
    de guardiões, TEE, FHE, MPC, iO.

### 4.2. O papel do blockchain e do farol: o «detector dinâmico no blockchain» na forma correta

A pergunta do dono sobre um detector dinâmico no blockchain recebe a seguinte resposta. O blockchain
faz bem o que se exige de um detector, *exceto* o segredo:

- **fixa a resposta antes da escolha da verificação** — sem isso, nenhuma aleatoriedade ajuda;
- **armazena compromissos** com rodadas futuras e sais, para que ninguém possa escolher o resultado
  conveniente;
- **torna a escolha reproduzível**: qualquer nó, após a rodada, calcula por si mesmo o que foi
  escolhido e verifica o fundamento da decisão mesmo após a parada total da rede;
- **executa a queima e o cálculo único**.

A «dinamicidade» não é dada pela cifragem das regras, mas pelo fato de a instância de verificação ser
derivada, a cada vez, de aleatoriedade que ainda não existia no momento da fixação da resposta. Para
uma resposta privada, essa aleatoriedade é a moeda do pagador; para decisões comuns — o farol segundo
D20. Os trabalhos chamaram isso assim: «gerador aberto de regras no núcleo mais uma instância da regra
derivada do farol, cuja rodada é designada antes da fixação» (claude1); «as regras são abertas, o
segredo está apenas na escolha: quem, quando e qual regra aplicar» (mm4); «imprevisível, e não
secreto» (mm3).

Dois erros que se deve evitar:

- **Farol na decisão monetária do pagador** (mm3, mm4). O sorteio público diz *o que* verificar, mas
  quem verifica é o mesmo pagador; um pagador preguiçoso não verificará nem por sorteio público, e não
  há sanção por não verificar sem caução (R5). O sorteio público aqui apenas acrescenta a suposição de
  honestidade do farol e a latência da rodada (críticos Claude, DeepSeek; mm2 e claude2 dizem o
  mesmo). mm3 e mm4 não concordam com isso (seção 7).
- **Modo alternativo «pelo último valor disponível»** (mm3). Se o farol está indisponível e as
  verificações da época usam um valor já conhecido, o trapaceiro sabe antecipadamente o que não será
  verificado. Isso viola diretamente D20. Com a rodada indisponível, a transação em disputa espera ou a
  verificação é obrigatória.

Mais um esclarecimento: «escolher o conveniente entre dois bits independentes» reduz a probabilidade de
verificação obrigatória de `p` para `p²` (crítico ChatGPT), enquanto *misturar* duas fontes com um hash
unívoco é exatamente o que D20 exige. O complemento proposto por mm5 a D19 «a moeda secreta e o farol
não se misturam» confunde essas duas ações e contradiria D20 (crítico Claude).

### 4.3. Preço

O segredo das regras não muda o preço: não afeta nem `ρ` nem `γ`.

| `n_w` | `p = R/(R + H_lock)` | Verificação `p·ρ` com `ρ` = 0,10 / 0,21 / 0,40 | Total contra Q8_0, lote 1 | Lote 8 |
|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5…+82,3% | +152…+186% |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0…+80,2% | +150…+181% |
| 4320 | 0,023% | 0,0023% / 0,0049% / 0,0093% | +50,0…+80,0% | +150…+180% |

Tabela — [cálculo] pela fórmula `γ(1 + pρ) − 1` e pelos `ρ`, `γ` medidos (crítico MiniMax, conferido
pelos críticos DeepSeek e Claude). O crítico ChatGPT lembra que os pontos extremos do intervalo de `γ` e
`ρ` foram tomados de placas diferentes e não foram medidos em par; é um envelope, não uma medição.

- **Novato.** A primeira resposta é verificação completa, 10–40% da sua geração. Com trabalho honesto
  estritamente sequencial e crescimento de `H_lock` em `R` por tarefa, o número esperado de
  verificações completas nas primeiras 30 tarefas é `1 + 1/2 + … + 1/30 ≈ 3,995`; isso é 1,33% /
  2,80% / 5,33% do trabalho da janela com `ρ` = 0,10 / 0,21 / 0,40 (mm1, crítico ChatGPT) [cálculo].
  Com início paralelo a partir de conta vazia, cada solicitação custa uma verificação completa.
- **Referência de 5%.** Como acréscimo pela verificação, é atingível: `p·ρ ≤ 0,05` exige `p` não maior
  que 50% / 23,81% / 12,5%, ou seja, `H_lock/R ≥ ρ/0,05 − 1` = 1 / 3,2 / 7 (gpt1, gpt2) [cálculo].
  Como «5% acima da geração usual» — não: o próprio perfil exato custa +50…+80% [medido γ]. O único
  caminho para 5% são núcleos mais rápidos e bit a bit iguais.
- **Acréscimos da estratégia.** 32–64 bytes de compromisso ou centenas de bytes de VRF por resposta onde
  é necessária a verificabilidade da moeda; o farol — centenas de bytes por rodada por lote e a
  latência de uma rodada apenas para amostras comuns (crítico Claude) [cálculo].
- **Quem paga** (mm4, crítico MiniMax). O acréscimo do perfil exato `γ − 1` é suportado pelo executor em
  cada resposta paga; a verificação `p·ρ` — pelo pagador, com seu pré-pagamento. A transferência da
  verificação para o pagador elimina o papel de «verificador a quem se paga pela verificação» de
  [CURRENT_DESIGN](CURRENT_DESIGN.md), seção 1. Então ou o preço `R` cresce 50–80%, ou a margem do
  executor tende a zero. Esta é uma questão separada do dono (seção 5).
- **Loteria B** (são pagas apenas as respostas escolhidas e completamente verificadas; variante de gpt1,
  gpt2 e do crítico ChatGPT). Com fração de escolha de 5%, as verificações custam em média 0,5 / 1,05 /
  2% do tempo da geração exata, mas 95% das respostas permanecem não verificadas e não pagas; a
  variância de um pagamento individual é `19R²`; a probabilidade de não receber nenhum pagamento em 20
  solicitações independentes é `0,95²⁰ ≈ 35,85%`, em 30 — 21,46% [cálculo].
- **Treinamento.** A repetição completa da etapa custa cerca de 100% da etapa por cada nó verificador; a
  referência de 20% não é demonstrada por nenhum esquema. Com `N = 1000` nós receptores, mesmo com
  custos adicionais nulos, para uma verificação resta não mais que 0,0002 do trabalho da etapa (crítico
  ChatGPT) [cálculo].

### 4.4. Risco residual

Ganho esperado de uma falsificação contra a inação; «dano» — fração de falsificações não detectadas do
sabotador, todas com a marca «não verificado». A tabela foi montada a partir das tabelas dos críticos
Claude, DeepSeek, ChatGPT e MiniMax e de STRATEGY_SEARCH 5.3; **estão destacadas as células corrigidas
por este conselho**. O detector oculto não melhora nenhuma linha [cálculo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novato, `H = 0` |
|---|---|---|---|---|---|
| Dinheiro, o pagador verifica por si; o registro está vivo, D26 e D23 resolvidos | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verificação sempre) |
| O mesmo, mas a coalizão `q = 1` inclui os produtores de blocos e censura a disputa | — | — | — | até `+R` | até `+R` |
| Resposta falsa com a marca «verificado» | 0 | 0 | 0 | 0 | 0 |
| Dano com `p = R/(R + H)`: toda a série de `n_w` falsificações passa | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 no pagador honesto |
| Dano com `p = 3R/(R + H)` | ≈ 12,5% | o mesmo | o mesmo | o mesmo | 0 |
| Pagadores preguiçosos da fração `λ`, o executor não os distingue | ≤ 0 com `p(1 − λ) ≥ R/(R + H)` | o mesmo | o mesmo | o mesmo | **`+λR`** |
| Pagadores preguiçosos distinguíveis (por sondagens com novas chaves — gratuitamente) | até `+R` | até `+R` | até `+R` | até `+R` | **até `+R`** |
| Pagador sem equipamento delegou a verificação a um trio aleatório | +0,001R | +0,027R | +0,125R | +R | o mesmo |
| Amostra comum segundo D20, ao menos uma fonte honesta | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 com a externa honesta; caso contrário até `+R` | o mesmo |
| Apenas o farol interno de participantes 64/43 | ≤ 0 exceto 4,8·10⁻²⁸ | exceto 9,4·10⁻¹⁰ | exceto 0,41% | até `+R` | o mesmo |
| Para comparação: regra secreta de época no comitê | vaza em 10 aplicações com probabilidade 0,65; depois cerca de `(1 − p)·E·R` por época | 0,97 | 0,999 | até `+R` por falsificação | as sondagens são gratuitas: até `+R` |
| Treinamento sem nó autoverificador | até `+R` | até `+R` | até `+R` | até `+R` | até `+R` |

Como ler a tabela:

- **A linha «≤ 0 com qualquer `q`»** só é verdadeira nas condições nomeadas: `q` é a parcela de conluio
  entre os verificadores externos; se a mesma coalizão controla a produção de blocos ou o farol, ela
  pode atrasar ou censurar a prova (gpt1 e gpt2 disseram isso diretamente). Também são necessários
  `δ ≪ W`, a queima atômica (D26), a solução do conflito com D16 e a regra de disputas falsas (D23,
  cálculo M9).
- **A execução da verificação é tão importante quanto a frequência.** Exemplo do crítico ChatGPT:
  `R = 1`, `H = 3`, `p = 1/4`, `c_f = 0` dão expectativa exatamente nula; se o pagador executa apenas
  90% das verificações designadas, a probabilidade de detecção é 0,225 e o ganho `+0,1R` [cálculo]. Se
  a primeira falsificação pode ser explicada como falha pelo D16 atual e `H` é preservado, a expectativa
  `(1 − p)R − c_f` é positiva.
- **«≈ 50%»** — é a probabilidade de que passe *toda a série* de `n_w = H/R` falsificações com
  crescimento de `H` após cada omissão (`h/(h + n)` com `n = h`). Uma falsificação direcionada de uma
  chave madura passa com probabilidade `1 − p`: com `H = 4320R`, isso é cerca de 99,977% (crítico
  ChatGPT segundo ds2).
- **As linhas «preguiçosos»** foram corrigidas: o valor anterior 0 para o novato é falso (seção 1, item
  6). Cenário: uma chave fresca apresenta uma falsificação ao pagador `X`; se `X` verifica, perde-se
  apenas `c_f`, não há nada para queimar; se `X` é preguiçoso, a chave recebe `R` e o conhecimento «`X`
  é preguiçoso»; depois as chaves maduras da coalizão apresentam falsificações apenas aos preguiçosos
  (crítico Claude). O crítico ChatGPT acrescentou que, mesmo com indistinguibilidade total, a condição
  `p(1 − λ) ≥ 1` para o novato é impossível de cumprir com `λ > 0`, e as chaves não vinculáveis fecham
  apenas um canal de distinção: texto, tempo, tamanho da solicitação e pagamento vinculado permanecem.

### 4.5. Novato

O novato com conta vazia (`H_lock = 0`) contra um pagador honesto é sempre verificado e perde `c_f`. A
ocultação das regras aqui não acrescenta nada. Duas ressalvas deste conselho: contra um pagador
preguiçoso, o novato recebe até `+R` (seção 4.4), e as novas chaves gratuitas podem elevar a fração de
solicitações completamente verificadas: se a fração de trabalho nos primeiros pedidos de chaves vazias é
`f`, e nos demais `p = 0,1`, o acréscimo é `ρ[f + 0,1(1 − f)]`, e a condição de 5% com `ρ = 0,21` dá
`f ≤ 0,1534` (crítico ChatGPT) [cálculo]. Nenhum esquema do conselho até agora resiste ao fluxo de novas
chaves e ao autopagamento ao mesmo tempo.

### 4.6. Pagador preguiçoso

A estratégia depende de o pagador realmente lançar a moeda e verificar. Um pagador preguiçoso que o
executor consegue distinguir dá até `+R` a qualquer chave. Meios em ordem decrescente de força: (a) o
programa do pagador, por padrão, executa a regra do núcleo, e desligar a verificação retira da resposta a
marca «verificado»; (b) chaves não vinculáveis do pagador (claude1) — é necessário um mecanismo de
pagamento sem emissor com privilégios especiais: a assinatura cega precisa de um emissor, o Privacy Pass
(de memória) é um esquema com emissor de servidor; um emissor de limiar reintroduz `q` (crítico Claude);
(c) o sorteio público do farol *não* corrige o pagador preguiçoso (seção 4.2). Como conciliar a não
vinculabilidade com a regra de disputas falsas sem caução (D23) não está resolvido.

### 4.7. Usuário sem equipamento

O usuário que não pode recalcular a resposta por si mesmo não está protegido por esta estratégia. Se ele
delega a verificação a um trio aleatório, a coalizão recebe `q³R`: +0,001R / +0,027R / +0,125R / +R; com
um assistente — `qR`, e com um cúmplice escolhido de propósito — até `+R` com qualquer fração média
(crítico ChatGPT) [cálculo]. Um vazamento positivo limitado é diretamente proibido por D1, portanto este
é um buraco aberto de D21. O detector oculto não a fecha: claude1 mostrou um contraexemplo com «canários
secretos» — um verificador em conluio passa honestamente por todas as tarefas de controle alheias e
mente apenas nas suas próprias falsificações, que reconhece pela chave do executor ou pela liberdade de
escolha (a falsificação não precisa ser determinística, a resposta exata é determinística). A variante
honesta é vender dois níveis de serviço com a diferença claramente escrita: «verificado por mim» e
«verificado pelos designados, vazamento `R·q^k`» (mm1).

### 4.8. Dano

O sabotador não precisa de lucro. Com qualquer frequência `p < 1`, parte das suas falsificações passa. A
única proteção é a marca «não verificado» por padrão e «verificado» apenas após a verificação completa
antes da exibição. O detector oculto não muda a linha de dano (todos os trabalhos). mm1 encontrou o único
lugar onde a *escolha fresca* muda substancialmente o quadro do dano: na verificação parcial (sobretudo
da etapa de treinamento), contra uma amostra fixa aberta, o trapaceiro, com uma única execução exata,
encontra as células não verificáveis e falsifica apenas elas, detecção 0; a escolha fresca da amostra
após a fixação dá detecção `s` (fração da parte verificada) para um desvio e `1 − (1 − s)^m` para `m`
desvios. Os críticos DeepSeek e Claude esclareceram: é aleatoriedade fresca, e não segredo das regras; o
motivo de tal falsificação é o dano, e não o dinheiro (contra o trabalho honesto, a falsificação exata
ganha cerca de zero); e a conclusão depende da suposição não estabelecida de que as células da etapa de
treinamento podem ser falsificadas independentemente.

---

## 5. Decisões

As redações abaixo são **recomendações**, e não decisões aceitas. Os requisitos imutáveis R1–R6 não
mudam pela edição de linhas do roteiro. Segundo D4, após o lançamento com impressão digital fixada,
alterar o conjunto de transições admissíveis exige a migração para uma nova rede; a troca de chave não
dá esse direito (crítico ChatGPT).

### 5.1. D4 — complementar, sem mudar o sentido

O texto atual de D4: a verificação é automática, sem votações; cada nó executa por si mesmo a verificação
segundo a impressão digital fixada das regras. O conselho é unânime contra enfraquecer D4 em favor
de regras secretas: uma regra secreta exige aceitar o veredito dos detentores da chave, do enclave ou de
um grupo, que o nó não pode verificar por si mesmo. O crítico ChatGPT mostrou como seria tal
enfraquecimento: «o nó aceita o veredito do programa atual, escolhido pelos detentores da chave da
época», «o nó aceita o relatório de um programa medido por uma cadeia de confiança do fabricante» ou «o
nó aceita um bit emitido pelo grupo».

**Complemento proposto** (união das variantes dos críticos Claude e ChatGPT, claude1, claude2, gpt1, da
proposta D27 de mm5):

> «O núcleo pode receber como entrada aleatoriedade desconhecida do executor até a fixação final do
> resultado: (a) a moeda secreta da parte cuja própria decisão é protegida, lançada após a fixação; (b)
> os valores das fontes D20 em rodadas designadas antes da fixação e que ocorrem depois dela. O gerador
> da instância de verificação, a família de verificações admissíveis e a lei de escolha são parte aberta
> do núcleo com impressão digital fixada; novas regras em momento aleatório são novos valores de
> aleatoriedade, e não novos algoritmos. A instância implementada que afeta direitos de terceiros é
> publicada não depois do pagamento e é recalculada por cada nó. A marca local do pagador, por si só, não
> cria evidência de rede sobre o trabalho. O fundamento de uma decisão comum não contém regras secretas
> de longa duração nem chaves de verificação, comitês de limiar, atestações TEE e vereditos fechados;
> eles são admissíveis apenas como verificações adicionais que elevam a frequência».

**O que não muda:** a imutabilidade do núcleo, a ausência de votações, a verificação autônoma por cada nó.
**O que quebra:** nada; o complemento fecha a direção dos «detectores secretos» como fundamento de
garantia. A possibilidade de uma prova publicamente verificável da relação fixada (ZK) permanece aberta e
não exige alteração de D4 (crítico ChatGPT).

### 5.2. D20 — esclarecer

O texto atual de D20: não menos que duas fontes públicas independentes, valor em um momento designado
antecipadamente após a fixação final, sem direito de omissão.

**Esclarecimento proposto** (crítico Claude com complementos do crítico ChatGPT):

> «Não menos que duas fontes públicas independentes; seus valores são combinados por uma função hash
> unívoca com rótulo de domínio e identificador do lote, e não pela escolha de um dos valores. A rodada
> de cada fonte é designada antes da fixação final e ocorre após a aceitação final do bloco com a
> fixação. São proibidos omissão, novo sorteio, substituição da fonte ou passagem a um valor conhecido
> anteriormente; com a rodada indisponível, a transação em disputa espera, e uma nova solicitação não
> recebe bilhete para essa rodada. O farol é usado para amostras que afetam direitos de terceiros
> (treinamento, exame, loteria com prêmio comum, designação de verificadores); para a verificação privada
> do pagador sobre seu próprio dinheiro, ele não é necessário. O farol de limiar interno dos participantes
> pode ser uma das fontes apenas com a suposição registrada sobre a parcela de conluio dos seus detentores
> e não pode ser o único. O VDF do mesmo bloco não é considerado uma fonte independente. A confiança nas
> fontes é uma suposição segundo R4».

**O que exclui:** o modo alternativo «último valor disponível» (mm3), a alteração de mm5 a D19 («não
misturar as fontes»), o farol na decisão monetária do pagador (mm3, mm4). **Risco aberto:** se «esperar a
rodada» significa atraso infinito, este é um risco não fechado R1/R6 (crítico ChatGPT); o crítico
MiniMax propõe, em vez de esperar, considerar a verificação obrigatória.

### 5.3. O que não muda

- **D1** — não mudar e não enfraquecer para «enquanto `q` é pequeno»; um vazamento positivo limitado
  continua sendo violação (todos os trabalhos e críticos).
- **D7** — uma regra secreta não o cumpre com nenhum limiar (seção 2.4).
- **D19** — não mudar: o complemento de mm5 é errôneo (seção 4.2).
- **D6** — a ocultação não muda a linha de dano; as marcas são esclarecidas conforme a questão 3 da
  síntese anterior.

### 5.4. Relação com as oito questões da síntese anterior

As oito questões de [STRATEGY_SEARCH](STRATEGY_SEARCH.md), seção 6, permanecem abertas. Este conselho
acrescentou a elas:

| Questão da síntese anterior | O que o sexto conselho acrescentou |
|---|---|
| 1. D21, D11, D2: pagar ou não a resposta omitida pela moeda | Não há novos argumentos. Corrigida a célula «pagador preguiçoso × novato» (até `+R`): se o pagamento do omitido é permitido, é necessária proteção contra a distinção dos preguiçosos. O crítico ChatGPT continua a favor da verificação completa como contrato principal e da loteria B como separada |
| 2. D7: qual verificação é admissível para o pagamento | Confirmado que nem a ocultação, nem a atestação, nem o comitê podem reduzir a frequência mínima; podem apenas elevá-la. Acrescentado: importa a fração de verificações *executadas*, e não apenas a frequência (exemplo `+0,1R`) |
| 3. D6: marcas | Armadilha, estatística e detector oculto não dão a marca «verificado» |
| 4. D16: falha honesta | Se a primeira falsificação pode ser declarada falha e `H` é preservado, a moeda não dissuade: `(1 − p)R − c_f > 0`. A decisão sobre D16 é necessária antes de qualquer ativação do pagamento do omitido |
| 5. D8: prazo e direitos de disputa | A condição `δ ≪ W` e a vivacidade do registro entram na linha «≤ 0» (seção 4.4) |
| 6. D23: bloqueio até M9 | Nenhum dos onze trabalhos calculou M9; o bloqueio permanece. A não vinculabilidade dos pagadores acrescenta uma nova questão a M9 |
| 7. Novo D26: bloqueio do valor | Confirmada a necessidade da queima atômica da onda; o bit comum da época é um novo contraexemplo (`+8,1R`) |
| 8. D1: mudar ou não | Não mudar |

### 5.5. Novas questões-decisões deste conselho

**Questão A (D4).** Aceitar o complemento de D4 da seção 5.1? *Recomendação dos críticos Claude,
ChatGPT e DeepSeek:* sim; o sentido de D4 não muda. *Onde divergiram:* o crítico ChatGPT propõe uma
redação mais detalhada, que fala explicitamente da verificação «por prova publicamente verificável da
afirmação fixada»; o crítico DeepSeek considera suficiente uma nota curta sobre aleatoriedade após a
fixação; o crítico MiniMax (como mm2 e mm5) considera que D4 não precisa ser alterado de modo algum,
porque a regra de verificação já é aberta.

**Questão B (D20).** Aceitar o esclarecimento de D20 da seção 5.2? *Recomendação:* sim. *Onde
divergiram:* o que fazer com a indisponibilidade da rodada — esperar (críticos Claude e ChatGPT) ou
considerar a verificação obrigatória (críticos DeepSeek e MiniMax). A espera pode se tornar atraso
infinito; a verificação obrigatória muda o preço e, na loteria, a composição dos vencedores.

**Questão C (farol ou moeda na decisão monetária).** Registrar que, para a verificação privada do pagador
sobre seu próprio dinheiro, o farol não é usado? *Recomendação* dos críticos Claude e DeepSeek, bem como
de claude1, gpt1, gpt2, ds1, ds2, mm1, mm2: sim. *Contra:* mm3, mm4, mm5 (sorteio público em vez de
moeda), claude2 (VRF do pagador mais farol para assuntos comuns). O crítico DeepSeek propõe primeiro
comparar os dois esquemas com um miniagente nos mesmos ataques (seção 6).

**Questão D (pagadores não vinculáveis).** Incluir no programa de pesquisa um mecanismo em que o executor
não possa vincular as solicitações de um mesmo pagador? *Recomendação* do crítico Claude: sim, como
pesquisa; até a sua construção, a tabela de risco contém a linha «os preguiçosos são distinguíveis: até
`+R`». *Aberto:* pagamento sem emissor com privilégios especiais, compatibilidade com D23, distinção por
texto e tempo.

**Questão E (peso).** Registrar na especificação de peso ([CURRENT_DESIGN](CURRENT_DESIGN.md), seção 4)
que o peso pelo qual são selecionados detentores ou verificadores não cresce com solicitações autopagas?
*Recomendação* do crítico Claude: sim. claude2 propunha a seleção «por peso de trabalho verificado» sem
essa ressalva.

**Questão F (quem paga pelo perfil exato).** Como distribuir o acréscimo `γ − 1` se o papel do verificador
pago desaparece? *Levantaram* mm4 e o crítico MiniMax; não foi proposta solução.

**Questão G (novas decisões de mm5).** Aceitar D27 («segredo da escolha, e não segredo da verificação») e
D28 («moeda com revelação postergada»)? *Recomendação dos críticos:* D27, em sentido, está incluído no
complemento de D4 (seção 5.1); D28 duplica o compromisso da moeda de gpt2 e claude1 e só faz sentido se o
compromisso é publicado *antes* da fixação da resposta.

---

## 6. O que calcular com miniagentes e o que verificar por experimento

### 6.1. Miniagentes (frações exatas, hash de controle, repetição em um segundo dispositivo)

Lista comum dos quatro críticos. Para cada cálculo, guardar a descrição das regras, as entradas, as
frações exatas, o pior histórico, a versão e o hash de controle (crítico ChatGPT).

1. **Regra de época contra moeda fresca.** Onda, `H_lock`, queima de todo o valor, sequência adaptativa.
   Referências: `+8,1R` / `−2,3751096381R` (gpt2), `98,01R` (claude2), 1/5 → 1/9 → 0 (claude1),
   `+4,4295R` / `−2,49676R` / `+7,2R` (conselho anterior e crítico ChatGPT).
2. **Sondagens de pagadores preguiçosos com novas chaves.** Expectativa da sondagem, tempo até o
   reconhecimento do pagador, ganho das chaves maduras; com pagadores vinculáveis e não vinculáveis.
   Expectativa do crítico Claude: com vinculabilidade, a dissuasão contra os preguiçosos é nula.
3. **Moeda secreta contra sorteio público do farol** nos mesmos ataques (crítico DeepSeek). Expectativa:
   resultados monetários iguais e custo maior no sorteio público.
4. **Programa linear da mistura de testes** (gpt1, gpt2): referência «três classes → 2/3 contra 1/2»,
   adição de uma classe não coberta → 0; minimax pela matriz «teste × falsificação».
5. **Caudas do limiar:** binomiais, sem reposição, por peso com autopagamento, com suborno após a
   designação. Referência «3 de 5»: `107/12500`, `4077/25000`, `1/2`, `1`; SHA-256 de controle das
   quatro linhas de gpt1, repetido pelo crítico ChatGPT:
   `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Armadilhas:** `1/((1 − σ)ρ)` na grade de `ρ` e `σ`; reconhecimento da repetição; amortização do
   banco de referências contra o recálculo; verificação da afirmação de mm2 sobre o custo quase nulo da
   repetição de uma solicitação verificada.
7. **Desvios em VRF e no compromisso do pagador:** recusa de revelar, várias chaves, interrupção após a
   revelação, loteria com prêmio comum.
8. **Mistura de fontes D20:** viés com uma fonte honesta, com retenção do bloco, com indisponibilidade da
   rodada; proibição do «último valor».
9. **Falsificação «cirúrgica» de mm1** contra amostra fixa aberta e amostra fresca: detecção 0 contra
   `s`; limiar `p·s ≥ (R − c)/(R + H_lock)`.
10. **Contagem de operações não lineares por token** segundo a configuração fixada D5 para as estimativas
    de FHE e MPC (agora 1,4·10⁷–2,6·10⁷ aproximadamente); estimativas de DKG, commit–reveal, VRF em
    bytes e mensagens.
11. **Lote 8 no pagador** (mm3): `ρ` foi medida em relação à geração em lote, e o recálculo de uma
    resposta pelo pagador não fica mais barato assim.
12. **Correção de tabelas:** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), a célula «preguiçoso × novato»
    em STRATEGY_SEARCH 5.3.
13. **M9** — custo da disputa para a regra D7 e condição de suspensão do bloqueio D23; autodisputa,
    limite de devolução, fluxo de novas chaves.

### 6.2. Experimentos

**Para a conclusão sobre o detector oculto, não é necessário experimento:** são teoremas, e a medição
não os refuta (claude1, claude2, ds2, críticos Claude e DeepSeek). Experimentos com FHE, MPC e TEE
também não são necessários: o melhor resultado deles não muda os teoremas.

**No âmbito de D5 (permitido):** O5 — qualidade em 320 tarefas; O3 e O4 com núcleos mais rápidos e bit a
bit iguais — o único caminho para a referência de 5%.

**Fora de D5 — apenas com autorização separada do dono:**

- tempo de uma passagem de verificação na CPU de um notebook e de um telefone, inicialização a frio e a
  quente, energia;
- até que ponto os metadados da solicitação (tempo, tamanho, texto) permitem ao executor distinguir um
  pagador verificador — disso depende o custo das chaves não vinculáveis;
- a frequência de divergências silenciosas de hardware `P_f` — antes de qualquer alteração de D16;
- a fração de coincidência de tokens entre Q8_0 e o perfil exato (para estimar a falsificação barata e
  para a decodificação especulativa exata);
- a latência e o custo da rodada de um farol real, o comportamento com uma fonte silenciosa;
- para as armadilhas — se a verificação é reconhecida e quanto custam as referências;
- a repetição exata da etapa de treinamento como pré-condição de qualquer verificação dela.

---

## 7. Divergências não resolvidas pelo conselho e referências duvidosas

### 7.1. Divergências

1. **Pagamento da resposta omitida pela moeda contra a verificação completa de cada resposta paga.**
   claude1, claude2, ds1, ds2 e mm1–mm5 apoiam-se no pagamento do omitido sob risco de queima do valor
   não vencido; gpt1, gpt2 e o crítico ChatGPT — na verificação completa como contrato principal e na
   loteria B como separada. Herdado do conselho anterior; decisão do dono sobre D21, D11, D7.
2. **Farol ou moeda na decisão monetária do pagador** — seção 5.5, questão C. mm3 e mm4 consideram que o
   sorteio público remove a suposição de um pagador honesto; os críticos Claude e DeepSeek consideram
   isso um erro (um pagador preguiçoso não verificará nem por sorteio público). Não calculado.
3. **`R/(R + H_lock)` ou `R/H`.** O primeiro é exato para o dinheiro; o segundo dá margem e um número
   esperado finito de falsificações até a detecção com `H` fixo, mas custa cerca de duas vezes mais com
   `H` pequeno. O crítico ChatGPT mostrou que, com crescimento de `H` após cada omissão, em ambas as
   regras o número médio de omissões até a primeira detecção é infinito. O conselho não apresentou novos
   argumentos.
4. **Armadilha como ganho autônomo.** mm2 (a referência secreta é o único ganho real) e ds1 (economia da
   referência em cache) contra claude2, mm4, mm5, gpt1 e os críticos Claude e DeepSeek. O crítico
   ChatGPT assumiu uma posição intermediária: uma referência já conhecida do pagador honesto pode
   reduzir o custo marginal, e para armadilhas frescas indistinguíveis `σ` pode ser 0 mesmo com `q = 1`
   entre executores externos. O cálculo não foi realizado.
5. **Mistura de tipos de verificação como meio de economia.** gpt1, gpt2, claude2 — possível com
   cobertura provada das classes de erro; mm2 — nunca. Para o Qwen, a cobertura não está provada.
6. **Farol de limiar interno dos participantes.** mm3 — o melhor primitivo; mm5 — apenas externo;
   claude1, claude2 e o crítico Claude — admissível apenas como uma das fontes.
7. **Até que ponto R2/R3 proíbem segredos comuns.** ds1, mm1, mm3 — por princípio; claude2, críticos
   Claude e ChatGPT — apenas segredos necessários para verificar decisões passadas.
8. **Custo do MPC.** As estimativas divergem em ordens de grandeza: ds1 — 2,4–14 MB por token (os críticos
   consideram que este é o custo do traço de verificação, e não do MPC); crítico Claude — 0,15–1 GB por
   token; crítico ChatGPT — 448 MB por posição; crítico MiniMax — até 180 TB por resposta (ele considera
   todas as multiplicações em rede, e o crítico ChatGPT observa que a multiplicação de um peso aberto por
   uma ativação compartilhada, em muitos protocolos, é executada localmente). A conclusão «o MPC está
   fora do orçamento e depende de `q`» não muda por isso.
9. **Multiplicadores de FHE:** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵`; o crítico ChatGPT considera incorreto
   multiplicar a estimativa por bootstraps por `ρ` de uma passagem pronta, e é necessária uma estimativa
   da mesma passagem sob um esquema concreto. As conclusões não dependem disso.
10. **Amostra oculta na verificação parcial** (mm1): «detector secreto» ou moeda fresca — divergência de
    palavras; a aplicabilidade à etapa de treinamento depende da independência não medida das células.
11. **D16.** Queimar `H_lock` por qualquer divergência comprovada, com indenização aos honestos a partir
    da arrecadação da rede (linha de claude1 e dos críticos Claude e DeepSeek), contra a preservação das
    recompensas anteriores em caso de falha honesta (gpt1, gpt2, crítico ChatGPT). É necessária a medição
    de `P_f`.
12. **Treinamento.** Nenhum esquema cumpre D7 com `q = 1` dentro de 20%.
13. **Principal classe de falsificações:** a «cirúrgica» cara (mm1) ou a Q8_0 barata (mm3, mm4). Não
    medido.

### 7.2. Erros encontrados nos números dos trabalhos

Para que números errôneos não entrem em outros documentos:

| Trabalho | Afirmação | Correto [cálculo dos críticos] |
|---|---|---|
| mm1 | Com `H_lock = 10R`, frequência 0,0909 e custo de verificação 0,005–0,009% | `0,0909·ρ` = 0,91–3,64% |
| mm1 | Vazamento da «dezena» com `q = 0,1`: `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Limiar 25% com `H_lock = R` | 29,29% com os próprios parâmetros de mm1 |
| mm5 | `p·ρ` = 0,021–0,042% com `p = 0,1` | 2,1–4,0% (a própria tabela de mm5 está correta) |
| mm5 | «FHE é determinístico, o observador constrói um dicionário» | Esquemas FHE seguros são probabilísticos |
| mm5 | «VRF é imprevisível para o dono» | O dono calcula a VRF quando quiser |
| mm5 | Repetição completa da etapa de treinamento ≈ 36,8% | 36,8% é um exemplo de carga mista; repetição da etapa ≈ 100% |
| mm2 | «5% são atingíveis com `p ≤ 0,33%`» | Com `ρ = 0,21`, é admissível `p ≤ 23,8%` |
| mm4 | «VRF não revela a escolha» | A verificação da prova VRF revela o valor |
| ds2 | `N·H_s ≈ 2718` tentativas | Cerca de 890 sem reposição; basta uma posição segura |
| ds1 | A armadilha custa `φ·ρ`, a referência em cache economiza | A armadilha custa não menos que uma geração do executor; o cache primeiro precisa ser obtido |
| ds1, ds2 | As armadilhas acrescentam detecção `φ` com qualquer `q` | Não mais que `φ(1 − q)` na repetição; com `q = 1` — 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Pagador preguiçoso × novato = 0 | Até `+R` |
| claude2 | Fórmula do exemplo de época `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98,01R`; a coincidência é casual |

### 7.3. Referências duvidosas (avaliações dos críticos de memória, sem conferência)

| Trabalho | Afirmação | Avaliação |
|---|---|---|
| mm5 | «RandAILight» como farol | Duvidoso; o nome é desconhecido dos críticos |
| mm5 | «iO é teoricamente possível, Bark e coautores ~2001» | Confundido: Barak e coautores 2001 — impossibilidade da ofuscação de «caixa preta»; candidatos a iO — Garg e coautores 2013 |
| mm1 | «Roteiro de iO de Barak e coautores, 2019» | Duvidoso |
| mm2 | Apêndice F: «Ben-Or e coautores», «Allingham, Melvin, Temple 1992», «Dwork ~1999», «Hashcash — Khomstein», «Awasthi», «Randcast Bader ~2020» | Duvidoso em quase todos os pontos; não transferir para a síntese |
| mm3 | «Cui, Wang e outros, Skoglid e outros» sobre moving target defense | Duvidoso |
| ds1 | «Canetti 1997 — funções pontuais no modelo de oráculo aleatório» | Duvidoso (de memória — suposição do tipo DDH) |
| ds1 | «Bishop–Jain–Kowalczyk 2018» | Duvidoso quanto ao ano (de memória, 2015) |
| ds1, ds2 | «drand ~30 s» | Parcialmente: de memória, em cadeias diferentes, 30 s e 3 s |
| ds2 | «MPC 5,98·10¹² MAC (claude2)» | A referência é imprecisa |
| claude1 | «SGX.Fail, chave mestra da Secret Network, 2022» | Duvidoso nos detalhes (o próprio autor assinalou) |
| claude1 | Privacy Pass como exemplo de emissão sem uma parte especial | De memória — esquema com emissor de servidor |
| claude2 | Limite inferior de PIR — Beimel, Ishai, Malkin | Duvidoso: seus trabalhos são sobre PIR com pré-processamento; o limite clássico, de memória, é de Chor e coautores |
| claude2 | Lowd–Meek, Tramèr: `d` consultas binárias bastam para qualquer classificador | Duvidoso em geral |

As demais referências dos trabalhos (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin,
Micali–Rabin–Vadhan, Boneh e coautores sobre VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi,
jogos de inspeção, Barak e coautores sobre a impossibilidade da «caixa preta») parecem aos críticos
corretamente atribuídas quanto à direção; as fontes primárias não foram conferidas.

---

## 8. Quem fez o quê

O conselho trabalhou com os materiais do projeto, sem acesso à rede e sem experimentos.

- **Onze trabalhos independentes:** ChatGPT — dois (gpt1, gpt2), DeepSeek — dois (ds1, ds2), Claude —
  dois (claude1, claude2), MiniMax — cinco (mm1 com ênfase na economia, mm2 — na proteção contra a
  fraude, mm3 — na distribuição e recuperação, mm4 — nos contraexemplos, mm5 — nas soluções não
  convencionais). Cada trabalho analisou seis direções da incumbência: quem detém a chave, como
  verificar por uma regra desconhecida, o que pode ser um detector secreto, a teoria, o preço e a
  compatibilidade com as decisões.
- **Quatro críticas:** uma de ChatGPT, DeepSeek, Claude e MiniMax (a crítica do MiniMax é apresentada
  como proposta com crítica). Cada crítico leu todos os onze trabalhos, procurou erros e contraexemplos e
  recalculou os números-chave. O crítico DeepSeek verificou a aritmética com programas locais em frações
  exatas, o crítico Claude — com cálculos curtos em Python, o crítico ChatGPT reproduziu o hash de
  controle da tabela de gpt1.
- **Síntese:** este documento foi composto por Claude com base nos trabalhos e nas críticas. Não foram
  acrescentadas novas avaliações e números além dos trabalhos, das críticas, dos resultados de D5 e de
  STRATEGY_SEARCH; onde os críticos divergiram, isso é indicado.
