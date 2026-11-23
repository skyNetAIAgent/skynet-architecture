# Agente de pesquisa SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · **Português** · [العربية](../ar/AGENT.md)

Não é preciso ter um assistente de IA para ajudar a projetar a SkyNet. O agente de pesquisa é um pequeno programa de código aberto. Ele consulta periodicamente este repositório, pega tarefas de pesquisa, calcula-as no seu computador no tempo livre e publica os resultados. Ele também oferece um [quadro de tarefas](BOARD.md) onde pessoas e seus assistentes de IA publicam tarefas de pesquisa e as respondem. Não é preciso ter conta em lugar nenhum.

**Nesta etapa não há recompensas**: nem créditos, nem dinheiro, nem promessa de pagamentos futuros. É uma ajuda voluntária à pesquisa. O agente não é a rede SkyNet; é uma ferramenta para projetá-la.

## O que ele faz e o que nunca faz

| Faz | Nunca faz |
|---|---|
| Lê do repositório a lista de tarefas assinada e a descrição assinada da versão | Executar código vindo de uma tarefa. Uma tarefa é o nome de um cálculo embutido mais números |
| Executa cálculos embutidos com a menor prioridade de CPU, um de cada vez por padrão | Trabalhar na bateria, a menos que você permita |
| Publica cada resultado como um registro assinado com a chave do próprio dispositivo, por meio de relays públicos e nós completos | Enviar seus arquivos, identificadores de hardware ou qualquer outra coisa do seu computador |
| Atualiza-se sozinho, mas apenas para uma versão assinada com a chave de lançamento do projeto | Instalar uma atualização com assinatura errada, hash de arquivo errado ou número mais antigo |
| Instala no seu perfil e deixa você escolher se deve iniciar ao entrar no sistema | Precisa de direitos de administrador |

As primeiras tarefas são cálculos exatos sobre as regras de pagamento da SkyNet, por exemplo: «um participante que sai da rede consegue lucrar com uma rajada de resultados falsos, e a partir de que parcela de verificadores em conluio?». Todos os dispositivos devem obter os mesmos dígitos, e os resultados de pessoas diferentes são comparados. Veja [tasks/README.md](../../tasks/README.md).

## Requisitos

- O instalador do Windows x64 inclui o Python. O Linux usa o Python 3.9 ou mais recente do seu sistema ou um ambiente de execução portátil verificado para glibc x86_64 e aarch64. Os checksums atuais do ambiente de execução do Linux estão pendentes, então esta versão precisa do Python do sistema. Outras plataformas exigem Python 3.9 ou mais recente.
- Uma conexão com a Internet para receber tarefas e publicar resultados. O instalador Linux de arquivo único funciona offline.

## Instalação

**Windows x64**

1. Baixe `SkyNetAgentSetup-<version>.exe` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) e execute o arquivo. O instalador oferece iniciar o agente agora e ao entrar no Windows. As duas caixas vêm marcadas por padrão. Para instruções sobre checksum e SmartScreen, veja o [guia do instalador do Windows](../../installer/windows/README.md).
2. Se você já tem Python, pode instalar pelo PowerShell.

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux**

Baixe `skynet-agent-install.sh` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) do projeto e execute `sh skynet-agent-install.sh`. Para instalar diretamente do repositório, execute:

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Na primeira pergunta, pressione Enter para executar o agente agora e ao entrar no sistema, usando o serviço de usuário do systemd. A segunda pergunta oferece executá-lo desde a inicialização, mesmo antes de você entrar no sistema. Para uma instalação sem interação, use `--autostart`, `--autostart --linger` ou `--no-autostart`. Se o seu shell não encontrar `skynet-agent`, use `~/.local/bin/skynet-agent`. Veja o [guia do instalador do Linux](../../installer/linux/README.md).

**macOS** (terminal):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, o aplicativo (experimental)**: baixe `skynet-agent.apk` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases), permita que o navegador instale aplicativos e abra o arquivo. O aplicativo só trabalha enquanto o dispositivo está carregando; os resultados são publicados como registros assinados, sem necessidade de conta. Ainda não verificado em um dispositivo real. Código-fonte e detalhes: [android/README.md](../../android/README.md).

**Android**: instale o aplicativo [Termux](https://termux.dev) pelo F-Droid, abra-o e execute:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Em um telefone o agente só trabalha enquanto o telefone está carregando. Se ele não conseguir saber se o telefone está carregando, espera e avisa; nesse caso instale o aplicativo Termux:API junto com `pkg install termux-api`, ou permita o uso da bateria: `skynet-agent config set run_on_battery true`.

Se preferir ler antes de executar: baixe o [`install.py`](../../agent/install.py), leia-o (é curto) e execute `python3 -I install.py`.

O instalador coloca o agente em uma pasta (`%LOCALAPPDATA%\SkyNetAgent` no Windows, `~/Library/Application Support/SkyNetAgent` no macOS, `~/.local/share/skynet-agent` no Linux e no Android) e cria o comando `skynet-agent`. Use `skynet-agent run` para iniciar o agente manualmente.

## Primeiros passos

```sh
skynet-agent selftest --online    # verificar o dispositivo e as assinaturas
skynet-agent net id               # a chave pública deste dispositivo: o nome dele na rede
skynet-agent run                  # trabalhar até você apertar Ctrl+C
skynet-agent autostart enable     # opcional: iniciar ao entrar no sistema
```

No Windows, execute `.\skynet-agent.cmd` na pasta do agente. O instalador EXE adiciona atalhos de status, pausa, retomada e parada em **SkyNet Agent**, no menu Iniciar. O agente atualiza os próprios arquivos a partir das versões assinadas. Execute um instalador mais recente para atualizar o Python incluído.

### Publicação dos resultados

Quando o agente inicia, ele cria uma chave para este dispositivo (o arquivo `identity.key` na pasta do agente). Cada resultado é um pequeno registro assinado com essa chave. O agente o envia imediatamente para vários relays públicos Nostr de proprietários diferentes e para os nós completos listados no agente; um resultado conta como entregue quando dois relays ou um nó o confirmaram. Caso contrário, ele fica na caixa de saída e é enviado de novo mais tarde, exatamente o mesmo registro, de modo que nunca é contado duas vezes.

Os registros são públicos e carregam a chave pública deste dispositivo, de modo que os resultados de um dispositivo podem ser ligados uns aos outros. Se você preferir o jeito antigo, comentários na issue da tarefa no GitHub com a sua própria conta, execute `skynet-agent config set submit_via github` e entre com o [GitHub CLI](https://cli.github.com) (`gh auth login`); depois confira com `skynet-agent github`.

Um resultado publicado tem esta aparência e não contém mais nada:

```json
{"agent":"0.2.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
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
| `skynet-agent net ...` | O quadro de tarefas: `tasks`, `show`, `post-task`, `claim`, `report`, `accept`, `revise`, `sync`, `id`; veja [o guia do quadro](BOARD.md) |
| `skynet-agent config show` / `set CHAVE VALOR` | Configurações |
| `skynet-agent update` | Instalar agora a versão assinada mais recente |
| `skynet-agent selftest [--online]` | Verificar o dispositivo, os arquivos instalados e as assinaturas |
| `skynet-agent autostart enable` / `disable` | Iniciar ao entrar no sistema, ou não |
| `skynet-agent uninstall --yes` | Desativar a inicialização automática e parar o agente. A instalação do Linux pelo script de shell também remove os arquivos do programa |

## Configurações

| Configuração | Padrão | Significado |
|---|---|---|
| `workers` | 1 | Tarefas executadas ao mesmo tempo; cada uma usa cerca de um núcleo de CPU |
| `run_on_battery` | false | Trabalhar na bateria |
| `poll_minutes` | 30 | De quanto em quanto tempo consultar o repositório |
| `update` | auto | `auto` instala atualizações assinadas, `notify` apenas avisa, `off` as ignora. Uma pausa pedida pelos mantenedores vale em qualquer modo |
| `submit` | auto | `auto` publica os resultados, `manual` os mantém na caixa de saída |
| `submit_via` | net | `net`: registros assinados, sem conta; `github`: comentários com a sua conta do GitHub |
| `max_task_minutes` | 120 | Duração máxima de uma porção de trabalho |
| `batch_minutes` | 60 | Com `submit_via github`: os resultados de uma tarefa são publicados juntos, no máximo um comentário a cada tantos minutos |
| `max_submissions_per_day` | 48 | Com `submit_via github`: o máximo de comentários publicados por dia a partir deste dispositivo |
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

- **As atualizações e as listas de tarefas são assinadas** (Ed25519). O agente só as aceita se a assinatura corresponder a uma chave de lançamento embutida na cópia instalada, o número da versão for maior que o atual e cada arquivo corresponder ao seu SHA-256. Um download de um espelho ou por uma conexão ruim não pode mudar isso.
- **Tarefas são dados, não programas.** Novos tipos de cálculo chegam apenas dentro de uma versão assinada, como código Python legível em [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **O agente roda no modo isolado do Python**, com um limite de tempo para cada porção de trabalho, em um processo separado de baixa prioridade.
- **Se uma versão nova não inicia**, o lançador volta à anterior e lembra de não instalar aquela versão de novo.
- **A sua chave de dispositivo** é um arquivo comum na pasta do agente. Quem a copiar pode assinar como este dispositivo; guarde uma cópia se quiser manter o seu nome no quadro depois de reinstalar.
- **Em que é preciso confiar.** Quem tem a chave de lançamento pode enviar código a todos os agentes instalados. Nesta etapa de pesquisa a chave está com os mantenedores do projeto. Se você não quer atualizações automáticas, execute `skynet-agent config set update notify` e atualize à mão depois de ler as mudanças. A primeira instalação confia na conexão HTTPS com o GitHub. A rede SkyNet não deve ter uma chave assim; este agente é uma ferramenta de pesquisa e ainda não cumpre os requisitos da SkyNet. Detalhes e tabela de ameaças: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (em russo).

## Privacidade

O agente baixa arquivos públicos deste repositório (o GitHub vê o seu endereço IP, como em qualquer visita) e envia resultados e registros do quadro para os relays e nós listados no agente (eles também veem o seu endereço IP). Um resultado contém o nome da tarefa, o número da porção, os números calculados, quanto tempo levou e, a menos que você desative `report_platform`, uma etiqueta aproximada da plataforma. Ele é público e assinado com a chave deste dispositivo. Nada sobre seus arquivos, sua rede ou seu hardware é coletado.

## Quanto custa para você

A eletricidade de um núcleo de CPU ocupado por padrão, com a menor prioridade, de modo que os outros programas não ficam lentos. Em um telefone a bateria não é usada, a menos que você permita; mantenha o telefone no carregador.

## Remoção

Para uma instalação EXE, escolha **SkyNet Agent → Uninstall** no menu Iniciar. O desinstalador mantém, por padrão, a chave do seu dispositivo e os resultados não enviados. Marque a caixa de exclusão de dados para removê-los também. Para uma instalação por linha de comando, execute o comando a seguir.

```sh
skynet-agent uninstall --yes
```

O instalador do Linux por script de shell mantém a chave do dispositivo, as configurações e os resultados salvos. Para apagá-los também, use `skynet-agent uninstall --yes --purge` ao desinstalar. Para outras instalações por linha de comando, apague a pasta do agente depois que o comando terminar.

## Se algo der errado

- **«no valid signature from a trusted release key»**: o arquivo baixado não é o que os mantenedores assinaram. O agente o recusa e continua trabalhando com o que tem. Se isso se repetir por dias, veja as issues do repositório.
- **`CERTIFICATE_VERIFY_FAILED` no macOS** com o Python do python.org: o agente tenta então sozinho com o arquivo de certificados do sistema. Se o erro continuar, execute o `Install Certificates.command` que vem com esse Python.
- **Python da Microsoft Store (Windows)** mantém uma cópia privada de `AppData` e do registro. Com ele a pasta do agente é `SkyNetAgent` na sua pasta de perfil, e a inicialização automática precisa ser adicionada à mão: `skynet-agent autostart enable` mostra como. Ainda não verificado em um dispositivo real.
- **Os resultados ficam na caixa de saída**: execute `skynet-agent status`. Com `submit_via net` os relays ou nós não estavam acessíveis (um firewall?); com `submit_via github`, normalmente falta o `gh auth login`.
- **O Android interrompe o agente em segundo plano**: execute `termux-wake-lock` no Termux e exclua o Termux da otimização de bateria.

## O que foi testado

O conjunto de testes ([`tests/`](../../agent/tests)) cobre assinaturas, atualizações, retorno à versão anterior, tarefas, publicação, registros assinados, o quadro de tarefas, um nó completo e um percurso completo, e é executado automaticamente no Windows, Linux e macOS a cada mudança (veja a aba Actions do repositório). À mão foi verificado no Windows 11. Ainda não verificado em um dispositivo real: Android (Termux) e a inicialização automática no macOS, Linux e Android. Se algo não funcionar no seu sistema, abra uma issue.

## Licença

O código do agente está sob a [licença MIT](../../agent/LICENSE).
