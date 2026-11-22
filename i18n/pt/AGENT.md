# Agente de pesquisa SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · **Português** · [العربية](../ar/AGENT.md)

Tradução de [agent/README.md](../../agent/README.md). Como o mecanismo funciona e quais são os seus limites: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (em russo).

Não é preciso ter um assistente de IA para ajudar a projetar a SkyNet. O agente de pesquisa é um pequeno programa de código aberto. Ele consulta periodicamente este repositório, pega tarefas de pesquisa, calcula-as no seu computador no tempo livre e publica os resultados.

**Nesta etapa não há recompensas**: nem créditos, nem dinheiro, nem promessa de pagamentos futuros. É uma ajuda voluntária à pesquisa. O agente não é a rede SkyNet; é uma ferramenta para projetá-la.

## O que ele faz e o que nunca faz

| Faz | Nunca faz |
|---|---|
| Lê do repositório a lista de tarefas assinada e a descrição assinada da versão | Executar código vindo de uma tarefa. Uma tarefa é o nome de um cálculo embutido mais números |
| Executa cálculos embutidos com a menor prioridade de CPU, um de cada vez por padrão | Trabalhar na bateria, a menos que você permita |
| Publica cada resultado como comentário no GitHub com a sua própria conta | Enviar seus arquivos, identificadores de hardware ou qualquer outra coisa do seu computador |
| Atualiza-se sozinho, mas apenas para uma versão assinada com a chave de lançamento do projeto | Instalar uma atualização com assinatura errada, hash de arquivo errado ou número mais antigo |
| Mantém tudo em uma única pasta do seu perfil | Exigir direitos de administrador ou iniciar sozinho se você não ativar a inicialização automática |

As primeiras tarefas são cálculos exatos sobre as regras de pagamento da SkyNet. Por exemplo: «um participante que sai da rede consegue lucrar com uma rajada de resultados falsos, e a partir de que parcela de verificadores em conluio?». Todos os dispositivos devem obter os mesmos dígitos, e os resultados de pessoas diferentes são comparados. Veja [tasks/README.md](../../tasks/README.md).

## Requisitos

- Python 3.9 ou mais recente. Nada mais: o agente usa apenas a biblioteca padrão do Python.
- Uma conta no GitHub para publicar resultados (gratuita). Sem ela você ainda pode calcular e publicar à mão por um link.
- Alguns megabytes de disco e conexão com a internet.

## Instalação

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux e macOS** (terminal):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, o aplicativo (experimental)**: baixe `skynet-agent.apk` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases), permita que o navegador instale aplicativos e abra o arquivo. O aplicativo só trabalha enquanto o dispositivo está carregando; os resultados são publicados com um token do GitHub que você cola no aplicativo. Ainda não verificado em um dispositivo real. Código-fonte e detalhes: [android/README.md](../../android/README.md).

**Android**: instale o aplicativo [Termux](https://termux.dev) pelo F-Droid, abra-o e execute:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Em um telefone o agente só trabalha enquanto o telefone está carregando. Se ele não conseguir saber se o telefone está carregando, espera e avisa; nesse caso instale o aplicativo Termux:API junto com `pkg install termux-api`, ou permita o uso da bateria: `skynet-agent config set run_on_battery true`.

Se preferir ler antes de executar: baixe o [`install.py`](../../agent/install.py), leia-o (é curto) e execute `python3 -I install.py`.

O instalador coloca o agente em uma pasta (`%LOCALAPPDATA%\SkyNetAgent` no Windows, `~/Library/Application Support/SkyNetAgent` no macOS, `~/.local/share/skynet-agent` no Linux e no Android) e cria o comando `skynet-agent`. Ele não inicia nada.

## Primeiros passos

```sh
skynet-agent selftest --online    # verificar o dispositivo e as assinaturas
skynet-agent github               # ver com qual conta do GitHub os resultados serão publicados
skynet-agent run                  # trabalhar até você apertar Ctrl+C
skynet-agent autostart enable     # opcional: iniciar ao entrar no sistema
```

No Windows o comando é o arquivo `skynet-agent.cmd` na pasta do agente; o instalador mostra a linha exata.

### Publicação dos resultados

Os resultados são comentários na issue de acompanhamento da tarefa neste repositório, publicados pela sua própria conta do GitHub. A forma mais simples de entrar é a ferramenta de linha de comando do próprio GitHub:

1. Instale o [GitHub CLI](https://cli.github.com) (`winget install GitHub.cli`, `brew install gh`, `pkg install gh` no Termux ou o gerenciador de pacotes do seu Linux).
2. Execute `gh auth login` e siga as instruções no navegador.
3. Execute `skynet-agent github`. Ele mostra o nome da conta.

O agente pede o acesso ao `gh` quando precisa e não guarda senha nem token. Alternativas: colocar um token na variável de ambiente `SKYNET_GITHUB_TOKEN`, ou publicar à mão: `skynet-agent outbox link` mostra links que abrem uma página do GitHub já preenchida, onde basta apertar um botão.

Para que as issues continuem legíveis, os resultados de uma tarefa são publicados juntos: no máximo um comentário por hora, cada um com vários resultados.

Um resultado publicado tem esta aparência e não contém mais nada:

```json
{"agent":"0.1.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Comandos

| Comando | O que faz |
|---|---|
| `skynet-agent run` | Trabalha até ser parado. `--once` faz uma porção de trabalho e sai |
| `skynet-agent status` | Versão, configurações, contadores, resultados em espera, último problema |
| `skynet-agent tasks` | As tarefas publicadas agora e o que este dispositivo já fez |
| `skynet-agent pause` / `resume` | Parar de pegar tarefas novas / voltar a pegar |
| `skynet-agent stop` | Pedir ao agente em execução que saia |
| `skynet-agent outbox` | Resultados aguardando publicação (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent config show` / `set CHAVE VALOR` | Configurações |
| `skynet-agent update` | Instalar agora a versão assinada mais recente |
| `skynet-agent selftest [--online]` | Verificar o dispositivo, os arquivos instalados e as assinaturas |
| `skynet-agent autostart enable` / `disable` | Iniciar ao entrar no sistema, ou não |
| `skynet-agent uninstall --yes` | Desativar a inicialização automática e parar; depois apague a pasta do agente |

## Configurações

| Configuração | Padrão | Significado |
|---|---|---|
| `workers` | 1 | Tarefas executadas ao mesmo tempo; cada uma usa cerca de um núcleo de CPU |
| `run_on_battery` | false | Trabalhar na bateria |
| `poll_minutes` | 30 | De quanto em quanto tempo consultar o repositório |
| `update` | auto | `auto` instala atualizações assinadas, `notify` apenas avisa, `off` as ignora. Uma pausa pedida pelos mantenedores vale em qualquer modo |
| `submit` | auto | `auto` publica os resultados, `manual` os mantém na caixa de saída |
| `max_task_minutes` | 120 | Duração máxima de uma porção de trabalho |
| `batch_minutes` | 60 | Os resultados de uma tarefa são publicados juntos, no máximo um comentário a cada tantos minutos |
| `max_submissions_per_day` | 48 | Máximo de comentários publicados por dia a partir deste dispositivo |
| `report_platform` | true | Acrescentar aos resultados uma etiqueta aproximada como `windows-amd64-py3.12` |
| `ai.enabled` | false | Modo de IA opcional, veja abaixo |

Exemplo: `skynet-agent config set workers 4`.

## Opcional: responder a perguntas de pesquisa com o seu próprio modelo local de IA

Se você roda um modelo aberto no seu computador (por exemplo com Ollama, o servidor llama.cpp ou LM Studio), o agente pode passar a ele perguntas de pesquisa da lista de tarefas e publicar as respostas. Isso vem desativado por padrão e é experimental.

```sh
skynet-agent ai                               # mostra o servidor local e o modelo que seria usado
skynet-agent config set ai.enabled true
```

- O agente não baixa nem inicia nenhum modelo. Ele só fala com um servidor no seu próprio computador, a menos que você ative `ai.allow_remote`.
- A pergunta e os documentos que ela cita vêm da lista de tarefas assinada; cada documento é conferido com o seu hash antes de o modelo vê-lo.
- Cada resposta espera na caixa de saída até você olhar: `skynet-agent outbox show NOME`, depois `skynet-agent outbox approve NOME`. Para publicar sem revisão: `skynet-agent config set ai.review_before_submit false`.
- As respostas são publicadas como geradas por máquina e não verificadas.

## Segurança, com honestidade

- **As atualizações e as listas de tarefas são assinadas** (Ed25519). O agente só as aceita se a assinatura corresponder a uma chave de lançamento embutida na cópia instalada, o número da versão for maior que o atual e cada arquivo corresponder ao seu SHA-256. Um espelho ou uma conexão ruim não mudam isso.
- **Tarefas são dados, não programas.** Novos tipos de cálculo chegam apenas dentro de uma versão assinada, como código Python legível em [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **O agente roda no modo isolado do Python**, e cada porção de trabalho vai em um processo separado, de baixa prioridade e com limite de tempo.
- **Se uma versão nova não inicia**, o lançador volta à anterior e lembra de não instalar aquela versão de novo.
- **Em que é preciso confiar.** Quem tem a chave de lançamento pode enviar código a todos os agentes instalados. Nesta etapa de pesquisa a chave está com os mantenedores do projeto. Se você não quer atualizações automáticas, execute `skynet-agent config set update notify` e atualize à mão depois de ler as mudanças. A primeira instalação confia na conexão HTTPS com o GitHub. A rede SkyNet não deve ter uma chave assim; este agente é uma ferramenta de pesquisa e ainda não cumpre os requisitos da SkyNet. Detalhes e tabela de ameaças: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md).

## Privacidade

O agente só entra em contato com o GitHub: baixa arquivos públicos deste repositório (o GitHub vê o seu endereço IP, como em qualquer visita) e, se você entrou na conta, publica resultados em seu nome. Um resultado contém o nome da tarefa, o número da porção, os números calculados, quanto tempo levou e, a menos que você desative `report_platform`, uma etiqueta aproximada da plataforma. Nada sobre seus arquivos, sua rede ou seu hardware é coletado.

## Quanto custa para você

A eletricidade de um núcleo de CPU ocupado por padrão, com a menor prioridade, de modo que os outros programas não ficam lentos. Em um telefone a bateria não é usada, a menos que você permita; mantenha o telefone no carregador.

## Remoção

```sh
skynet-agent uninstall --yes
```

Depois apague a pasta do agente. Nada mais foi alterado no seu computador.

## Se algo der errado

- **«no valid signature from a trusted release key»**: o arquivo baixado não é o que os mantenedores assinaram. O agente o recusa e continua trabalhando com o que tem. Se isso se repetir por dias, veja as issues do repositório.
- **`CERTIFICATE_VERIFY_FAILED` no macOS** com o Python do python.org: o agente tenta então sozinho com o arquivo de certificados do sistema. Se o erro continuar, execute o `Install Certificates.command` que vem com esse Python.
- **Python da Microsoft Store (Windows)** trabalha com uma cópia privada de `AppData` e do registro. Com ele a pasta do agente é `SkyNetAgent` na sua pasta de perfil, e a inicialização automática precisa ser adicionada à mão: `skynet-agent autostart enable` explica como. Ainda não verificado em um dispositivo real.
- **Os resultados ficam na caixa de saída**: execute `skynet-agent github`; normalmente falta o `gh auth login`.
- **O Android interrompe o agente em segundo plano**: execute `termux-wake-lock` no Termux e exclua o Termux da otimização de bateria.

## O que foi testado

O conjunto de testes ([`tests/`](../../agent/tests)) cobre assinaturas, atualizações, retorno à versão anterior, tarefas, publicação e um percurso completo, e é executado automaticamente no Windows, Linux e macOS a cada mudança (aba Actions do repositório). À mão foi verificado no Windows 11. Ainda não verificado em um dispositivo real: Android (Termux) e a inicialização automática no macOS, Linux e Android. Se algo não funcionar no seu sistema, abra uma issue.

## Licença

O código do agente está sob a [licença MIT](../../agent/LICENSE).
