<!-- translation of docs/RESEARCH_AGENT.md, source sha256: be3193497fd35b1568b634f7647119965e68e6e665fea52b5a8ecb8aa477aa9e -->

# Programa-agente: como ajudar o projeto sem um assistente de IA

[English](../../docs/RESEARCH_AGENT.en.md) · [中文](../zh/RESEARCH_AGENT.md) · [Español](../es/RESEARCH_AGENT.md) · [Français](../fr/RESEARCH_AGENT.md) · [Deutsch](../de/RESEARCH_AGENT.md) · [Italiano](../it/RESEARCH_AGENT.md) · [Русский](../../docs/RESEARCH_AGENT.md) · **Português** · [العربية](../ar/RESEARCH_AGENT.md)

Estado em 22 de novembro de 2026. Versão do agente 0.1.0. Instruções para o participante:
[agent/README.md](../../agent/README.md) ([em russo](../ru/AGENT.md)).

## Por quê

O repositório é pensado para pessoas que têm um assistente de IA: ele lê os documentos e ajuda
a projetar. A maioria das pessoas não tem esse assistente, mas tem um computador ou um telefone.
O programa-agente dá a elas uma forma de participar: ele consulta periodicamente este repositório,
pega tarefas, executa-as no dispositivo do participante e publica os resultados.

Nesta etapa **não há recompensas**: nem créditos, nem dinheiro, nem promessas de pagamentos futuros.
O objetivo é atrair para o projeto da arquitetura o máximo possível de recursos de computação
e de verificadores independentes.

O agente é uma **ferramenta de pesquisa, e não a rede SkyNet**. Ele é mais simples e mais centralizado
do que a rede deve ser, e não cumpre os requisitos obrigatórios dela. Abaixo isso é dito
diretamente em cada ponto.

## Como funciona

| Parte | Onde fica | O que faz |
|---|---|---|
| Lista de tarefas | `tasks/index.json` e a assinatura `tasks/index.json.sig` | Nomeia o cálculo embutido, seus parâmetros e o número de porções independentes |
| Agente | `agent/skynet_agent/`, apenas a biblioteca padrão do Python 3.9+ | Verifica assinaturas, escolhe uma porção, calcula, publica, atualiza-se |
| Descrição da versão | `agent/release.json` e a assinatura | Lista os arquivos do agente com tamanho e SHA-256 |
| Lançador | `agent/launcher.py` | Inicia a versão atual, passa para a nova, volta atrás quando ela está quebrada |
| Resultados | Comentários na tarefa do GitHub em nome do participante | Registro legível por máquina com o hash do resultado |
| Resumo | `results/`, criado por `tools/collect_results.py` | Compara os resultados de pessoas diferentes, confere novamente os achados |

Um ciclo de trabalho do agente:

1. A cada 30 minutos (com dispersão) baixa a descrição da versão e a lista de tarefas.
2. Verifica a assinatura de cada um deles com a chave de lançamento embutida na cópia instalada.
3. Se há uma versão com número maior, baixa os arquivos dela, confere cada um com o hash,
   coloca ao lado da atual e reinicia.
4. Escolhe uma porção aleatória da tarefa que ainda não calculou.
5. Calcula-a em um processo separado com a menor prioridade e limite de tempo.
6. Coloca o resultado na «caixa de saída» e publica-o como comentário na tarefa do GitHub. Os resultados de uma
   tarefa são publicados em lote, no máximo um comentário por hora, para não inundar a tarefa
   e os seguidores com notificações. Depois de uma tentativa malsucedida, a próxima é adiada: por um minuto,
   depois pelo dobro, mas nunca mais de uma hora. Se não for possível publicar (não há acesso ao GitHub), o agente,
   após trezentos resultados não publicados, deixa de pegar trabalho e informa sobre isso.

Não há planejador: cada agente escolhe a porção sozinho. A coincidência de porções entre participantes diferentes
é intencional: todas as tarefas de cálculo são de números inteiros, portanto em qualquer dispositivo se obtêm
os mesmos dígitos, e uma porção é considerada confirmada quando o mesmo hash
foi publicado por tantas contas diferentes quanto a tarefa exige.

## A tarefa são dados, não programa

O agente nunca baixa nem executa código vindo da tarefa. A tarefa nomeia um dos
cálculos embutidos no agente («núcleo») e passa a ele números. Cada núcleo verifica
os parâmetros e limita o volume de trabalho. Um novo tipo de cálculo só aparece com uma nova
versão assinada do agente, cujo código-fonte fica no repositório e pode ser lido diretamente.

Núcleos da versão 0.1:

| Núcleo | O que calcula |
|---|---|
| `selftest` | Cálculo de controle com números inteiros: o hash deve coincidir em todos os dispositivos |
| `exit-scam-a` | A expectativa exata de pagamento de um participante que, antes de sair, entrega resultados falsos (variante A de [CURRENT_DESIGN](CURRENT_DESIGN.md)); percorre uma família de estratégias e informa as que são mais vantajosas do que a saída honesta |
| `lottery-b` | A probabilidade exata de um mês ou trimestre deficitário, se pagar apenas pelas tarefas verificadas (variante B) |
| `ai-answer` | A pedido do participante: uma pergunta para o modelo de IA local que ele mesmo executa |

O modelo exato de cada cálculo está registrado no início do arquivo-fonte do núcleo, para que qualquer um possa
recalcular o resultado de forma independente. As tarefas e o sentido delas: [tasks/README.md](../../tasks/README.md).

**Limite com a regra do projeto sobre experimentos.** As primeiras tarefas são cálculos por fórmulas
dos documentos (análise de custo e busca de contraexemplos) e perguntas a modelos de linguagem.
Isso não é medição em hardware nem experimentos com a rede. As tarefas de medição (por exemplo,
se os bits da saída de números inteiros coincidem em placas de vídeo diferentes) só são publicadas depois da
decisão do dono do projeto de abrir os experimentos.

## Modo de IA (opcional, experimental)

O participante que executa localmente um modelo aberto (Ollama, o servidor llama.cpp, o LM Studio
e similares com interface compatível com a OpenAI) pode ativar `ai.enabled`. Então o agente
passa ao modelo perguntas da lista assinada e publica as respostas. Assim, pessoas sem assinatura
de IA, mas com placa de vídeo, tornam-se participantes do «conselho de modelos».

- O agente não baixa nem inicia o modelo e, por padrão, fala apenas com o servidor
  no mesmo computador.
- A pergunta e os documentos que ela cita são definidos pela lista assinada. Cada documento
  é conferido com o hash, por isso não é possível impor ao modelo outro texto.
- A resposta, por padrão, espera na «caixa de saída» até que o participante a aprove: o texto é publicado
  em nome dele.
- A resposta é marcada como gerada por máquina e não verificada por ninguém. O número de respostas por pergunta é limitado.

Verificado apenas em um servidor fictício nos testes automáticos. Com ambientes reais de
execução de modelos, o modo ainda não foi verificado.

## Aplicativo para Android (experimental)

Para quem não quer configurar o Termux, há um aplicativo: um arquivo APK, botão «Start».
Código-fonte e instruções: [android/README.md](ANDROID.md). No aplicativo estão embutidos o mesmo
pacote `skynet_agent` e o Python (via Chaquopy). Diferenças em relação ao agente no computador:

- O Android não permite iniciar processos Python separados, por isso a porção é calculada no processo
  em segundo plano do próprio aplicativo, uma por vez. Se a porção passa do limite, o vigia encerra esse
  processo, o Android inicia o serviço de novo, e a tarefa fica para os dispositivos mais rápidos.
- A nova versão do agente é obtida do repositório com a mesma assinatura da chave de lançamento. A cópia
  embutida a verifica; se a nova versão não inicia aqui ou os arquivos dela foram alterados, o aplicativo
  volta à embutida.
- O próprio aplicativo (tela, serviço, vigia) só muda com um novo APK. O APK é assinado com uma
  chave separada dos mantenedores do projeto: é o segundo ponto único de confiança, que não deve existir na rede.
- Os resultados são publicados com o token do GitHub que o participante cola no aplicativo.
- Só trabalha enquanto o dispositivo está carregando, a menos que o participante permita o contrário. Não há modo de IA.

Estado em 22 de novembro de 2026: o aplicativo compila, e sua parte em Python passa nos testes no
computador (`agent/tests/test_android_glue.py`). A compilação de verificação com uma chave de teste passou
no emulador Android 14 (x86_64) com um repositório de teste local: instalação, verificação de assinaturas,
cálculo das 7 porções de teste sem erros, espera sem carregador, trabalho em segundo plano, gravação do token
e uso dele com a API real do GitHub, parada e reinício com estado preservado.
Em um telefone real o aplicativo ainda não foi executado, e a compilação para ARM (`arm64-v8a`) não foi verificada. Ele não é distribuído pelo Google Play: as regras dele proíbem aplicativos
que baixam código executável.

## Em que o agente confia

| O quê | Confiança |
|---|---|
| Assinatura Ed25519 com a chave de lançamento | Sim. Sem ela não se aceita nem a versão, nem a lista de tarefas |
| Canal (HTTPS, espelho, o próprio GitHub) | Não para a integridade: a substituição de um arquivo quebra a assinatura ou o hash |
| Conteúdo da tarefa | Não: os parâmetros são verificados, o volume de trabalho é limitado, não há código na tarefa |
| Resposta do modelo local | Não: é texto, e é publicado como não verificado |
| Primeira instalação | Sim, ao canal HTTPS até o GitHub. Você pode verificar o instalado com o comando `selftest --online` |

**Limite honesto.** Quem tem a chave de lançamento pode entregar o programa a todos os agentes
instalados. Hoje a chave está com os mantenedores do projeto. É o ponto único de confiança que não deve existir na rede SkyNet:
no projeto-alvo, o programa só é atualizado para a versão cujo hash
foi aceito por votação dos participantes no registro comum, e uma assinatura com a chave de alguém não é suficiente
([CURRENT_DESIGN, seção 8](CURRENT_DESIGN.md)). O participante que não quer confiar na chave
define `update` como `notify` e atualiza manualmente, depois de ler as mudanças.

## Tabela de ameaças

| Ameaça | Como é coberta | O que resta |
|---|---|---|
| Invasão do repositório ou de uma conta com permissão de escrita: substituição do agente | A versão só é aceita com a assinatura de uma chave que não está no repositório | Coberto enquanto a chave não for roubada |
| Substituição de um arquivo no caminho ou em um espelho | Assinatura da descrição da versão e SHA-256 de cada arquivo | Coberto |
| Retrocesso para uma versão antiga vulnerável | O número da versão deve ser maior que o atual | Coberto para os agentes instalados. Uma nova instalação pega o que está no repositório |
| Tarefa maliciosa | A tarefa não carrega código; o núcleo verifica os parâmetros e limita o volume de trabalho e de memória; há limite de tempo | Limitado: uma tarefa assinada pode ocupar o processador até o limite de tempo |
| Repetição de uma lista antiga assinada de tarefas | O número da lista deve ser não menor que o já visto; a lista pode ter prazo de validade | Limitado: uma instalação nova pode receber uma lista antiga e calcular à toa tarefas encerradas |
| Versão quebrada | O lançador volta à versão anterior após três quedas rápidas ou se os arquivos da nova versão sumiram, e memoriza o número inválido. Pedidos repetidos de reinício ele executa com pausa crescente | Coberto para quedas na inicialização. Um erro silencioso no cálculo é pego pela comparação de resultados |
| Roubo da chave de lançamento | A chave fica fora do repositório; no Windows é criptografada para a conta do dono | **Aberto.** O ladrão pode lançar uma versão maliciosa. A troca de chave é feita com uma nova versão assinada pela chave antiga, e o ladrão também tem acesso a ela |
| Perda da chave de lançamento | Cópia de segurança com o dono | Sem a chave não se pode atualizar os agentes instalados: os participantes terão de instalar o agente de novo |
| Falsificação de resultado | O cálculo de números inteiros é comparado entre contas diferentes; os achados são recalculados na coleta | Limitado: uma pessoa com duas contas «confirmará» a si mesma. Não há recompensas, então não há ganho nisso, mas um sabotador é possível. Os mantenedores recalculam seletivamente |
| Fluxo de comentários-lixo de contas alheias | O coletor aceita apenas registros com o hash correto e tarefa conhecida | Limitado pelos meios do GitHub |
| Vazamento do token do GitHub | O agente não guarda o token, pega-o do `gh` ou de uma variável e não o envia a lugar nenhum além do GitHub por HTTPS, sem redirecionamentos | O token com permissão de escrita em repositórios públicos continua sendo responsabilidade do participante |
| Código alheio perto do agente (módulo plantado na pasta atual) | Modo isolado do Python (`-I`) | Coberto. Não há proteção contra um programa com os direitos do mesmo usuário no mesmo computador |
| Consumo de recursos do participante | Um processo por padrão, menor prioridade, pausa na bateria, limite de tempo, comandos `pause` e `stop` | A eletricidade o participante gasta por conta própria e sem recompensa |
| Parada de todos os agentes pelos mantenedores | Marcação assinada `halt` na descrição da versão; vale também com as atualizações desligadas | É uma alavanca intencional: apenas parada, sem iniciar nada |

## O que o agente informa sobre si

Apenas o conteúdo do registro publicado: o nome da tarefa, o número da porção, os números do resultado,
o tempo de cálculo e, se não estiver desativado, uma etiqueta aproximada da plataforma como `linux-amd64-py3.12`.
As requisições vão apenas ao GitHub. Não são coletadas informações sobre arquivos, rede e hardware do participante.

## Procedimento para os mantenedores

A chave de lançamento é criada uma vez e fica guardada fora do repositório:

```
python tools/keytool.py generate
```

A cópia de segurança do segredo o dono faz por conta própria, manualmente, com o comando `python tools/keytool.py backup`,
e a guarda fora do computador. O segredo não pode ser mostrado a assistentes, nem colado em chats e arquivos.

Nova versão do agente:

```
python tools/make_release.py --seq <próximo número> --version <x.y.z>
```

em seguida, o envio dos arquivos alterados de `agent/` para o repositório. Nova lista de tarefas:

```
python tools/sign_tasks.py
```

em seguida, o envio de `tasks/index.json` e `tasks/index.json.sig`. Coleta dos resultados:

```
python tools/collect_results.py
```

Para parar o trabalho de todos os agentes até corrigir um erro: lançar uma descrição de versão com
`--halt-through <número>` e a razão.

## O que não há aqui e por que é honesto dizer

- **Isso não é uma rede distribuída.** As tarefas e as versões são distribuídas por um único repositório, assinadas por uma única
  chave, e os resultados são recebidos por uma única plataforma. Os requisitos R1–R4 dos
  [requisitos obrigatórios](../ru/REQUIREMENTS.md) não se aplicam ao agente e não são cumpridos por ele.
- **É preciso uma conta no GitHub.** Sem ela, os resultados só são publicados à mão por um link.
- **Não há proteção contra múltiplas contas.** Para a etapa sem recompensas isso é aceitável.
- **O Android não foi verificado em um dispositivo real**; a inicialização automática no macOS, Linux e Android
  foi verificada apenas no nível dos arquivos criados. Dois casos são tratados pela documentação e também
  não foram verificados em dispositivos reais: o Python da Microsoft Store no Windows (ele vê
  uma cópia própria de `AppData` e do registro, por isso a pasta do agente fica no perfil, e a inicialização automática
  é adicionada à mão) e o Python do site python.org no macOS sem os certificados instalados
  (o agente repete a requisição com o arquivo de certificados do sistema).
- **As primeiras tarefas são leves.** Todo o primeiro lote (702 porções) levou em um único computador
  de mesa 15,5 horas de tempo de processador com 16 processos simultâneos na menor
  prioridade, ou seja, cerca de uma hora de relógio [medido em um PC, em 22 de novembro de 2026].
  O mecanismo está pronto para receber tarefas pesadas. O que resultou: [results/FIRST_RUN.md](../../results/FIRST_RUN.md).

## O que vem a seguir

1. Tarefas de medição em dispositivos diferentes: a principal incógnita do projeto é a coincidência
   do resultado bit a bit em placas de vídeo diferentes. Isso são experimentos, e eles aguardam a decisão do dono.
2. Abandono da conta do GitHub: recepção dos resultados por várias plataformas públicas
   independentes, como no projeto-alvo da rede.
3. Abandono da chave única: várias assinaturas independentes, depois a aceitação das versões pelas regras
   da própria rede.
4. Gestão do modelo local: download de um modelo aberto com verificação do hash, para que
   o modo de IA seja ativado com um único comando.
