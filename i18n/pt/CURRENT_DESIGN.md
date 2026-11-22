<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# O projeto atual da arquitetura

[English](../../docs/CURRENT_DESIGN.en.md) · [中文](../zh/CURRENT_DESIGN.md) · [Español](../es/CURRENT_DESIGN.md) · [Français](../fr/CURRENT_DESIGN.md) · [Deutsch](../de/CURRENT_DESIGN.md) · [Italiano](../it/CURRENT_DESIGN.md) · [Русский](../../docs/CURRENT_DESIGN.md) · **Português** · [العربية](../ar/CURRENT_DESIGN.md)

Situação em 22 de novembro de 2026. Este é um **projeto, não uma implementação**. Não houve
experimentos sobre ele. Os números marcados com [cálculo] foram obtidos por fórmula, não medidos.

## Onde estamos agora

A ideia está formulada no [manifesto](MANIFESTO.md), os requisitos obrigatórios estão aprovados,
a base da arquitetura foi escolhida: uma rede sem coordenadores, um registro comum em um blockchain público, o pagamento
por trabalho verificado e o pagamento diferido em vez de depósito. Um pequeno piloto confiável já executou
o modelo Qwen em vários computadores ([resultados do piloto](PILOT_RESULTS.md)).

O mais difícil está adiante. Ainda não foi encontrada uma forma barata de verificar o trabalho de modo
que a fraude seja inútil mesmo em conluio. Um modelo que melhora a si mesmo de forma confiável e segue
as leis da SkyNet ainda é uma meta de pesquisa. As tarefas para coautores estão nas
[questões em aberto](OPEN_QUESTIONS.md).

Marcações de status:

| Marcação | Significado |
|---|---|
| **Aceito** | Aprovado no projeto como decisão |
| **Candidato** | Variante escolhida, ainda não aprovada ou não construída |
| **Proposta** | Levada para decisão, não aprovada |
| **Aberto** | Não há decisão |

## 1. Esquema geral (aceito como base)

Na rede **não há coordenadores** nem papéis com direitos especiais. Todos os participantes têm o
mesmo programa. Dentro dos controles deslizantes de recursos, ele mesmo:

| Trabalho | O que faz | Pelo que se paga |
|---|---|---|
| Calcula | Executa uma etapa de treinamento ou uma solicitação do usuário | Pelo resultado aceito |
| Verifica | Recalcula o resultado de outro, se o sorteio o escolheu | Pela verificação feita |
| Monitora | Pode recalcular qualquer resultado e contestá-lo | Parte do que é debitado quando uma falsificação é encontrada |
| Armazena e distribui | Guarda os dados com os quais trabalha | Paga quem recebe os dados |
| Escreve no registro | Reúne os registros dos participantes em um blockchain | Reembolso de despesas |
| Ajuda a se encontrar | Retransmite conexões para dispositivos atrás de um roteador | Entra no pagamento da entrega |

**Registro comum** — um contrato em um blockchain público existente, sem chave de administrador.
Ele guarda as regras e a impressão digital do programa, as contas (créditos disponíveis, valor
pendente, peso do trabalho verificado), as impressões digitais dos resultados entregues, as
disputas, as votações, o catálogo de modelos e o plano de treinamento. O registro funciona mesmo
quando todos os nós da SkyNet estão desligados. O blockchain **não foi escolhido** (Aberto).

**Aleatoriedade pública** decide a quem cabe a tarefa, o que é verificado e quem verifica.
Ela surge depois que o resultado é fixado. Candidato: mistura do beacon drand e da aleatoriedade
do blockchain (Candidato, fontes não escolhidas).

## 2. Vida de uma tarefa (candidato)

1. A tarefa de treinamento deriva do plano comum da rede; a solicitação vem do usuário com pagamento.
2. O executor é designado pela aleatoriedade entre os dispositivos com recursos adequados.
3. O programa calcula e registra as impressões digitais dos estados intermediários.
4. A impressão digital do resultado entra em um pacote, e o pacote vai para o registro. A recompensa
   entra no valor «pendente».
5. A aleatoriedade, depois da entrega, decide se a tarefa será verificada.
6. A tarefa escolhida é recalculada de forma independente por três participantes aleatórios, às cegas.
7. Coincidiu bit a bit — confirmado. Não coincidiu — disputa, resolvida pelo recálculo da etapa
   elementar em disputa **no próprio registro**, e não por votação.
8. A janela de verificação é de três dias: qualquer um pode contestar o resultado.
9. Depois da janela, a recompensa fica disponível.

**Pagamento diferido em vez de depósito (aceito).** Pelo resultado, o participante responde apenas
com o valor pendente — suas recompensas dos últimos três dias. Nada é cobrado antecipadamente; os
créditos já disponíveis nunca são debitados.

## 3. Como tornar a fraude não lucrativa: duas variantes

### Variante A. Verificação por amostragem com débito (especificação atual)

A parcela de verificação é `p = 4R / (R + H)`, mas não inferior a 1%; o débito por resultado
incorreto é `B = 4R/p − R`, não maior que o valor pendente `H` (`R` é o preço da tarefa). Assim,
cada falsificação custa, em média, quatro preços de tarefa para qualquer frequência de verificação
[cálculo]. A falsificação passa apenas se os três verificadores estiverem em conluio: com uma
parcela de conluio `q`, a probabilidade é `q³`. A fraude não é lucrativa enquanto o grupo em conluio
detiver menos de ~91% do peso dos verificadores [cálculo].

**Fraqueza.** Uma falsificação não verificada é paga e permanece na rede. É uma aposta que tem
resultados vencedores para o fraudador.

**Cálculo preliminar (22 de novembro de 2026, um computador, não confirmado por outros
participantes).** A estimativa de «91%» vem da média de uma única falsificação. Ela não leva em
conta que o participante só pode perder, no máximo, o valor pendente: não há depósitos nem multas.
Para um participante que sai e entrega falsificações em lotes antes da conclusão das verificações, a
enumeração exata de estratégias no modelo `exit-scam-a` dá um limite mais baixo [cálculo]:

| Regras | Sair com falsificações é lucrativo a partir da parcela de conluio de |
|---|---|
| Tarefas pequenas idênticas, 399 preços pendentes, um lote | 89,2% |
| Tarefas pequenas idênticas, 1200 preços pendentes, um lote | 90,8% |
| Tarefas pequenas idênticas, três lotes, regra «não mais de um terço em trabalho» | 89,0% |
| Tarefas de tamanho arbitrário, três lotes, regra «não mais de um terço» | 87,5% |
| Tarefas de tamanho arbitrário, dois lotes de até 100 tarefas, sem a regra «não mais de um terço» | 80% |
| Sem conluio, tarefas de tamanho arbitrário, dois lotes (92 milhões de estratégias) | não lucrativo |

Sem a regra «não mais de um terço», as recompensas não verificadas do primeiro lote aumentam o
valor pendente e o tamanho permitido das tarefas do segundo, por isso essa regra é obrigatória. O
modelo está registrado no início do arquivo do kernel
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) e reproduz os números do exemplo da
especificação («cerca de 78, 107 e 17»). As tarefas estão descritas em
[tasks/README.md](../../tasks/README.md), e a primeira execução em
[results/FIRST_RUN.md](../../results/FIRST_RUN.md). Esses números se tornarão um resultado do projeto
depois da confirmação independente por outros participantes.

### Variante B. A rede paga apenas pelo que foi verificado (proposta, aguardando decisão)

A tarefa se torna um bilhete de loteria. O sorteio escolhe uma parcela `p` das tarefas (por
exemplo, 1%); apenas elas são verificadas e **apenas elas são pagas, mas `1/p` vezes mais caras**.
Em média, um participante honesto recebe o mesmo, e uma falsificação não escolhida não rende **nada**.

- Sem conluio, a falsificação rende exatamente zero.
- Com conluio, o pagamento indevido ocorre no máximo `q^k` por tarefa verificada (k é o número de
  verificadores): 0,1% com q = 10% e k = 3 [cálculo]. Cada tentativa malsucedida queima todo o
  valor pendente.
- Furos encontrados: um novato em conluio recebe em média `q^k` do preço por tentativa e não perde
  nada; uma «campanha de saída» com muitas falsificações de uma vez. As correções foram propostas:
  vagas de aprendiz com orçamento limitado, anulação de todos os ganhos não vencidos de uma chave
  quando uma falsificação é pega, teto de tarefas abertas.
- Preço: a renda fica irregular. Para um dispositivo fraco, cerca de ±13% ao mês [cálculo].

Ambos os esquemas exigem que o resultado **coincida bit a bit** em dispositivos diferentes. Caminho
proposto: aritmética inteira (`int8/int32`) do modelo, em que a ordem da soma não afeta o resultado.
**A velocidade e a qualidade do Qwen inteiro não foram medidas**; um perfil int8 reproduzível
conhecido foi 5,2 vezes mais lento que o normal (Aberto).

Disputa barata: dividindo o cálculo ao meio até uma única operação, e depois a verificação da
multiplicação de matrizes por um vetor aleatório (algoritmo de Freivalds). Economia de cerca de 100
vezes no número de multiplicações em matrizes grandes, 2,6 vezes em LoRA, sem ganho na geração token
a token [cálculo] (Candidato).

## 4. Peso e novos participantes (candidato)

- **Peso** é a soma dos preços dos resultados que passaram na verificação nos últimos 30 dias. Não
  se pode comprá-lo, transferi-lo nem acumulá-lo. O número de contas não dá nada: as chances e os
  votos são proporcionais ao peso.
- **O novato** primeiro faz reverificações «de aprendiz» de tarefas de outros: sua resposta não
  decide nada e é paga apenas se coincidir com o resultado aceito. Depois recebe tarefas que são
  sempre verificadas, e depois cada vez menos.
- O peso é calculado separadamente para cada modelo. Em um modelo que poucos treinam, o círculo de
  verificadores é pequeno e é mais fácil dominá-lo (Aberto).

## 5. Encontrar a si mesmo e recuperação (candidato)

| Onde | O que sobrevive ao desligamento total |
|---|---|
| Registro no blockchain público | Regras, contas, peso, impressão digital do modelo, plano de treinamento, disputas, endereços dos nós que escreveram |
| Discos dos participantes e espelhos públicos | Pesos do modelo, estado do treinamento, dados; qualquer cópia é conferida com a impressão digital do registro |
| Distribuição do programa | Identificador da rede, endereço do registro, lista inicial de pontos de encontro |

Três maneiras independentes de se encontrar, qualquer uma basta: registros assinados em locais
externos («pontos de encontro»), redes abertas de descoberta de nós (por exemplo, DHT libp2p),
endereços no próprio registro. A janela de verificação não avança enquanto a rede está parada, senão
a falsificação poderia ser entregue antes da parada.

Pontos fracos: a autenticidade da primeira instalação (o novato descobre o endereço do registro de
fora); o bloqueio total de todos os caminhos ao mesmo tempo; a confiança em dois de três
fornecedores do ponto de controle após uma longa inatividade.

## 6. Solicitações e privacidade (candidato)

A solicitação é criptografada para o dispositivo do executor e vai diretamente ou por um
retransmissor, sob pseudônimo. No registro há apenas impressões digitais. Cerca de 1% das
solicitações são vistas ainda por três verificadores.

**Ressalva honesta.** Em um computador comum, o dono do dispositivo com o programa modificado pode
ler a solicitação que ele calcula. A computação totalmente homomórfica para esses modelos é
milhares de vezes mais lenta. Por isso, dois modos: comum (barato) e protegido (apenas em hardware
que prova que o dono não olhará para dentro; mais caro, baseia-se na confiança no fabricante).

## 7. Treinamento e escolha do plano (proposta)

Um catálogo aberto de modelos e conjuntos de dados com licenças livres, fixados por impressões
digitais. A rede, por regra, monta variantes de treinamento, dá a cada uma uma execução de teste e
divide a capacidade livre pelos resultados e pela votação por peso. A nova versão do modelo substitui
a anterior apenas se passou melhor no exame, cujas tarefas foram escolhidas pela aleatoriedade depois
da fixação dos pesos. A contribuição de uma única tarefa para a atualização dos pesos é limitada; a
parte «leve» da etapa (a soma das contribuições) é sempre recalculada.

Um modelo que **melhora a si mesmo de forma confiável e infinita** é uma meta de pesquisa, não uma
tecnologia pronta. Primeira etapa realista: ajuste fino automático e seleção por exame.

## 8. Mudança de regras (candidato)

As regras só mudam por uma nova versão do programa, aceita por 3/4 de **todo** o peso após uma
votação de no mínimo 14 dias e com prazo anunciado de 30 dias. O freio geral (mais da metade do
peso) só pode parar a nova versão do modelo. Proposta: um núcleo de verificação imutável, que não
pode ser revogado por votação (aguardando decisão).

## 9. Resumo dos ataques

Das 60 maneiras de fraude analisadas: 18 fechadas, 6 não lucrativas, 19 limitadas, 16 abertas (para
a variante A). Principais pontos abertos:

1. **Maioria por peso.** Um grupo com 3/4 do peso pode mudar as regras; em uma rede pequena, essa
   parcela pode ser alcançada com trabalho honesto em capacidade alugada. Por isso o início é
   fechado, com créditos de aprendizado.
2. **Fundamentos não construídos.** A coincidência bit a bit e o recálculo da disputa no registro
   para o modelo completo não foram construídos.
3. **Um sabotador que não precisa de lucro.** Pode estragar o treinamento dentro da parcela de seu
   próprio trabalho; o exame não pega backdoors ocultos.
4. **Solicitações de terceiros** no modo comum e nas disputas.
5. **Disponibilidade dos dados.** Não há como julgar a disputa «entregou ou não entregou os dados
   grandes».
6. **Entrada na rede.** A fila para as vagas de aprendiz e a autenticidade da primeira instalação.

Detalhes e tarefas para coautores estão em [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
