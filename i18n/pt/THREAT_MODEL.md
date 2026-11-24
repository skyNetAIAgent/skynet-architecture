<!-- translation of docs/THREAT_MODEL.md, source sha256: 96c64b91168c36392f3f705d1ce619df7c73340c08bffee57773d75508990fff -->

# Modelo do adversário e tabela de ataques

[English](../../docs/THREAT_MODEL.en.md) · [中文](../zh/THREAT_MODEL.md) · [Español](../es/THREAT_MODEL.md) · [Français](../fr/THREAT_MODEL.md) · [Deutsch](../de/THREAT_MODEL.md) · [Italiano](../it/THREAT_MODEL.md) · [Русский](../../docs/THREAT_MODEL.md) · **Português** · [العربية](../ar/THREAT_MODEL.md)

Situação em 24 de novembro de 2026.

Este documento é o resultado do conselho de modelos para a etapa 1 do roteiro («Formulação precisa»,
[ROADMAP](ROADMAP.md), seção 4). Nele estão reunidos o modelo do adversário, a conferência do número
de ataques, o status de cada um dos 60 ataques da especificação para as variantes A e B, os novos
ataques encontrados pelo conselho e as questões que só o dono do projeto pode resolver.

**Status do documento.** É o resultado de raciocínio e de cálculo por fórmulas, não uma medição.
Não houve experimentos, execuções da rede nem recálculos de software para ele. Os números marcados
com [cálculo] foram obtidos por fórmulas nos trabalhos do conselho e verificados manualmente pelos
críticos; não foram repetidos em um segundo dispositivo. Só se torna decisão aceita o que o dono do
projeto aprovar. Todo o resto aqui é avaliação do conselho e, em caso de discordância, está indicado
«controverso».

**Como ler.** A seção 1 define quem ataca e o que conta como ganho. A seção 2 explica a divergência
entre 59 e 60. A seção 3 é a tabela principal: por ela, qualquer participante pode nomear um ataque
não fechado e conferir isso nos documentos de origem. A seção 4 é um resumo curto, a seção 5 são as
questões ao dono e a seção 6 é quem participou.

Documentos de origem: decisões D1–D5 em [ROADMAP](ROADMAP.md), seção 3; variantes A e B em
[CURRENT_DESIGN](CURRENT_DESIGN.md), seção 3; [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); primeira execução [FIRST_RUN](FIRST_RUN.md);
requisitos obrigatórios [REQUIREMENTS](REQUIREMENTS.md). A tabela de 60 ataques foi tirada
da especificação da rede sem coordenadores de 20 de novembro de 2026 (a seguir SPEC); os números das
linhas 1.1–7.4 são os dela.

---

## 1. Modelo do adversário

### 1.1. Notações e variantes

| Símbolo | Significado |
|---|---|
| `R`, `c` | Preço da tarefa e custo da execução honesta, `c ≤ R` |
| `H` | Valor pendente: recompensas ainda não vencidas da chave nos últimos três dias. Só se pode debitar dele (não há depósitos nem multas, requisito R5) |
| `p` | Parcela de verificação: em A `p = 4R/(R+H)`, mas não menor que 1%; em B é constante, por exemplo 1% |
| `B` | Débito em A: `B = 4R/p − R`, não maior que `H`; com `p > 1%` é `B = H`, caso contrário `B = 399R` |
| `k` | Número de verificadores da tarefa, 3 (nas rodadas de sorteio, em média 3,5–4,5) |
| `q`, `q_eff` | Parcela da coalizão em todo o peso dos verificadores do modelo e entre os que realmente verificam a tarefa (seção 1.7) |
| `G` | Preço total da disputa no registro |

**Variante A** (especificação atual): verificação por amostragem com débito de `H`; a entrega não
verificada e não contestada é paga. **Variante B** (proposta): só são pagas as tarefas escolhidas por
sorteio e confirmadas, ao preço `R/p`; o que não foi escolhido não é pago a ninguém; a falsificação
detectada queima todo o `H` da chave. B está descrita em esboço, e o conselho analisou «B como
descrita»: não há no texto o caminho do novato, a admissão de verificadores por `H`, a tarifa dos
verificadores nem a fonte de `R/p` para solicitações.

### 1.2. Quem ataca

Os perfis foram unificados a partir de todos os seis trabalhos. As combinações são obrigatórias:
coalizão com chaves gratuitas, locatário que se tornou coalizão, participante honesto por muito tempo
em conluio, usuário em conluio com os verificadores, sabotador com chaves gratuitas.

| Perfil | Do que dispõe | O que quer |
|---|---|---|
| Solitário | Suas chaves, seu dispositivo, programa alterado | Créditos sem trabalho ou acima do trabalho |
| Coalizão com parcela `q` | Chaves sob gestão comum; transferência instantânea de resultados, passos de cálculo, estados e solicitações; caixa comum | Passar uma falsificação, receber pagamento por verificações sem recálculo, ganhar votações |
| Dono de muitas chaves | Quantas chaves quiser, quase de graça; o peso e o `H` das chaves novas são zero | Filas, vagas de aprendiz, distribuição de dados, atribuições, bilhetes da B |
| Locatário de capacidade | Horas de GPU a preço de mercado, trabalho honesto e pago pela rede | Uma parcela do peso e, depois, conluio, modelo raro ou regras |
| Sabotador sem lucro | Disposto a perder todas as recompensas ainda não vencidas | O próprio dano: modelo, respostas, backdoor, parada |
| Participante com conta vazia | `H = 0`, sem peso | Qualquer pagamento sem trabalho |
| Honesto por muito tempo, depois sai | `H` e peso grandes; escolhe o momento, o tamanho e o número de ondas | Mais que `H` mais o pagamento honesto das últimas tarefas |
| Usuário | Sua solicitação, créditos, direito de disputa, conluio com o executor ou com os verificadores | Resposta grátis, reembolso por resposta correta, dados alheios |
| Operadores de retransmissores, pontos de encontro, nós de registro, pontos de acesso à blockchain, guardiões de dados | Veem endereços e horários, atrasam, não repassam, mostram um ambiente falso | Censura, isolamento do nó, revelação de identidade, pagamento por registros |
| Partes externas | Farol de aleatoriedade, produtor de bloco, fornecedores de pontos de verificação, fabricante do modo protegido, distribuidor do programa | Deslocar a amostragem, impor uma história ou um programa falso |
| Dono de dispositivos alheios | Chaves de trabalho roubadas ou infectadas | Confirmar falsificações, arriscando o `H` alheio |

### 1.3. O que o adversário pode e o que não pode

**Pode:** criar quantas chaves quiser; executar um programa alterado e ler tudo em seu dispositivo,
incluindo solicitações privadas no modo comum; transferir qualquer dado dentro da coalizão;
desligar-se, escolher o momento da entrega, calar-se, entregar dados a alguns nós e não a outros,
manter uma única cópia; alugar capacidade; votar e comprar votos; oferecer abertamente um suborno por
contrato inteligente (as confirmações ficam no registro, o pagamento pode ser executado sem
confiança); como produtor de bloco — não publicar o bloco e escolher um de dois valores de
aleatoriedade; controlar parte dos retransmissores e cercar o nó; ter ganho externo ou valorizar o
próprio dano.

**Não pode** (são suposições, é preciso declará-las diretamente): falsificar a assinatura de uma chave
alheia não roubada, encontrar uma colisão de hash, abrir um compromisso de duas maneiras, falsificar
o sorteio secreto (VRF); reescrever os blocos finais de uma blockchain pública, o registro não tem
chave de administrador e está correto (premissa 1 da SPEC; o programa não foi escrito); prever ou
deslocar a aleatoriedade depois da fixação do lote (premissa 2; as fontes não foram escolhidas; a
mistura protege contra previsão, mas não contra a manipulação pelo último fornecedor, N13); obter
coincidência bit a bit sem calcular (premissa 3; não verificado); alterar o resultado do recálculo da
etapa no registro (premissa 4; não construído para o modelo completo); alterar o programa de outro nó
(D4); debitar créditos disponíveis alheios, receber um segundo pagamento pelo mesmo número, revogar
um lote entregue.

**O que a rede não vê em princípio:** a quem pertencem as chaves e se os participantes são
independentes; se o nó entregou dados a outro; o que roda no computador alheio; em que o recálculo
difere de uma cópia do estado alheio. Se os casos honesto e falso dão ao nó os mesmos dados, nenhuma
regra os distingue ([OPEN_QUESTIONS](OPEN_QUESTIONS.md)).

### 1.4. Ganho do adversário e dano à rede

O ganho é calculado para toda a coalizão a partir de um mesmo estado inicial, com os mesmos direitos,
tarefas e horizonte até o acerto final, incluindo a saída. Somam-se os créditos vencidos, os
reembolsos, o valor do serviço recebido e dos novos direitos; subtraem-se os custos reais (trabalho,
energia, aluguel, gas, pagamentos externos). As transferências dentro da coalizão se anulam, um
crédito não é contado duas vezes, a perda da vítima por si só não é receita da coalizão. Tipos de
ganho: créditos por uma declaração falsa (falsificação, cópia, confirmação sem recálculo, linha
alheia); custos economizados com o mesmo pagamento; peso e lugares no sorteio; reembolso por uma
resposta correta ou parte não paga dos dados; ganho por efeito — influência sobre a resposta ou o
modelo, leitura da solicitação alheia, controle das regras, da emissão, do catálogo, do plano, o
próprio dano.

O dano à rede é calculado à parte, em suas próprias unidades: um resultado incorreto foi aceito; o
resultado foi usado antes da verificação; créditos foram emitidos sem trabalho; um honesto perdeu
`H`; pagamentos ou a entrada de novatos foram congelados; dados privados foram revelados; a história,
as regras, o programa ou a versão do modelo foram substituídos; a rede gastou trabalho em
verificações e disputas impostas. Dano sem ganho não viola D1, mas pode violar outros requisitos; na
tabela isso é «n/a» com o nome do requisito.

### 1.5. Registro formal de D1

D1 (aceito em 23 de novembro de 2026): «o fraudador não obtém o que deseja»; o ganho esperado com a
falsificação não é maior que zero em comparação com o trabalho honesto e com a inação, para qualquer
coalizão, inclusive um novato com conta vazia e qualquer número de chaves; um vazamento limitado e
positivo não satisfaz o critério.

Seja `U(σ)` a utilidade esperada da coalizão sob a estratégia `σ`. Para cada estratégia com declaração
falsa são necessárias **ambas** as desigualdades:

- `Δ₀ = E[U(σ) − U(inação)] ≤ 0` — cada declaração falsa é substituída pela recusa da tarefa (o `H₀`
  já ganho, com isso, vence);
- `Δч = E[U(σ) − U(trabalho honesto)] ≤ 0` — cada declaração falsa é substituída pela execução honesta.

O requisito vale para qualquer `q` de 0 a 1, com `H = 0` e qualquer número de chaves. Para refutá-lo
basta um estado admissível e uma diferença positiva. Não se pode comparar com a maior das duas bases:
com inação 0, ganho honesto 0,60 e declaração falsa 0,20, essa comparação dá «não há violação», embora
`Δ₀ = +0,20` [cálculo].

Um trabalho propôs dividir D1 em nível econômico (apenas créditos) e nível por efeito (influência sobre
a resposta e o modelo, leitura da solicitação, dano). O conselho não decide isso por conta própria: a
questão foi levada ao dono (seção 5, questão 1). Na tabela, o ganho apenas por efeito é marcado «não
(ef.)».

### 1.6. Princípio geral da coluna «dados para recusa»

Quando o executor está em conluio com todos os verificadores designados, o nó vê apenas dados
combinados: impressões digitais do resultado e do passo, estados revelados com provas de inclusão.
Todos eles são compatíveis com a falsificação. Permanecem verificáveis de forma independente apenas a
entrada e o modelo fixado, pelos quais o nó pode recalcular a tarefa por conta própria — cerca de
+100% de trabalho [cálculo]; nem A nem B exigem isso, e para uma solicitação privada um nó externo não
tem nem a entrada. Por isso, na tabela, muitas vezes está «não, exceto o recálculo completo».

### 1.7. Parcela de conluio `q_eff`

Todos os limiares do tipo «até 91%» se referem à parcela da coalizão entre os que realmente verificam
a tarefa. `q_eff` é a parcela da coalizão entre os verificadores que (1) foram admitidos à tarefa
(pela regra 2.6 da SPEC, na tarefa de um executor antigo é preciso `H_v ≥ B`, até `399R`),
(2) responderam dentro do prazo da rodada e (3) receberam os dados para a verificação. Exemplo
[cálculo]: 3.000 dispositivos domésticos honestos de 8 horas e 100 honestos de 24 horas contra 800
alugados de 24 horas. A parcela do adversário em todo o peso é 42,1% (19.200 de 45.600 horas de
dispositivo por dia); um dispositivo doméstico acumula cerca de `144R < 399R` e não é admitido às
tarefas de executores antigos; entre os admitidos, `q_eff = 800/900 = 88,9%`, `q_eff³ ≈ 0,70`.
Ressalva dos críticos: isso se aplica às tarefas com `B = 399R`. A condição (3) pode elevar `q_eff`
até um com qualquer parcela total (N2). A fórmula `q^k` só é válida para escolhas independentes; na
SPEC as rodadas vão até três respostas, e para um conluio parcial é preciso a distribuição dos que
responderam.

### 1.8. Fórmulas básicas [cálculo]

- **A, uma falsificação:** ganho `R − 4R(1 − q³)`; prejudicial com `q < 0,9086`. **Novato A:**
  `p = 1`, `B = H = 3R`, ganho `R(4q³ − 3)`.
- **A, saída com falsificações** (enumeração FIRST_RUN em um único dispositivo, não confirmada):
  vantajosa a partir de `q = 0,875` (quaisquer tamanhos, três ondas, regra «não mais de um terço de
  `H` em trabalho»; 1,00004·H₀ em 0,875, 1,034·H₀ em 0,880), a partir de 0,890 (tarefas idênticas), a
  partir de 0,800 sem a regra do terço; sem conluio, entre 92 milhões de estratégias não há saída
  vantajosa (o melhor é 0,980·H₀). Isso é uma enumeração de famílias, não uma prova.
- **B, uma falsificação** é vantajosa com `q^k > pH/(R + pH)`; com `p = 1%`, `k = 3`: `q ≈ 0,928` para
  `H = 400R`, `0,659` para `40R`, qualquer `q > 0` para `H = 0`. O pagamento bruto médio por
  falsificação é `R·q^k` e não depende de `p`.
- **B, onda de `N` falsificações:** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. A primeira
  falsificação é vantajosa com `H₀` abaixo de 2,8R / 14,3R / 52R / 105R / 269R para `q` = 0,3 / 0,5 /
  0,7 / 0,8 / 0,9. Com `H₀ = 0`, o maior ganho por chave é cerca de `q^k·R/(e·p·(1 − q^k))`: 0,037R /
  1,0R / 5,3R / 19R para `q` = 0,1 / 0,3 / 0,5 / 0,7. Uma onda sem enumeração é uma estimativa
  inferior.
- **Probabilidade de pagamento falso** por tarefa sem disputa externa: em A `1 − p + p·s`, em B `p·s`
  (`s` é a probabilidade de conluio total na escolha); com `p = 0,01`, `s = 0,125` — 0,99125 e
  0,00125, e o pagamento falso bruto com `R = 1` — 0,99125 e 0,125. Não se pode comparar as variantes
  apenas pela frequência de pagamento falso.

---

## 2. Conferência «60 e 59»

Na SPEC há exatamente 60 linhas (12 + 12 + 10 + 5 + 11 + 6 + 4): 18 fechadas, 6 prejudiciais, 19
limitadas, 16 abertas e **uma «não ataque» — a linha 1.9** (entregar um resultado correto calculado
em equipamento alheio é permitido pela decisão D2); o resumo do CURRENT_DESIGN, seção 9, e o
parágrafo «Em resumo» da SPEC somaram apenas quatro categorias e perderam a quinta, daí 59. Todos os
seis trabalhos e todos os três críticos chegaram a isso de forma independente. O registro correto:
60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Tabela de ataques

### 3.1. Notações

**Status:** fech. — o nó rejeita o ataque pelos dados do registro sob as premissas indicadas; prej. —
o ataque é possível e, em média, prejudicial até o limite indicado; lim. — é possível, mas o dano ou
o ganho é limitado por uma regra; aberto — não há solução; não é ataque.

**D1:** sim — o ganho não é maior que zero para qualquer coalizão; **não** — existe uma estratégia
com ganho positivo ao menos contra uma das bases; cond. — cumprido apenas sob as premissas
indicadas, que não dependem da parcela de conluio (premissas 1–4 da SPEC, ainda não construídas);
não (ef.) — não há ganho monetário ou ele não foi estabelecido, mas se alcança ganho por efeito
(seção 1.5); n/a — no ataque não há declaração falsa em busca de ganho, ficou afetado o requisito
indicado; ? — a regra não foi definida, o sinal do ganho não foi estabelecido.

**Dados** — por quais dados verificáveis de forma independente o nó rejeitará a declaração falsa em
caso de conluio do executor com todos os verificadores. «controverso» — os trabalhos ou críticos
divergiram e a disputa não foi resolvida. As referências «N…» levam aos novos ataques da seção 3.9.

### 3.2. Executor

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 1.1 | Novato com conta vazia entrega uma falsificação | prej. até `q ≈ 0,909`: as primeiras tarefas são sempre verificadas, ganho `R(4q³−3)`. Controverso: o crítico ChatGPT considera a linha aberta, pois os `3R` iniciais podem ser obtidos por cópia (2.2, N1) | **não** com `q ≥ 0,909` e, para qualquer `q > 0`, por meio do pagamento das reverificações de aprendiz | aberto: `R·q^k` por tentativa sem perdas, chaves quantas quiser | **não** para qualquer `q > 0` | Não, exceto o recálculo completo pela entrada aberta; para uma solicitação — só com o usuário | Verificar os primeiros resultados pagos de um modo que cada nó executa por conta própria; até então — apenas trabalho não pago. Em B — admissão por `H` (N16) |
| 1.2 | Participante antigo falsifica parte das tarefas | prej. até `q ≈ 0,909`; 99% das falsificações não são verificadas e permanecem na rede | **não** com `q` alto | prej. com `q^k R < p(1−q^k)H`: 0,928 com `H = 400R`, 0,659 com `40R`, qualquer `q` com `H = 0` ou a partir de uma chave vazia (N16) | **não** | Não, exceto o recálculo completo | Verificação do resultado pago que não dependa da parcela de conluio (etapa 4). Em B — `p` e admissão em função de `H` |
| 1.3 | Honesto por muito tempo, depois grande fraude e saída | prej. apenas nas famílias enumeradas abaixo de 0,875 / 0,890 / 0,800 (seção 1.8) | **não** com `q ≥ 0,875`; abaixo disso não está provado | aberto: a campanha de saída não foi calculada; com `H` pequeno é vantajoso para qualquer `q > 0` | **não** | Não, exceto o recálculo | Prova para todas as estratégias em A; cálculo da campanha de saída em B, incluindo `H₀ = 0` (etapa 2) |
| 1.4 | Entrega uma falsificação e desaparece ao ver a amostra | fech.: o lote não é revogado, o desaparecimento após a amostragem é resultado incorreto | cond. | o mesmo | cond. | A linha do lote e a ausência de revelação até o prazo | Uma falha de comunicação honesta é indistinguível (custo para os honestos); para uma solicitação privada — a disponibilidade da entrada |
| 1.5 | Descobre ou manipula a amostra com antecedência | aberto hoje: fechado apenas sob a premissa 2, e as fontes não foram escolhidas (assim avaliaram os trabalhos ChatGPT; os críticos Claude e ChatGPT concordam) | cond.; **não** com a manipulação pelo último fornecedor (N13) | o mesmo | o mesmo | Valores públicos do farol e do bloco; o conluio do limiar do farol ou a retenção do bloco não são visíveis por eles | Escolher as fontes; a rodada do farol estritamente depois da aceitação final do bloco; registrar a confiança nas partes externas como suposição |
| 1.6 | Pagamento duplo ou tarefa alheia | lim.: o número é único, mas a linha com tarefa alheia o registro só rejeita por objeção; se o executor está desligado durante toda a janela, a linha vence. Confirmaram todos os três críticos | **não**: pagamento de `R` a uma chave alheia | o mesmo | **não** | A atribuição é computável se a lista dos admitidos ao sorteio estiver no registro | O registro verifica a atribuição por conta própria no recebimento da linha (barato) |
| 1.7 | Atribui tarefas a si mesmo, inventa trabalho | aberto: o executor é escolhido por sorteio (essa parte está fechada), mas a regra de aprovação do plano de treinamento não foi aceita (ROADMAP, «O que não foi resolvido», item 5); a repetição de conteúdo gera vários pagamentos (N22). Crítico DeepSeek: «fechado para um plano fixo, aberto para o plano» | **não** | o mesmo | **não** | O nó verifica que a tarefa está no plano; o direito de emissão e a não repetição — não | Regra do plano no núcleo imutável; emissão apenas pelo lugar permitido do plano; crédito uma única vez pelo conteúdo |
| 1.8 | Pega as tarefas vantajosas, abandona as demais | lim.: o que foi abandonado vai para outro | sim com custos iguais; controvertido se um pequeno ganho da seleção com custos desiguais viola D1 | lim.; a seleção após o sorteio é impossível | o mesmo | Atribuição e prazo no registro | Custo igual das tarefas; a cota diminui após os abandonos |
| 1.9 | Resultado calculado em equipamento alheio | não é ataque (D2) | n/a | não é ataque | n/a | — | Distinguir da entrega repetida do mesmo resultado (N1, N22) |
| 1.10 | Arrasta a disputa ou se cala | lim.: o silêncio é derrota; com `H` pequeno, a rede paga a diferença de custos da disputa | n/a; controvertido com disputa cara (N3) | lim.; `H` muitas vezes é próximo de zero | o mesmo | Cronômetros das jogadas no registro | Prazos das jogadas; orçamento do preço da disputa |
| 1.11 | Falsificações antes da parada da rede | fech.: a janela não corre enquanto a rede está parada; o limiar não foi escolhido | cond. | o mesmo | cond. | O tempo da janela pelos lotes com parcela de peso não inferior ao limiar | Escolher o limiar (3.10); guardar as linhas durante a parada (N7) |
| 1.12 | Esconde a falsificação, não entregando os dados | aberto para dados grandes: o registro não vê «deu ou não deu»; para o treinamento é preciso o estado da etapa anterior | **não** | aberto; não pago, mas já utilizado | **não** | Para dados pequenos — publicação na blockchain; para grandes — não | Disponibilidade dos dados antes do sorteio; «sem dados até o prazo — incorreto» também para o estado de treinamento (N2, M3) |

### 3.3. Verificador

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 2.1 | Confirma sem recalcular | Controverso. fech. para um verificador fora da coalizão (quatro trabalhos, críticos Claude e DeepSeek); aberto segundo a avaliação dos trabalhos ChatGPT e do crítico ChatGPT: dentro da coalizão os mesmos dados são compatíveis com a ausência de recálculo | sim para um não vinculado; dentro da coalizão — 2.2 | o mesmo | o mesmo | Seu estado em um ponto aleatório e prova de inclusão; a origem do cálculo não é verificável | Não publicar estados intermediários em nome da disponibilidade (N11) |
| 2.2 | Pagamento da verificação do próprio grupo sem recálculo | lim.: cerca de 0,3% da renda com 10% de peso [cálculo: 0,01·3·0,1] | **não** para qualquer `q > 0`: economia de recálculo (cinco trabalhos, todos os três críticos) | lim., se a verificação em B é paga como em A (a tarifa não foi definida) | **não** com o mesmo pagamento | Não: recálculo e cópia dão os mesmos dados | Não pagar pela repetição; a correção «pagar da recompensa da tarefa verificada» não zera o ganho (seção 4.5) |
| 2.3 | Conluio do executor com todos os verificadores | prej. até `q_eff ≈ 0,909` (saída — 0,875) | **não** | prej. pela fórmula da seção 1.8 | **não** | Não, exceto o recálculo completo; solicitação privada — só com o usuário | Verificação que não dependa da parcela de conluio (etapa 4), ou enfraquecimento explícito de D1 (questão 2) |
| 2.4 | Suborno ou pressão após a amostragem | aberto: o verificador da solicitação se revela ao executor; suborno por contrato (N4); com M1 o subornado não arrisca nada. A queda foi confirmada por todos os três críticos | **não** | o mesmo; com `H = 0` o suborno é mais barato | **não** | Não | Solicitação aos verificadores sem contato com o executor; consequências da não revelação (M1) |
| 2.5 | Um grupo responde primeiro e ocupa as vagas | fech.: contam todas as respostas dentro do prazo; o prazo não foi escolhido | cond. | o mesmo | cond. | Horário das respostas no registro | Prazo da rodada não menor que o ciclo diário; considerar o crescimento de `q_eff` |
| 2.6 | Conta com peso e sem `H` confirma falsificações | fech.: admissão apenas com `H_v ≥ B`; efeito colateral — crescimento de `q_eff` (N5) | sim | aberto: não há regra de admissão em B | **não**: a coalizão recebe `R/p` sem risco | `H` do verificador no registro (em A) | Uma medida própria de responsabilidade do verificador em B |
| 2.7 | Acusa falsamente um executor honesto | fech. sob a premissa 4 (não construída) | cond. | o mesmo | cond. | Recálculo da etapa no registro | Máquina de referência do modelo completo; reembolso por tempo limite — 2.8, 4.2 |
| 2.8 | Acusa um executor desligado | lim.: para uma solicitação privada não há defensor, queima-se o `H` do honesto | **não** para a combinação «usuário + verificadores» (reembolso por uma resposta correta recebida); n/a para pura sabotagem | o mesmo | o mesmo | Para o treinamento, qualquer um defende pela entrada aberta; para uma solicitação privada não há dados | Cópia da solicitação disponível ao defensor sem revelação |
| 2.9 | Fluxo de disputas falsas | lim. pelo custo do `H` do atacante | n/a (verificação barata) | lim.; em B `H` muitas vezes é 0 | n/a | Resultado da disputa no registro | Resolver a contradição N23 |
| 2.10 | Interceptação da descoberta alheia | aberto: a ordem não foi trabalhada | **não**: parcela do debitado para o interceptador | aberto; o prêmio em B não foi definido | ? | Objeção oculta `hash(descoberta ‖ chave)` com marca do bloco | Entrega oculta com revelação e vínculo à chave (barato); atesta a prioridade da fixação, não o momento da abertura |
| 2.11 | Denuncia a própria falsificação em troca de uma parte do débito | fech. para a tarefa escolhida; a autodenúncia isolada é prejudicial | sim | o prêmio em B não foi definido | ? | O registro não paga ao descobridor antes do fim da verificação designada | Regra de prêmio para B |
| 2.12 | Recusa verificações | lim.: o sorteio passa para a rodada seguinte | n/a; controvertido: com `G > B` é mais vantajoso para o discordante calar-se (N3), depende do orçamento `G` | o mesmo | o mesmo | — | Orçamento `G`; consequências da ausência sem depósitos |

### 3.4. Conjunto de contas, peso e votações

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 3.1 | Milhares de contas | fech. para o peso e os votos; lim. no conjunto: os pagamentos de aprendiz, a distribuição e as atribuições crescem com o número de chaves (críticos Claude e DeepSeek). Crítico ChatGPT: o número de tentativas pagas depende dos lugares atribuídos, não dos registros | **não** | aberto: cada chave com atribuição é um bilhete com esperança `R·q^k` | **não** | Não há dados que vinculem as chaves | Entrada sem pagamentos até a verificação independente; em B — admissão por `H` (N16) |
| 3.2 | Inflação do peso com falsificações ou solicitações a si mesmo | prej. até o limiar; falsificações não verificadas que passaram pela janela recebem peso | **não** na fronteira | aberto: com `H = 0`, a falsificação escolhida dá peso quase de graça | **não** | Não, exceto o recálculo | Peso apenas pelo verificado de forma independente; conciliar «passou pela janela» (SPEC) e «passou pela verificação» (CURRENT_DESIGN) |
| 3.3 | Aluga capacidade e acumula peso honestamente | aberto em uma rede pequena: para ¾ do peso — um mês e meio com o triplo do trabalho dos demais, para 91% — dez vezes mais [cálculo da SPEC] | n/a (o aluguel é permitido por D2); leva a 2.3 e 3.7 | o mesmo | n/a | Não: o trabalho é honesto | Verificação que não dependa da parcela de peso; núcleo imutável (D4) |
| 3.4 | Tarefas grandes que só ele mesmo verificará | fech. pela regra do tamanho pequeno igual; a captura das tarefas pequenas do modelo raro — linha 3.5 | sim | o mesmo | sim | O tamanho da tarefa é regra do núcleo | — |
| 3.5 | Captura das verificações do modelo raro | aberto: `q_eff ≈ 1` é alcançável | **não** | o mesmo | **não** | Não | Não pagar pelo modelo sem um limiar de verificadores independentes em outro equipamento |
| 3.6 | Contas vazias nas vagas de aprendiz | aberto: fila de novatos honestos; pagamento do aprendiz pela cópia (2.2) | **não** por meio da cópia; n/a para a fila | aberto; o orçamento de vagas fica com quem tem mais chaves | **não** | Não | Não pagar pela reverificação de aprendiz; prazo de liberação da vaga (N28) |
| 3.7 | ¾ do peso mudam as regras a seu favor | Controverso. Críticos Claude e DeepSeek: aberto — D4 protege o núcleo de verificação, mas não a emissão, a aposta, a cobrança, o freio e o catálogo. Crítico ChatGPT: lim. — D4 tem prioridade sobre a SPEC antiga, o lucro exige uma mudança concreta | **não** (captura da emissão), controvertido | o mesmo | o mesmo | Impressão digital do núcleo: o nó recusa uma versão que altere o núcleo | Enumerar a composição do núcleo (questão 5) |
| 3.8 | Bloqueia decisões (½ — modelo, ¼ — regras) | lim.: reversível, mas o erro não se corrige | n/a (resiliência) | o mesmo | n/a | — | — |
| 3.9 | Compra votos | lim.: é preciso ¾ de todo o peso; o contrato executa o suborno | como 3.7: **não**, se a maioria altera a emissão; controvertido | o mesmo | o mesmo | Não | Como 3.7 |
| 3.10 | Deixa de entregar lotes para congelar a janela | aberto: limiar alto — congelamento dos pagamentos; baixo — a coalizão mantém a janela com seus lotes, as falsificações vencem (N14) | **não** (ramo do limiar baixo) | o mesmo; a falsificação escolhida recebe `R/p` | **não** | Tempo e parcelas de peso dos lotes | Limiar com prova dos dois lados; distinguir o peso ativo da rede e a composição dos verificadores |

### 3.5. Usuário

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 4.1 | Não paga pela resposta, gasta os créditos duas vezes | lim. por uma parte da resposta; o gasto duplo está fechado | **não**: a parte não paga é um vazamento positivo (questão 3) | o mesmo | **não** | Fixação dos créditos; o registro não vê a transferência de uma parte | A troca honesta sem uma parte confiável é impossível no caso geral: reduzir a parte ou reconhecer a suposição |
| 4.2 | Contesta uma resposta correta para obter reembolso | aberto por dois caminhos: a disputa se encerra pela coincidência dos verificadores sorteados (N17); reembolso por tempo limite com o executor desligado. A avaliação «fechado» em três trabalhos foi considerada exagerada por todos os três críticos | **não** | o mesmo | **não** | Recálculo no registro — só se a disputa chegou até ele | Direito de levar a disputa até o recálculo; regra de tempo limite; defensor com os dados |
| 4.3 | Usuário e executor emitem créditos com solicitações | fech.: as solicitações não emitem créditos | sim | fech., se `R/p` é pago apenas com os pagamentos dos usuários; a fonte não está registrada | cond. | Regra de emissão | Registrar a fonte de `R/p` em B (questão 12) |
| 4.4 | Sobrecarrega a rede com solicitações | lim. pela carteira | n/a | o mesmo | n/a | — | — |
| 4.5 | Copia o modelo e atende fora da rede | aberto na contagem da SPEC (faz parte das 16) | n/a: risco para a demanda | o mesmo | n/a | — | — |

### 3.6. Registro, programa e comunicação

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 5.1 | Reescreve a história ou as contas | fech. sob a premissa 1 | cond. | o mesmo | cond. | Blocos finais por pontos independentes | Verificação formal do programa do registro |
| 5.2 | O nó de registro não repassa ou distorce registros | lim. para a censura (o próprio registro custa moedas da blockchain, inacessível a uma conta vazia); aberto para uma linha com preço ou destinatário incorreto sem objeção (críticos DeepSeek e ChatGPT) | **não** | o mesmo | **não** | O preço e o destinatário são verificáveis, mas hoje só por objeção | Verificação da linha no recebimento; reembolso de registros sem emissão (N12) |
| 5.3 | Programa falso para o novato | aberto: endereço e referência da mesma fonte | n/a (autenticidade) | o mesmo | n/a | Não antes da primeira instalação | Fontes independentes do endereço e da impressão digital; compilação reproduzível |
| 5.4 | Atualização maliciosa | lim.: D4 permite recusar uma impressão digital alheia do núcleo; não há compilação reproduzível do programa do nó, por isso o «fechado» da SPEC não se sustenta; para o restante do programa — aberto | n/a | o mesmo | n/a | Impressão digital no registro sem vínculo verificável com o código-fonte | Compilação reproduzível; a coincidência com o texto aprovado não prova sua segurança |
| 5.5 | Pagamento de armazenamento inexistente ou entrega a si mesmo | fech.: nada é emitido pelo armazenamento | sim | o mesmo | sim | Regra de emissão | — |
| 5.6 | Recebe o pagamento, não entrega os dados | lim. por uma parte | **não**: vazamento de uma parte no lado do recebedor sem recibo (questão 3) | o mesmo | **não** | Impressão digital da parte; o recibo confirma o pagamento, não a entrega | Como 4.1 |
| 5.7 | Bloqueia todos os caminhos de encontro | aberto com o bloqueio de todos os caminhos | n/a (descentralização) | o mesmo | n/a | — | — |
| 5.8 | Cerca o nó com um estado falso | lim. pela confiança em dois de três fornecedores; com o conluio deles — aberto (N29) | cond. | o mesmo | cond. | Bloco final por pontos independentes | Cliente leve com verificação de consenso |
| 5.9 | Divide a rede para obter dois pagamentos | fech.: um único registro | sim | o mesmo | sim | O número da tarefa em um único registro | Rachadura das regras — N15 |
| 5.10 | Rouba uma chave de trabalho | lim.: a chave não gasta os créditos da carteira | Controverso: n/a (dano à vítima) ou **não** — chaves roubadas confirmam falsificações às custas do `H` alheio (N9, apoiado pelo crítico Claude) | o mesmo | o mesmo | A assinatura não mostra o operador | Revogação da chave; armazenamento em hardware |
| 5.11 | Esgota a distribuição gratuita | aberto: se bastará para os novatos, não verificado | n/a (negação de serviço); controvertido se o benefício é definido para «quem chega pela primeira vez» | o mesmo | o mesmo | O novo dono é indistinguível de uma nova chave do anterior | Distribuição apenas por tarefas já atribuídas |

### 3.7. Modelo e treinamento

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 6.1 | O sabotador entrega contribuições incorretas | lim.: cerca de `x/3` das contribuições com parcela de trabalho `x` [cálculo da SPEC]; com conluio total não está provado; a contribuição age imediatamente (N21) | n/a quanto aos créditos; não (ef.) | aberto: a falsificação não escolhida é gratuita, o limite `x/3` não vale (críticos Claude e ChatGPT) | **não** | Não, exceto o recálculo | Promover apenas contribuições verificadas (custo — atraso e memória) |
| 6.2 | Comportamento oculto | aberto: o exame detecta degradação, não o backdoor | não (ef.) | o mesmo | não (ef.) | Não; o backdoor é possível até com a etapa correta | Tarefa de pesquisa |
| 6.3 | Conjunto de dados malicioso ou licença alheia | aberto: um cálculo correto sobre dados maliciosos não se corrige | n/a; não (ef.) | o mesmo | o mesmo | Não: o hash e a inscrição são iguais para o titular e para o terceiro | Limitar o catálogo a fontes verificáveis |
| 6.4 | Ajuste ao exame | lim.: as tarefas são escolhidas após a fixação | não (ef.) dentro do não mensurável | o mesmo | o mesmo | Momento da escolha das tarefas | — |
| 6.5 | Falsificação dos resultados do exame | prej. até o limiar 2.3; o exame é verificado sempre, sem loteria | **não** com `q` alto | como em A; a fórmula `R·q^k` não se aplica ao exame (seção 4.5) | **não** | O exame é pequeno e aberto: cada nó pode recalculá-lo por conta própria | Recálculo do exame por cada nó (recomendado pelo crítico DeepSeek; crítico ChatGPT: o preço e a obrigatoriedade não foram estabelecidos) |
| 6.6 | Captura da votação sobre o plano | lim.: propriedade do esquema | n/a; **não** em combinação com 1.7 | o mesmo | o mesmo | Não | Ver 1.7 |

### 3.8. Confidencialidade

| № | Resumo | A | D1 em A | B | D1 em B | Dados para recusa em caso de conluio | O que é preciso para fechar |
|---|---|---|---|---|---|---|---|
| 7.1 | O dono do dispositivo lê as solicitações | aberto no modo comum | n/a; não (ef.) — a privacidade foi violada | o mesmo | o mesmo | Não | Modo protegido ao custo da confiança no fabricante (N25) |
| 7.2 | Coleta em massa de solicitações alheias | lim. pela parcela de atribuições e de vagas de verificação | n/a; não (ef.) | o mesmo | o mesmo | — | — |
| 7.3 | Vinculação das solicitações do usuário | aberto: pseudônimo e endereços no retransmissor | n/a | o mesmo | n/a | — | Pagamento não vinculável |
| 7.4 | Leitura da solicitação por meio da verificação ou da disputa | aberto: cerca de 1% das solicitações são vistas por mais três dispositivos; uma disputa falsa publica um fragmento | n/a; não (ef.) | o mesmo; a parcela `p` não limita a revelação — a disputa é aberta pelo usuário | o mesmo | — | Disputa sem revelação (prova de conhecimento zero da etapa) |

### 3.9. Novos ataques encontrados pelo conselho

As duplicatas de trabalhos diferentes foram unificadas. «Trabalhos» — quantos dos seis trabalhos da
rodada 1 destacaram o ataque; «Críticos» — a conclusão da rodada 2. Os números N1… são próprios deste
documento e não coincidem com os números locais nos trabalhos. Não há novos ataques refutados; onde a
justificativa foi refutada, isso é dito.

| № | Ataque | Trabalhos | Críticos | A · D1 | B · D1 | O que é preciso para fechar |
|---|---|---|---|---|---|---|
| N1 | **Um cálculo — muitos pagamentos.** Uma chave da coalizão recalcula uma vez a tarefa alheia (mesmo honesta) e distribui o passo a todas as suas chaves sorteadas como verificadoras ou aprendizes para essa tarefa. Generaliza 2.2: não é preciso conluio com o executor | 1 | Confirmaram todos os três; o ganho cresce com o número de vagas pagas atribuídas, não de chaves | aberto · **não** | aberto · **não** | Não há dados. Nenhum pagamento deve depender da repetição de trabalho já feito |
| N2 | **Fome de dados dos verificadores honestos.** O verificador pega a solicitação com o executor e se revela; o executor da coalizão entrega a solicitação apenas aos seus; o honesto que «não recebeu» não responde e não perde nada; as rodadas continuam até se reunirem três respostas da coalizão | 1 (parcialmente mais 3) | Correto com ressalva: são necessárias cerca de `3/(λ·q)` rodadas diárias — cerca de 15 dias com `q = 5%`, `λ ≈ 4`, cerca de 75 dias com `q = 1%` [cálculo], o ataque é notável pelo registro. O mecanismo «publicação de cópia criptografada» é citado na SPEC, mas não definido. Para o treinamento — apenas com uma única cópia da entrada | aberto · **não** para solicitações | aberto · **não** | O registro não vê a transferência. Disponibilidade das entradas antes do sorteio; para uma solicitação privada não há solução; ver M3 |
| N3 | **A disputa custa mais que a aposta.** O jogo da disputa no piloto — 93 transações, 5,8–6,3 milhões de gas: cerca de US$ 18 com 1 gwei e US$ 3.000 por ETH, cerca de US$ 360 com 20 gwei [cálculo; os preços são suposições]. A repetição da linha — 14,1 milhões de gas, outro protótipo, não se pode somar | 1 (adjacente mais 3) | Correto como dilema, os números são condicionais: ou o lado certo arca com `G − B`, e o honesto discordante se cala; ou a rede reembolsa `G` (assim se lê 1.10 da SPEC), e o sabotador obriga a rede a pagar `G` por cada falsificação detectada | aberto · **não** | aberto · **não** | Orçamento `G` para a cadeia escolhida; tarefas cujo erro exige disputa — apenas com `H ≥ G` |
| N4 | **Suborno «P+ε»:** o contrato paga ao verificador ε pela confirmação e promete reembolsar `H_v` em caso de detecção. Subtipo de 2.4 | 1 | Crítico DeepSeek: substancial; crítico ChatGPT: a exequibilidade e o equilíbrio não estão provados | aberto · **não** | aberto · **não** | Verificação em que a concordância não decide nada; ver M1 |
| N5 | **Crescimento de `q_eff` pela admissão `H_v ≥ B`:** 42,1% do peso total dão 88,9% entre os admitidos (seção 1.7) | 2 | Confirmado; apenas para tarefas com `B = 399R` | lim. · **não** com captura | aberto (2.6) | Calcular os limites por `q_eff`; calcular o compromisso entre o tamanho do débito e a largura da rodada |
| N6 | **O peso desaparece após 30 dias corridos de parada:** a janela para, o peso é contado «em 30 dias»; o primeiro grupo que retorna recebe todo o peso | 1 | Correto pela letra da SPEC, mas condicional: não se diz se é tempo corrido ou ativo; com peso zero de todos, o sorteio não está definido | aberto · **não** | aberto · **não** | Contar o peso pelo tempo ativo da rede (barato) e definir o crédito inicial |
| N7 | **As linhas dos lotes vivem cerca de 18 dias, a janela pode ficar parada mais tempo:** após a parada resta uma raiz sem linhas, não há com que contestar | 3 | Confirmaram todos | aberto · ? | aberto · ? | Guardar as linhas e as bases das transições por todo o prazo de verificação e disputa; sem dados, o lançamento em disputa espera |
| N8 | **O próprio modelo no catálogo dá `q = 1`:** um modelo que só o equipamento da coalizão executa | 1 | Crítico ChatGPT: é uma combinação de 1.7, 3.5 e 6.6; não está provado que uma pequena parcela de peso leve o modelo ao catálogo | aberto · **não** | aberto · **não** | Não pagar pelo modelo sem uma rodada mínima de verificadores em outro equipamento |
| N9 | **Dispositivos alheios como peso gratuito de verificadores:** chaves de trabalho roubadas confirmam falsificações, queima-se o `H` das vítimas. Extensão de 5.10 | 1 | Confirmado; o aumento de `q` — pelo peso das chaves capturadas, não pelo número de dispositivos | aberto · **não** | aberto · **não** | Armazenamento da chave em hardware; considerar a invasão no `q` admissível |
| N10 | **A entrega instantânea de falsificações aumenta o fluxo de atribuições** (B) | 1 | Condicional: o crescimento de 10–100 vezes não decorre das regras da SPEC | lim. · sim | aberto · **não** | Ritmo de atribuições apenas pelo trabalho verificado |
| N11 | **Disponibilidade contra 2.1:** a publicação de estados intermediários em nome de N2 permite confirmar sem recálculo | 1 | Limitação de uma mudança proposta, não um ataque autônomo | — | — | Publicar apenas as entradas; os intermediários — na disputa |
| N12 | **Cobrança pelo registro no livro acima dos custos:** reembolso de registros de lixo ou cartel de nós de registro | 2 | A regra de reembolso não está definida na SPEC; a renda normal do intermediário não viola D1 | aberto · cond. | aberto · cond. | Reembolsar apenas registros com resultados aceitos e não acima da comissão real |
| N13 | **Manipulação pelo último fornecedor de aleatoriedade:** se a rodada do farol é conhecida antes do bloco decisivo, seu produtor escolhe entre dois valores; em A `p → p²`, ganho de cerca de +0,96R por falsificação [cálculo]. Crítico Claude: com o cronograma dos produtores conhecido de antemão, a coalizão entrega lotes sob seus próprios blocos | 4 | Confirmaram todos; os números valem apenas com a ordem errada das fontes | aberto · **não** com a ordem errada | o mesmo | Rodada do farol estritamente após a aceitação final do bloco |
| N14 | **A janela corre sem maioria:** coalizão de 40%, o desligamento de metade dos honestos lhe dá 40/70 = 57% entre os ativos [cálculo]. Subtipo de 3.10 | 2 | Confirmado como subtipo de 3.10 | prej. · **não** para vazamentos do tipo B | aberto · **não** | Ver 3.10 |
| N15 | **Rachadura das regras:** valores ainda não vencidos vencem nos dois ramos | 1 | Condicional: a duplicação de um compromisso não está provada | aberto · ? | aberto · ? | Contrato separado com separação dos saldos |
| N16 | **Em B, a contenção está vinculada à chave, mas o acesso às tarefas não:** falsificações a partir de uma chave vazia separada dão `R·q^k` sem perdas. Raiz comum de 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + crítico Claude | Dois trabalhos justificaram o furo pelo fato de que um participante comum da B tem `H = 0` em 23,5–54,7% das janelas; esse argumento foi refutado (seção 4.5). A forma correta foi dada pelo crítico Claude | — | aberto · **não** | Admissão aos bilhetes com `H` não menor que o pagamento esperado pela falsificação; então B perde a parcela de verificação baixa constante (questão 8) |
| N17 | **A disputa do usuário é decidida pela amostra, não pela aritmética:** a disputa é encerrada se os verificadores sorteados coincidirem com o executor | 1 | Confirmaram os críticos Claude e DeepSeek; crítico ChatGPT: correto, mas 4.2 trata da pretensão oposta | aberto · **não** | aberto · **não** | Direito de levar a disputa ao recálculo no registro |
| N18 | **Falsificações → peso → `q`.** Extensão de 3.2 | 1 | Confirmado; a conclusão monetária exige considerar os pagamentos futuros | lim. · **não** na fronteira | aberto · **não** | Peso apenas pelo verificado de forma independente |
| N19 | **Lixo de chaves gratuitas antes da atribuição** sobrecarrega nós e filas | 4 | Confirmado; vagas para um novato honesto não são garantidas em nenhuma variante. A avaliação «o lixo custa à rede 3–4,5 de trabalho com custos quase nulos em A» foi refutada pelo crítico Claude | aberto · n/a | aberto · **não** em combinação com bilhetes gratuitos | Rejeitar mensagens sem atribuição antes do processamento caro; o caminho a partir de conta zero é obrigatório |
| N20 | **Divergência imposta das aritméticas** do executor e do árbitro | 2 | Confirmado; a divergência por si só não prova ganho | aberto · ? | aberto · ? | Semântica executável única das operações e verificação das implementações por uma referência |
| N21 | **Uso do resultado antes da verificação:** a resposta foi lida, a etapa foi tomada como etapa seguinte e permanece na linhagem do modelo | 5 (+1 em 6.1) | Confirmaram todos; o dano é possível até com `q = 0`; `1 − p` é a parcela não escolhida, não a aplicada | aberto · não (ef.) | aberto · não (ef.) | Verificar o bloco antes da entrega; promover apenas o descendente verificado (custo — atraso e memória) |
| N22 | **Um direito de emissão sob números diferentes** (execuções de teste idênticas, repetição da etapa após reinício) | 3 | Confirmado; dois pedidos legítimos podem ter a mesma saída | aberto · **não** | aberto · **não** | Crédito uma única vez pelo direito canônico ao lugar do plano |
| N23 | **Contradição das regras de disputa a partir de conta zero** (o ROADMAP exige, a SPEC não) | 1 | Confirmaram os críticos DeepSeek e ChatGPT | aberto · n/a | aberto · n/a | Decisão do dono (questão 4) |
| N24 | **Apropriação da tarefa de um executor desligado** — desdobramento de 1.6 | 2 | Confirmado | ver 1.6 | ver 1.6 | Verificação da atribuição no recebimento da linha |
| N25 | **Conluio com o fabricante do modo protegido** | 1 | Correto dentro de 7.1 | aberto · n/a | aberto · n/a | Registrar a suposição de confiança no fabricante |
| N26 | **Recibos falsos de transferência de dados** | 1 | Não há renda externa: a coalizão paga a si mesma | aberto · n/a | aberto · n/a | Não há indício da entrega de dados grandes |
| N27 | **Não entrega seletiva pelo retransmissor** | 1 | Confirmado quanto à disponibilidade | lim. · n/a | lim. · n/a | Vários retransmissores, caminhos alternativos |
| N28 | **«Aprendiz eterno»** ocupa a vaga e não conclui a reverificação (relacionado a 3.6) | 1 | Confirmado | aberto · n/a | aberto · n/a | Prazo e liberação automática da vaga |
| N29 | **Conluio de dois dos três fornecedores do ponto de verificação** (relacionado a 5.8) | 1 | Confirmado; «mais fornecedores» não resolve o conluio da maioria exigida | lim. · cond. | lim. · cond. | Cliente leve com verificação de consenso |
| N30 | **Ao usuário foi entregue um bloco diferente do fixado** | 1 | Confirmado | aberto · ? | aberto · ? | Vincular o bloco entregue a um compromisso e verificar antes do uso |
| N31 | **Erro comum no próprio núcleo** aceita uma transição incorreta em todos os nós | 1 | Confirmado; diferente de N20 | aberto · ? | aberto · ? | Especificação independente da transição; segundo D4, a correção só ocorre pela transição para uma nova rede |
| N32 | **Reconhecimento de uma solicitação privada curta pela impressão digital pública** | 2 | Confirmado condicionalmente: hash determinístico e um conjunto pequeno de textos | aberto · não (ef.) | o mesmo | Compromissos ocultadores com aleatoriedade fresca |

**Encontrados apenas pelos críticos** (não verificados pelos demais participantes):

| № | Ataque | Quem | A · D1 | B · D1 | O que é preciso para fechar |
|---|---|---|---|---|---|
| M1 | **Recusa gratuita de revelação.** Os verificadores da coalizão entregam um «confirmo» oculto e o revelam apenas se todas as respostas entregues forem dela; caso contrário, calam-se e não perdem nada. O suborno de um verificador externo torna-se sem risco: em vez do risco de `399R` — zero [cálculo]. Condição: se as respostas ocultas são visíveis antes da revelação — não está definido na SPEC | crítico Claude | aberto · **não** | aberto · **não** | Consequências da não revelação sem depósitos (perda do pagamento e do peso da rodada) ou ocultação do número e da autoria das respostas; o custo para os honestos desligados não foi calculado |
| M3 | **Carga pelo mecanismo de disponibilidade.** Se ao «não recebi» se responde com a publicação obrigatória de uma cópia, o verificador da coalizão sempre declara «não recebi»; com `q = 10%`, `λ ≈ 4` isso é cerca de 34% das tarefas escolhidas [cálculo] | crítico Claude | aberto · n/a | o mesmo | A declaração de não entrega deve custar ao declarante não menos que a publicação provocada (do seu `H`) |
| M4 | **Falha e fraude sob a mesma regra de débito:** a causa não se verifica por uma saída incorreta idêntica | crítico ChatGPT | ? | ? | Não foi apresentada uma regra justa para ambos os lados (questão 11) |

(M2 do crítico Claude é N16.)

---

## 4. Resultado

### 4.1. Quantos ataques violam D1

Contagem pela tabela das seções 3.2–3.8 [cálculo pela tabela]. As linhas marcadas «controverso» estão
incluídas e são nomeadas à parte.

| | Variante A | Variante B |
|---|---|---|
| Ganho monetário («**não**»), de 60 linhas | 24 (e mais 2 condicionalmente: 1.5 com a ordem errada das fontes, 6.6 em combinação com 1.7): 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25: as mesmas sem 2.10 (em B «?»), mais 2.6 e 6.1 (e as mesmas 2 condicionalmente) |
| Apenas ganho por efeito («não (ef.)») | 7: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6: as mesmas sem 6.1 |
| Novos ataques com «**não**» monetário (N1–N32, M1) | 14 | 16 |

As linhas controvertidas estão marcadas com asterisco (3.7, 3.9, 5.10). Sem elas, restam 21 em A e
22 em B. O número de linhas não pode ser somado como o número de modos independentes de fraude: um
mesmo esquema muitas vezes é descrito por várias linhas. A conclusão principal não depende da
contagem: **nem a variante A nem a variante B cumprem D1 na forma literal**, e todos os seis trabalhos
e todos os três críticos concordam com isso.

**Comparação entre A e B.** B, na forma descrita, é pior que A com `H` vazio e baixo quando
`0 < q < 0,909`: uma chave vazia recebe `R·q^k` por tentativa sem perdas (N16). Com `q = 0`, B é
melhor: a falsificação não escolhida não rende nada, mesmo com a saída. Com `q ≥ 0,909`, as duas
perdem. Se o caminho do novato de A for transferido para B (verificação completa das primeiras
tarefas), a diferença nas chaves vazias desaparece (`q^k R − (1 − q^k)·3R`, como em A [cálculo]), mas
B perde a parcela de verificação baixa constante. Isso é uma entrada para a decisão D3 na etapa 2, não
a decisão em si.

### 4.2. Críticos para o lançamento da rede com créditos reais

Resumo das avaliações dos trabalhos e dos críticos. Um início fechado com créditos de treinamento não
é bloqueado por esses pontos, exceto a privacidade, a recuperação (N6, N7) e os pontos sem os quais o
piloto não verifica o que deveria verificar (N2, N3).

1. **Conluio por `q_eff`:** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 e N5. Em ambas as variantes, a
   aceitação depende da concordância da amostra de participantes.
2. **Pagamento da repetição:** 2.2, 3.6, N1. Viola D1 para qualquer `q > 0`; não foi encontrada uma
   correção barata.
3. **Chaves vazias em B:** N16, 1.1-B, 3.1-B.
4. **Direito de emissão e destinatário:** 1.7, 1.6, 5.2, N22, e também 3.7 para a emissão fora do
   núcleo.
5. **Disponibilidade dos dados:** 1.12, N2, N7.
6. **Disputas:** 4.2 e N17; o preço da disputa N3, a ele ligada 2.12; a contradição N23; M1.
7. **Uso antes da verificação:** N21, 6.1, N30 (se o dono incluir o efeito em D1).
8. **Recuperação:** N6 (peso após a parada) e N7 (linhas dos lotes).
9. **Entrada e programa:** 5.3, 5.4, N19.
10. **Privacidade:** 7.1, 7.4, N32 — violam uma condição obrigatória independentemente do dinheiro.

### 4.3. Raiz comum

Em ambas as variantes, a aceitação comum do resultado depende da concordância de uma amostra aleatória
de participantes, isto é, de assinaturas que, em caso de conluio, não provam nada. Por isso o limite
da proteção sempre se expressa pela parcela de conluio `q_eff`, e `q_eff` pode ser elevado pelo
aluguel de capacidade, pela captura de um modelo raro, pela regra de admissão por `H` (N5), pela fome
de dados (N2), por chaves roubadas (N9) ou por uma longa parada (N6). Os dados verificáveis de forma
independente sob conluio total são apenas a entrada e o modelo, pelos quais o nó pode recalcular a
tarefa por conta própria; nem A nem B exigem isso, e para uma solicitação privada o nó não tem nem a
entrada. D1 só é alcançável por uma verificação que não dependa da parcela de conluio (etapa 4
[ROADMAP](ROADMAP.md)), ou por um enfraquecimento explícito de D1 para «com `q < q*`» por decisão do
dono.

### 4.4. Correções baratas confirmadas pelos críticos

| Correção | Fecha | Ressalva |
|---|---|---|
| O registro verifica por conta própria a atribuição, o preço e o destinatário da linha no recebimento, e não por objeção | 1.6, 5.2, N24 | A lista dos admitidos ao sorteio deve estar no registro |
| Crédito uma única vez pelo direito canônico ao lugar do plano e pela impressão digital do conteúdo | N22, parte de 1.7 | Dois pedidos legítimos podem dar a mesma saída; o furo principal de 1.7 — a regra do plano — permanece |
| Entrega oculta da objeção com revelação e vínculo à chave | 2.10 | Atesta a prioridade da fixação, não o momento da abertura |
| Contar o peso e a janela pelo tempo ativo da rede, não pelo calendário | N6 | É preciso uma regra de crédito inicial após a parada |
| Rodada do farol estritamente após a aceitação final do bloco | 1.5 (parte), N13 | As fontes ainda não foram escolhidas |
| Cada nó recalcula o exame por conta própria antes de aceitar a versão | 6.5 | Recomendado por um crítico; o preço e a obrigatoriedade ainda não foram estabelecidos |
| Corrigir o resumo do CURRENT_DESIGN: 60 = 18 + 6 + 19 + 16 + 1 | Conferência 59/60 | — |

### 4.5. Conclusões refutadas

Estas afirmações dos trabalhos da rodada 1 foram consideradas erradas pelos críticos; não foram
transferidas para a tabela.

| Afirmação | Onde | Por que está errado |
|---|---|---|
| Limiar de vantagem da falsificação em B `q^k > H/(H+R)` | um trabalho DeepSeek | Perdeu-se o fator `p`. O correto é `q^k > pH/(R+pH)`. Com `p = 1%`, `H = 400R`, `q = 0,95`: ganho `0,857R`, perda esperada `0,01·0,143·400R = 0,572R`, resultado +0,285R por falsificação, enquanto pela fórmula errada — prejuízo [cálculo]. O erro superestima a proteção quase até o total (0,999 em vez de 0,93) |
| O limiar de 90,9% do novato A «é válido sob a suposição de que os 3R foram acumulados por conluio» | o mesmo trabalho | O limiar não depende de como os `3R` foram obtidos |
| A falsificação do exame em B dá `R·q^k` | os dois trabalhos DeepSeek | O exame é verificado sempre, sem loteria; a fórmula da loteria não se aplica a ele |
| A correção 2.2 «pagar aos verificadores com a recompensa da tarefa verificada» zera o ganho | um trabalho Claude | Quem copia continua economizando o recálculo; contra a inação o ganho também é positivo; a correção não afeta a cópia em uma tarefa honesta alheia (N1). Ela remove apenas a emissão de créditos por uma verificação vazia |
| «Um participante comum da B tem `H = 0` em 23,5–54,7% das janelas, e nesse período a falsificação não ameaça nada» | os dois trabalhos Claude | Os números `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` estão corretos, mas é a parcela de janelas depois do fato. O `H` queima no momento da detecção, incluindo os ganhos vindos depois da entrega. A conclusão sobre o furo é correta por outro motivo — pela chave vazia (N16) |
| D1 é verificado comparando com a maior das duas bases | um trabalho Claude | Deixa passar o caso com ganho positivo contra a inação (exemplo na seção 1.5) |
| «O lixo custa à rede 3–4,5 de trabalho com custos quase nulos do atacante» (variante A) | um trabalho Claude | Em A a chave só recebe tarefas com `H ≥ 3R`, e cada resultado de lixo queima esses `3R`; não há amplificação múltipla. A amplificação existe apenas em B sem admissão por `H` |
| Status corrigidos na tabela: 2.6-B «fechada» (trabalhos DeepSeek e Claude); 1.7 «fechada / sim», 1.6 e 4.2 «fechadas / sim», 4.1 e 5.6 «D1 sim», 2.2 «não viola D1» (trabalhos DeepSeek, parcialmente Claude); 3.4 «não», 2.7 «aberta / não», 5.11 «não» (trabalhos ChatGPT) | vários | As justificativas estão nas linhas correspondentes da tabela: não há regra de admissão em B; a regra do plano está aberta; a verificação da atribuição e a disputa do usuário dão ganho; D1 proíbe vazamento limitado; o ganho em 3.4 e 2.7 foi tirado das linhas vizinhas; não há benefício pessoal na SPEC |
| 1.3: ganho de 1,034·H₀ no ponto 0,875 | um trabalho Claude | 1,034·H₀ se refere ao ponto 0,880; em 0,875 — 1,00004·H₀ |

Permanecem controvertidas (não refutadas) as avaliações 2.1 «aberta» nos dois trabalhos ChatGPT e 3.7
«limitada»: os críticos divergiram (linhas 2.1 e 3.7 da tabela).

---

## 5. Questões ao dono

Decisões sem as quais a etapa 1 não pode ser fechada. O conselho não as toma.

1. **O efeito entra em D1?** Um trabalho propôs distinguir D1 econômico (apenas créditos) e D1 por
   efeito (influência sobre a resposta e o modelo, leitura da solicitação, o próprio dano). As palavras
   «o fraudador não obtém o que deseja» no sentido literal incluem o efeito; então o uso do resultado
   antes da verificação (N21) viola D1 em ambas as variantes para qualquer `q`, e só se pode fechá-lo
   com verificação antes da entrega e da promoção (custo — atraso e memória).
2. **Exigir uma verificação que não dependa da parcela de conluio, ou enfraquecer D1 para «com
   `q < q*`»?** Sem uma das duas, D1 é inalcançável tanto em A como em B.
3. **Vazamento de uma parte na troca** (4.1, 5.6): a troca honesta sem uma parte confiável é
   impossível no caso geral. Reconhecê-lo como suposição explícita ou considerá-lo violação de D1?
4. **Disputa a partir de conta zero** (N23): o ROADMAP a exige, a SPEC não. Com o que, então, limitar
   o fluxo de disputas falsas sem depósitos?
5. **Composição do núcleo imutável** (3.7): entram nele a regra de emissão, a aposta, a cobrança da
   rede, o freio e o catálogo, ou apenas a verificação?
6. **Regra de aprovação do plano de treinamento** (1.7, ROADMAP «O que não foi resolvido», item 5):
   quem e como autoriza que uma tarefa emita créditos.
7. **Tempo para o peso e a janela** (N6): tempo corrido ou tempo ativo da rede.
8. **Admissão às tarefas em B** (N16): introduzir em B a dependência do acesso em relação a `H`,
   sabendo que então B perde a parcela de verificação baixa constante. Isso é uma entrada para D3.
9. **Preço da disputa** (N3): qual cadeia considerar para o orçamento `G` e quem arca com a diferença
   `G − B` — o lado certo ou a rede.
10. **Pagar ou não pela verificação repetida e pelas reverificações de aprendiz** (2.2, N1), se a
    cópia não se distingue do recálculo?
11. **Falha honesta de hardware:** debitar por ela da mesma forma que pela fraude.
12. **Fonte do pagamento `R/p` em B para solicitações** (4.3): apenas dos pagamentos dos usuários ou
    com emissão.

---

## 6. Quem fez o quê

O conselho de modelos trabalhou com os materiais do projeto, sem acesso à rede e sem experimentos.

- **Rodada 1, seis trabalhos independentes:** dois trabalhos ChatGPT, dois trabalhos DeepSeek, dois
  trabalhos Claude. Cada um elaborou o modelo do adversário, a conferência das 60 linhas, os status
  para as variantes A e B, os dados para recusa e novos ataques.
- **Rodada 2, três críticas:** uma de ChatGPT, uma de DeepSeek e uma de Claude. Cada crítico leu todos
  os seis trabalhos, conferiu as afirmações com os documentos de origem, recalculou as fórmulas
  manualmente e indicou divergências e erros.
- **Consolidação:** este documento foi elaborado por Claude a partir dos trabalhos e das críticas.
  Onde os críticos divergiram, na tabela está «controverso»; nenhuma avaliação nova própria foi
  adicionada na consolidação.
