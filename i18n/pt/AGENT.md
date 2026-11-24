# Agente de pesquisa SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · **Português** · [العربية](../ar/AGENT.md)

Você pode ajudar a projetar a SkyNet deixando o seu computador realizar parte da pesquisa. O agente é um pequeno programa de código aberto. Ele consulta este repositório em busca de tarefas, faz uma porção de um cálculo e compartilha o resultado. Você também pode publicar uma pergunta de pesquisa ou responder à de outra pessoa no quadro de tarefas. Não é preciso ter conta nem assistente de IA. [Guia do quadro de tarefas](BOARD.md)

**Nesta etapa não há recompensas.** Não há créditos, pagamentos nem promessas de pagamentos futuros. Esta é uma pesquisa voluntária para ajudar a projetar a rede SkyNet.

## O que ele faz e o que nunca faz

| Faz | Nunca faz |
|---|---|
| Lê uma lista de tarefas assinada. Cada tarefa indica um cálculo embutido e fornece as suas entradas | Executa código vindo de uma tarefa ou de uma publicação no quadro |
| Executa uma porção de trabalho de cada vez por padrão, com prioridade baixa de CPU | Inicia uma nova porção quando detecta alimentação pela bateria, por padrão |
| Assina os resultados com a chave deste dispositivo e, por padrão, os envia para relays públicos e um nó completo | Inclui seus arquivos pessoais ou identificadores de hardware em um resultado automático |
| Verifica a assinatura do projeto antes de instalar uma atualização de desktop | Aceita uma atualização baixada com assinatura inválida, hash de arquivo errado ou número da versão mais antigo |
| Instala no seu perfil e deixa você escolher se deve iniciar ao entrar no sistema | Exige direitos de administrador para uma instalação normal de desktop |

Uma pergunta de pesquisa é se um participante prestes a sair pode lucrar com uma rajada de resultados falsos. Quantos verificadores teriam de ajudar? Dispositivos diferentes que recebem a mesma porção desse cálculo devem obter exatamente a mesma resposta, para que os seus resultados possam ser comparados. [Tarefas de pesquisa](../../tasks/README.md)

## Requisitos

- Windows em x64 (amd64) ou ARM64, ou Linux em amd64, arm64 ou ARMv7. O agente de desktop na versão 1.0.1 é um único programa Go. Os instaladores da página Releases incluem o executável, pronto para executar. O macOS não é suportado.
- Para o aplicativo experimental para Android, Android 7.0 ou mais recente em arm64-v8a ou x86_64.
- Uma conexão com a Internet para receber novas tarefas e publicar resultados. O instalador Linux da página Releases pode instalar offline.

## Instalação

**Windows**

1. Escolha o instalador do Windows (`.exe`) para o seu computador, amd64 ou arm64, na página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Compare o checksum SHA-256 do arquivo com o checksum de uma fonte confiável e execute o instalador. Você pode escolher iniciar o agente agora e iniciá-lo ao entrar no sistema. O instalador adiciona atalhos ao menu Iniciar. [Guia do instalador do Windows](../../installer/windows/README.md)

**Linux**

Baixe `skynet-agent-install.sh` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) e execute `sh skynet-agent-install.sh` como seu usuário normal. O arquivo inclui executáveis para as três arquiteturas Linux suportadas.

Você também pode instalar pela rede com o comando abaixo. Ele precisa de `curl`, `jq`, `xxd`, `sha256sum` e OpenSSL com suporte a Ed25519.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Por padrão, o instalador mantém a sua configuração atual de inicialização ao entrar no sistema. Em uma instalação nova, inicie o agente você mesmo com `skynet-agent run`. Para iniciá-lo agora e ao entrar no sistema, execute `sh skynet-agent-install.sh --autostart`. Isso usa o seu serviço de usuário do systemd. Acrescente `--linger` para executar desde a inicialização e após sair da conta, ou use `--no-autostart` para desativar o serviço. Se o seu shell não encontrar o comando, use `~/.local/bin/skynet-agent`. [Guia do instalador do Linux](../../installer/linux/README.md)

**Android (experimental)**

Baixe `skynet-agent.apk` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases). Abra o arquivo e permita a instalação pelo navegador ou gerenciador de arquivos quando o Android pedir. Abra o **SkyNet Agent** e toque em **Start**. Por padrão, ele só calcula enquanto o dispositivo está carregando. A opção **Start after reboot** vem desativada por padrão.

O APK tem o seu próprio número de versão. A versão 0.3.0 do aplicativo inclui o agente Go 1.0.0. O aplicativo oferece atualizações na sua tela ou em uma notificação. Ele verifica a descrição assinada da versão e o tamanho e o SHA-256 do APK antes de pedir que você confirme a instalação no Android. [Guia do Android](../../android/README.md)

A chave do seu dispositivo, as configurações e os resultados ficam na sua pasta do agente. O padrão é `%LOCALAPPDATA%\SkyNetAgent` no Windows e `~/.local/share/skynet-agent` no Linux (ou `$XDG_DATA_HOME/skynet-agent`, se definido). O instalador do Linux também aceita `SKYNET_AGENT_HOME` ou `--home DIR` para escolher outra pasta. O Android mantém o seu perfil no armazenamento privado do aplicativo.

Se você já executa o agente Python em um desktop suportado com as atualizações automáticas ativadas, ele passa sozinho para Go por meio da versão ponte **0.4.0** assinada. Ele mantém a chave do seu dispositivo, o progresso e os resultados não enviados. A ponte anterior e o seu interpretador são mantidos para reversão.

## Primeiros passos

No Linux, use os comandos abaixo. No Windows, abra o PowerShell na pasta do agente e use `.\skynet-agent.exe launch` no lugar de `skynet-agent`. Por exemplo, `.\skynet-agent.exe launch status` mostra o seu status por meio do lançador permanente.

```sh
skynet-agent verify-install       # verifica os arquivos da versão instalada e executa um cálculo de teste
skynet-agent selftest --online    # executa o cálculo e confere os documentos assinados online
skynet-agent net id               # mostra a chave pública deste dispositivo, o seu nome no quadro
skynet-agent run                  # se ele ainda não estiver em execução, trabalhe até apertar Ctrl+C
```

Use `skynet-agent autostart status` para ver se a inicialização ao entrar no sistema está ativa. Para ativá-la, use `skynet-agent autostart enable`.

### Publicação dos resultados

O agente salva cada resultado concluído na caixa de saída. Ele usa a chave de assinatura em `identity.key` na pasta do agente e cria uma na primeira vez, se o arquivo não existir. Por padrão, ele envia o resultado assinado para relays públicos Nostr e um nó completo. Um nó ou dois relays distintos precisam confirmar o recebimento antes de o agente mover o resultado para `sent`. Caso contrário, ele fica na caixa de saída. Cada nova tentativa usa o mesmo registro assinado com o mesmo ID.

Aqui está parte de um resultado de uma tarefa que usa o cálculo de teste embutido. O resultado completo também traz o nome da tarefa, os segundos decorridos, a versão do formato, o número da versão do agente e, por padrão, uma etiqueta de plataforma. O registro assinado em torno dele carrega a chave pública do dispositivo, um carimbo de data e hora, o ID do registro e a assinatura.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Comandos

| Comando de desktop | O que faz |
|---|---|
| `skynet-agent run` | Trabalha até ser parado. `--once` tenta no máximo uma unidade. `--no-submit` mantém os resultados locais nesta execução. `--no-update` pula a instalação de atualizações. `--verbose` acrescenta detalhes ao log. |
| `skynet-agent status` | Mostra a versão, a pasta do agente, o estado da alimentação, os contadores de trabalho, os resultados em espera e os problemas recentes. |
| `skynet-agent tasks` | Lista as tarefas de pesquisa automáticas, quais estão prontas e quantas unidades este dispositivo concluiu. |
| `skynet-agent pause` / `resume` | Deixa as unidades ativas terminarem e deixa de iniciar novas, ou volta a permitir novas unidades. |
| `skynet-agent stop` | Pedir ao agente em execução que saia. |
| `skynet-agent outbox` | Lista, exibe, envia ou descarta entradas na fila. Use `edit` e `approve` para revisar rascunhos de relatórios de IA conforme descrito abaixo. |
| `skynet-agent ai` | Mostra o servidor de modelo e o modelo selecionado. Use `ai answer TASK-ID` para redigir um relatório do quadro. |
| `skynet-agent net` | Navegue pelo quadro com `tasks` ou `show`. Use `post-task`, `claim`, `report`, `accept` ou `revise` para participar. `sync` repete as publicações pendentes no quadro e busca registros. `id` mostra a sua chave pública. [Guia do quadro](BOARD.md) |
| `skynet-agent config` | `show` lista as configurações, `get KEY` mostra uma e `set KEY VALUE` a altera. |
| `skynet-agent update` | Verifica se há uma versão de desktop assinada mais recente e a instala, se ela for elegível para este dispositivo. |
| `skynet-agent selftest [--online]` | Confere um cálculo com a sua resposta conhecida. Acrescente `--online` para conferir as assinaturas da lista de tarefas e da descrição da versão mais antiga do projeto. |
| `skynet-agent verify-install` | Verifica os arquivos da versão instalada e executa o cálculo de teste. |
| `skynet-agent version` | Mostra a versão do agente, o número da versão, a versão do Go e a plataforma. |
| `skynet-agent autostart` | `status` mostra se a inicialização ao entrar no sistema está ativa. `enable` a ativa e `disable` a desativa. |
| `skynet-agent uninstall --yes` | Remove uma instalação do Linux. Acrescente `--purge` para apagar também os dados salvos. |

## Configurações

| Configuração | Padrão | Significado |
|---|---|---|
| `workers` | 1 | Número de unidades que o agente de desktop pode executar ao mesmo tempo, de 1 a 256. O Android executa uma. |
| `run_on_battery` | false | Permite calcular na bateria. |
| `paused` | false | Aguarda antes de iniciar novas unidades. Os comandos `pause` e `resume` alteram esta configuração. |
| `poll_minutes` | 30 | Intervalo aproximado entre consultas ao repositório, de 5 a 1440 minutos. As consultas que falham têm o seu próprio intervalo de novas tentativas. |
| `update` | auto | No desktop, `auto` instala atualizações assinadas elegíveis, `notify` registra no log quando uma está disponível e `off` ignora a instalação e os avisos. Os três modos ainda verificam se há uma pausa assinada dos mantenedores. |
| `submit` | auto | `auto` envia os resultados conforme o trabalho avança. `manual` os mantém na caixa de saída até você executar `skynet-agent outbox send`. |
| `submit_via` | net | Publica registros assinados por meio de relays e nós. Este é o único canal que funciona na versão 1.0. |
| `max_task_minutes` | 120 | Limite de tempo por unidade, de 1 a 1440 minutos. Um limite menor na tarefa tem precedência. |
| `report_platform` | true | Inclui o sistema operacional, a arquitetura do processador e a versão do Go nos novos resultados, por exemplo `linux-amd64-` seguido da versão do Go. |

Por exemplo, `skynet-agent config set workers 4` permite até quatro workers de desktop. O perfil também preserva os antigos limites de comentários do Python.

## Redigir relatórios do quadro com um modelo local de IA

Inicie um servidor de modelo e execute `skynet-agent ai` para ver qual modelo o agente encontrou. Com `ai.endpoint` vazio, ele tenta o Ollama na porta 11434, o llama.cpp na 8080 e o LM Studio na 1234, todos em loopback. Use `config set ai.endpoint URL` para selecionar um servidor ou `config set ai.model NAME` para selecionar um modelo listado. O padrão é o primeiro modelo listado. Um endpoint remoto exige `ai.allow_remote true` e recebe o texto da tarefa.

Execute `skynet-agent ai answer TASK-ID` para um rascunho, ou `skynet-agent config set ai.enabled true` para ativar a redação automática durante as consultas ao quadro. A redação automática vem desativada por padrão. O agente ignora tarefas com um relatório aceito, um relatório deste dispositivo ou um rascunho existente ou descartado. Ele passa o título, a pergunta e os critérios de aceitação ao modelo como texto não confiável. O modelo não recebe ferramentas nem acesso a arquivos. O limite combinado da tarefa é de 16,000 caracteres. Os padrões de `ai.timeout_minutes` e `ai.max_answer_chars` são 30 minutos e 8,000 caracteres.

```sh
skynet-agent outbox list
skynet-agent outbox show NAME          # lê o relatório e o seu SHA-256
skynet-agent outbox approve NAME SHA256 # usa o digest impresso por show
skynet-agent outbox send               # envia agora as entradas elegíveis
```

Cada rascunho traz o resumo público `machine-generated, unverified`. Para substituir o texto, execute `skynet-agent outbox edit NAME FILE`, depois mostre e aprove o rascunho editado. Editar invalida a aprovação anterior. Um relatório aprovado pode ser enviado no próximo envio automático ou por `outbox send` no modo manual. Use `outbox drop NAME` para descartar o rascunho e ignorar essa tarefa nas consultas futuras.

## Segurança, com honestidade

- **As atualizações e as listas de tarefas são assinadas.** O agente confere as suas assinaturas Ed25519 com a chave de lançamento do projeto embutida no programa. Antes de passar para uma atualização de desktop, ele verifica o número da versão, confere o tamanho e o SHA-256 do executável e executa um cálculo de teste. Ele recusa listas de tarefas mais antigas e para de iniciar trabalho a partir de uma lista expirada.
- **Tarefas fornecem dados.** Os únicos cálculos que uma tarefa pode escolher estão embutidos no executável. Adicionar um novo tipo de cálculo exige uma nova versão de desktop ou uma atualização do aplicativo Android. [Código-fonte Go dos cálculos](https://github.com/skyNetAIAgent/skynet-architecture/tree/main/agent-go/kernels)
- **Cada unidade roda em um processo separado** na sua conta. O worker pede prioridade baixa de CPU. O agente para o worker se ele atingir o limite de tempo.
- **Uma atualização de desktop pode ser revertida.** O lançador verifica a versão ativa antes de iniciá-la. Se essa verificação falhar, ou se três tentativas seguidas de executar o agente travarem no primeiro minuto, o lançador pode restaurar uma versão anterior verificada, se houver uma disponível. Ele se lembra do número da versão que falhou.
- **A sua chave de dispositivo é um arquivo não criptografado.** Quem copiar `identity.key` pode assinar como este dispositivo. Uma cópia de segurança privada permite manter o seu nome no quadro depois de reinstalar.
- **A primeira instalação depende de onde você obtém o instalador ou o script.** Depois da instalação, quem controla a chave de lançamento do projeto pode assinar código novo que roda com as suas permissões de usuário. Os mantenedores detêm essa chave nesta etapa de pesquisa. Para revisar as atualizações de desktop antes, use `skynet-agent config set update notify` e execute `skynet-agent update` quando estiver pronto. A rede SkyNet proposta deve funcionar sem uma chave de lançamento central. [Projeto do agente de pesquisa e tabela de ameaças, em russo](../../docs/RESEARCH_AGENT.md)

## Privacidade

O GitHub vê o seu endereço IP quando você baixa tarefas ou atualizações. Os relays e nós completos que você contata também veem o seu endereço IP. O nó completo embutido usa HTTP não criptografado. Os resultados e as publicações no quadro são públicos. A chave pública deles permite que os leitores liguem registros do mesmo dispositivo.

Os resultados automáticos contêm dados do cálculo e os campos descritos acima. Use `skynet-agent config set report_platform false` para omitir a etiqueta de plataforma dos resultados futuros. O agente não examina os seus arquivos pessoais nem inclui números de série de hardware. Quando você publica uma tarefa ou um relatório no quadro, o texto que você escolhe enviar se torna público.

## Quanto custa para você

Um worker ocupado pode usar cerca de um núcleo de CPU. A prioridade baixa ajuda outros programas a obter tempo de CPU quando precisam. O trabalho ainda consome eletricidade e pode produzir calor. Em um notebook, o agente verifica a alimentação cerca de uma vez por minuto. Por padrão, ele espera para iniciar novas unidades quando detecta alimentação pela bateria. Uma unidade já em execução pode terminar, e o agente de desktop pode começar a trabalhar se a fonte de alimentação for desconhecida.

No Android, desconectar o carregador cancela a unidade atual e a deixa disponível para tentar de novo. Selecione **Also work on battery power** no aplicativo se quiser que ele continue calculando sem o carregador.

## Remoção

No Windows, use o desinstalador do **SkyNet Agent**. Ele mantém, por padrão, a chave do seu dispositivo, as filas e o histórico de versões. Escolha a opção de exclusão de dados durante a desinstalação para removê-los também.

No Linux, execute o comando a seguir. Ele desativa o serviço de usuário, para o agente e remove os programas instalados. A sua chave, as configurações, o progresso e as filas são mantidos.

```sh
skynet-agent uninstall --yes
```

Para remover também os dados salvos do agente, use `skynet-agent uninstall --yes --purge` ao desinstalar. No Android, desinstale o **SkyNet Agent** pelas configurações do Android para remover o aplicativo e os seus dados locais. Os registros publicados continuam públicos.

## Se algo der errado

- **“no valid signature from a trusted key”** significa que o documento baixado não passou na verificação. O agente o recusa. Ele ainda pode usar uma lista de tarefas verificada anteriormente até que essa lista expire. No desktop, `skynet-agent status` mostra o último erro do repositório. O log de execução é `logs/agent.log` dentro da pasta do agente.
- **Os resultados ficam na caixa de saída.** Use `skynet-agent status` ou `skynet-agent outbox list` para ver o que está esperando. No modo manual, execute `skynet-agent outbox send`. Se poucos relays ou nós responderem, o resultado continua na fila para outra tentativa.
- **Uma instalação mais antiga mostra “GitHub submission is unsupported”.** Execute `skynet-agent config set submit_via net` para usar registros assinados nos novos resultados. As entradas já marcadas para o GitHub e as respostas antigas de IA ficam na caixa de saída para inspeção.
- **O agente está em execução, mas nenhum trabalho novo começa.** Verifique `skynet-agent tasks` e o log de execução. Ele pode estar pausado, esperando alimentação, sem tarefas elegíveis ou esperando espaço na caixa de saída. No Android, conecte o carregador e toque em **Start** se você parou o aplicativo antes.

## O que foi testado

Os testes do agente são executados automaticamente no Windows e no Linux. Eles cobrem listas de tarefas assinadas, cálculos com respostas conhecidas, atualizações e reversão, registros assinados, entrega, o quadro de tarefas e uma execução que inicia um worker e entrega o seu resultado a um nó simulado.

Instalações reais foram testadas no Windows 11, no Linux Mint, no Ubuntu Server e em um emulador de Android 14. O aplicativo Android ainda não foi verificado em um dispositivo físico. Se algo não funcionar no seu sistema, abra uma issue.

## Licença

O código do agente está sob a [licença MIT](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/agent-go/LICENSE).
