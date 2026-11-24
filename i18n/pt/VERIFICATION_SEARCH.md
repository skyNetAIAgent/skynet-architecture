<!-- translation of docs/VERIFICATION_SEARCH.md, source sha256: cdf54a57e7747ae1f862b5b29fa7a53eee7fca80d8bae17a0cbc60f022cec00b -->

# Busca de uma verificação que não dependa da parcela de conluio

[English](../../docs/VERIFICATION_SEARCH.en.md) · [中文](../zh/VERIFICATION_SEARCH.md) · [Español](../es/VERIFICATION_SEARCH.md) · [Français](../fr/VERIFICATION_SEARCH.md) · [Deutsch](../de/VERIFICATION_SEARCH.md) · [Italiano](../it/VERIFICATION_SEARCH.md) · [Русский](../../docs/VERIFICATION_SEARCH.md) · **Português** · [العربية](../ar/VERIFICATION_SEARCH.md)

Situação em 24 de novembro de 2026.

Este documento é o resultado do conselho de modelos para a etapa 4 do roteiro («Busca de uma garantia
que não dependa da parcela de conluio», [ROADMAP](ROADMAP.md), seção 4). O conselho buscou uma
verificação que cada nó executa por conta própria, de modo que a concordância ou o conluio dos outros
verificadores não decida nada. A busca abrangeu dois tipos de trabalho: a resposta do modelo Qwen a uma
solicitação do usuário e o passo de treinamento.

**Status do documento.** É o resultado de raciocínio e de cálculo por fórmulas, não uma medição.
Não houve experimentos com o modelo, execuções da rede, sistemas de provas nem model checking para
ele. Os participantes e os críticos executaram apenas programas aritméticos curtos e pequenas
enumerações no processador; duas dessas enumerações dos trabalhos ChatGPT foram repetidas por dois
críticos, e os hashes de controle coincidiram. Os números marcados com [cálculo] foram obtidos por
fórmulas a partir de parâmetros nomeados explicitamente. Os participantes substituíram por conta
própria os parâmetros dos modelos e das placas de vídeo; nenhum trabalho os conferiu com a configuração
publicada do Qwen3.5-4B ou de um modelo com cerca de 27 bilhões de parâmetros. **São decisões aceitas
apenas as decisões D1–D25** em [ROADMAP](ROADMAP.md), seção 3. Todo o resto aqui é avaliação do
conselho. Onde os críticos divergiram, está «controverso».

**Como ler.** A seção 1 trata do que se busca e em que condições. A seção 2 trata do que foi provado
impossível e de quais afirmações de impossibilidade foram refutadas. As seções 3 e 4 analisam
mecanismos para a resposta do modelo e para o passo de treinamento, com o melhor candidato e suas
limitações. A seção 5 trata do que permaneceu não provado e de quais experimentos e cálculos o
resolverão. A seção 6 são as questões ao dono. A seção 7 é quem participou.

**Resumo curto.**

1. **Resposta do modelo.** Uma verificação que não dependa da parcela de conluio existe apenas onde o
   próprio pagador, cujo dinheiro está em jogo, verifica toda a resposta. O melhor candidato é o
   «PPS»: o pagador recalcula em uma única passagem a solicitação e a resposta pronta no perfil inteiro
   exato, o pagamento sai apenas do seu pré-pagamento, e a disputa por prova de erro é verificada por
   cada nó. O preço calculado é 1,2–3,8% do tempo de geração, mas apenas com geração de uma resposta
   por vez [cálculo]. O candidato não cobre o consumidor sem equipamento e depende de uma coincidência
   de bits não medida.
2. **Passo de treinamento.** Não foi encontrada uma verificação do próprio passo dentro de cerca de
   20%, independente da parcela de conluio. Todos os seis trabalhos e todas as três críticas concordam
   com isso.
3. **O único caminho sobrevivente para o treinamento** muda aquilo pelo que se paga: a rede paga
   pela melhoria comprovada do modelo em um exame escolhido após a fixação da atualização. Pela
   decisão D18, esse caminho é investigado como candidato a uma nova unidade de pagamento, mas ainda
   não foi aceito; são necessários cálculos, um experimento e as correções encontradas pelos críticos.
4. **Decidem o experimento D5** (coincidência de bits do Qwen3.5-4B inteiro em duas placas de vídeo e
   entre dois modos de cálculo, tempo, qualidade) **e os cálculos dos mini-agentes** da seção 5.3; com
   base neles se toma a decisão final sobre o pagamento do treinamento (D18).

Documentos de origem: decisões D1–D17 e etapa 4 em [ROADMAP](ROADMAP.md); modelo do adversário
e registro formal de D1 em [THREAT_MODEL](THREAT_MODEL.md), seção 1.5; variantes A e B
em [CURRENT_DESIGN](CURRENT_DESIGN.md); [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); [requisitos obrigatórios](../ru/REQUIREMENTS.md). Os
participantes também leram pesquisas anteriores do projeto sobre aritmética exata, sumcheck/GKR,
Brakedown e o preço da testemunha para LoRA (documentos `LORA_*` e `HONESTY_RESEARCH_GATE` do arquivo
de pesquisa; eles não fazem parte deste repositório). Os participantes ainda não tinham as decisões
D6–D17: elas foram aceitas no mesmo dia. Na consolidação, essas decisões foram aplicadas às conclusões
dos trabalhos; onde a decisão muda o veredito, isso é dito diretamente.

---

## 1. Formulação

### 1.1. O que se busca

Busca-se um procedimento que o nó execute por conta própria com dados que a coalizão não pode
falsificar: a entrada da tarefa, o modelo fixado, as regras fixadas e, possivelmente, uma prova
matemática. A decisão do nó não deve depender de assinaturas e vereditos de outros nós. Então a
parcela de verificadores em conluio `q`, inclusive `q = 1`, não influi na decisão.

Dois tipos de trabalho:

- **(a) resposta do modelo** Qwen da ordem de 4–27 bilhões de parâmetros a uma solicitação do usuário;
- **(b) passo de treinamento** (LoRA ou completo) sobre uma porção de dados determinada.

### 1.2. Condições obrigatórias

| Condição | O que dela decorre para a verificação |
|---|---|
| **D1** | O ganho esperado de qualquer declaração falsa não é maior que zero tanto contra a inação (`Δ₀ ≤ 0`) quanto contra o trabalho honesto (`Δч ≤ 0`), para qualquer coalizão, inclusive um novato com conta vazia e qualquer número de chaves. São necessárias **ambas** as desigualdades ([THREAT_MODEL](THREAT_MODEL.md), seção 1.5). Um vazamento limitado e positivo como `R·q^k` na variante B não serve |
| **D2** | Só se paga por um resultado verificável. Tempo de trabalho, potência declarada e equipamento ligado não servem de base. O modo como o executor obteve o resultado correto (cache, outra máquina) não importa |
| **D4** | A verificação é automática, sem votações; cada nó a executa por conta própria segundo a impressão digital fixada das regras |
| **D6** | O dano entra em D1: uma resposta falsa não deve ser entregue ao usuário como verificada, e um passo falso não deve entrar no modelo. O resultado só é usado após uma verificação independente da parcela de conluio ou é explicitamente marcado como não verificado |
| **D7** | É exigida uma verificação que não dependa da parcela de conluio. Não se admite enfraquecer D1 para «enquanto os em conluio forem menos que `q*`» |
| **D8** | Só podem contestar os verificadores da tarefa designados por sorteio e o usuário quanto à sua própria solicitação. Sem depósito. Os demais comunicam a suspeita no quadro, sem direito de parar o pagamento |
| **D15** | Um recálculo simples, que pode ser copiado, não é pago |
| **R5** | Sem depósitos, contribuições nem multas. Só se pode perder recompensas ainda não vencidas («valor pendente» `H`) |
| **Referências de preço** | Um acréscimo pela verificação de cerca de 5% do trabalho para solicitações e cerca de 20% para treinamento. São referências, não requisitos confirmados |

Decisões relacionadas: D9 (o plano de treinamento é derivado por uma regra do catálogo e dos
resultados do exame, os créditos são emitidos uma única vez por conteúdo da tarefa), D10 (a troca
ocorre por uma única entrada do registro), D12 (as janelas são contadas em tempo ativo da rede), D14
(o preço da disputa é o da rede de segundo nível mais barata), D16 (uma falha honesta de hardware
não é punida), D17 (os pagamentos por solicitações na variante B saem apenas dos pagamentos dos
usuários).

Amostragem estatística, confiança em enclave de hardware e pequeno erro criptográfico conforme os
requisitos são suposições: podem ser propostas, mas devem ser declaradas diretamente.

### 1.3. Modelos e parâmetros usados pelos trabalhos

Não havia manifesto fixado do Qwen3.5-4B nos materiais. Cada trabalho adotou sua própria configuração
densa convencional, por isso «4B» em trabalhos diferentes significa números diferentes. Se o Qwen3.5
tiver camadas híbridas de atenção linear, todas as frações de atenção e as conclusões sobre a
coincidência dos modos de cálculo mudam (seção 5).

| Trabalho | Resposta do modelo (a) | Passo de treinamento (b) |
|---|---|---|
| claude1 | «4B»: 36 camadas, largura 2560, consultas de atenção 4096, chaves/valores 1024, MLP 9728, vocabulário 151 936, entrada e cabeça compartilhadas (4,022 bilhões de parâmetros). «27B»: 64 camadas, 5120, 6144, 1024, 20 480, 151 936, separadas (26,386 bilhões). Solicitações de 500/500 e 2000/1000 tokens | LoRA de posto 16 nas matrizes das camadas superiores, exame `n = 10⁴–10⁶` posições |
| claude2 | A mesma «4B». Solicitação de 1000 tokens, resposta 500; trabalho da solicitação 5,98·10¹² MAC [cálculo] | LoRA de posto 16/64 em todas as sete matrizes, contexto 4096, lote de 64 ou 7680 sequências |
| gpt1 | «S»: 36 blocos, 2560, KV 640, MLP 11 008, 151 936. «Lg»: 48, 5120, 1024, 31 232. Entrada 128, saída 32 tokens | 8 microlotes de 512 tokens, LoRA de posto 8 em Q, V |
| gpt2 | «Pequeno»: 36, 3072, KV 768, MLP 8192, vocabulário 150 000. «Grande»: 60, 6144, 1024, 18 432. Entrada 128, saída 128 | O mesmo que gpt1 |
| ds1 | Classe Qwen3-4B: 4·10⁹ parâmetros, 36 camadas, 2560, MLP 9728 | Perfil Qwen2.5-1.5B de pesquisas anteriores: 28 blocos, 1536, MLP 8960, LoRA de posto 8 em q/v, 512 tokens × 8 microlotes |
| ds2 | 36 camadas, 2560, MLP 8960, cabeças 32/8; contexto 2048, resposta 200 | O mesmo perfil de 1.5B |

Equipamento (ficha técnica de memória, não conferida): classe RTX 2060 — 336 GB/s de memória, cerca de
103 TOPS INT8, 6 GB; classe RTX 4090 — 1008 GB/s, cerca de 660 TOPS, 24 GB. As frações do pico, 0,8
para memória e 0,4 para computação, são hipotéticas. A única medição de velocidade é 73,8 tokens/s do
Qwen3-4B Q4_K_M na RTX 2060 no piloto ([PILOT_RESULTS](PILOT_RESULTS.md)). É outro formato de pesos,
e ele não confirma nem refuta os modelos acima.

O registro comum de D1 para uma declaração falsa, com o qual os trabalhos concordaram: com preço da
tarefa `R`, custo do trabalho honesto `c`, custo da falsificação `c_f` e probabilidade de sua aceitação
`ε`, são necessários `Δ₀ = εR − c_f ≤ 0` e `Δч = εR − c_f − (R − c) ≤ 0` [cálculo].

---

## 2. Limites inferiores: o que foi provado impossível

### 2.1. Limites confirmados pelos críticos

Estas são afirmações sobre **classes** de verificações. Nenhuma delas exclui todas as verificações
imagináveis; ninguém provou um limite inferior geral de preço para todos os algoritmos.

1. **Indistinguibilidade.** Se o nó aceita um resultado apenas por mensagens de outros nós, então,
   com o conluio de todos os seus autores, existe um resultado falso que ele aceitará: a coalizão
   enviará as mesmas assinaturas e impressões digitais que com um resultado honesto. Com `q = 1`, o nó
   está protegido apenas pelo que verificou por conta própria. (claude1, lema 1; claude2, 3.1; gpt2,
   9.4; ds2, 6.1. Todos os críticos concordam.)
2. **Escala «cada nó por conta própria».** Se a mudança do estado comum (emissão de créditos, peso)
   deve ser protegida para cada um dos `N` nós completos, cada um deles verifica cada um desses
   resultados, e o preço total não é menor que `N·v`, onde `v` é o preço de uma verificação. Para caber
   em 5% ou 20%, com `N = 1000` é preciso `v/W ≤ 5·10⁻⁵` ou `2·10⁻⁴` de trabalho [cálculo]. Daí três
   modos de obter independência do conluio: decide o único participante cujo dinheiro está em jogo; a
   verificação é comprimida (prova sucinta ou exame pequeno); o resultado não muda o estado comum de
   modo algum. (claude1, lema 2; claude2, 3.4; gpt1, §2; ds2, 6.1. Todos os críticos concordam; o
   crítico ChatGPT corrigiu a fórmula de ds2 para `1 + n·a` em vez de `(1 + a)·n`.)
3. **Amostragem de células sem codificação.** Se o nó lê em média `s` de `N` células substituíveis de
   forma independente (camadas, posições, sequências), existe uma célula que ele verifica com
   probabilidade não maior que `s/N`; sua substituição passa com probabilidade não menor que `1 − s/N`.
   (claude2, 3.2; gpt2, 9.2; gpt1, 5.4; claude1, I2. O crítico Claude apontou uma lacuna de rigor para
   o verificador cujas moedas dependem da raiz do traço; a conclusão não muda por isso.)
4. **Verificação por amostragem e margem do executor.** Para uma declaração falsa `σ` com custos `c_σ`
   e valor pendente `H`, D1 contra a inação exige `π(σ) ≥ (R − c_σ)/(R + H)`, onde `π` é a
   probabilidade de detecção. Para uma falsificação barata e conta vazia, é preciso `π ≈ 1`, isto é,
   verificação completa. Para uma falsificação quase honesta, é necessária uma fração de verificação
   não menor que `m/(1 + m)` com margem `m`. Para uma chave com `H > 0` e verificação de um bloco de
   `L + 1`, é preciso `H ≥ R·((L+1)/m_s − 1)`: 36R para 36 camadas e 64R para 64 camadas com um bloco
   verificável [cálculo]. A aleatoriedade fresca do nó torna `π` independente do conluio, mas não a
   torna igual a um. (claude1, lema 3; claude2, 3.11, obtido independentemente. Todos os críticos
   concordam. O crítico ChatGPT esclareceu: com a verificação obrigatória do bloco de saída, o limiar
   para uma tentativa quase gratuita é 35R.)
5. **Verificações lineares fixadas sobre o corpo.** `t < n` verificações lineares fixadas de antemão
   têm um núcleo comum não nulo: não veem um erro pertencente a ele. Um vetor uniforme fresco,
   escolhido após a fixação, deixa passar um erro fixado não nulo com probabilidade não maior que
   `1/p`. Sobre inteiros limitados, o limite não se aplica (ver 2.2, item 3). (gpt1, 5.2; gpt2, 9.1;
   claude2, 3.5; ds2, 5.2; claude1, B4.)
6. **Erro zero equivale a determinismo.** Uma verificação com zero aceitações falsas para quaisquer
   moedas torna-se determinística pela fixação das moedas. (claude2, 3.6.)
7. **Aleatoriedade comum sob conluio total.** Com `q = 1`, a aleatoriedade comum a todos os nós só é
   possível de fora da rede (farol externo ou Fiat–Shamir); a troca de compromissos entre nós do
   SkyNet não ajuda. As moedas pessoais de nós diferentes dão decisões diferentes, e não se obtém um
   cálculo único. (claude2, 3.8; gpt2, 6.1. O crítico ChatGPT acrescentou: o farol deve ser não
   deslocável, acessível e revelar-se estritamente após a aceitação final do bloco; isso já é o ataque
   1.5 e N13 em [THREAT_MODEL](THREAT_MODEL.md).)
8. **Repetições gratuitas.** Se a tentativa pode ser repetida quase de graça (por exemplo, a
   aleatoriedade é derivada do hash da própria declaração), a probabilidade de sucesso cresce com o
   número de tentativas. Para a escolha de células, não se pode usar Fiat–Shamir. (claude2, 3.3;
   ds2, 5.1.)
9. **O verificador que constrói o resultado por conta própria.** Se o nó calcula todo o estado por
   conta própria e lê a declaração apenas para comparar, então, removendo a comparação, obtém-se um
   executor honesto com o mesmo trabalho. Logo, essa verificação custa não menos que 100% do trabalho
   ótimo. Só pode ser barata a verificação com uma dica: resposta pronta, traço ou prova. (gpt2, 9.5.
   Os críticos Claude e DeepSeek chamaram esta de melhor formulação do limite geral.)
10. **Certificado do token vencedor.** Para um estado oculto em posição geral, não se pode certificar o
    vencedor sem obter informações sobre cada linha do vocabulário que pode vencer. No pior caso,
    verifica-se todo o vocabulário. (claude1, B6; gpt2, 9.3.)
11. **Entrada privada.** Um nó externo sem a solicitação não pode verificar a resposta se não houver
    uma prova de conhecimento zero. O crítico ChatGPT esclareceu o limite: um compromisso ocultador
    junto com essa prova poderia transmitir a propriedade necessária, e o lema não exclui isso.
    (claude2, 3.7; ds2, 6.2; gpt1, §1.)

### 2.2. Afirmações de impossibilidade refutadas pelos críticos

1. **«O D1 literal exige erro exatamente zero»** (ds1, F1). É verdade apenas se a tentativa não custa
   nada. Se a aleatoriedade é externa e imprevisível, e cada tentativa exige uma nova fixação
   e custa `c_min > 0`, então `Δ₀ ≤ εR − c_min ≤ 0` com `ε ≤ c_min/R` (claude1, lema 4; ds2, 5.1).
   O próprio candidato de ds1 também se apoia em hash com erro maior que zero. Todos os três críticos
   refutaram. Ressalva do crítico ChatGPT: o projeto ainda não estabeleceu o limite inferior do preço
   da tentativa mais barata para qualquer coalizão, por isso o erro pequeno só é compatível com D1
   condicionalmente (questão 2 na seção 6).
2. **«A verificação da resposta pronta custa +100% do tempo por definição»** (ds1, F2). É falso para
   a resposta pronta: ao verificar todas as posições em uma única passagem, os pesos são lidos uma vez,
   e não a cada token. Pelo número de operações, a verificação é de fato igual à geração, mas em tempo,
   com geração de uma resposta por vez, ela pode ser dezenas de vezes mais rápida. Além disso, ds1
   comparou perfis de pesos incomparáveis. Todos os três críticos refutaram.
3. **«A verificação linear exata exige não menos que `N` formas e `N²` operações»** (ds1, F3). É falso
   duas vezes: coeficientes frescos após a fixação dão passagem com probabilidade de cerca de
   `Q^(−s)`, e sobre inteiros limitados basta uma forma com empacotamento posicional `Σ y_i·B^i` com
   `B > 2U` (gpt1, 5.3; gpt2, 6.2); a matriz identidade lê as coordenadas em `O(N)`. Todos os três
   críticos refutaram.
4. **«O tráfego mínimo da verificação da resposta é igual ao tamanho do traço de cálculo»** (conclusão
   do lema 5.3 de ds2). A verificação da resposta pronta precisa apenas dos tokens da resposta, e o
   verificador de uma prova sucinta lê a prova e as raízes, e não os próprios dados. Todos os três
   críticos refutaram.
5. **«Qualquer geração honesta é obrigada a executar tantas operações quanto a verificação em uma
   passagem»** (claude1, §4.1 e B5). É um limite superior do preço da verificação, e não inferior
   (crítico Claude), e não vale se o executor tem um cache legítimo do resultado pronto (crítico
   ChatGPT).
6. **«A verificação exata barata é impossível sem aleatoriedade secreta ou criptografia»** (claude2,
   3.5). Contraexemplo — a equação normal exata da regressão de crista sobre números racionais é
   verificada de forma determinística (crítico ChatGPT).

### 2.3. Limites controversos ou condicionais

- **Tamanho do exame `n ≳ 2σ²·ln(1/ε)/δ²`** (claude2, 3.10). Os críticos Claude e DeepSeek a aplicam
  como estimativa de trabalho. O crítico ChatGPT mostrou que de uma única variância não se pode
  derivar o `n` necessário para qualquer distribuição: são necessárias alternativas dadas e uma
  unidade de amostragem independente. **Controverso**: serve como estimativa no modelo nomeado, não
  como teorema.
- **Barreira quantitativa da prova completa** (claude2, 3.9): o orçamento de 5% deixa cerca de 1–5,
  o orçamento de 20% — cerca de 6–18 operações no corpo por célula não linear, enquanto as construções
  conhecidas de arredondamento custam dezenas, e o softmax, centenas [cálculo com os custos supostos].
  Todos os críticos concordam que este é um limite das construções conhecidas, não um teorema.

---

## 3. Resposta do modelo (a)

### 3.1. Todos os mecanismos considerados

O «preço» é indicado como acréscimo ao trabalho da execução honesta; todos os números são [cálculo]
pelos parâmetros dos trabalhos. O «veredito» é o resultado após as três críticas e levando em conta
D6–D17.

| Mecanismo (trabalhos) | Essência | Garantia e suposições | Dados do nó | Conluio e contraexemplo | Preço [cálculo] | Veredito |
|---|---|---|---|---|---|---|
| **Repetição completa por cada nó**, passagem causal pela resposta pronta (todos os seis) | O nó com a entrada calcula por conta própria todas as posições e verifica cada token e a primeira causa de parada | Erro zero com perfil exato, entrada autêntica e núcleo em bom estado | Solicitação, resposta, modelo, perfil, semente | O conluio não ajuda: decide o próprio recálculo | Cerca de 100% das operações para cada um dos `N` nós; um nó externo não vê a solicitação privada | **Sustenta-se** como referência; não cabe em 5% com verificação por todos os nós |
| **I1 / PPS** (claude1): verifica o pagador | O pagador recalcula em uma única passagem a solicitação e a resposta no perfil inteiro «INT-canônico»; o pagamento sai apenas do seu pré-pagamento; não há emissão nem peso pela solicitação paga | Erro zero sob A1 (os mesmos bits em equipamentos diferentes **e** na decodificação token a token e na passagem de toda a sequência em uma única placa), A2 (o registro armazena), A3 (hash, criptografia), A4 (o pagador publica a prova de erro no prazo), A5 (os dados da disputa estão disponíveis) | Solicitação, resposta (`T·4` bytes), impressões digitais do modelo e do perfil, semente; pesos em memória 4,02 GB para 4B W8, 12,8–25,6 GB para 27B | Decide o único participante cujo dinheiro está em jogo; o conluio «pagador + executor» apenas transfere os próprios créditos deles | 4B, 500/500, RTX 2060: 3,98·10¹² MAC, 0,19 s contra 7,5 s de geração — cerca de 2,5–2,6%; todos os cenários 1,2–3,8% com geração de uma resposta por vez; 8–22% com lote 8; 21–48% com lote 32. Sem GPU, cerca de 8 s para 1000 tokens no processador — 100–300% | **Sustenta-se com correções** (todos os três críticos); correções em 3.2 |
| **I8 — disputa pelas raízes das camadas** (claude1) | O executor fixa as impressões digitais do fluxo residual por camada. O pagador encontra o primeiro bloco em que o recálculo diverge e publica sua entrada; cada nó recalcula um bloco. Sem prova dentro da janela, o pagamento vai para o executor | Não há prova falsa de erro sob A1; a recusa falsa do pagador é impossível | Entrada do bloco (10–20 MB com 1000 posições), pesos de uma camada (101–388 MB) | Cada nó decide a verificação por conta própria. Contraexemplos: o executor registra no registro apenas a impressão digital do texto cifrado e não entrega a própria resposta; o registro é igual com a resposta entregue e retida; a censura do bloco na janela depende de validadores externos | Cerca de 1,0·10¹¹ MAC por nó para 4B, 3,9·10¹¹ para 27B; com 1000 nós, uma disputa falsa — da ordem de 10–20 GB de tráfego da rede (estimativa do crítico Claude) | **Sustenta-se com correções**: texto cifrado no registro, limite de disputas falsas, tempestividade e censura como suposições declaradas |
| **M1 — Freivalds do pagador com vetor secreto** (ds2) | O pagador recalcula as operações elemento a elemento, e verifica as multiplicações de matrizes por produtos escalares no seu vetor secreto fresco | Erro não maior que `N/p` para todas as igualdades, desprezível com `p ≈ 2⁶¹`; são necessárias a verificação de faixa e as somas brutas antes do arredondamento | Traço de cálculo do executor | Verifica o próprio pagador. Contraexemplo ao cache do vetor: conhecendo o vetor de uma camada, o executor controla a saída dessa camada em todas as solicitações futuras (crítico DeepSeek) — o vetor precisa ser fresco a cada solicitação | Declarado 2,7%; não se reproduz: softmax 0,79%, e não 2,45%, e com o preço da multiplicação no corpo em 10–100 MAC as projeções dão +1,6–15,8% (crítico DeepSeek). Tráfego — **controverso**: cerca de 14 MB por token com int32 brutos e cerca de 15 GB de traço de uma solicitação de 1850 tokens (crítico Claude); 7,419 MB por token mesmo em INT16 e 7,477 GB de pré-preenchimento (crítico ChatGPT); cerca de 2,4 MB por token se o próprio pagador recalcula as estimativas de atenção (crítico DeepSeek) | **Sustenta-se como verificação** para um pagador sem GPU, mas com canal rápido; o preço declarado foi refutado |
| **I2 — camadas por amostragem** com aleatoriedade fresca do nó (claude1; ds1, 3.1; gpt2, §8) | O nó verifica `m_s` camadas aleatórias de `L` por impressões digitais | Passagem de um erro isolado com probabilidade `1 − m_s/(L+1)` | Entrada da camada, pesos da camada | Falsificação: resposta de um modelo pequeno mais traço honesto do grande; um passo é distorcido, depois há continuação coerente | Hash do traço 0,38–4 GB; 1–8% para o executor, dependendo da velocidade do hash | **Refutado** para conta vazia (limite 2.1, item 4); serve apenas para chaves com `H ≥ 35–64R` |
| **PVYa** (claude2): o usuário verifica uma amostra de células «bloco × token» com sua aleatoriedade secreta | Escolha da célula proporcional à sua fração de operações | Apenas o ganho monetário, não o dano | Células do traço, caminho na árvore de impressões digitais | Contraexemplo do crítico Claude: resposta de um modelo pequeno e traço de prefill honesto; a falsificação barata em tempo é detectada com probabilidade de cerca de 0,3–1%, `Δч ≈ +0,94c`. Crítico ChatGPT: no modelo de custos iguais, `Δ₀/c = +0,019`; é necessária também a vinculação das chaves e dos valores de atenção ao prefixo | Para o usuário, de <0,001% a 2,7%, a variante estrita cerca de 5,6%; para o executor, o hash de cerca de 4 GB de traço — 2–4 s de processador, 30–50% do tempo da solicitação na RTX 2060 | **Refutado** (críticos Claude e ChatGPT). O crítico DeepSeek o aceitava com a separação das variantes estrita e relativa, mas a variante relativa não cumpre o registro bilateral de D1, e por D6 é necessária também uma garantia quanto ao dano, que a PVYa não oferece |
| **I3 — Freivalds pelo traço** por um nó da rede (claude1; ds1, 2.2; gpt1; gpt2, 6.1) | Verificação de cada multiplicação por um vetor aleatório sobre o traço enviado | `≤ 1/p` por erro; são necessárias as saídas brutas antes do arredondamento | Todo o traço | O conluio não ajuda se o vetor é fresco | Traço de 4,4 GB por resposta (4B), 15,2 GB (27B); para prefill de 4096 posições, apenas gate/up — 5,74 GB em INT16 contra 0,755 GB na estimativa de ds1 (crítico ChatGPT) | **Refutado como verificação barata**: esbarra no tráfego, não na aritmética |
| **I4 — tabelas de somas parciais** (todos os seis) | O nó constrói de antemão tabelas das saídas da camada por grupos de entradas | Exato com pesos canônicos | Tabelas | — | Grupo 2: 859 GB para uma matriz de 4B, cerca de 476 TB o corpo inteiro; planos de bits — não menos que 128 tamanhos do modelo | **Refutado por cálculo** (todos os críticos) |
| **I5 — certificado do token vencedor** (claude1; ds1, 2.5; gpt1, 4.3; gpt2, 5.3) | Árvore de clusters de linhas da cabeça com limites superiores provados | Exato para a escolha gulosa com cobertura completa do vocabulário e estado oculto verificado | Estado oculto da última camada | Um estado oculto substituído certifica outro token | Economiza não mais que a fração da cabeça: 2,10% / 0,60% (gpt1), 6,04% / 1,76% (gpt2), até 9,67% (claude1); no pior caso, todo o vocabulário | **Sustenta-se como parte** da verificação (escolha gulosa) |
| **Gumbel-max como amostrador canônico** (claude1; claude2, 5.5) | A escolha com temperatura reduz-se a `argmax(z/τ + g)` com ruído de PRF pela semente | A identidade é válida | Semente | A distribuição difere da top-p/top-k usual — é uma mudança de produto | Ruído fresco a cada token: cerca de `V` valores de PRF e máximos de grupo, 75,97 milhões de valores de PRF para 500 tokens | **Sustenta-se** como modo de definir a escolha; a economia do certificado para a amostragem **não está justificada** (críticos DeepSeek e ChatGPT) |
| **Certificado de Gumbel «com folga»** (claude2, 5.5) | Aceita-se o token quase vencedor dentro de uma tolerância | — | — | Contraexemplo: com logits iguais e diferença de ruído menor que `2η`, passa um token incorreto (crítico ChatGPT); qualquer tolerância abre a substituição (ds2, 6.4) | — | **Refutado** |
| **Certificado intervalar com recálculo exato em caso de ambiguidade** (gpt1, 4.4; gpt2, 5.4) | Aproximação de posto baixo da matriz congelada e limite provado do resíduo; onde o intervalo admite arredondamentos diferentes, o nó recalcula exatamente | Erro zero com normas do resíduo calculadas de forma independente e recálculo obrigatório | Fatores e normas dos resíduos próprios | Não se pode tomar chaves e valores da mensagem do executor | A passagem rápida 0,521% das operações da camada; para 5%, a fração de saídas ambíguas não é maior que 4,479% em uma camada aquecida e 1,342% com preparação fria (crítico ChatGPT). Crítico Claude: com pesos próximos do posto completo, os intervalos quase certamente cobrem muitas células, e o preço fica próximo de 100% | **Sustenta-se** matematicamente; o **preço é controverso**, não demonstrado |
| **Empacotamento posicional exato** (gpt1, 5.3; gpt2, 6.2) | Uma forma linear `Σ y_i·B^i` sobre inteiros | Exato com `B > 2U` e faixas provadas | Somas brutas | Pequena enumeração: com `B = 8`, 9 aceitações corretas e 0 falsas; com `B = 4`, 20 falsas de 29 (repetido por dois críticos, os hashes coincidiram) | Quase sem ganho: para W8A16 com largura 3072, uma palavra de 64 bits por saída | **Sustenta-se** como primitiva exata, não traz barateamento |
| **Cache de prefixos verificados** (gpt2, 5.1) | O nó reutiliza o estado que ele mesmo derivou | Exato para a mesma posição e versão | Cache próprio | Uma raiz alheia pode vincular um estado incorreto | Ganho apenas em repetições; o mesmo cache está disponível ao executor | **Sustenta-se**, no caso geral não barateia |
| **Provas sucintas sumcheck/GKR** para a resposta (claude1, I6; claude2, 4.9 e 5.7) | O executor prova toda a passagem; cada nó verifica a prova | Garantia computacional; o limite de erro de ponta a ponta para o grafo do Qwen não foi derivado | Prova, pesos para a avaliação em um ponto aleatório | O conluio não ajuda com o esquema completo e entradas verificadas | Referência FlashProve 70–95× o próprio perfil (o denominador não está claro); estimativa de claude2 — 6–20 vezes mais caro que o trabalho com contexto 2048; na melhor leitura, cerca de 16,8× (crítico ChatGPT) | **Sustenta-se** como garantia condicional; **não cabe** em 5% |
| **Mudar a tarefa: pagar pelo resultado verificável** (claude1, I7; claude2, 5.4; gpt1, 3.1; gpt2, 4) | Por exemplo, um vetor que satisfaz a fórmula SAT, código que passa nos testes, uma solução com resposta verificável | Exato para o seu predicado | Tarefa e resultado | O executor pode enviar um resultado correto que o modelo não produziu; por D2 isso é permitido | Verificação de SAT — não mais que `3m` leituras | **Sustenta-se para uma classe estreita**; a fração dessas solicitações é desconhecida; o diálogo livre não é coberto |
| **P0 / M4 — a solicitação paga não gera emissão nem peso** (claude1, claude2, ds2) | O dinheiro apenas passa do pagador ao executor | A transferência dos próprios créditos é neutra dentro da coalizão | — | Sem essa regra, a verificação pelo pagador não protege a rede (limite 2.1, item 2) | 0 | **Sustenta-se**; está de acordo com D17 |
| **Verificador de lote de um nó dedicado, pagamento apenas do prefill** (ds1, 3.3–3.4) | Um nó verifica o lote; paga-se o prefill exato | — | — | A assinatura do nó dedicado é igual na verificação real e na simulada; um prefill exato com resposta inventada passa | — | **Refutado** (crítico ChatGPT) |
| **Produto das probabilidades de erro de nós diferentes** (ds1, 3.2) | Cada nó verifica com sua própria aleatoriedade | — | — | Funciona apenas com aceitação obrigatória por todos os nós honestos; com `q = 1` eles não existem | — | **Refutado** |
| **Disputa aberta na janela** (todos os seis) | Qualquer um pode objetar antes do fim da janela | É necessário um observador honesto com dados e tempo | — | Se todos os que viram os dados se calarem, o resultado falso passa com probabilidade 1; o piloto mostrou isso | Piloto: 93 transações e 5,8–6,3 milhões de gas na disputa Cartesi | **Refutado** como verificação independente do conluio; além disso, D8 limita o círculo dos que contestam |
| **Delegação por um pagador fraco** (claude1, 4.10) | O pagador delega a verificação ao seu dispositivo ou a um nó escolhido | A confiança no escolhido é uma suposição do pagador | — | Com escolha aleatória, volta a dependência de `q` | — | **Suposição**, não solução |

### 3.2. Melhor candidato para a resposta do modelo e correções dos críticos

**Candidato.** O próprio pagador verifica toda a resposta. Se ele tem uma placa de vídeo em que o
modelo cabe, é o PPS (claude1). Se não tem placa de vídeo, mas tem um canal rápido, é o M1 (ds2)
com vetor secreto fresco a cada solicitação. Em ambos os casos, a solicitação paga não gera emissão
de créditos nem peso (P0; isso está de acordo com D17), e a disputa é decidida por cada nó pela prova
de erro (I8). Por que o conluio não ajuda: a decisão é tomada pelo único participante cujo dinheiro
está em jogo; ele tem os dados completos — solicitação, resposta e modelo; a verificação é completa,
e não por amostragem.

**Correções sem as quais o candidato não se sustenta.**

1. **Retenção da resposta.** É preciso colocar no registro o próprio texto cifrado da resposta, e não
   apenas sua impressão digital: cerca de 2–4 KB por resposta (crítico Claude). Isso coincide com D10:
   a troca por uma única entrada do registro.
2. **Disputas falsas.** A coalizão «pagador = executor» pode criar quantas solicitações pequenas
   quiser e abrir uma disputa para cada uma, que todos os nós baixam e recalculam. D8 limita o fluxo
   de disputas pelo número de solicitações, mas as solicitações pagas a si mesmos não são limitadas
   por esse teto. Nenhum trabalho deu solução (seção 5, tarefa M9).
3. **Tempestividade e censura.** O pagador deve estar na rede e conseguir publicar a prova dentro da
   janela, e o registro deve aceitá-la. A censura do bloco na janela depende da honestidade dos
   validadores externos do registro. É uma suposição sobre conluio em outro conjunto, e precisa ser
   declarada diretamente. Para o telefone do pagador, ela é violada com mais frequência. A janela,
   por D12, é contada em tempo ativo da rede.
4. **Vinculação das pontas.** A disputa sobre a primeira camada exige a vinculação à solicitação
   privada original, e a disputa sobre a última — ao texto cifrado pago (crítico ChatGPT).
5. **Parada.** É preciso verificar a primeira causa de parada. A condição «último token EOS ou limite
   atingido» deixa passar uma resposta acrescentada após um EOS precoce (crítico ChatGPT).
6. **Aritmética do INT-canônico.** O produto das probabilidades de atenção pelos valores na
   especificação acumula em int64. Se não for executado nos núcleos tensoriais, o preço do cenário
   longo 2000/1000 cresce de 3,8% para cerca de 8% (estimativa do crítico Claude); a saída é decompor
   a probabilidade de 16 bits em duas metades de 8 bits. O crítico ChatGPT encontrou mais três
   lacunas: com uma única chave permitida, o softmax dá o valor 65 536, que não cabe em 16 bits; a soma
   dos quadrados no RMSNorm pode estourar int64 (três componentes de `2³¹−1` já dão mais que
   `INT64_MAX`); são necessárias larguras explícitas, posições RoPE e ordem de arredondamento. O
   próprio princípio resiste a essas correções.
7. **Entrega em fluxo.** Por D6, o usuário não deve ver texto não verificado como verificado. Na
   entrega em fluxo, cada prefixo mostrado deve ser verificado, e a frequência dessas verificações
   entra no preço (gpt2, §1).

**Limitações do candidato.**

- O preço de 1,2–3,8% só é válido com geração de uma resposta por vez. É vantajoso para o executor
  agrupar solicitações em lotes, e com lote 8–32 a comparação honesta dá 8–48% [cálculo].
- O candidato não cobre o consumidor sem equipamento. Para 27B, o pagador precisa de não menos que
  13 GB de memória de vídeo. O consumidor principal, segundo os requisitos, é o participante sem
  equipamento. Por D6, a resposta dele só pode ser entregue com a marca «não verificado»; como pagar
  ao executor por isso sem violar D1, nenhum trabalho resolveu.
- Tudo depende da suposição A1, não medida: a coincidência de bits em placas de vídeo diferentes
  **e** entre a decodificação token a token e a passagem de toda a sequência em uma única placa. Se o
  Qwen3.5 tiver camadas recorrentes de atenção linear, sua forma paralela arredonda de outro modo, e
  o preço da verificação pode crescer cerca de duas vezes (claude1, 3.4, estimativa com 10 µs por
  passo admitidos).
- A disputa revela a solicitação: a entrada do bloco reconstrói o texto de forma quase reversível.
  Não há disputa sem revelação.
- A energia não foi medida: ao esbarrar na computação, a placa de vídeo consome mais do que ao
  esbarrar na memória, por isso a fração por energia pode ser maior que a fração por tempo.
- Aceleradores (certificado intervalar, certificado do vencedor para a escolha gulosa, cache dos
  próprios prefixos) são admissíveis apenas sobre a verificação completa, e não em vez dela.

---

## 4. Passo de treinamento (b)

### 4.1. Todos os mecanismos considerados

A principal diferença em relação à resposta do modelo: o passo de treinamento não tem um pagador cujo
dinheiro está em jogo. O pagamento ocorre por emissão de créditos, por isso, pelo limite 2.1, item 2,
a base deve ser verificada por cada nó completo. Por D15, além disso, esse recálculo simples não é
pago.

| Mecanismo (trabalhos) | Essência | Garantia e suposições | Dados do nó | Conluio e contraexemplo | Preço [cálculo] | Veredito |
|---|---|---|---|---|---|---|
| **T1 — repetição completa da transição** por cada nó (todos os seis) | O nó repete o passo a partir do pai aceito e compara todo o estado seguinte, incluindo os pesos master, os momentos m, v do otimizador e o número do passo | Erro zero com perfil exato e dados autênticos | Pai, lote de dados, regras | Verificar apenas os pesos é pouco: os mesmos pesos com v zerado mudam o passo seguinte (crítico ChatGPT) | +100% para cada nó, no total `N × 100%`; por exemplo, cerca de 2,62·10¹⁵ MAC para recalcular um lote de 64 × 4096 para 4B | **Sustenta-se** como referência; não cabe em 20% |
| **T2 — camadas, microlotes e passos por amostragem** (claude1; ds1, 3.1) | O nó verifica uma parte aleatória do passo | `1 − m_s/L` de passagem | Parte do traço | Falsificação: entregar uma atualização aleatória ou copiada; substituir um gradiente de fronteira | Com `N = 1000`, 36 camadas e uma camada verificada — cerca de 28 trabalhos por passo | **Refutado** (limite 2.1, item 4) |
| **VYa-S** (claude2): o farol escolhe células «bloco × sequência», e cada nó verifica a prova comprimida delas | Probabilidade de passar `(1 − f)^s` com fração de falsificação `f` | Farol externo, hash, prova da célula; apenas o ganho monetário, não o dano | Provas das células escolhidas | Crítico Claude: copiar o traço de uma sequência para todo o lote — só as células de vinculação ficam inconsistentes (cerca de 10,5% do peso); com `s = 30`, `Δ₀ ≈ +0,036R`; com `s = 10`, `Δ₀ ≈ +0,33R` e `Δч ≈ +0,26c`. Crítico ChatGPT: o gradiente nulo na fronteira do bloco torna todas as células inferiores internamente corretas; na fórmula foi colocada a fração do trabalho economizado em vez da fração de igualdades incorretas; mesmo com igualdade entre elas, `Δ₀/c ≈ +0,096`. Crítico DeepSeek: cumpre-se apenas `Δч ≤ 0`, e D1 exige também `Δ₀ ≤ 0` | Provas 0,66%, recálculo das entradas 0,39%, hash 3,7–10% com `s = 30`; fronteiras das camadas — 96,64 GB por tarefa de 64 sequências e 11,60 TB por tarefa de 7680 | **Refutado na forma atual** (todos os três críticos). A correção proposta — verificação separada da vinculação por sequências aleatórias; não foi calculada |
| **T3 — prova sucinta do passo** sumcheck/GKR com compromissos (claude1, T3; claude2, 4.9; ds1, 2.9; gpt1, 6.3; gpt2, 7.2) | O executor prova toda a transição, e cada nó verifica uma prova | Garantia computacional com esquema completo com vinculação da entrada, arredondamentos, faixas e otimizador; o limite de erro de ponta a ponta não foi derivado | Prova, raízes, uma passagem pelos pesos por lote | O conluio não ajuda com um transcrito comum | Referência VeriLoRA cerca de 137× (121,93 s de prova para 0,89 s de treinamento, outro modelo 3B); o orçamento deixa 11,43% — uma diferença de cerca de 1200×. Para o perfil de 1.5B, uma única divisão exata do softmax — 11 973 394 432 células do corpo e 10 998 054 912 verificações de faixa, 356,835 GiB antes do alinhamento; gravação de 3,067 TB a 100 GB/s — 30,67 s contra 6,6 s de orçamento com passo de 60 s | **Sustenta-se como direção**; os arranjos concretos foram refutados, 20% não demonstrados. O crítico ChatGPT considera esta a linha de pesquisa mais forte para o passo inalterado |
| **M1 para treinamento** (ds2) | Vetor secreto mais recálculo das operações elemento a elemento | Como em 3.1 | Traço | Não há vinculação do traço ao lote designado: um cálculo correto sobre dados substituídos passa (crítico DeepSeek) | Declarado 1,5%; não foram consideradas as operações inversas elemento a elemento (cerca de ×2–2,5) nem o preço da multiplicação no corpo. Tráfego 16,08 GB por passo em INT16, 64,318 GB em INT64 — não menos que 514,5 s a 1 Gbit/s | **Refutado** para treinamento por tráfego e vinculação |
| **Freivalds pelo traço do passo** (ds1, 2.2; gpt2, 6.1) | Verificação de cada multiplicação do passo | `≤ p^(−t)` | Todo o traço | — | 64,3 GB por passo (1.5B); 123,92–410,44 GB para LoRA e 369,72–2073,34 GB para treinamento completo por passo (gpt2); não menos que 991 s a 1 Gbit/s | **Refutado** como verificação barata |
| **T5 — o passo como fórmula de atualização** (todos os seis) | Os nós verificam os multiplicadores da atualização, e não a nova matriz | Verifica apenas a última soma | Multiplicadores | Contraexemplo: um gradiente enviado `G = 0`, com o verdadeiro não nulo, passa na verificação da fórmula | Cerca de 10⁻⁶ de trabalho | **Refutado** como verificação do passo; o recálculo do otimizador e da soma entra no núcleo |
| **Apenas o delta do LoRA** (ds1, 3.5) | Verificar apenas o adaptador | — | — | A saída da parte congelada depende da nova entrada | — | **Refutado** |
| **T4 — pagamento pela melhoria**, medida por cada nó em uma amostra fresca (claude1) | A atualização é fixada antes da rodada; o farol externo escolhe `n` posições do exame; cada nó calcula por conta própria a diferença truncada de perdas; paga-se o excesso sobre o limiar de confiança | Pagamento de uma atualização sem melhoria com probabilidade `≤ ε = 2⁻⁴⁰` com farol externo, amostragem com reposição, perfil exato e fixação antes do farol; o preço da tentativa deve ser não menor que `ε·κ·B/2` | Conjunto do exame, todas as `K` atualizações da rodada | Não há verificadores, cada nó calcula. Contraexemplos: (1) o truncamento das diferenças paga uma atualização prejudicial: +0,01 nat em 99,5% das posições e −20 em 0,5% dão, após o truncamento, +0,005 com o verdadeiro −0,09 (crítico Claude); +0,1 em 99% e −100 em 1% dão +0,089 com o verdadeiro −0,901 (crítico ChatGPT); (2) o conjunto público permite aprender diretamente nele; (3) uma duplicata com ruído, na fusão por soma, dá uma contribuição positiva | Limiar com `B = 2`: 0,0745 nat com `n = 10⁴`, 0,0236 com `n = 10⁵` (Hoeffding). Para caber em 20%, são necessários `D ≥ n(1 + K·a)/0,6` tokens de treinamento por nó por rodada; com `K = N = 10⁴`, isso é 1,85·10⁸ tokens, cerca de 26 h. Cache de estados — 0,51 GB pela estimativa de claude1 ou 524,3 GB em int16, se as posições forem tomadas de prefixos diferentes de 1024 tokens (crítico ChatGPT) | **Sustenta-se com correções** como nova unidade de pagamento; não verifica o passo. É controverso se a revelação seletiva de candidatos após o farol é perigosa: crítico Claude — não com `ε = 2⁻⁴⁰`; crítico ChatGPT — não foi considerado |
| **ODU** (claude2): pagamento pela melhoria comprovada em um exame escolhido pelo farol após a fixação | O proponente prova o exame; cada nó verifica a prova, em vez de recalcular | Como T4, mas remove o crescimento do preço com o número de nós; o treinamento pode ser feito em qualquer aritmética | Prova do exame | Crítico Claude: o proponente calcula o exame de graça na própria máquina e prova apenas os candidatos vencedores, por isso é preciso `ε ≲ 0,23%`, e não 10%. Crítico ChatGPT: o mesmo argumento, mais a seleção adaptativa no exame comum e o fato de que o pagamento pelo limite de confiança não se soma telescopicamente (0,16 em vez de 0,20 no exemplo). Crítico DeepSeek: `ε = 10%` passa formalmente, mas apenas ao custo de todo o orçamento de 20% | Prova do exame cerca de 2,4 h por candidato, em sequência: com 100 candidatos, a época não é mais curta que 10 dias (crítico Claude). Fração do exame 0,655% dos tokens de treinamento, 0,327% se também se provar o pai — cerca de 858 tokens, menos que uma sequência de 4096 (crítico ChatGPT) | **Sustenta-se com correções** como estrutura; `ε` é **controverso** (2 de 3 críticos: é preciso muito menos que 10%); a atribuição não foi resolvida |
| **Exame de ds1** (ds1, 2.8): 20–82 tokens, «erro zero» | Paga-se pela melhoria em um exame pequeno | «Erro zero» apenas por definição | — | O ruído da média, cerca de 0,28 nat em 82 tokens, com melhoria do passo de 10⁻⁴–10⁻³ (crítico DeepSeek) — paga-se o ruído; a fonte de aleatoriedade não foi nomeada; o exame não vê os momentos substituídos do otimizador | Declarado +1–3%; com o contexto completo de cada um dos 20 tokens avaliados — 103,4% da estimativa matricial do passo (crítico ChatGPT) | **Refutado** |
| **Passo amortecido de Gauss–Newton com certificado dual** (gpt1, 6.4) | Novo otimizador; o executor dá um vetor curto, e o nó prova cada bit do passo arredondado com `4λδ² > η²‖r‖²` | Erro zero para o novo passo com um modelo linear dado | Forward exato e duas passagens de derivadas | Um empate na fronteira exata de arredondamento exige a solução exata (crítico ChatGPT) | `3N/(2k+2)`: 8,82% com `k = 16` e `N = 1`, 75% com `k = 1`; com `N = 100` — centenas de por cento | **Sustenta-se** como contrato alterado; o preço cresce com `N`, a qualidade é desconhecida |
| **Critério exato: regressão de crista, cabeça linear** (claude1, T6; claude2, 4.1; gpt1, 3.2; gpt2, 4; ds1, 2.1; ds2, M2) | O nó verifica a condição de ótimo `Xᵀ(Xw − y) + λw = 0` | Exato com atributos autênticos | Atributos, rótulos | Os atributos precisam ser verificados separadamente; no M2 de ds2 falta o termo `λw`, e um ótimo incorreto passa (crítico ChatGPT) | 44,4% com posto 8 e 12,1% com 32 em relação à construção da matriz (gpt1); 0,390% em outro arranjo (gpt2) | **Sustenta-se para uma tarefa estreita**; não é o treinamento do Qwen, e a fração desse trabalho é desconhecida |
| **Vários primeiros passos LoRA diferentes** (gpt2, 7.3) | Com adaptador nulo, as partes comuns são calculadas uma única vez | Exato | Cache comum | Não se transfere para os passos seguintes | 16,70% para seis inícios permitidos contra seis execuções frias | **Sustenta-se**, a aplicabilidade é estreita |
| **Treinamento de ordem zero** (claude2, 5.8); **corpo pequeno nos núcleos tensoriais** (claude2, 5.11); **cache do prefixo congelado e LoRA nos blocos superiores** (claude1; claude2, 5.9) | Barateamentos | — | — | A ordem zero muda o otimizador; o corpo pequeno não dá o erro declarado sem limites de faixa | Cache do prefixo — cerca de 20,97 TB para um milhão de sequências de 4096 | Ideias; **não provadas** |
| **T7 — disputa aberta** (todos os seis) | — | É necessário um observador | — | Para o treinamento não há observador interessado | — | **Refutado** |

### 4.2. Melhor candidato para o passo de treinamento e suas limitações

**Não há verificação do próprio passo dentro de 20%, independente da parcela de conluio.** Este é um
resultado negativo geral, confirmado de lados diferentes: a escala `N·v`, o traço de 64 GB–2 TB por
passo, provas dezenas a centenas de vezes mais caras que o trabalho, o orçamento das operações
elemento a elemento.

Com a **base de pagamento inalterada**, restam dois caminhos: a repetição completa da transição
(referência, +100% por nó) e, a longo prazo, a prova obrigatória de todo o passo (T3). Para T3 são
necessários um grafo concreto, robustez comprovada da composição e um orçamento completo; hoje não há.

Com a **mudança da base de pagamento** (decisão do dono, seção 6, questão 1), o melhor candidato é a
combinação de T4 e ODU com as correções dos críticos:

1. O exame é escolhido por um farol externo estritamente após a fixação de todas as atualizações e a
   aceitação final do bloco.
2. O limiar é tomado de um limite estatístico com `ε` criptograficamente pequeno (como em T4), e não
   10%.
3. O exame é verificado por prova (estrutura da ODU), para que o preço não cresça com o número de nós.
4. As perdas são limitadas pela própria aritmética (probabilidade mínima no perfil) e não são
   truncadas; caso contrário, pagam-se atualizações prejudiciais.
5. A atribuição das duplicatas precisa ser resolvida sem uma cadeia sequencial de provas. Nenhum
   trabalho resolveu isso.

**Limitações.**

- Não é uma verificação do passo. O exame não vê os momentos do otimizador, não certifica a origem
  da atualização e não exclui o treinamento no próprio exame.
- Por D6, um passo falso não deve entrar no modelo. A melhoria no exame não prova a ausência de dano
  em solicitações raras nem de backdoors (Q4 em [OPEN_QUESTIONS](OPEN_QUESTIONS.md)). O candidato
  limita o ganho monetário, mas não o dano.
- Não se sabe se a melhoria honesta de uma atualização excede o limiar: o ruído da diferença de perdas
  `σ` não foi medido. Se não excede, os participantes honestos não recebem pagamento, e R6 é violado.
- Dispositivos fracos com melhoria pequena não passam o limiar; «toda a capacidade livre aprende»
  cumpre-se apenas como «aprende», não como «recebe pagamento».
- Relação com D9: o plano de treinamento já é derivado dos resultados do exame. Isso faz do exame
  parte do núcleo, mas não resolve a questão de se é possível pagar pela melhoria em vez do passo.

---

## 5. O que não está provado e como verificá-lo

### 5.1. O que não está provado

1. A coincidência de bits do perfil inteiro em placas de vídeo diferentes e entre a decodificação
   token a token e a passagem de toda a sequência em uma única placa (A1, questão Q2). Disso dependem
   o PPS, o M1, o certificado intervalar e qualquer repetição exata.
2. O tempo de verificação da resposta pronta em relação à geração em placas reais com lotes 1, 8, 32;
   a energia; o comportamento das camadas híbridas de atenção linear.
3. A qualidade e a velocidade do perfil inteiro do Qwen3.5-4B em relação ao usual.
4. O preço do certificado intervalar e do certificado do vencedor com pesos reais.
5. A disponibilidade dos dados da disputa, o limite de disputas falsas sem depósitos, a tempestividade
   e a censura do registro.
6. Para o pagamento pela melhoria: a magnitude da melhoria honesta contra o limiar, a regra de
   atribuição sem ganho de duplicatas, o limite de perdas sem truncamento, o preço da prova do exame.
7. Para a prova sucinta do passo: o orçamento completo de um passo e o limite de erro de ponta a ponta.
8. A configuração exata do Qwen3.5-4B e do modelo de cerca de 27B: todos os números dos trabalhos
   foram substituídos manualmente.

### 5.2. Experimentos mínimos

A decisão D5 autoriza o primeiro experimento: o Qwen3.5-4B inteiro na RTX 2060 do Linux doméstico
do mantenedor, no computador dele e, com consentimento, nos dispositivos de outros participantes
por meio de mini-agentes, após a etapa 0. Perfis, métricas e limiares são definidos antes da medição.
A coincidência de bits refere-se apenas às configurações testadas.

| № | Experimento | O que se mede | Refuta o candidato se |
|---|---|---|---|
| O1 (D5) | Qwen3.5-4B inteiro em duas placas de vídeo diferentes | Hashes dos logits e dos tokens em um mesmo conjunto de solicitações; primeiro token divergente, EOS, empates, contexto longo, solicitações com logits próximos | Ao menos um bit difere com a mesma especificação |
| O2 (D5) | Passagem de toda a sequência contra decodificação token a token em uma única placa | A mesma comparação de bits; separadamente para as camadas híbridas, se houver | Ao menos um bit difere |
| O3 (D5) | Velocidade: verificação da resposta pronta contra geração | Tempo com lotes 1, 8, 32 e combinações entrada/saída 128/32, 128/128, 500/500, 2000/1000; implementação do produto de atenção em 16 e 8 bits; memória, tráfego | A fração de verificação com lote 1 é maior que 5% |
| O4 (D5) | Velocidade do perfil inteiro contra o usual nas mesmas placas | Tokens por segundo, memória | A desaceleração torna o serviço desvantajoso (definir o limiar antes do experimento) |
| O5 (D5) | Qualidade do perfil inteiro contra o usual | O mesmo conjunto de tarefas | A perda de qualidade é maior que o limiar definido de antemão |
| O6 (fora de D5, precisa de autorização separada) | Ruído da melhoria de um único adaptador LoRA | Distribuição da diferença de perdas base/adaptador de posto 16 após um dia de treinamento, `σ` e `δ/σ` | A melhoria honesta é tipicamente menor que o limiar com um tamanho de exame admissível |
| O7 (fora de D5; a execução de sistemas de provas está atualmente proibida por uma restrição de pesquisa) | Preço da prova de um bloco forward em 4096 tokens | Coeficiente `P` | `P` é maior que cerca de 300 — então a ODU e a VYa-S não cabem (estimativa de claude2) |
| O8 (fora de D5) | Razão entre o preço da multiplicação no corpo e o MAC tensorial na RTX 2060 e na RTX 4090 | Coeficiente `R_f` | Decide todas as estimativas de Freivalds e GKR |
| O9 (fora de D5) | Energia da verificação | Joules por verificação e por geração | A fração por energia é maior que a referência |

### 5.3. Cálculos exatos que podem ser atribuídos a mini-agentes

São cálculos determinísticos sem medições. Para cada tarefa são fixados a versão do procedimento,
os bytes de entrada ou o gerador com limites de enumeração, os inteiros ou frações exatos, a
serialização da resposta e o SHA-256; o resultado é repetido em um segundo dispositivo. A coincidência
confirma a conta, mas não a semântica nem a desigualdade econômica.

| № | Tarefa | Parâmetros | O que decide |
|---|---|---|---|
| M1 | Relação do grafo pelo manifesto fixado do Qwen3.5-4B e do modelo de cerca de 27B (`config.json` publicado com hash) | Formas e tipos de todas as operações de preenchimento do contexto, geração, verificação da resposta e passo de treinamento; MAC, bytes das somas brutas, tempo de vida dos buffers; camadas híbridas; LoRA e treinamento completo | Esclarece os numeradores e denominadores de todas as estimativas |
| M2 | Tabela da fração de verificação `ρ(B)` pelo modelo «teto» | `L, d`, larguras de atenção e MLP, vocabulário, `P, T`, lote `B ∈ {1, 8, 32}`, largura de banda de memória, TOPS, frações do pico | Previsão para o experimento O3 |
| M3 | Limites de estouro do INT-canônico | Todos os acumuladores conforme a especificação, incluindo o produto de atenção até `T ≤ 32 768`, a soma dos quadrados do RMSNorm, o tamanho da probabilidade no softmax; variante com duas metades de 8 bits | Encontra uma entrada com estouro ou prova sua ausência |
| M4 | Tráfego exato do M1 | int32 brutos e traço da solicitação em uma grade (entrada, saída, modelo); com e sem recálculo das estimativas de atenção pelo pagador | Remove a divergência dos críticos sobre o tráfego do M1 |
| M5 | Onda de falsificações para esquemas por amostragem com `H > 0` | `π = m_s/(L+1)`, `H₀` inicial, `R`, teto de tarefas abertas; enumeração do tamanho e do número de ondas | O `H*` mínimo com o qual a falsificação antes da saída é desvantajosa |
| M6 | VYa-S: enumeração de estratégias de cópia e entradas degeneradas | Fração `f`, número de células `s`, pesos das células, número de verificações de vinculação `s'`; antes e depois da correção | O maior `Δ₀`; se a correção se sustenta |
| M7 | Economia da prova seletiva e da revelação na ODU e em T4 | `e/R`, `P`, margem `m`, número de chaves e candidatos | O maior `ε` admissível |
| M8 | Escala de T4 | `D(N)` com `K = N`, `n`, `a`, `ε` | Limite do número de proponentes para 20% |
| M9 | Preço da disputa falsa do I8 | Tráfego e computação da rede em função de `N`, `P + T`, do passo das impressões digitais `k` | Se é necessário um limite de disputas falsas e qual |
| M10 | Tabelas do limiar `t(n, ε, V̂)` | Hoeffding e Bernstein empírico com o termo `B`; grade `n, ε, B` | Exame mínimo |
| M11 | Truncamento das perdas | A maior fração paga de atualizações prejudiciais com `B, n, ε`; limite de perdas do INT-canônico como função da probabilidade mínima | Escolha de `B` sem pagar pelo dano |
| M12 | Atribuição em um modelo de fusão de brinquedo | Perdas linear-quadráticas, gradientes conhecidos; regras «separadamente», «deixar um», Shapley; duplicatas e duplicatas com ruído; frações exatas | Se existe uma regra sem ganho de duplicatas |
| M13 | Dicas e gadgets da prova sucinta | Número de valores com arredondamento, divisão e tabelas por token e camada; células, acessos a tabelas e compromissos por uma operação de arredondamento e softmax | Barreira 2.3 e estimativa de T3 |
| M14 | Pequenas enumerações para verificar fórmulas | Empacotamento posicional com `B = 8` e `B = 4` (repetição dos hashes); cadeia de 8 transições com escolha 2: 224 pares, 56 detectados, 168 não detectados; corpo F₅ e erro (1, −1): 5 passagens em 25 | Verificação da implementação dos modelos probabilísticos |
| M15 | Certificado do vencedor em matrizes estruturadas sintéticas | Linhas agrupadas em clusters, diferença de logits dada, empates, escala comum | Economia com distribuições diferentes; com pesos reais — após O1 |
| M16 | Certificado intervalar em prefixos fixados | Fração de saídas ambíguas `u`, número de recálculos completos, preço da preparação por número de solicitações | Se a aceleração cabe em 5% (depois de os pesos estarem disponíveis) |
| M17 | Passo de Gauss–Newton em um bloco pequeno | Matriz racional explícita `J`, identidade `⟨Jx, z⟩ = ⟨x, Jᵀz⟩`, comprimentos dos inteiros, número de refinamentos, empates | Preço do novo contrato |
| M18 | Cálculo dos pagamentos e recuperação | Enumeração finita: um número de tarefa, dois pais, bifurcação, desaparecimento da entrada, conluio de todos os designados, conta vazia | Não mais que um pagamento por resultado; nada é aplicado antes da aceitação |

---

## 6. Decisões exigidas por esta etapa

O conselho não toma decisões. Abaixo estão as questões com a recomendação do conselho. O dono
encarregou o mantenedor de resolvê-las; as decisões D18–D25 foram aceitas em 24 de novembro de
2026 e registradas em [ROADMAP](ROADMAP.md), seção 3. Cada decisão é indicada após a questão.

1. **Mudar a base de pagamento do treinamento para «pagamento pela melhoria comprovada»?** Por D2
   paga-se por um resultado verificável; a melhoria em um exame é formalmente um resultado
   verificável, mas é outro objeto, e não o passo executado. Três trabalhos (claude1, claude2, ds1)
   a consideram o principal candidato, e três (gpt1, gpt2, ds2) — outro contrato, e não uma
   verificação do passo. *Recomendação do conselho:* autorizar a investigação desse caminho como
   candidato a uma nova unidade de pagamento do treinamento, sem chamá-lo de verificação do passo.
   Decidir definitivamente após os cálculos M7, M8, M10–M12 e o experimento O6. Condições: farol
   externo após a fixação, `ε` criptograficamente pequeno, perdas sem truncamento, prova do exame,
   regra de atribuição sem ganho de duplicatas. Por D6, registrar que a melhoria não prova a ausência
   de dano.
   **Decidido — D18:** o caminho é investigado como candidato a uma nova unidade de pagamento do
   treinamento, mas não é aceito nem chamado de verificação do passo. A decisão de aceitação — após
   M7, M8, M10–M12 e o experimento O6 (ele está fora de D5 e exige autorização do dono). O modelo
   só é lançado pela regra D9. A busca de uma verificação do próprio passo (T3) continua.
2. **Um erro criptográfico pequeno é admissível?** Os requisitos o chamam de suposição. Os trabalhos
   claude1, claude2, ds2 e os críticos Claude e DeepSeek consideram que o erro `2⁻⁴⁰…2⁻¹²⁸` é
   compatível com D1 como expectativa, se a aleatoriedade é externa e imprevisível e cada tentativa
   custa mais que `ε·R`. Os trabalhos gpt1, gpt2 e o crítico ChatGPT: um erro pequeno não basta para
   D1, é necessário um limite inferior provado do preço da tentativa mais barata. ds1 considera que é
   necessário exatamente zero.
   *Recomendação do conselho:* aceitar o erro pequeno como suposição declarada diretamente sob três
   condições — farol externo estritamente após a aceitação final do bloco, proibição de Fiat–Shamir
   para a amostragem, limite inferior registrado do preço da tentativa. Sem essa decisão são
   impossíveis tanto o pagamento pela melhoria quanto as provas sucintas.
   **Decidido — D19:** o erro pequeno é admitido como suposição explícita sob essas três condições,
   não maior que `2⁻⁸⁰` por tentativa e com `ε·R` menor que o limite inferior registrado do preço da
   tentativa. A verificação por amostragem usual com erro `q^k` não é autorizada por isso.
3. **Qual farol externo e cuja confiança são admissíveis?** Sem uma fonte externa de aleatoriedade
   comum, com `q = 1` não funciona nenhum esquema com amostragem após a fixação (limite 2.1, item 7).
   As fontes ainda não foram escolhidas (ataque 1.5 e N13). *Recomendação do conselho:* escolher
   várias fontes independentes e registrar a confiança nelas como suposição.
   **Decidido — D20:** não menos que duas fontes públicas independentes, o valor é tomado em um
   momento designado de antemão após a fixação final, sem direito de omissão. As fontes concretas
   e o preço da influência sobre elas — na etapa 2. Não são incluídas antes da escolha de um esquema
   com amostragem.
4. **Aceitar que, para a resposta do modelo, uma verificação independente do conluio existe apenas
   no pagador que verifica por conta própria?** *Recomendação do conselho:* sim. Para o consumidor
   sem equipamento, a resposta é entregue com a marca «não verificado» (isso é admitido por D6), e a
   delegação da verificação é uma suposição dele próprio. Decidir separadamente como pagar ao executor
   por essa resposta sem violar D1: não há solução.
   **Decidido — D21:** sim. A rede não paga por uma resposta sem verificação. Um usuário sem
   equipamento pode designar ele mesmo um verificador; isso é uma suposição dele, e a rede não lhe
   promete D1. A garantia D1 para esse usuário permanece uma questão aberta.
5. **Autorizar mudanças no produto por uma verificação exata barata?** Aqui entram a escolha
   canônica do token por Gumbel-max (muda a distribuição em comparação com a amostragem usual
   top-p/top-k), o perfil inteiro exato (pode piorar a qualidade), tarefas com resultado verificável
   (fórmulas, testes) e novos otimizadores com certificado exato (Gauss–Newton, regressão de crista).
   *Recomendação do conselho:* autorizar como tipos separados de tarefas do plano, com contrato
   explícito, após os experimentos O5 e o cálculo M17.
   **Decidido — D22:** autorizar como tipos separados de tarefas do plano, com contrato explícito,
   após O5 e M17. A amostragem usual permanece disponível com a marca «não verificado».
6. **Como limitar as disputas falsas do pagador sem depósitos?** D8 limita as disputas pelo número de
   solicitações, mas a coalizão que paga as solicitações a si mesma contorna esse limite.
   *Recomendação do conselho:* calcular o preço da disputa falsa (M9) antes de decidir; o conselho não
   encontrou uma regra que não exija depósito.
   **Decidido — D23:** primeiro o cálculo M9. O PPS não é incluído enquanto não se escolher, para ele,
   uma regra de limitação de disputas falsas sem depósito.
7. **Guardar o texto cifrado da resposta no registro?** Sem isso, o executor pode reter a resposta.
   *Recomendação do conselho:* sim, cerca de 2–4 KB por resposta; isso está de acordo com D10.
   **Decidido — D24:** sim, o texto cifrado é gravado no registro em uma única entrada com a aceitação.
8. **O registro bilateral de D1 também é necessário para a falsificação parcial?** O trabalho claude2
   perguntava se é admissível uma falsificação que é pior que o trabalho honesto, mas melhor que a
   inação. O registro formal de D1 em [THREAT_MODEL](THREAT_MODEL.md), seção 1.5, já exige as duas
   desigualdades. *Recomendação do conselho:* não mudar; por isso a VYa-S e a PVYa na variante
   relativa foram rejeitadas.
   **Decidido — D25:** não mudar.

---

## 7. Quem fez o quê

O conselho de modelos trabalhou com os materiais do projeto, sem acesso à rede e sem experimentos.

- **Rodada 1, seis trabalhos independentes:** dois trabalhos ChatGPT (gpt1, gpt2), dois trabalhos
  DeepSeek (ds1, ds2), dois trabalhos Claude (claude1, claude2). Cada um analisou as direções da
  etapa 4 do roteiro, propôs mecanismos próprios e calculou seu preço. Programas aritméticos curtos
  foram executados por claude1, claude2, gpt1 e gpt2; gpt1 e gpt2 anexaram pequenas enumerações com
  hashes de controle.
- **Rodada 2, três críticas:** uma de ChatGPT, uma de DeepSeek e uma de Claude. Cada crítico leu todos
  os seis trabalhos, procurou contraexemplos e recalculou os números principais. Os críticos ChatGPT
  e DeepSeek repetiram as pequenas enumerações de gpt1 e gpt2 no processador; os hashes coincidiram.
- **Consolidação:** este documento foi elaborado por Claude a partir dos trabalhos e das críticas.
  Onde os críticos divergiram, está «controverso». Na consolidação, às conclusões foram aplicadas as
  decisões D6–D17, que os participantes não tinham; não foram acrescentadas novas avaliações nem
  números além dos trabalhos e das críticas.
