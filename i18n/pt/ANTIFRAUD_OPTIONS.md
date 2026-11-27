<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Variantes de combate à fraude: resultado das auditorias e do conselho de modelos

[English](../../docs/ANTIFRAUD_OPTIONS.en.md) · [中文](../zh/ANTIFRAUD_OPTIONS.md) · [Español](../es/ANTIFRAUD_OPTIONS.md) · [Français](../fr/ANTIFRAUD_OPTIONS.md) · [Deutsch](../de/ANTIFRAUD_OPTIONS.md) · [Italiano](../it/ANTIFRAUD_OPTIONS.md) · [Русский](../../docs/ANTIFRAUD_OPTIONS.md) · **Português** · [العربية](../ar/ANTIFRAUD_OPTIONS.md)

Situação em 27 de novembro de 2026.

**O que foi feito.** O dono do projeto reuniu seis auditorias independentes de completude e dois
mapas de mecanismos de proteção contra a fraude e propôs três ideias próprias: embutir a
verificabilidade no próprio modelo, tomar técnicas dos jogos e «cruzar» as formas de contornar a
verificação com trabalho útil. O conselho de modelos escreveu onze trabalhos independentes e quatro
críticas cruzadas e consolidou tudo isso nas variantes descritas abaixo.

**Status.** Este documento é raciocínio e cálculo. As grandezas medidas são tomadas apenas do
experimento D5 ([EXPERIMENT_D5](EXPERIMENT_D5.md)) e marcadas [medido]. Todo o resto está marcado
[cálculo] ou declarado suposição. As decisões aceitas continuam sendo apenas D1–D25
([ROADMAP](ROADMAP.md), seção 3); tudo o que aqui se propõe mudar são propostas do conselho, e não
decisões. O conselho não realizou novos experimentos, protótipos nem instalações. A literatura é
citada de memória dos modelos ou segundo os dados das auditorias e não foi conferida com as fontes
primárias. Consolidações anteriores: [STRATEGY_SEARCH](STRATEGY_SEARCH.md) e
[HIDDEN_DETECTOR](HIDDEN_DETECTOR.md).

**Notações.** `R` — preço da tarefa; `c` — custo do trabalho honesto no perfil exato (inteiro);
`c_f` — custo da falsificação para o trapaceiro; `H_lock` — valor bloqueado e não vencido da
chave; `p` — probabilidade de verificação da resposta; `q` — parcela de peso da coalizão entre os
verificadores designados; `ρ` — tempo de verificação de uma resposta pronta em uma passagem, em
frações do tempo de sua geração exata: 0,10–0,40 com lote 1 e 0,26–0,64 com lote 8 [medido];
`γ` — desaceleração do perfil exato em relação ao Q8_0 usual: 1,52–1,78 com lote 1 e 2,47–2,79 com
lote 8 [medido, apenas RTX 2060].

## Resumo curto

1. **Caro não é verificar, é calcular com exatidão.** A verificação de uma resposta custa 10–40% de
   sua geração [medido], mas o acréscimo principal é a desaceleração do perfil exato em 1,52–1,78
   vezes [medido]. A referência «cerca de 5%», com os núcleos atuais, é inalcançável em qualquer
   variante, por mais rara que seja a verificação [cálculo].
2. **A ideia «impressões digitais e recálculo de um trecho aleatório» funciona, mas não como
   barateamento da garantia.** Se `s` trechos de `N` são revelados, uma célula substituída de forma
   direcionada passa com probabilidade não menor que `1 − s/N`. A avaliação «30 vezes mais barato, e
   a fraude continua sendo detectada» significa, na prática, «30 vezes menos detecção». As
   impressões digitais são úteis em outro papel: uma raiz curta do traço permite resolver a disputa
   dividindo ao meio até um único passo e dá ao dispositivo fraco uma verificação parcial com marca
   honesta.
3. **A ideia «verificabilidade dentro do modelo» funciona em uma forma:** treinar adicionalmente ou
   reescrever os núcleos para que o perfil exato se torne rápido. Isso reduz `γ` e não enfraquece a
   garantia. As impressões digitais são escritas pelo programa, e não pelo modelo, e não precisam de
   treinamento adicional. As somas de verificação nas camadas protegem o executor honesto de falhas
   de equipamento, mas não de intenção.
4. **Dos jogos transfere-se apenas a ordem dos turnos:** «selou → fixação final → escolha secreta →
   revelação → recálculo». Ao cálculo estão ligados apenas dois turnos: o recálculo do trecho
   revelado e a verificação da testemunha da tarefa. Um jogo separado ao lado do trabalho útil não
   prova nada.
5. **São quatro variantes e um complemento:** verificação completa de cada resposta pelo pagador;
   loteria por pedidos inteiros; moeda secreta do pagador com valor bloqueado; tarefas com resultado
   verificável; e decodificação especulativa exata como possível forma de baratear a primeira e a
   terceira variantes.
6. **Recomendação.** O contrato principal é a verificação completa de cada resposta pelo pagador no
   perfil exato. Só ele cumpre as decisões aceitas sem alterá-las. Tarefas com resultado verificável
   são um tipo separado de tarefas e, por enquanto, a única garantia rigorosa para o treinamento. A
   loteria é a tarifa para lotes de pedidos. A moeda com valor bloqueado continua candidata até o
   cálculo M9 e as decisões do dono.
7. **Primeiro passo.** Um cálculo: M9 — disputas falsas sem depósito, todos os ramos de silêncio e
   recusa. Um experimento (com autorização do dono): nos perfis v2 e llama.cpp Q8_0 já montados,
   medir a coincidência de tokens com prefixo comum. Ele resolve de uma vez três questões (seção 5).
8. **Literalmente inexequível:** proteger o consumidor sem equipamento sob conluio total dos
   verificadores; verificar o passo de treinamento sob conluio total dentro de 20% de acréscimo;
   encaixar a resposta verificada em 5% com o `γ` medido. Os afrouxamentos mínimos estão formulados
   como perguntas ao dono na seção 7.

## 1. O que as auditorias encontraram

Rótulos das auditorias: RU — `SkyNet_audit_completeness_RU`; SC — `skynet_completeness_audit`; GPT —
`gpt-SkyNet-audit`; DS — `deepseek-AUDIT_REPORT`; GEM — `gemini_report`; CR — `chat_responses`;
mapas — `mehanizmy-anti-obman` (MEH) e `mechanisms_map_report` (MAP). Onde os trabalhos do conselho
leram de modo diferente quem chamou o quê, isso está marcado com a palavra «controverso».

### 1.1. Abordagens omitidas

| Abordagem | Quais auditorias a citaram | Avaliação do conselho |
|---|---|---|
| Impressões digitais de ativações, TOPLOC | SC, GPT, GEM, CR, DS (em uma linha), MAP; MEH — controverso | Não é base de pagamento; apenas sinal para verificação exata adicional (seção 2.4) |
| Esquemas otimistas, disputa com árbitro, divisão ao meio | Todas as seis e os dois mapas | Camada necessária de disputa; sob conluio total não há com quem disputar, por isso não substitui a verificação pelo pagador |
| Testes estatísticos de substituição do modelo | GPT, DS, GEM, CR, MAP; SC e RU — controverso | Apenas sinal para aumentar a frequência de verificação; não entra no núcleo |
| Aritmética de ponto flutuante reproduzível, núcleos inteiros do tipo Ozaki | SC, GEM, DS, GPT, RU; CR chama RepOps | Ponto flutuante não substitui o perfil inteiro; a aceleração dos núcleos é hipótese para experimento |
| Somas de verificação ABFT | SC, GEM, DS, GPT, RU | Autocontrole do nó honesto contra falhas; cobre apenas multiplicações lineares |
| Verificação de Freivalds | SC, CR, GPT, GEM, mapas | Funciona para a parte linear da aritmética exata com vetor secreto novo após a fixação |
| Disponibilidade dos dados | SC, DS, GPT; GEM — contra; RU e mapas — controverso | Engenharia da disputa e do treinamento, e não garantia de R4 |
| Desenho de mecanismos com verificação cara | GEM, DS, GPT, SC | Confirma o limiar `R/(R + H_lock)`; não dá nova alavanca |
| Atestação de hardware de GPU, TEE | Quase todos | Sinal adicional e modo de privacidade; não se pode reduzir por ele a frequência de verificação |
| Aval e seguro sem depósito do participante | SC, GEM, DS, GPT, RU | O cadeado alheio é, em essência, depósito de terceiro, questão para R5; o fundo de seguro abre a autodisputa |
| A experiência de Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | Todas as seis e os mapas | Todas se apoiam em depósito, validadores confiáveis, TEE ou «um honesto»; técnicas isoladas são transferíveis |

Citadas por apenas uma auditoria: provas seletivas por camadas como base (RU), vinculação do texto
cifrado da resposta ao compromisso por DLEQ (SC), pool de cupons (SC; segundo um dos trabalhos —
também GEM e GPT).

### 1.2. Pontos fracos das conclusões anteriores

- O limiar `p ≥ R/(R + H_lock)` é correto sob três condições que antes não foram nomeadas: preço não
  inferior ao custo, a moeda é realmente lançada, o valor está disponível para queima (GPT, SC, GEM,
  RU).
- A conclusão «a referência de 5% foi refutada» refere-se a uma implementação dos núcleos (GEM, SC,
  DS).
- A barreira das provas breves foi calculada para uma única disposição (SC, GEM, DS, GPT).
- A coincidência de bits é mostrada em seis configurações, e não «em qualquer hardware» (DS, GEM, SC,
  GPT). As críticas esclareceram: para a passagem longa sobre uma resposta pronta — em três.
- A afirmação «pagador preguiçoso e novato juntos dão zero» era um erro: o ganho chega a `+R`.
- A enumeração de «92 milhões de estratégias» não prova a completude (RU).
- A literatura dos conselhos anteriores é citada de memória (RU, GEM, DS, GPT).

### 1.3. Contradições entre requisitos e decisões

- **D16 contra a verificação por amostragem.** Se a falha honesta não é punida, o trapaceiro declara
  a falsificação uma falha e recebe `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** A terceira condição — «o erro multiplicado por `R` é menor que o preço da tentativa» — é
  inaplicável quando a tentativa é gratuita (DS, RU; no conselho — ChatGPT).
- **A emissão de créditos por treinamento com demanda zero**, o conluio total, o acréscimo de 20% e a
  verificação por cada nó, juntos, não se cumprem (DS, SC, GEM, GPT, CR, MEH).
- **O consumidor sem equipamento e R4** (SC, GEM, RU, CR).
- **O D1 literal exclui qualquer amostragem** (RU, DS).
- **Disputa sem depósito e fundo de disputas finito** (SC, GEM, GPT, RU).
- **«Primeiro a confiança total, depois os experimentos»** foi chamado de círculo vicioso: `γ`, `ρ`,
  a qualidade e a frequência de falhas são estabelecidos apenas por medição (DS, GPT). Esta é a
  opinião das auditorias e de um crítico; o conselho não violou nem revoga a restrição vigente aos
  experimentos.

### 1.4. Novos ataques

- **Pagador preguiçoso.** Se a parcela `λ` dos pagadores não verifica, o limiar passa a
  `R/((1 − λ)(R + H_lock))`; com conta vazia ele é maior que um, e o trapaceiro que reconheceu o
  pagador preguiçoso recebe até `+R` (SC) [cálculo].
- **A moeda não é imposta:** o programa do pagador pode ser recompilado com `p = 0` (GEM, SC).
- **Revenda da resposta entre sessões** («ataque da máfia»): o intermediário pega o pedido, compra a
  resposta de um executor honesto e não paga. Funciona sem conluio dos verificadores; cura-se com a
  ordem «pré-pagamento bloqueado → resposta → verificação no prazo → pagamento» (GEM; desenvolvido
  no conselho).
- **Venda do valor não vencido** antes da saída (RU). Cura-se com a proibição de transferência.
- **O autopagamento** aumenta o valor bloqueado e reduz a frequência de verificação. A crítica
  mostrou que o dinheiro não abre isso (o próprio dinheiro do trapaceiro queima na detecção), mas
  barateia o dano direcionado.
- **Inundação com chaves gratuitas:** cada nova chave exige verificação completa e sobrecarrega o
  pagador; é negação de serviço, e não roubo.
- **Substituição de um ou dois tokens dentro da janela de impressão digital do TOPLOC** (SC).

### 1.5. O que é duvidoso nas referências e nos números das auditorias

- **Aceleração dos núcleos segundo Ozaki até `γ` = 1,05–1,20.** Duvidoso: os núcleos rápidos de D5 já
  usam as mesmas instruções de 8 bits, e com eles mediu-se 1,52–1,78; 24 blocos de 32 são recursão,
  que a decomposição não acelera. Não se pode colocar esse número nas estimativas ao lado dos
  medidos.
- **TOPLOC:** «258 bytes por 32 tokens», «10–100 vezes mais rápido», «sobrecarga de 1–3%». Dois
  trabalhos confirmam de memória, três — «não consigo verificar»; para o SkyNet nada disso foi
  medido.
- **Não foi possível verificar:** os números de DeepProve e FlashProve, Verde (nas auditorias, três
  conjuntos diferentes de acréscimos), as perdas de TEE no H100, o preço de DLEQ em gas, os status e
  incidentes de Bittensor e de outras redes, vários números arXiv.
- **Atribuições incorretas:** o algoritmo Krum é atribuído aos autores errados (MEH); em uma
  auditoria há um erro aritmético no limiar (`c_f ≈ 0,3c`, `p ≥ 0,73`).
- Um mesmo número em duas auditorias não representa duas medições independentes: ambas podem estar
  recontando uma mesma fonte.

## 2. Ideias do dono levadas a construções

### 2.1. Verificabilidade dentro do modelo e treinamento adicional

- **«O modelo se protege» não funciona.** Os pesos e o código são abertos; o trapaceiro não é
  obrigado a executar o modelo. Todos os onze trabalhos confirmaram isso.
- **«O modelo escreve as impressões digitais»** — é um programa de hash em torno de pesos
  imutáveis. Não é preciso treinamento adicional e ele nada acrescenta.
- **As somas de verificação nas camadas (ABFT)** detectam falha aleatória. Um adversário que conhece
  o mecanismo escolhe um erro que preserva a soma. A recursão, as tabelas e a divisão na atenção não
  são cobertas por somas. A tese de vários trabalhos «o ABFT elimina o conflito de D16» foi
  considerada exagerada pelas críticas.
- **O treinamento adicional só faz sentido para reduzir `γ`:** fazer com que o perfil exato coincida
  com os núcleos rápidos de 8 bits («cânone arredondado», proposta do DeepSeek). Os bits continuam
  bits, a garantia não muda. Risco: o primeiro perfil de 8 bits em D5 já foi rejeitado por qualidade
  [medido]; o custo do treinamento e a perda de qualidade não foram medidos, e as horas de GPU
  citadas nos trabalhos são suposições.
- **O treinamento adicional «para robustez ao arredondamento»**, para que o perfil rápido seja
  verificado por tolerância, volta ao contrato com tolerância (seção 2.4) e não dá fronteira
  demonstrável.
- **Um modelo com menos estado** reduz o tráfego de verificação do trecho, mas não aumenta a parcela
  de substituições detectáveis.

**Veredito:** funciona uma forma — a aceleração do perfil exato. Ela se resolve por experimento.

### 2.2. Impressões digitais e recálculo de um trecho aleatório

**Construção.** O executor, antes da escolha do verificador, sela com uma raiz os tokens e os
estados intermediários. O verificador escolhe secretamente um trecho, recebe a entrada selada do
trecho e o recalcula no perfil exato. O trecho pode ser verificado sem recalcular todo o início da
resposta: isso também confirma D5, onde a passagem por trechos dá os mesmos hashes de estado
[medido]. A afirmação de vários trabalhos «não se pode recalcular um trecho sem o prefixo» foi
rejeitada pela crítica.

**Por que a fronteira `1 − s/N` não é contornada.** O trapaceiro calcula honestamente tudo, exceto
uma célula, e continua honestamente a partir do valor substituído. O traço é consistente em todos os
lugares, exceto em uma transição. Se `s` de `N` transições são reveladas, haverá uma transição que é
verificada com probabilidade não maior que `s/N`. As impressões digitais tornam a mentira detectável,
mas não a multiplicam. Só pode contornar a fronteira uma verificação em que qualquer mentira viola
uma grande parcela das igualdades (provas breves), e seu preço é o mesmo.

**Dois tipos de cortes** [cálculo pela configuração de D5]:

| Corte | O que atesta | O que é preciso transmitir | O que não detecta |
|---|---|---|---|
| Por camadas: um bloco em toda a sequência | Uma transição do bloco a partir da entrada apresentada; o bloco — cerca de 2,65% da passagem, a cabeça de saída — cerca de 15,1% | 0,78 / 4,9 / 14,6 MiB em 160 / 1000 / 3000 posições | Uma substituição montada em outra camada: chance de 1 em 32–33 |
| Por posições: todas as camadas em um segmento de 64 posições | Os tokens do segmento são iguais à escolha exata com o estado selado da borda esquerda | 48 MiB de estado e 64 KiB por cada posição anterior: 58 / 110 / 236 MiB | Uma posição substituída fora do segmento: passa com probabilidade `1 − L/T`, por exemplo 93,6% com 500 + 500 tokens |

O executor, com isso, precisa guardar 0,13–2,38 GiB de pontos de verificação por resposta durante a
janela de disputa [cálculo]. No registro pode ir apenas a raiz de 32 bytes: o próprio estado é 3–5
ordens de grandeza maior que a entrada de D24.

**A falsificação «rascunho com perfil rápido + passagem exata».** Foi encontrada pela crítica Claude.
O trapaceiro gera a resposta em Q8_0, depois faz uma passagem exata pelos tokens prontos e imprime o
traço. Nesse traço, todas as transições de todos os blocos são consistentes; não coincidem apenas as
posições em que o token do rascunho difere da escolha exata.

- O custo da falsificação é `c·(1/γ + ρ)`, a economia contra o trabalho honesto é `1 − 1/γ − ρ`:
  18,4% com `γ = 1,65`, `ρ = 0,21`; a falsificação compensa quando `ρ < 1 − 1/γ` (0,34 / 0,39 / 0,44
  com `γ` = 1,52 / 1,65 / 1,78) [cálculo].
- O corte por camadas não a detecta (exceto a chance de 1 em 32–33 na cabeça de saída).
- O corte por posições de comprimento 64 a detecta com probabilidade de 97%, se os tokens do Q8_0 e
  do perfil exato coincidem em 95% das posições; 49% com coincidência de 99%; 29% com 99,5%; 6,5% com
  99,9% [cálculo]. A parcela de coincidência não foi medida.
- A verificação completa sempre a detecta. A brecha diz respeito apenas aos esquemas em que o corte
  **substitui** a passagem completa.

Consequência: o corte atesta «o executor pagou ao menos pela passagem exata», e não «a resposta foi
gerada pelo perfil exato». Aqui as críticas divergiram: o DeepSeek considera que o corte por posições
detecta a substituição de toda a resposta por Q8_0 com probabilidade 1; o MiniMax — que essa
probabilidade não foi medida; o Claude apresentou o cálculo acima. Quem decide é a medição da
coincidência de tokens.

A crítica do MiniMax acrescentou: a falsificação gratuita «interromper a resposta antes» não cria
células falsas de modo algum. O comprimento da resposta e o motivo da parada devem fazer parte do
objeto de verificação.

**O que a raiz do traço ainda oferece:**

- **Disputa por divisão ao meio.** Duas partes com traços diferentes, em um número logarítmico de
  turnos, convergem para um único passo, que cada nó recalcula sozinho. A crítica esclareceu: os
  15–23 turnos declarados bastam apenas até a célula; dentro do bloco são necessárias mais cerca de
  27 divisões; a regra «silêncio é derrota» exige o cálculo M9.
- **Dispositivo fraco.** O pagador sem placa de vídeo pode verificar um segmento por resposta. Isso dá
  a marca «verificado parcialmente», e não «verificado». O custo para ele é o tráfego de 52–300 MiB
  por resposta e o tempo de processador; no telefone não foi medido.
- **Imutabilidade do histórico do executor** e disputa sobre uma solicitação privada com revelação de
  uma célula.

**Veredito:** a construção é possível e útil para a disputa e para o dispositivo fraco, mas não
barateia a garantia de D1 e D25. Para que a substituição pontual se torne menos vantajosa que a
inação, com 32 blocos é preciso revelar 2 / 4 / 7 / 10 blocos com margem de 5 / 10 / 20 / 30%
[cálculo], e contra o dano (D6) nem isso ajuda.

### 2.3. Técnicas dos jogos

| Técnica | Onde o turno está ligado ao cálculo | Onde não está ligado |
|---|---|---|
| «Selei — abri» | O trecho revelado é obrigado a coincidir com o recálculo a partir da entrada selada | O selo em si não prova nada: pode-se selar também uma mentira consistente |
| «Um corta — o outro escolhe» | A escolha é feita após a fixação com a moeda secreta do verificador | O que corta estraga uma parte de `N`; não há economia contra a verificação completa |
| Moeda comum das duas partes | Não é necessária quando está em jogo o dinheiro de um só pagador: basta a moeda secreta dele | Quem se revela por último frustra o resultado desfavorável; sob conluio total, todas as contribuições são conhecidas da coalizão |
| Cartas sem crupiê (mental poker) | — | Para escolher o número do trecho é redundante: o mesmo faz uma única função aleatória verificável |
| «Cada um vigia o rival» | O pagador verifica a própria resposta — é nisso que se baseiam todas as variantes da seção 3 | O executor não pode punir o pagador desonesto sem depósito (cálculo M9) |
| Cartas marcadas, comprador secreto | — | O segredo da armadilha em uma rede aberta só é guardado pelo pagador, por isso a armadilha coincide com a verificação dele e é mais cara que ela |

Uma fonte pública comum de aleatoriedade só é necessária onde se verifica o dinheiro de outros; então
vale D20 (não menos de duas fontes independentes).

**Veredito:** dos jogos tomaram-se a ordem dos turnos e o princípio principal «verifica quem tem
dinheiro em jogo». O jogo não transforma a amostragem em verificação completa.

### 2.4. Executor rápido e juiz exato

**Contrato com tolerância.** O executor calcula no Q8_0 rápido, o pagador faz a passagem exata e
aceita a resposta se, em cada posição, a avaliação do token escolhido fica atrás da maior em não mais
que `m`. A vantagem sobre o «certificado com margem» antes rejeitado: o veredito é calculado em
números inteiros e é igual em qualquer dispositivo. Mas a crítica encontrou quatro defeitos.

- **A tolerância legaliza respostas alheias.** Qualquer rascunho mais uma passagem exata mostra ao
  executor todas as avaliações; ele corrige as posições fora da tolerância e obtém uma resposta
  admissível. O produtor mais barato de tal resposta é o modelo-rascunho mais barato, e não o Q8_0 do
  mesmo modelo.
- **A liberdade de escolha é um canal de dano.** Nas posições com diferença menor que `m`, o token é
  escolhido pelo executor, incluindo a parada antecipada. Exemplo: as avaliações «continuar» e
  «parar» são 100 e 99; com `m = 1`, a resposta interrompida passa na verificação completa. Tal texto
  receberia a marca «verificado com tolerância» — em essência, isso é violação de D6. Uma marca
  semelhante já foi rejeitada pelo conselho anterior.
- **O executor honesto é obrigado a verificar a si mesmo**, senão perde o valor em um único resultado
  atípico, inclusive em uma entrada escolhida pelo pagador. Então o custo é `1 + ρ·γ`: +15…+71% com
  lote 1, e com lote 8 não há ganho contra a geração exata [cálculo].
- **O custo declarado «+0,01…+2,3%» não resistiu:** para revelar trechos o executor precisa de hashes
  de estado do perfil exato, ou seja, de uma passagem exata para cada geração [cálculo].

Mesmo com executor rápido, a passagem exata completa do juiz custa na RTX 2060 não menos que 31,9% do
tempo da geração usual [cálculo], portanto em 5% esse contrato não encaixa cada resposta.

**Decodificação especulativa exata** — o mesmo contrato com `m = 0`. O rascunho é obtido por qualquer
meio, paga-se apenas a resposta bit a bit igual à exata. O contrato e a garantia não mudam, D6 não é
afetado. O preço depende da parcela de coincidência de tokens e do comprimento das séries
coincidentes; estimativa inferior `1 + ρ·γ`. Não medido; com coincidência abaixo de cerca de 95% sai
pior que a geração exata direta.

**TOPLOC e impressões digitais com tolerância em ponto flutuante.** A impressão digital atesta que as
ativações são consistentes com o texto, e não de onde veio o texto. Falsificação: texto por qualquer
modelo, depois uma passagem do modelo declarado por esse texto — as impressões digitais são
autênticas. O veredito com tolerância depende do equipamento: dois nós honestos podem divergir, por
isso não se pode queimar o valor com base nele, e D4 é violado literalmente. Para que a tarifa com
tolerância seja barata, o verificador precisa de uma referência que não tem, enquanto ele mesmo não
calculou a passagem exata.

**Veredito:** o contrato com tolerância e as impressões digitais com tolerância não entram na lista de
variantes: eles mudam o produto e colocam uma marca em um texto escolhido pelo executor. São
admissíveis apenas como sinal para verificação exata adicional. A decodificação especulativa exata é
candidata a barateamento, decidida por uma medição.

## 3. Variantes integrais

Preço — acréscimo computacional total em relação à geração usual Q8_0 sem verificação
[cálculo pelas medições de D5]. Não entram nele o registro, as disputas, o armazenamento, o tráfego e
a energia: eles não foram medidos. Ganho — esperado, por uma falsificação apresentada. A borda
inferior «+67%» une o `ρ` da placa RTX 4070 Laptop ao `γ` da placa RTX 2060; em uma única RTX 2060 o
intervalo começa em +84%.

| № | Variante | Preço com lote 1 | Dinheiro do trapaceiro com `q` = 0,1 / 0,3 / 0,5 / 1 | Novato com conta vazia | Sabotador sem lucro | Principal risco residual |
|---|---|---|---|---|---|---|
| V1 | Verificação completa de cada resposta pelo pagador | +67…+149% (em uma única RTX 2060 +84…+149%) | `−c_f` com todos os `q` | `−c_f` | Não há marca falsa «verificado»; pode frustrar a entrega | Pagador preguiçoso; recusas falsas do pagador (M9) |
| V2 | Loteria por pedidos inteiros | +53…+82% e reserva do comprador `R/p` | `−c_f` com todos os `q` | 0 | A parcela `1 − p` das respostas não é verificada e não é contida por nada | Renda irregular; a reserva é questão para R5 |
| V3 | Moeda secreta do pagador e valor bloqueado | +50…+82%; a própria verificação 0,005–3,6% | Não mais que zero com todos os `q`, se o pagador lança a moeda a tempo | `−c_f` (verificação sempre) | Passa a parcela `1 − p`: até 99,98% | Pagador preguiçoso reconhecido — até `+R`; a falha honesta queima o valor |
| V4 | Tarefas com resultado verificável | `(N − 1)·v/w`, não medido | `−c_f` com todos os `q` | 0 | A testemunha incorreta não passa | Não é resposta de modelo nem passo de treinamento |
| V5 | Complemento: decodificação especulativa exata sobre V1 ou V3 | Não medido; estimativa inferior +15…+71% | Como na variante de base | O mesmo | O mesmo | A coincidência de tokens não foi medida |

**O pagador sem equipamento** não tem garantia em nenhuma variante. Se ele delega a verificação a um
trio de nós designados, o pagamento falso esperado é `R·q³`: 0,001`R` / 0,027`R` / 0,125`R` / `R` com
`q` = 0,1 / 0,3 / 0,5 / 1 [cálculo]. Isso já está registrado em D21.

### V1. Verificação completa de cada resposta pelo pagador

**Passos.** O pedido fixa o modelo, o perfil, a semente, os limites de comprimento e a condição de
aceitação. O executor calcula a resposta no perfil exato e fixa, em uma única entrada, o texto cifrado
e a raiz do traço. O pagador, antes da exibição, recalcula a resposta inteira em uma passagem,
incluindo o comprimento e o motivo da parada. A divergência significa não pagamento; o valor em
espera não queima. A marca «verificado» só é colocada após a passagem.

**Garantia e suposições.** A resposta falsa não é paga e não recebe marca com qualquer parcela de
conluio, para o novato e para qualquer número de chaves. Suposições: os bits coincidem no dispositivo
do pagador (mostrado em seis executores [medido], em telefones — não); o núcleo de verificação é
correto; o pagador realmente verifica.

**Preço.** `γ·(1 + ρ) − 1`: +67…+149% com lote 1; +211…+358% com lote 8 (em uma única RTX 2060
+251…+358%). Exemplo `γ = 1,65`, `ρ = 0,21`: +99,65%. Para o pagador, a verificação custa 15–71% do
tempo de sua própria geração usual [cálculo].

**O que mudar nas decisões.** Nada; são necessários esclarecimentos de D6 (duas marcas, nenhuma
intermediária), D16 (com verificação completa, a divergência implica apenas não pagamento) e D22
(seção 4).

**Não medido.** A qualidade do perfil exato (experimento O5); `γ` em outras placas; tempo e memória no
notebook e no telefone; o preço da disputa; o comportamento em recusas falsas do pagador.

### V2. Loteria por pedidos inteiros

**Passos.** O comprador reserva o prêmio com antecedência. Todos os resultados do lote de pedidos são
fixados antes do sorteio. O sorteio escolhe a parcela `p` dos pedidos; os escolhidos o pagador
verifica por completo e paga `R/p`; os restantes não são pagos e recebem a marca «não verificado».

**Garantia e suposições.** O pagamento falso é impossível mesmo com conta vazia e sem queima de
valores; D16 não precisa ser mudado. Suposições: sorteio por D20; a reserva do comprador não é
considerada depósito.

**Preço.** `γ·(1 + p·ρ) − 1`: +53…+82% com lote 1; exemplo `p = 0,05`, `γ = 1,65`, `ρ = 0,21`:
+66,73%. Mas para um **resultado verificado** há `1/p` vezes mais trabalho.

**Pontos fracos.** A renda é irregular: com `p = 0,1`, um novato honesto com probabilidade de 34,87%
não recebe nada pelos primeiros dez pedidos; com 6000 tarefas por mês, `p = 0,01` e custo de 95% do
preço, a probabilidade de mês deficitário é de 33,10% [cálculo]. As respostas não verificadas não são
contidas por nada: o sabotador com chaves gratuitas fornece lixo gratuitamente.

**O que mudar.** Responder se a reserva `R/p` são «meios antecipados» segundo R5; escolher as fontes de
aleatoriedade segundo D20.

**Não medido.** A probabilidade exata de ruína ao longo do caminho, o tamanho da reserva, a demanda por
essa tarifa.

### V3. Moeda secreta do pagador e valor bloqueado

Esta é a estratégia do conselho 5 ([STRATEGY_SEARCH](STRATEGY_SEARCH.md)) com correções.

**Passos.** A resposta é fixada no perfil exato. Após a fixação, o programa do pagador lança sua moeda
secreta e verifica a resposta por completo com probabilidade não inferior a `R/(R + H_lock)`; no
novato — sempre. Uma divergência provada queima, com um único ato, todo o valor não vencido da chave,
incluindo as recompensas da mesma onda; ao prejudicado devolve-se não mais que `R`. O valor não
vencido não pode ser transferido, vendido nem empenhado. A resposta pulada pela moeda é paga e recebe
a marca «não verificado».

**Garantia e suposições.** O resultado esperado de qualquer série de falsificações não excede o valor
bloqueado com qualquer parcela de conluio: exemplo de controle — uma onda de dez falsificações dá
+4,4295`R` sem queima e −2,49676`R` com ela [cálculo, reproduzido pelas críticas]. Suposições: o
pagador realmente lança a moeda e verifica a tempo; o registro está disponível; o valor realmente se
perde.

**Preço.** +50…+82% com lote 1; a própria verificação em chaves maduras — 0,005–3,6% do trabalho. A
primeira janela do novato custa 1,3–5,3% do trabalho da janela em unidades de geração exata [cálculo].

**Pontos fracos.** A brecha do pagador preguiçoso não é fechada por nenhuma correção: com conta vazia
e `λ > 0` o limiar é inexequível. Com o D16 vigente, o trapaceiro declara a falsificação uma falha e
recebe `(1 − p)·R − c_f`. O sabotador passa com probabilidade `1 − p`. Um acréscimo barato é o piso da
frequência (por exemplo, `p ≥ 1/11` custa 0,9–3,6% do trabalho), mas mesmo então 90,9% das
falsificações do sabotador passam [cálculo].

**O que mudar.** D2, D11 e D21 (pagamento da resposta pulada pela moeda); D7; revogação de D16 para
divergência publicada; nova decisão sobre o valor bloqueado; resposta se a queima é multa segundo R5;
cálculo M9.

**Não medido.** A frequência de falhas silenciosas de equipamento — dela depende quantos participantes
honestos perderão o valor; a parcela de pagadores que realmente executa a verificação.

### V4. Tarefas com resultado verificável

**Passos.** O plano (D9) resolve antecipadamente uma tarefa cujo resultado é acompanhado de uma
testemunha verificável por máquina: testes, prova formal, solução de um problema com certificado de
otimalidade. A candidatura é selada antes da revelação da testemunha, para que ela não possa ser
interceptada. Cada nó verifica a testemunha sozinho; o pagamento é único pelo conteúdo da tarefa.

**Garantia.** A testemunha incorreta não passa sob conluio total, conta vazia e qualquer número de
chaves.

**Preço.** Se `N − 1` nós verificam por `v` com custo de geração `w`, o acréscimo é `(N − 1)·v/w`. Com
`N = 1000` ele cabe em 20% apenas se `v/w ≤ 2·10⁻⁴`; com `v/w = 10⁻³` isso já é 99,9% [cálculo]. A
razão `v/w` foi tomada das auditorias e não foi medida.

**Pontos fracos.** É outro produto: não é uma resposta livre de modelo nem um passo de gradiente. A
tarefa pode ser resolvida sem modelo e sem placa de vídeo. A regra que gera tarefas difíceis úteis não
foi apresentada. A verificação da testemunha é copiável, por isso não é paga por D15: a ideia «o
telefone ganha verificando certificados» contradiz isso.

**O que mudar.** Complementar D9 e D15; D18 continua sendo pesquisa.

**Não medido.** Que parcela do trabalho da rede cabe nessa classe.

### V5. Complemento: decodificação especulativa exata

O rascunho é obtido por qualquer meio rápido; o executor mesmo o confere com a passagem exata e
corrige as divergências; paga-se apenas a resposta bit a bit exata. A garantia é a mesma da variante
de base V1 ou V3; as decisões, exceto o esclarecimento de D22, não mudam. O ganho só é possível se os
tokens do perfil rápido e do exato coincidem com frequência e em séries longas. Nada disso foi medido.

## 4. Recomendação do conselho e primeiro passo

**Recomendação (consolidação).** O contrato principal é **V1**. Só ele cumpre D1, D6, D7 e D25 para a
resposta sem novas suposições sobre frequência, valor bloqueado e queima, e não exige alteração das
decisões aceitas. Todos os onze trabalhos dão para ele a mesma fórmula de preço. **V4** — um tipo
separado de tarefas do plano. **V2** — tarifa para lotes de pedidos acordados. **V3** — candidata:
incluir só após o cálculo M9 e decisões explícitas do dono. **V5** e a aceleração dos núcleos exatos —
caminhos para reduzir o preço, e não contratos separados.

**Esclarecimentos de decisões para V1** (propostas, não decisões):

- D6: as marcas são duas — «verificado» após verificação completa bit a bit antes da exibição, e «não
  verificado».
- D16: com a verificação de cada resposta pelo pagador, a divergência implica apenas não pagamento.
- D19: se a tentativa é gratuita, a suposição de D19 não se aplica.
- D22: o rascunho pode ser obtido por qualquer meio; paga-se apenas a resposta bit a bit igual à
  exata. O comprimento da resposta e o motivo da parada fazem parte do objeto de verificação.
- D12 não mudar: a substituição do tempo ativo pela altura dos blocos da cadeia externa permite que
  valores não vencidos amadureçam enquanto a rede está indisponível.
- Nova decisão sobre o preço: em que perfil se calcula o volume de computação. Com preço de 1,10 do
  custo do perfil usual, o trabalho honesto no perfil exato é deficitário em 42–68% do custo
  [cálculo]; essa premissa em si não está aprovada no projeto.

**Um cálculo.** M9: disputas falsas sem depósito para o pedido avulso — silêncio de cada parte,
autodisputa, autopedido com disputa falsa, limites de bytes e cálculos por processo, fonte dos meios.
Sem ele, nenhuma variante é incluída (D23).

**Um experimento** (é preciso autorização do dono; extensão dos O3 e O4 já realizados). Nos perfis v2
e llama.cpp Q8_0 já montados, com prefixo comum, medir a parcela de coincidência de tokens, a
distribuição do atraso da avaliação do token escolhido e os comprimentos das séries de coincidência.
Ele resolve três questões: se V5 se paga; se o contrato com tolerância é viável; se o corte por
posições detecta a falsificação «rascunho + passagem exata», isto é, se o pagador sem placa de vídeo
tem alguma proteção. Primeiro vale verificar se nas gravações de D5 se conservaram as avaliações
completas dos dois perfis.

**Onde as críticas e os trabalhos divergiram.**

1. **Qual contrato é o principal.** Os críticos Claude e ChatGPT — V1. O crítico DeepSeek — V3 com
   correções, e V1 como tarifa cara e modo de novato. O crítico MiniMax — V1 como tarifa básica e a
   moeda para chaves maduras, mas a rede paga apenas pelo verificado.
2. **Pagar ou não pela resposta pulada pela moeda.** A favor — a maioria dos trabalhos; contra — os
   dois trabalhos ChatGPT e um trabalho MiniMax. Se não se pagar, o executor honesto recebe `p·R` por
   tarefa, e isso é uma loteria sem o multiplicador `1/p`. Não há terceira opção; é escolha do dono.
3. **Qual experimento primeiro.** Os críticos Claude e ChatGPT — a coincidência de tokens dos dois
   perfis. Os críticos DeepSeek e MiniMax — um microbenchmark de núcleos de 8 bits do tipo Ozaki com
   conferência bit a bit: ele mostra se a referência de 5% é alcançável em geral. A consolidação o
   coloca em segundo.
4. **O `γ` alcançável.** 1,05–1,20, 1,1–1,3 ou «não vai diminuir». Não medido.
5. **São depósito segundo R5** a queima do valor não vencido, a reserva de disputa, a reserva da
   loteria, o longo prazo de vencimento e o aval.
6. **Limitar o valor bloqueado por cima.** Um teto de 10`R` limita o número esperado de falsificações,
   mas torna a verificação de chaves maduras cerca de 400 vezes mais cara [cálculo de um crítico, não
   reconferido].
7. **Terceira marca.** O crítico MiniMax propõe «verificado parcialmente»; o crítico Claude — apenas
   duas marcas.

## 5. Treinamento: o que existe e o que não existe

**O que não existe.** Nenhum trabalho dá garantia para o passo de treinamento. O treinamento não tem
pagador: a base da emissão de créditos deve ser verificada por cada nó completo. O treinamento inteiro
não foi construído nem medido; as medições de D5 referem-se apenas à passagem direta e não se
transferem para a passagem inversa e o otimizador.

**O que existe.**

- **Repetição completa do passo por cada nó** — rigoroso, mas custa `N` passos adicionais: com dez nós,
  cerca de 1000% [cálculo].
- **Cortes do passo:** o nó verifica uma célula em cerca de quatro mil. Preço 0,24% / 2,4% / 24% com
  10 / 100 / 1000 nós [cálculo], mas sob conluio total a detecção é zero.
- **Pagamento do resultado verificável** (V4): garantia rigorosa para uma afirmação estreita.
  Verifica-se a testemunha da tarefa, e não o passo de gradiente; as formulações dos trabalhos «o
  treinamento está resolvido» e «o dano está excluído» foram consideradas exageradas pela crítica.
- **Pagamento pela melhoria comprovada no exame** (D18) continua sendo pesquisa: o exame atesta a nota
  em um conjunto dado, mas não a ausência de porta dos fundos nos pesos.

**Limite.** Com 1000 nós e acréscimo de 20%, toda a verificação independente de um nó deve custar não
mais que 0,0002 do trabalho do passo [cálculo]. A prova breve do passo, segundo todas as estimativas
do projeto, é ordens de grandeza mais cara.

**Recomendação do conselho.** Emitir créditos apenas por resultados que cada nó verifica sozinho; não
incluir na versão do modelo um passo não verificado (isso já é D6).

## 6. O que é literalmente inexequível: perguntas ao dono

O conselho não propõe mudar os textos R1–R6. As propostas de dois trabalhos de alterar R4 e R6 foram
rejeitadas pela crítica: é a base imutável. A impossibilidade geral de conciliar R4 e R6 para todos os
algoritmos concebíveis não está demonstrada; abaixo está o que é inexequível com as construções
encontradas.

| № | O que é inexequível | Afrouxamento mínimo | Recomendação do conselho |
|---|---|---|---|
| 1 | Proteger o consumidor sem equipamento sob conluio total dos verificadores: os casos honesto e falso lhe dão mensagens idênticas | A garantia é prometida apenas à parte que verifica sozinha; aos demais a resposta é mostrada com a marca «não verificado», e a grandeza do risco `R·q³` é declarada diretamente | Aceitar: isso já está registrado em D21, só é preciso transferi-lo para a descrição para o usuário |
| 2 | Verificar o passo de treinamento sob conluio total dentro de 20% | (a) pagar pelo resultado verificável, e não pelo passo; (b) admitir «ao menos um nó completo honesto»; (c) remover a referência de 20% para a rede pequena | (a): o único caminho com garantia rigorosa; com isso, parte da capacidade livre fica sem treinamento pago |
| 3 | Encaixar a resposta verificada em 5% com o `γ` medido = 1,52–1,78 | Considerar a referência de 5% um objetivo de engenharia, publicar o preço real e conduzir a redução de `γ` como tarefa separada | Aceitar; 5% é referência do roteiro, e não texto de R6 |
| 4 | Conter pela economia o sabotador que não precisa de lucro, com `p < 1` | Apenas as marcas e a proibição de usar o não verificado (D6) | Já aceito; não há novas medidas |
| 5 | Disputa sem depósito com fundo de disputas finito | Decidir se o pré-pagamento bloqueado do comprador é considerado depósito segundo R5 | Decidir após o cálculo M9 |
| 6 | Ter confiança total na decisão antes de quaisquer medições | Permitir uma lista limitada de medições das quais depende a escolha | Decisão do dono; o conselho nomeia duas medições da seção 4 e o experimento O5 |

Perguntas adicionais: pagar ou não pela resposta pulada pela moeda (seção 4, item 2); em que perfil se
calcula o preço da tarefa; admitir ou não o aval de terceiro.

## 7. O que calcular com mini-agentes e o que verificar por experimento

**Cálculos** (frações exatas, hash de controle, repetição em um segundo dispositivo; não são
experimentos sobre o protocolo):

1. M9 por todos os ramos do pedido avulso.
2. Ganho da falsificação «rascunho + passagem exata» sob os cortes em uma grade de `γ`, `ρ`, parcela
   de coincidência, comprimento do segmento e da resposta, margem.
3. Moeda com piso de frequência e parcela de pagadores preguiçosos, incluindo conta vazia.
4. Falsificação mista «tudo honesto, exceto uma coluna» e falsificação por interrupção da resposta.
5. Loteria: probabilidade exata de ruína ao longo do caminho e tamanho da reserva do comprador.
6. Tamanhos exatos da entrada da célula e do passo da disputa pela lista do perfil v2 (conferir 48 MiB
   e 64 KiB).
7. Inundação com novas chaves: carga sobre o pagador e derivação da cota de novas chaves.
8. Enumeração dos menores conjuntos falsos de células em um modelo pequeno.
9. Reunião de `ρ` e `γ` em uma mesma placa e comprimentos iguais; preço por um resultado verificado.

**Experimentos.** O O5 é permitido pela decisão D5. Os demais estão fora de D5 e exigem autorização do
dono:

1. Coincidência de tokens e atraso das avaliações do Q8_0 contra v2 — o primeiro experimento.
2. O5 — qualidade do perfil v2 em 320 tarefas.
3. Microbenchmark de núcleos de 8 bits com conferência bit a bit — verificação da estimativa de Ozaki.
4. `γ` e `ρ` em pares na mesma placa, incluindo RTX 4070 Laptop.
5. Tempo e memória da passagem e do segmento no processador do notebook e no telefone.
6. Preço da impressão do traço, cobertura do ABFT e frequência de falhas silenciosas.
7. Experimentos de treinamento O6 e O7 — separadamente, após a decisão sobre D18.

## 8. Quem fez o quê

- **ChatGPT:** dois trabalhos independentes e crítica de todos os trabalhos.
- **DeepSeek:** dois trabalhos independentes e crítica com recálculo dos números por aritmética exata.
- **Claude:** dois trabalhos independentes, a crítica e esta consolidação.
- **MiniMax:** cinco trabalhos independentes e crítica.
- **Gemini** não participou do conselho: não havia chave no hub de modelos; sua auditoria estava entre
  os dados de entrada.
- **Auditorias externas e mapas de mecanismos** — dados de entrada reunidos pelo dono; o conselho não
  os reconferiu com as fontes primárias.

Limitações da consolidação: o crítico ChatGPT analisou dez trabalhos dos onze; o crítico Claude leu um
dos trabalhos não por inteiro; os cálculos das críticas foram feitos, cada um, em um computador e
aguardam repetição pelos mini-agentes.
