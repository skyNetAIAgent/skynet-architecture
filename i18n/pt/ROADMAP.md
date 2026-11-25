<!-- translation of docs/ROADMAP.md, source sha256: e04c1849e93c4065aafdb97330a2a708285d48546175f4847bdfd81e8506b881 -->

# Roteiro: defesa contra fraude

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · **Português** · [العربية](../ar/ROADMAP.md)

Situação em 23 de novembro de 2026 (atualizado após o lançamento da v0.2.2). Este é um **plano de trabalho, não uma promessa de resultado**. A marca `[x]`
significa «feito, e isso pode ser conferido no repositório ou nos registros da rede»; `[ ]` significa
«não feito». Os números marcados com [cálculo] foram obtidos por fórmula, não medidos. O roteiro é atualizado
a cada mudança de status.

## 1. Objetivo e critérios de prontidão

**Objetivo da etapa atual do projeto:** encontrar um modo de verificar a honestidade em que sejam cumpridos
ao mesmo tempo os requisitos obrigatórios ([REQUIREMENTS](REQUIREMENTS.md)):

- não se pode fraudar a rede: a fraude é inútil ou dá prejuízo, inclusive para um novato com conta vazia,
  em conluio e com muitas chaves;
- nenhum pagamento antecipado: nem depósitos, nem contribuições, nem multas;
- participar é vantajoso e a verificação da honestidade é barata. Valores de referência do acréscimo pela
  verificação: cerca de 5% do trabalho para solicitações ao modelo e cerca de 20% para o treinamento
  (não confirmados).

**O trabalho é considerado concluído quando houver tudo o que está listado:**

1. **Está registrado o que exatamente é garantido** (decisão D1): para o resultado da solicitação, a etapa de
   treinamento, o pagamento e o histórico; para conta vazia, número arbitrário de chaves, saída e conluio total
   dos verificadores da tarefa. O requisito admite «a fraude é inútil»; não é obrigatório provar prejuízo
   estrito em cada tentativa.
2. **Para cada ataque da tabela de ataques está registrada a regra pela qual o nó rejeita a declaração falsa
   e de quais dados ele faz isso.** Estão indicados separadamente a probabilidade de aceitação falsa, o dano
   à rede e o ganho líquido da coalizão em relação à inação e em relação ao trabalho honesto.
   Contraexemplo para a regra: casos honesto e falso em que o nó vê os mesmos dados.
   A amostragem, a baixa probabilidade de erro e o «haverá um observador honesto» são registrados como premissas.
3. **Foi calculado o preço completo da verificação** em relação à mesma tarefa sem verificação: o trabalho
   do executor e dos verificadores, memória, tráfego, armazenamento, escrita no registro, disputas, repetições
   após falhas. São deduzidos o ganho líquido de um participante com muitos recursos com eletricidade cara,
   o valor adicional que um participante com equipamento de baixo desempenho precisa pagar e o preço para o
   consumidor sem equipamento. A escrita e a disputa estão disponíveis a partir de conta zero; só se pode
   perder recompensas ainda não vencidas.
4. **Os cálculos são reproduzíveis:** estão anexadas a versão das regras e do núcleo, as entradas, os limites
   da enumeração, a saída e a impressão digital; o cálculo foi repetido em um segundo dispositivo. A repetição
   confirma o cálculo, mas não a correção do próprio modelo: esta é justificada separadamente.
5. **Foi medido o que não se pode estabelecer por raciocínio:** a coincidência do resultado bit a bit em
   placas de vídeo diferentes, a velocidade e a qualidade do modelo que usa aritmética inteira, o preço da
   disputa. Os perfis, as métricas e os limiares são definidos antes da medição.
6. **Os demais requisitos não são violados:** a rede funciona sem qualquer um dos nós ou locais, encontra-se
   após a parada total, as bases dos créditos são recuperadas; com a divisão da rede, o pagamento em disputa
   espera a história comum, a repetição não é paga duas vezes.

Um desfecho honesto também é um resultado: se para alguma classe de tarefas a verificação barata for
impossível, isso é mostrado por uma prova com a classe de tarefas e os dados do verificador nomeados,
e não pela ausência de ideias.

## 2. Onde estamos agora

| O quê | Status | Onde está registrado |
|---|---|---|
| Por assinaturas e respostas curtas não se pode estabelecer qual dispositivo trabalhou e por quanto tempo: intermediário, cache e placa ociosa fornecem os mesmos dados | Estabelecido por raciocínio | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), «O que já foi descartado» |
| A rede paga pelo resultado verificável, e não pelo recurso | Aceito (D2); a unidade do resultado e a condição de aceitação ainda não foram definidas | [CURRENT_DESIGN](CURRENT_DESIGN.md), seção 1 |
| Pagamento diferido em vez de depósito: o participante responde apenas pelo valor pendente | Aceito | CURRENT_DESIGN, seção 2 |
| Variante A: verificação por amostragem com débito | Especificação atual | CURRENT_DESIGN, seção 3 |
| Variante B: a rede paga apenas pelas tarefas verificadas, `1/p` vezes mais caras | Candidato principal; escolha após a comparação (D3) | CURRENT_DESIGN, seção 3 |
| Coincidência do resultado bit a bit por aritmética inteira | Medido em entradas curtas: processador, RTX 2060 e RTX 4070 Laptop produzem os mesmos bits para o Qwen3.5-4B com aritmética inteira (24 de novembro de 2026); contexto longo, velocidade e qualidade ainda não foram medidos | [EXPERIMENT_D5](EXPERIMENT_D5.md), seção 7 |
| Disputa por divisão ao meio com recálculo de uma etapa no registro | Medido para uma linha do modelo; para o modelo completo não foi construído | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Verificação do produto de matrizes com o auxílio de um vetor aleatório dentro da disputa | Candidato, há apenas estimativa calculada | CURRENT_DESIGN, seção 3 |
| Núcleo de verificação imutável, que não pode ser revogado por votação | Aceito (D4) | CURRENT_DESIGN, seção 8 |

**O que se sabe sobre a força da defesa.**

- Variante A, sem conluio: na família enumerada (duas ondas de falsificações, 92 milhões de estratégias),
  sair com falsificações não rende mais do que a saída comum [cálculo].
- Variante A, conluio: os primeiros pontos da grade em que sair com falsificações é lucrativo são — parcela
  de conluio de 87,5% (tarefas de tamanho arbitrário) e 89,0% (tarefas idênticas) com a regra «não mais de
  um terço em trabalho», 80% sem essa regra. O passo da grade é 0,002–0,02; outras famílias de estratégias
  não foram enumeradas [cálculo, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, sem conluio: com comparação exata, a falsificação não é paga.
- Variante B, conluio: `q` é a parcela do peso da coalizão entre os verificadores do modelo em questão.
  A falsificação é paga apenas se a tarefa for escolhida e todos os `k` verificadores estiverem em conluio.
  O pagamento médio por uma falsificação entregue é igual a `R·q^k` (`R` é o preço da tarefa) e não depende
  de `p` [cálculo]. Com `q = 1`, esse é o preço completo. Não há nada a debitar de um novato com conta vazia.
- Pagamento indevido nulo com conluio total dos verificadores não foi mostrado nem para a variante A, nem
  para a variante B. Ele é dado pela verificação de cada resultado pago por dados que qualquer nó verifica
  por conta própria. O recálculo completo acrescenta cerca de 100% de trabalho. Medições do piloto: a prova
  RISC Zero para uma linha do modelo levou 22 min 10 s para ser construída; a execução de oito linhas na
  zkVM foi cerca de 17.700 vezes mais lenta que o normal, sem construir a prova. Essas medições não dão um
  limite inferior geral do preço.
- Irregularidade da renda na variante B: com 6.000 tarefas por mês, verificação de 1 em 100 e custo de 95%
  do preço, a probabilidade de um mês com prejuízo é 33,10% [cálculo, FIRST_RUN].
- A primeira execução dos cálculos (702 porções) foi feita em um computador. Até 23 de novembro, o segundo
  dispositivo recalculou todas as 702 porções; todas coincidiram. Seus registros estão assinados pela chave
  `46000d30…` e disponíveis no nó completo. Os dois dispositivos pertencem aos mantenedores, portanto isso
  ainda não é uma confirmação por um participante independente.

**O que não está resolvido.**

1. Novato com conta vazia em conluio (variante B): ganho médio de `R·q^k` por tentativa, sem perdas.
2. «Muito tempo honesto, depois frauda em grande escala e sai»: a perda é limitada pelo valor pendente,
   o ganho cresce com o número de falsificações. As correções para a variante B foram propostas, mas não
   calculadas.
3. Fluxo de lixo de chaves gratuitas. A chave não custa nada; cobrar em trabalho de processador coloca
   os dispositivos fracos em situação pior.
4. Resultado usado antes da verificação. A resposta já foi lida pelo usuário, a etapa já entrou no
   treinamento; limitar os pagamentos não corrige isso. Na variante B, isso vale também para as tarefas
   não escolhidas.
5. Tarefas de treinamento pagas pela emissão de créditos: quem e por qual regra as aprova.
   Uma tarefa executada corretamente, mas auto-atribuída, não deve gerar créditos.
6. Modelo raro: o círculo de verificadores é pequeno, e o `q` para ele pode ficar próximo de um.
7. Disponibilidade dos dados e disputa por solicitação privada sem revelar a solicitação.
8. A coincidência bit a bit do modelo com aritmética inteira foi confirmada apenas em entradas curtas de
   três dispositivos; contexto longo, velocidade e qualidade não foram medidos.
9. Um sabotador que não precisa de lucro e o envenenamento dos dados de treinamento. A proteção econômica
   não age sobre eles.

## 3. Decisões

As decisões D1–D5 foram tomadas em 23 de novembro de 2026, e as D6–D25, em 24 de novembro de 2026 (por determinação do dono; as D18–D25, sobre questões da etapa 4, com justificativas em [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), seção 6).

| Nº | Questão | Decisão |
|---|---|---|
| D1 | O que é aceito como garantia | **O fraudador não obtém o que deseja.** Não se pode excluir as tentativas de fraude, mas toda tentativa deve ser inútil para quem a faz: o ganho esperado com a falsificação não é maior que zero em comparação com o trabalho honesto e com a inação, para qualquer coalizão, inclusive um novato com conta vazia e qualquer número de chaves. O objetivo é que o resultado falso não seja pago de forma alguma. Não se exige prejuízo estrito em cada tentativa. Um vazamento limitado, mas positivo (por exemplo, `R·q^k` para um novato na variante B) **não satisfaz** o critério e continua sendo um furo aberto |
| D2 | Base do pagamento | **Aceito: apenas o resultado verificável é pago.** Equipamento ligado, tempo de trabalho e potência declarada não são base do pagamento: a placa de vídeo pode ser carregada com algo alheio |
| D3 | Variante A ou B | **A decisão é tomada após a comparação nos mesmos ataques e ao mesmo preço (etapa 2).** O candidato principal é a variante B |
| D4 | Núcleo de verificação imutável | **Aceito em forma reforçada.** A verificação ocorre automaticamente, sem participação humana e sem votações. As regras de verificação não mudam por votação. Cada nó executa a verificação por conta própria segundo a impressão digital fixada das regras, portanto a substituição do algoritmo em um nó ou por um fornecedor do programa não muda a decisão dos demais. Aberto: como corrigir um erro no próprio núcleo (apenas com a transição para uma nova rede) e como o participante se convence de que seu programa corresponde à impressão digital publicada (compilação reproduzível). A chave de lançamento com que os miniagentes são assinados hoje é uma ferramenta de pesquisa; ela não deve existir na rede alvo |
| D5 | Primeira experiência com o Qwen3.5-4B com aritmética inteira | **Permitida:** a placa de vídeo RTX 2060 no Linux doméstico do mantenedor, o computador dele e, com consentimento, os dispositivos de outros participantes por meio dos miniagentes. É executada após a etapa 0 |
| D6 | O dano entra no D1 | **Sim** (decidido em 24 de novembro de 2026 por determinação do dono). «O fraudador não obtém o que deseja» refere-se não apenas aos créditos, mas também ao resultado: uma resposta falsa não deve ser entregue ao usuário como verificada, nem uma etapa falsa deve entrar no modelo. Por isso o resultado só é usado após uma verificação que não dependa da parcela de conluio, ou é explicitamente marcado como não verificado |
| D7 | Verificação que não depende da parcela de conluio, ou enfraquecimento do D1 | **É exigida uma verificação que não dependa da parcela de conluio** (24 de novembro de 2026). O D1 não é enfraquecido para «enquanto os que estão em conluio forem menos que q\*». A etapa 4 passa a ser a principal |
| D8 | Disputa a partir de conta zero | **Só podem disputar os verificadores designados por sorteio para essa tarefa e o usuário em relação à sua própria solicitação** (24 de novembro de 2026). Sem depósito; o fluxo de disputas é limitado pelo número de verificações e solicitações. Os demais comunicam a suspeita no quadro, sem direito de interromper o pagamento |
| D9 | Quem aprova o plano de treinamento | **Ninguém pessoalmente: o plano é derivado por uma regra fixada a partir do catálogo aberto e dos resultados do exame** (24 de novembro de 2026). Sem votações. Os créditos são emitidos apenas para tarefas do plano, uma única vez por conteúdo de tarefa |
| D10 | Vazamento de uma parte na troca | **É considerado violação do D1.** A troca de créditos e outros valores passa apenas pelo registro, com uma única entrada para ambas as partes, sem uma parte confiável fora do registro |
| D11 | Composição do núcleo imutável | **A verificação, a regra «só o verificado é pago», a regra de emissão de créditos, a disputa e as regras do registro.** As tarifas, a taxa da rede e o catálogo de modelos mudam apenas dentro dos limites fixados no núcleo |
| D12 | Tempo para o peso e janelas de verificação | **Tempo ativo da rede**, e não o calendário: enquanto a rede está parada, o peso não envelhece e a janela de verificação não corre |
| D13 | Admissão às tarefas na variante B | **É introduzido o caminho do novato da variante A:** o acesso às tarefas depende do valor pendente da chave. A escolha final entre A e B (D3) ocorre após a comparação |
| D14 | Preço da disputa | **Para o orçamento, toma-se uma rede de segunda camada com o registro mais barato.** A diferença entre o preço da disputa e o valor que se pode debitar do perdedor é paga pela taxa de rede dos consumidores, e não pela emissão de créditos |
| D15 | Verificações repetidas e de aprendiz | **O recálculo simples, que pode ser copiado, não é pago.** A verificação só é paga onde seu resultado não pode ser obtido copiando a resposta de outra pessoa |
| D16 | Falha honesta de hardware | **Não é punida como fraude:** a tarefa não é paga, o valor pendente não é perdido; o número dessas falhas por chave é limitado |
| D17 | Fonte do pagamento pelas solicitações na variante B | **Apenas dos pagamentos dos usuários**, sem emissão de créditos |
| D18 | Pagamento do treinamento por melhoria comprovada | **É investigado como candidato a uma nova unidade de pagamento do treinamento, mas não foi adotado.** Não é uma verificação de etapa nem uma prova da ausência de dano: o modelo é liberado apenas pela regra D9. A decisão de adoção vem depois dos cálculos M7, M8, M10–M12 e da experiência O6 (fora do D5, é preciso autorização do dono). A busca por uma verificação da própria etapa continua |
| D19 | Pequeno erro criptográfico | **É admitido como premissa explícita** sob três condições: aleatoriedade de um farol externo após a fixação final, amostragem não derivada dos dados do executor (sem Fiat–Shamir), com o limite inferior do preço da tentativa registrado e `ε·R` menor que ele. O erro não é maior que `2⁻⁸⁰` por tentativa. A verificação por amostragem comum com vazamento `q^k` não é resolvida por isso |
| D20 | Farol externo | **Não menos de duas fontes públicas independentes**; o valor é tomado em um momento designado previamente, após a fixação final, sem direito de omitir a consulta. As fontes e o preço da influência sobre elas são escolhidos na etapa 2; a confiança nelas é registrada como premissa. Não são incluídos antes da escolha do esquema com amostragem |
| D21 | Quem verifica a resposta do modelo | **A verificação da resposta que não depende do conluio fica apenas com o pagador, que verifica por conta própria.** A rede não paga por uma resposta sem verificação. Um usuário sem equipamento pode designar ele mesmo um verificador; essa é uma premissa dele, e a rede não promete o D1 para ele. A garantia para esse usuário continua sendo uma questão aberta |
| D22 | Mudanças de produto para uma verificação barata | **São permitidas como tipos separados de tarefas do plano com contrato explícito** (escolha canônica de token, perfil com aritmética inteira, tarefas com desfecho verificável, otimizadores exatos), depois da experiência O5 e do cálculo M17. A amostragem comum continua com o rótulo «não verificado» |
| D23 | Disputas falsas do pagador | **Primeiro, o cálculo M9.** A verificação pelo pagador não é ativada enquanto não for escolhida uma regra que limite disputas falsas sem depósito |
| D24 | Texto cifrado da resposta no registro | **Sim:** é registrado em uma única entrada, com o aceite, cerca de 2–4 KB por resposta |
| D25 | Registro bilateral do D1 | **Não muda:** a falsificação que é pior que o trabalho honesto, mas mais vantajosa que a inação, também viola o D1 |

**Ordem de trabalho.** Primeiro é concluída a etapa 0 — miniagentes e aplicativos para smartphones,
para que outras pessoas possam se juntar ao trabalho. Depois, as etapas 1–5 segundo este roteiro.

## 4. Etapas e lista de verificação

A etapa 0 é concluída primeiro. Depois, as etapas 1–4 acontecem ao mesmo tempo: são cálculos e
raciocínios. A etapa 5 (a experiência permitida pela decisão D5) acontece depois da etapa 0. A etapa 6
consolida os resultados.

### Etapa 0. Miniagentes e aplicativos para smartphones (executada primeiro)

**Objetivo da etapa.** Em cada plataforma suportada, a pessoa percorre o caminho «baixou → instalou →
executou» e, depois disso, o miniagente se atualiza sem participação humana, pega tarefas e devolve o
resultado. Sem conta, sem direitos de administrador, sem Python previamente instalado.
Cada passo foi verificado em um dispositivo real, e não apenas por testes automáticos.

**Pronto quando** para cada plataforma da lista abaixo: uma pessoa sem experiência percorreu o caminho
com uma única página de instruções; o agente nesse dispositivo recebeu por conta própria uma nova versão,
pegou por conta própria uma tarefa da nova lista, seu resultado apareceu no nó completo e coincidiu com
o resultado de outro dispositivo. Estão registrados o sistema, a arquitetura, as versões antes e depois
e o identificador do registro no nó.

Plataformas: Windows, Linux, Android (decisão de 23 de novembro de 2026). Para macOS e iOS, os
miniagentes não são feitos nem verificados. O comando de instalação para Linux possivelmente funciona
também no macOS, mas isso não é suportado. A versão para Windows é lançada sem assinatura de código:
na instalação, o Windows mostra o aviso do SmartScreen, que é preciso confirmar manualmente; a
autenticidade do arquivo é verificada pela impressão digital publicada e pela assinatura do projeto.

Já feito:

- [x] Repositório público, base imutável em nove idiomas (etiqueta `core-v1`).
- [x] Programa agente para Windows e Linux: tarefas e atualizações assinadas, verificações
      automáticas no CI (versão 0.2.0). Instalação com um único comando no terminal; é preciso
      Python 3.9+.
- [x] Resultados e [quadro de tarefas](BOARD.md) sem conta.
- [x] Primeiro nó completo, que guarda o histórico de registros.
- [x] Primeira tarefa de pesquisa «Defesa contra fraudadores» no quadro, em nove idiomas.
- [x] Aplicativo Android de teste 0.1.0 (verificado apenas no emulador).

**Passo 1. Confiabilidade da atualização (versão 0.2.1, sem novas tarefas)**

- [x] A primeira instalação verifica a assinatura da versão com uma chave embutida no próprio instalador,
      **antes** da execução do código baixado (antes, o agente baixado verificava a si mesmo).
- [x] Troca para a nova versão em uma única operação atômica: primeiro o novo diretório é preparado e
      verificado, depois um único ponteiro é alterado; o conjunto funcional anterior é preservado.
- [x] O maior número de versão aceito fica guardado fora dos diretórios de versão e também é verificado
      na reinstalação (proteção contra a reversão para uma versão antiga).
- [x] A chave do dispositivo, as configurações, o progresso e os resultados não enviados ficam guardados
      fora dos diretórios de versão e sobrevivem à atualização e à reinstalação.
- [x] Sem rede, o agente continua trabalhando na última versão funcional e repete a conexão com
      intervalo crescente.
- [x] Verificação automática no CI: arquivo substituído, chave alheia, número antigo, arquivo a mais,
      download interrompido e Python incompatível são rejeitados, e a versão funcional permanece.
- [x] **Verificação ao vivo no servidor:** a instalação 0.2.0 passou sozinha para a 0.2.2 em 23 de
      novembro de 2026, e a chave do dispositivo e o progresso foram preservados. No Linux doméstico, o
      agente foi instalado de novo com o novo instalador (0.2.2); a próxima versão verificará sua
      autoatualização.
- [x] Verificação ao vivo da autoatualização no Windows: a instalação do dono passou sozinha por
      0.2.2 → 0.3.0 → Go 1.0.1 (23 de novembro de 2026).

**Passo 2. Android: aplicativo sem token**

- [x] Novo APK 0.2.0 com o agente 0.2.2 embutido: publicação por registros assinados; a tela do token e as
      dicas sobre o token são removidas.
- [x] Corrigir a falsa reversão sem rede: antes, três execuções sem conexão marcavam a nova versão
      funcional como defeituosa. Agora a versão é confirmada por autoverificação local.
- [x] Uma vez por dia, o aplicativo verifica novas versões do APK, confere a impressão digital e a
      assinatura do projeto e oferece a instalação; a instalação é confirmada pela pessoa (assim funciona
      o Android fora da loja).
- [x] Início após a reinicialização segundo o interruptor do usuário (verificado no emulador).
- [x] Verificação da atualização sobre o APK 0.1.0 no emulador Android 14: os dados são preservados.
- [x] APK 0.4.1 (24 de novembro de 2026): corrigido o envio de resultados — o Android proibia o modo de
      armazenamento da chave do dispositivo; no emulador, 4 de 4 foram calculados e enviados sem token.
- [x] APK 0.4.2: o início após a reinicialização está ativado por padrão (verificado pela reinicialização
      do emulador). A antiga versão de teste 0.1.0, que pedia token, foi marcada como obsoleta.
- [ ] Verificação da oferta de um novo APK pelo próprio aplicativo (funcionará com a próxima versão do
      APK).
- [ ] **Verificação ao vivo em um telefone real** (é preciso um participante com telefone): instalação,
      funcionamento durante o carregamento, reinicialização, economia de energia do fabricante.

**Passo 3. Windows: instalador de um único arquivo**

- [x] `SkyNetAgentSetup.exe` é montado no GitHub Actions, sem assinatura de código; dentro dele,
      um Python embutível do python.org, o agente e a versão assinada. Ao lado são publicados a
      impressão digital dele e a assinatura do projeto. Instalação no perfil do usuário, sem direitos
      de administrador, funciona sem rede.
- [x] Atalhos no menu «Iniciar»: estado do agente, pausa, continuação, parada, remoção.
- [x] As caixas de seleção «iniciar agora» e «iniciar ao entrar» no instalador estão ativadas por padrão
      (desde 1.3.3); a escolha é preservada na atualização.
- [x] Remoção por «Aplicativos»; ao remover, é possível preservar a chave do dispositivo.
- [x] Verificação automática no CI em um Windows limpo sem Python: instalação, autoverificação, remoção.
- [x] Verificação ao vivo no computador de uma pessoa: o dono instalou o agente a partir do Releases
      (versão v0.2.2).

**Passo 4. Linux**

- [x] O instalador usa o Python 3.9+ do sistema e, se não houver, instala um Python portátil e
      confere sua impressão digital. Há também um instalador de um único arquivo sem rede (versão
      v0.2.2).
- [x] Desde 1.3.3, o instalador inicia o agente imediatamente, registra o serviço de usuário do systemd
      (início após a reinicialização) e tenta ativar o funcionamento sem entrar no sistema (linger);
      `--no-autostart` — apenas a instalação.
- [x] Desde 1.3.4, o agente encontra sozinho o nó completo em sua rede local (consulta por UDP, resposta
      apenas para endereços privados). Necessário onde o roteador não deixa passar de dentro da rede para
      o endereço externo do nó; antes isso era contornado com a configuração manual do endereço.
- [x] Verificação ao vivo da busca do nó na rede local: o agente 1.3.4, sem configuração manual, encontrou o nó e apareceu na página dos agentes (25 de novembro de 2026).
- [x] Verificação no CI: Debian 12 sem Python e Ubuntu 24.04 com Python; instalação ao vivo no Linux Mint.
- [ ] Verificação ao vivo com um participante sem vínculo com os mantenedores.

**Passo 5. Agente em Go em vez de Python (decisão do dono de 23 de novembro de 2026)**

O agente foi reescrito em Go: um único programa pequeno, Python não é necessário. O Python embutido e sua
atualização não são mais necessários, por isso o passo anterior «atualização do Python embutido» foi removido.

- [x] Assinaturas, tarefas, sete núcleos de cálculo, registros, Nostr, quadro, ciclo de trabalho, atualização
      pelo segundo canal (`agent/v2/release.json`), lançador, início automático — em Go, apenas
      a biblioteca padrão (o código foi escrito pelo ChatGPT e verificado pelo DeepSeek).
- [x] Os resultados em Go coincidem com os do Python bit a bit em todas as porções rápidas do padrão
      de referência e em todas as porções pesadas verificadas; a conferência de todas as 1.199 porções continua.
- [x] Compilação reproduzível: as mesmas impressões digitais dos programas na compilação no Windows e no Linux.
- [x] A ponte em Python 0.4.0 migra por conta própria os agentes instalados para Go, preservando a chave
      do dispositivo, o progresso e a fila. Transição ao vivo: o servidor, o Linux doméstico e o Windows do dono
      passaram sozinhos para o Go 1.0.1.
- [x] Instaladores em Go: Windows 4,7 MB, Linux em um único arquivo; aplicativo Android 0.3.0 com
      motor Go, cerca de 8 MB em vez de 40 (verificado no emulador Android 14).
- [x] Versões em Go 1.1.0–1.3.4 (24 de novembro de 2026): respostas do modelo local de IA, cálculos
      da etapa 4, página dos agentes, início automático, busca do nó na rede local; os agentes
      instalados se atualizavam sozinhos.
- [ ] Remover a ponte e as cópias em Python após duas versões verificadas em Go.

**Passo 6. Fluxo de tarefas**

- [x] Quatro novas tarefas de cálculo da etapa 2 (campanha de saída na variante B, vagas de aprendiz,
      loteria com parcela de verificação ajustada, certificado do token vencedor) — novos núcleos
      embutidos do agente 0.3.0, 515 porções na lista de tarefas nº 2. A matemática foi conferida de
      forma independente por outro método em 111 pontos. O certificado em matrizes aleatórias não traz
      economia (cerca de 0,8% de trabalho extra), por isso foram mantidas 20 porções como base de
      comparação com os pesos do modelo real.
- [x] As novas tarefas exigem o agente 0.3.0 ou superior; o agente antigo pula a tarefa incompatível
      e continua o trabalho (verificado por teste).
- [ ] Quando todas as tarefas estão calculadas, o agente espera e pega por conta própria a lista seguinte.
- [ ] O coletor de resultados trabalha por agendamento no nó completo e publica um resumo.
- [ ] Confirmação independente de todas as 702 porções da primeira lista. O segundo dispositivo (servidor
      dos mantenedores) recalculou todas as 702, todas coincidiram; ainda não há um participante sem
      vínculo com os mantenedores.

**Passo 7. Piloto com outras pessoas**

- [x] Página [«Como se conectar»](CONNECT.md) em nove idiomas: um link para cada sistema.
- [x] Página dos agentes online no nó completo: `http://62.213.14.254:8790/agents` — sistema operacional,
      processador, RAM, placas de vídeo, versão, porções; sem IP e nomes de computadores. O agente informa
      sobre si a cada 2 minutos; 5 minutos de silêncio o removem da lista (agente 1.3.0+).
- [ ] Um participante sem vínculo com os mantenedores em cada plataforma; os critérios de prontidão da
      etapa estão cumpridos.
- [ ] Segundo e terceiro nós completos com donos diferentes.

**Passo 8. Agentes de IA**

- [x] O agente retira sozinho as novas tarefas do quadro e as repassa ao modelo local do participante; a
      resposta é enviada apenas depois da aprovação por uma pessoa. O texto da tarefa é tratado como não
      confiável (agente 1.1.0, desativado por padrão).
- [ ] Instruções para o assistente de IA: como pegar uma tarefa do quadro, entregar o relatório e verificar
      o de outra pessoa.
- [ ] Relatório para uma tarefa do quadro feito por um participante sem vínculo com os mantenedores.

**Decisões do dono sobre a etapa 0** (23 de novembro de 2026): macOS e iOS não são feitos; a versão
para Windows é lançada sem assinatura de código.

### Etapa 1. Formulação precisa

- [x] As decisões D1 e D2 foram tomadas e registradas (seção 3).
- [ ] Para uma solicitação aberta e uma etapa de treinamento, estão registrados: a regra de aceitação,
      a aritmética, a base da emissão de créditos, o momento de fixação do resultado em relação ao sorteio
      e o momento em que o resultado pode ser usado.
- [x] Modelo do adversário em um único documento: [THREAT_MODEL](THREAT_MODEL.md), seção 1 (conselho de
      seis modelos e três críticos, 24 de novembro de 2026).
- [x] A tabela de ataques analisados foi publicada em nove idiomas com o status de cada ataque para as
      variantes A e B: 60 ataques da especificação e 32 novos. A discrepância entre 59 e 60 foi
      explicada: no resumo faltou a linha 1.9 («não é ataque»).
- [x] Para cada ataque está registrado por quais dados verificáveis de forma independente o nó rejeitará
      a declaração falsa em conluio do executor e dos verificadores. Resultado: nem a variante A nem a
      variante B cumprem D1 literalmente; o ganho monetário é possível em 24 linhas de A e 25 linhas de B
      [cálculo].
- [x] Decisões sobre todas as doze perguntas da seção 5 do [THREAT_MODEL](THREAT_MODEL.md): D6–D17.

Pronto quando: qualquer participante puder nomear pela tabela um ataque não fechado e conferir isso.

### Etapa 2. Economia: cálculos executados pelos miniagentes

Cada tarefa é um modelo exato com uma grade finita de entradas; as probabilidades e as somas são calculadas
como frações exatas, e a impressão digital de cada porção é conferida entre os dispositivos.

- [x] Variante A, saída com falsificações: primeira execução.
- [x] Variante B, irregularidade da renda com parcela de verificação constante: primeira execução.
- [ ] Confirmação independente dos dois cálculos (ver etapa 0).
- [ ] **Campanha de saída na variante B.** Entradas: valor pendente `H₀`, preço `R`, parcela de verificação
      `p`, conluio `q` e `k`, teto de tarefas simultâneas `C`, número de ondas `T`. Uma única falsificação
      pega zera todo o valor pendente, inclusive os ganhos da onda. Encontrar o maior pagamento esperado
      acima de `H₀`, inclusive com `H₀ = 0`, `q = 0` e `q = 1`.
- [ ] **Vagas de aprendiz.** Por época, `S` vagas são distribuídas entre `n` chaves honestas e `m` chaves
      da coalizão. Encontrar o vazamento esperado ao longo de `E` épocas e a parcela de vagas que fica com
      os novatos honestos, com o crescimento de `m`.
- [ ] **Loteria com parcela de verificação ajustada.** Para `N` tarefas por mês, tomar o menor `p` em que,
      em média, não menos de 60 tarefas são pagas. Encontrar a probabilidade de mês e de trimestre com
      prejuízo, a probabilidade de um mês sem um único pagamento e o número de recálculos para a rede.
- [ ] **Certificado do token vencedor** (ver etapa 4): número de operações de verificação em relação ao
      recálculo completo da camada de saída em um conjunto dado de entradas.
- [ ] Fórmula do preço completo da verificação para três tipos de participantes; depois da etapa 5,
      as medições são inseridas nela.
- [ ] Comparação das variantes A e B nos mesmos ataques e ao mesmo preço; em seguida, a decisão D3.
      Um desfecho possível: as duas variantes permanecem como pesquisa.

Pronto quando: para cada variante houver uma tabela «parcela de conluio → maior ganho esperado do fraudador»,
recalculada em pelo menos dois dispositivos independentes.

### Etapa 3. Fechar os furos conhecidos

- [ ] **Novato com conta vazia.** Candidato: as primeiras tarefas do novato são tais que qualquer nó as
      verifica exatamente por conta própria, e só depois disso a recompensa e o peso são creditados. Opção
      reserva: orçamento comum de pagamentos de aprendiz por época; ele limita o vazamento, mas não o torna
      nulo, e o conluio pode ocupar todas as vagas.
- [ ] **«Muito tempo honesto, depois frauda em grande escala».** Candidato: teto sobre a soma de todos os
      compromissos abertos da chave, contando os maiores ganhos possíveis. Isso é o limite de uma onda, não
      um vazamento nulo.
- [ ] **Lixo de chaves gratuitas.** Candidato: o nó aceita dados apenas por números de tarefa permitidos,
      limita o tamanho, a fila e o trabalho por época. O canal ainda pode ser preenchido; não foi obtido
      um lugar garantido para o novato honesto com um número arbitrário de chaves.
- [ ] **Resultado usado antes da verificação.** Candidato: verificar o bloco da resposta antes da entrega;
      manter a etapa de treinamento em um ramo separado e promover apenas o descendente verificado. Preço:
      atraso e memória.
- [ ] Tarefas de treinamento: regra de aprovação sem um participante com direitos especiais.
- [ ] Modelo raro: limiar derivado da distribuição do peso, abaixo do qual a rede não paga pelo modelo.
- [ ] Verificador preguiçoso e reapresentação de um resultado conhecido: compromissos ocultadores com
      revelação, crédito único pelo conteúdo.
- [ ] Falha de equipamento de um participante honesto: regra que não dá ganho ao fraudador.
- [ ] Disponibilidade dos dados e disputa por solicitação privada sem revelação.
- [ ] Janela de disputa na parada da rede, proteção contra histórico desatualizado, divisão da rede.

Pronto quando: para cada item forem publicados uma construção com premissas, um ataque a ela e o preço,
ou um contraexemplo, ou o status «aberto» com o motivo.

### Etapa 4. Busca por uma garantia que não dependa da parcela de conluio

Busca-se uma verificação que cada nó executa por conta própria, de modo que a concordância dos verificadores
não decida nada. As direções não foram aprovadas. Para cada uma é preciso indicar as operações verificadas,
os dados, a probabilidade de erro e o preço de uma solicitação ou etapa inteira; em seguida, levá-la a uma
construção ou fechá-la com um contraexemplo.

- [x] O conselho de modelos (seis trabalhos e três críticas) analisou todas as direções; o resultado e as
      tarefas para os miniagentes estão em [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), 24 de novembro de 2026.
- [x] Primeiros cálculos exatos para os miniagentes: M8, M10, M12 e M14 da seção 5.3 do compêndio
      ([STAGE4_KERNELS](STAGE4_KERNELS.md)), agente 1.2.0, lista de tarefas nº 3. Os cálculos M5, M7 e
      M18 foram adiados: os trabalhos não têm regras suficientes para defini-los de forma inequívoca.
- [ ] **Tarefas com um sinal exato e barato de correção.** Exemplo: para a regressão ridge, o nó verifica
      a condição de ótimo em uma única passada pelos dados. Pergunta: qual parcela do trabalho da rede se
      encaixa em tais tarefas. Começar por essa direção: ela dá pagamento indevido nulo. *Resultado:* mantém-se
      para uma classe estreita de tarefas; a parcela desse trabalho é desconhecida.
- [x] **Verificação de cada produto de matrizes com o auxílio de um vetor aleatório** em vez do recálculo.
      O vetor é escolhido depois da fixação do resultado; a probabilidade de deixar passar um erro não
      depende do conluio. É vantajoso para lotes grandes; na geração de um token por vez não há ganho. As
      demais operações (arredondamento, ativações, cache, otimizador) precisam ser verificadas separadamente.
      *Resultado:* refutado como verificação barata pelo nó da rede (esbarra no tráfego); mantém-se como
      verificação do pagador com canal rápido.
- [ ] **Verificação da resposta pronta por uma única passada do modelo** com perfil exato e aleatoriedade
      definida na tarefa. O número de operações é da mesma ordem que o da geração; se isso cabe em 5% não
      foi estabelecido. *Resultado:* melhor candidato para a resposta do modelo — verificação pelo pagador,
      1,2–3,8% na geração de uma resposta por vez [cálculo]; aguarda a experiência D5 e a decisão D23.
- [x] **Tabelas de somas parciais exatas para camadas imutáveis:** o nó deriva uma vez as tabelas a partir
      dos pesos e depois obtém a saída da camada por leituras e somas. Aplicável também a um único token;
      esbarra no volume de memória. *Resultado:* refutado por cálculo.
- [x] **Certificado do token vencedor** para um vocabulário grande: o executor entrega a cobertura do
      vocabulário em grupos, o nó verifica os limites superiores e desce a tokens individuais apenas onde o
      limite não separa o vencedor. No pior caso, todo o vocabulário é verificado. *Resultado:* mantém-se
      como parte da verificação da escolha gulosa.
- [x] **Etapa de treinamento como fórmula exata de atualização:** os nós guardam e verificam não a nova
      matriz de pesos, mas os multiplicadores da atualização. Derivado apenas para a camada linear com
      SGD simples. *Resultado:* refutado como verificação da etapa.
- [x] **Disputa aberta a qualquer participante durante a janela.** Garantia condicional: é preciso pelo
      menos um observador que tenha recebido os dados e conseguido contestar. Quem paga a observação com
      conta vazia não está resolvido. Deixar como reserva. *Resultado:* refutado como verificação independente
      do conluio.
- [ ] **Pagamento pela melhoria medida do modelo** em tarefas escolhidas depois da fixação dos pesos. Muda
      a base do pagamento e exige uma decisão separada. Serve para a seleção de versões do modelo. *Resultado:*
      único caminho sobrevivente para o treinamento, com correções; é investigado conforme o D18.
- [ ] **Provas de computação para o treinamento (sumcheck, GKR)** para uma única etapa determinada:
      orçamento completo com faixas, arredondamento e vinculação da entrada à tarefa. *Resultado:* mantém-se
      como direção; arranjos concretos foram refutados, 20% não foram demonstrados.
- [x] **Limite inferior:** mostrar quais classes de verificações não podem ser sem erro. Início: um conjunto
      fixo de verificações lineares em número menor que o tamanho do resultado sempre deixa passar algum
      erro; permanecem abertas a aleatoriedade fresca e as entradas com estrutura conhecida. *Resultado:*
      os limites que se mantiveram foram publicados em [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), seção 2.
- [ ] Ideias dos participantes e dos assistentes de IA do quadro: cada uma passa pela mesma análise,
      inclusive o caso `q = 1`.

Pronto quando: para cada direção forem publicados uma construção com orçamento, um contraexemplo ou um
limite provado. Considera-se encontrada a construção que cumpre todos os critérios da seção 1.

### Etapa 5. Fundamentos que só se estabelecem por experiência (permitidos por D5)

- [x] Plano da experiência: perfil com aritmética inteira do Qwen3.5-4B, protocolos O1–O5 e critérios de
      refutação antes da execução — [EXPERIMENT_D5](EXPERIMENT_D5.md), 24 de novembro de 2026. A segunda
      placa de vídeo é uma RTX 4070 Laptop no computador do dono.
- [x] Preparação (P0) e perfil v2: o modelo foi conferido com o código-fonte oficial; no processador,
      o perfil com aritmética inteira escolhe o mesmo token que o modelo oficial em 90 de 90 posições
      (correlação dos logits de 0,9996). O primeiro perfil v1 perdia precisão e foi substituído.
- [x] Entradas curtas: processador, RTX 2060 (Linux) e RTX 4070 Laptop (Windows) produzem os mesmos
      bits — 242 milhões de logits, 976 tokens e 37 mil hashes de estados por dispositivo; a geração
      por token e a passada por uma resposta pronta coincidem (O1 e O2, 24 de novembro de 2026).
- [x] Outra arquitetura: a AMD Radeon RX 580 (OpenCL, Mesa) e a NVIDIA via OpenCL produzem os mesmos bits que a versão CUDA e o processador, nas mesmas entradas curtas (25 de novembro de 2026).
- [x] Contexto longo (512 + 64, 2048 + 256, 4096 + 64 tokens): RTX 2060 (CUDA e OpenCL) e RTX 4070 Laptop
      produzem os mesmos bits; a geração coincide com a passada por uma resposta pronta (25 de novembro de 2026).
      RX 580: a geração coincide, a passada por uma resposta longa é interrompida pelo driver — é preciso
      fragmentar o núcleo de atenção.
- [x] Fração do tempo de verificação da resposta em relação à geração (O3): 0,10–0,40 com lote 1 na RTX 2060
      e na RTX 4070 Laptop — o limiar de 5% é refutado para a implementação atual (25 de novembro de 2026).
- [x] Sua velocidade em relação ao perfil comum (O4): na RTX 2060, 1,5–1,8 vezes mais lenta que o llama.cpp
      Q8_0 com lote 1, e 2,5–2,8 vezes mais lenta com lote 8 (25 de novembro de 2026).
- [x] Conselho de modelos sobre a verificação «não pelo método direto» (previsão de fraude, anomalias,
      verificação por amostragem, jogos de inspeção): [STRATEGY_SEARCH](STRATEGY_SEARCH.md), 25 de novembro de 2026.
- [ ] Sua qualidade em relação ao perfil comum no mesmo conjunto de tarefas.
- [ ] Planos de medição separados (fora do D5): energia da verificação, treinamento com aritmética inteira.
- [ ] Preço da disputa no registro para o modelo completo. Antes dela são necessários a escolha do
      blockchain, a máquina de referência do modelo completo, a vinculação dos dados de entrada, do
      comprimento e do caminho da computação.

Pronto quando: cada número foi medido, as condições da medição foram registradas e um segundo participante
repetiu a medição. A coincidência dos bits vale apenas para as configurações testadas.

### Etapa 6. Consolidação e aceitação

- [x] Decisão D4 sobre o núcleo imutável (seção 3).
- [ ] A composição do núcleo e o modo pelo qual o participante se convence de que seu programa corresponde
      à impressão digital publicada.
- [ ] Atualizar o CURRENT_DESIGN e a tabela de ataques com os resultados das etapas 1–5.
- [ ] Uma declaração rastreada no papel desde a autorização da tarefa até o uso do resultado, incluindo
      recusa, repetição e divisão da rede.
- [ ] Revisão aberta da construção final: conselho de modelos e tarefa no quadro.
- [ ] Para cada requisito foram publicados uma prova, uma medição, um contraexemplo ou o status «aberto».
      Verificação pelos seis critérios da seção 1.

## 5. Como o trabalho acontece

1. O item da lista de verificação vira uma tarefa: computacional (calculada pelos miniagentes, verifica-se
   se os resultados das execuções coincidem) ou de pesquisa (publicada no quadro).
2. Os participantes e seus assistentes de IA entregam relatórios. O relatório só é aceito se puder ser
   verificado: por recálculo, contraexemplo ou referência à fonte. O número de chaves concordantes não
   prova nada; a decisão do autor da tarefa no quadro não confirma o cálculo.
3. Com o resultado da verificação, a tarefa é fechada, refinada ou gera novas tarefas.
4. A mudança de status é registrada neste roteiro e no CURRENT_DESIGN em uma única edição, com data.

## 6. O que este roteiro não promete

- Que a solução exista nas condições dadas. Isso é objeto de busca.
- Prazos. O projeto não tem executores pagos; a velocidade depende dos participantes.
- Recompensas pela participação na concepção do sistema.
