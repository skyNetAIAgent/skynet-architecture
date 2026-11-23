<!-- translation of docs/ROADMAP.md, source sha256: 3060afa02f0adb73bcb1a9c7822d84ff2efe0f1ce1c8c105af2eda79e7dda071 -->

# Roteiro: defesa contra fraude

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · **Português** · [العربية](../ar/ROADMAP.md)

Situação em 23 de novembro de 2026. Este é um **plano de trabalho, não uma promessa de resultado**. A marca `[x]`
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
| Coincidência do resultado bit a bit por aritmética inteira | Candidato, não medido | OPEN_QUESTIONS, Q2 |
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
- A primeira execução dos cálculos (702 porções) foi feita em um computador. Até 22 de novembro, o segundo
  dispositivo recalculou 40 porções; todas coincidiram. Seus registros estão assinados pela chave `46000d30…`
  e disponíveis no nó completo. As outras 662 porções não foram confirmadas de forma independente.

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
8. A coincidência bit a bit e a velocidade do modelo que usa aritmética inteira não foram medidas.
9. Um sabotador que não precisa de lucro e o envenenamento dos dados de treinamento. A proteção econômica
   não age sobre eles.

## 3. Decisões

As decisões D1–D5 foram tomadas em 23 de novembro de 2026.

| Nº | Questão | Decisão |
|---|---|---|
| D1 | O que é aceito como garantia | **O fraudador não obtém o que deseja.** Não se pode excluir as tentativas de fraude, mas toda tentativa deve ser inútil para quem a faz: o ganho esperado com a falsificação não é maior que zero em comparação com o trabalho honesto e com a inação, para qualquer coalizão, inclusive um novato com conta vazia e qualquer número de chaves. O objetivo é que o resultado falso não seja pago de forma alguma. Não se exige prejuízo estrito em cada tentativa. Um vazamento limitado, mas positivo (por exemplo, `R·q^k` para um novato na variante B) **não satisfaz** o critério e continua sendo um furo aberto |
| D2 | Base do pagamento | **Aceito: apenas o resultado verificável é pago.** Equipamento ligado, tempo de trabalho e potência declarada não são base do pagamento: a placa de vídeo pode ser carregada com algo alheio |
| D3 | Variante A ou B | **A decisão é tomada após a comparação nos mesmos ataques e ao mesmo preço (etapa 2).** O candidato principal é a variante B |
| D4 | Núcleo de verificação imutável | **Aceito em forma reforçada.** A verificação ocorre automaticamente, sem participação humana e sem votações. As regras de verificação não mudam por votação. Cada nó executa a verificação por conta própria segundo a impressão digital fixada das regras, portanto a substituição do algoritmo em um nó ou por um fornecedor do programa não muda a decisão dos demais. Aberto: como corrigir um erro no próprio núcleo (apenas com a transição para uma nova rede) e como o participante se convence de que seu programa corresponde à impressão digital publicada (compilação reproduzível). A chave de lançamento com que os miniagentes são assinados hoje é uma ferramenta de pesquisa; ela não deve existir na rede alvo |
| D5 | Primeira experiência com o Qwen3.5-4B com aritmética inteira | **Permitida:** a placa de vídeo RTX 2060 no Linux doméstico do mantenedor, o computador dele e, com consentimento, os dispositivos de outros participantes por meio dos miniagentes. É executada após a etapa 0 |

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
- [x] O maior número de versão aceito fica guardado fora dos diretórios de versão e também é verificado
- [x] A chave do dispositivo, as configurações, o progresso e os resultados não enviados ficam guardados
- [x] Sem rede, o agente continua trabalhando na última versão funcional e repete a conexão com
- [x] Verificação automática no CI: arquivo substituído, chave alheia, número antigo, arquivo a mais,
- [ ] **Verificação ao vivo:** instalações 0.2.0 no Windows, no Linux doméstico e no servidor migram
      sozinhas para a 0.2.1; a chave do dispositivo e o progresso são preservados.

**Passo 2. Android: aplicativo sem token**

- [ ] Novo APK com o agente 0.2.1 embutido: publicação por registros assinados; a tela do token e as
      dicas sobre o token são removidas.
- [ ] Corrigir a falsa reversão sem rede: hoje três execuções sem conexão marcam a nova versão funcional
      como defeituosa. Confirmar a versão por autoverificação local.
- [ ] Uma vez por dia, o aplicativo verifica novas versões do APK, confere a impressão digital e a
      assinatura do projeto e oferece a instalação; a instalação é confirmada pela pessoa (assim funciona
      o Android fora da loja).
- [ ] Início após a reinicialização segundo o interruptor do usuário.
- [ ] Verificação da atualização sobre o APK 0.1.0 no emulador: o progresso e a chave são preservados.
- [ ] **Verificação ao vivo em um telefone real** (é preciso um participante com telefone): instalação,
      funcionamento durante o carregamento, reinicialização, economia de energia do fabricante.

**Passo 3. Windows: instalador de um único arquivo**

- [ ] `SkyNetAgentSetup.exe` é montado no GitHub Actions, sem assinatura de código; dentro dele,
      um Python embutível do python.org, o agente e a versão assinada. Ao lado são publicados a
      impressão digital dele e a assinatura do projeto. Instalação no perfil do usuário, sem direitos
      de administrador, funciona sem rede.
- [ ] Janela de status: se o agente está trabalhando, o que ele calcula, pausa, saída.
- [ ] Caixa de seleção «iniciar ao entrar» no instalador; a escolha é preservada na atualização.
- [ ] Remoção por «Aplicativos»; ao remover, é possível preservar a chave do dispositivo.
- [ ] Verificação em um Windows limpo, sem Python, em um perfil com caracteres cirílicos e espaços no
      nome.

**Passo 4. Linux**

- [ ] O instalador usa o Python 3.9+ do sistema e, se não houver, baixa um Python portátil e confere sua
      impressão digital.
- [ ] Serviço de usuário do systemd com o consentimento do usuário; trabalhar sem entrar no sistema é
      uma caixa de seleção à parte.
- [ ] Verificação no Linux Mint, Ubuntu e Debian.

**Passo 5. Atualização do Python embutido e dos invólucros**

- [ ] Descrição assinada do conjunto para cada sistema e arquitetura: versões e impressões digitais do
      Python, do instalador e do invólucro. O agente atualiza também o Python, e não apenas os próprios
      arquivos.

**Passo 6. Fluxo de tarefas**

- [ ] Quatro novas tarefas de cálculo da etapa 2 (campanha de saída na variante B, vagas de aprendiz,
      loteria com parcela de verificação ajustada, certificado do token vencedor) — novos núcleos
      embutidos; cada uma com uma porção de referência e impressão digital esperada.
- [ ] O código dos núcleos é lançado antes da lista de tarefas que os exige. O agente antigo pula a
      tarefa incompatível e continua o trabalho.
- [ ] Quando todas as tarefas estão calculadas, o agente espera e pega por conta própria a lista seguinte.
- [ ] O coletor de resultados trabalha por agendamento no nó completo e publica um resumo.
- [ ] Confirmação independente de todas as 702 porções da primeira lista de tarefas (hoje 40).

**Passo 7. Piloto com outras pessoas**

- [ ] Página «Como se conectar» em nove idiomas: um link para cada sistema.
- [ ] Um participante sem vínculo com os mantenedores em cada plataforma; os critérios de prontidão da
      etapa estão cumpridos.
- [ ] Segundo e terceiro nós completos com donos diferentes.

**Passo 8. Agentes de IA**

- [ ] O agente retira sozinho as novas tarefas do quadro e as repassa ao modelo local do participante; a
      resposta é enviada apenas depois da aprovação por uma pessoa. O texto da tarefa é tratado como não
      confiável.
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
- [ ] Modelo do adversário em um único documento: conluio, muitas chaves, saída, aluguel de capacidade;
      o que conta como ganho do fraudador e o que conta como dano à rede.
- [ ] A tabela de ataques analisados foi publicada no repositório em nove idiomas com o status de cada
      ataque para as variantes A e B. Antes da publicação, conferir as linhas: no resumo do CURRENT_DESIGN
      a soma das categorias é 18 + 6 + 19 + 16 = 59, enquanto são declarados 60.
- [ ] Para cada ataque está registrado por quais dados verificáveis de forma independente o nó rejeitará
      a declaração falsa em conluio do executor e dos verificadores.

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
      um lugar garantido para o novato honesto quando o número de chaves na rede é arbitrário.
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

- [ ] **Tarefas com um sinal exato e barato de correção.** Exemplo: para a regressão ridge, o nó verifica
      a condição de ótimo em uma única passada pelos dados. Pergunta: qual parcela do trabalho da rede se
      encaixa em tais tarefas. Começar por essa direção: ela dá pagamento indevido nulo.
- [ ] **Verificação de cada produto de matrizes com o auxílio de um vetor aleatório** em vez do recálculo.
      O vetor é escolhido depois da fixação do resultado; a probabilidade de deixar passar um erro não
      depende do conluio. É vantajoso para lotes grandes; na geração de um token por vez não há ganho. As
      demais operações (arredondamento, ativações, cache, otimizador) precisam ser verificadas separadamente.
- [ ] **Verificação da resposta pronta por uma única passada do modelo** com perfil exato e aleatoriedade
      definida na tarefa. O número de operações é da mesma ordem que o da geração; se isso cabe em 5% não
      foi estabelecido.
- [ ] **Tabelas de somas parciais exatas para camadas imutáveis:** o nó deriva uma vez as tabelas a partir
      dos pesos e depois obtém a saída da camada por leituras e somas. Aplicável também a um único token;
      esbarra no volume de memória.
- [ ] **Certificado do token vencedor** para um vocabulário grande: o executor entrega a cobertura do
      vocabulário em grupos, o nó verifica os limites superiores e desce a tokens individuais apenas onde o
      limite não separa o vencedor. No pior caso, todo o vocabulário é verificado.
- [ ] **Etapa de treinamento como fórmula exata de atualização:** os nós guardam e verificam não a nova
      matriz de pesos, mas os multiplicadores da atualização. Derivado apenas para a camada linear com
      SGD simples.
- [ ] **Disputa aberta a qualquer participante durante a janela.** Garantia condicional: é preciso pelo
      menos um observador que tenha recebido os dados e conseguido contestar. Quem paga a observação com
      conta vazia não está resolvido. Deixar como reserva.
- [ ] **Pagamento pela melhoria medida do modelo** em tarefas escolhidas depois da fixação dos pesos. Muda
      a base do pagamento e exige uma decisão separada. Serve para a seleção de versões do modelo.
- [ ] **Provas de computação para o treinamento (sumcheck, GKR)** para uma única etapa determinada:
      orçamento completo com faixas, arredondamento e vinculação da entrada à tarefa.
- [ ] **Limite inferior:** mostrar quais classes de verificações não podem ser sem erro. Início: um conjunto
      fixo de verificações lineares em número menor que o tamanho do resultado sempre deixa passar algum
      erro; permanecem abertas a aleatoriedade fresca e as entradas com estrutura conhecida.
- [ ] Ideias dos participantes e dos assistentes de IA do quadro: cada uma passa pela mesma análise,
      inclusive o caso `q = 1`.

Pronto quando: para cada direção forem publicados uma construção com orçamento, um contraexemplo ou um
limite provado. Considera-se encontrada a construção que cumpre todos os critérios da seção 1.

### Etapa 5. Fundamentos que só se estabelecem por experiência (permitidos por D5)

- [ ] Qwen3.5-4B com aritmética inteira em duas placas de vídeo diferentes: se os bits coincidem.
- [ ] Sua velocidade em relação ao perfil comum nas mesmas placas.
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
