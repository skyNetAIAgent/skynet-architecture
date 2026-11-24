<!-- translation of docs/CONNECT.md, source sha256: bd3f9740a67100d72b7a87b5073daf071ecf7c9648582be1586e382d46869750 -->

# Como participar

[English](../../docs/CONNECT.md) · [中文](../zh/CONNECT.md) · [Español](../es/CONNECT.md) · [Français](../fr/CONNECT.md) · [Deutsch](../de/CONNECT.md) · [Italiano](../it/CONNECT.md) · [Русский](../ru/CONNECT.md) · **Português** · [العربية](../ar/CONNECT.md)

Você pode ajudar a projetar a SkyNet com o seu computador ou celular. O agente de pesquisa é um pequeno
programa de código aberto: ele recebe cálculos de pesquisa assinados, os executa no tempo livre do seu
dispositivo e publica os resultados. Não é preciso ter conta em lugar nenhum. **Nesta etapa não há
recompensas**: esta é uma ajuda voluntária para a pesquisa, e não a própria rede SkyNet.

## Instalação

| Seu dispositivo | O que fazer |
|---|---|
| **Windows 10/11** (64 bits) | Baixe `SkyNetAgentSetup-<version>-amd64.exe` da [última versão](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) e execute-o. O Windows mostra "O Windows protegeu o seu PC" porque o arquivo não tem assinatura de código: escolha **Mais informações** e depois **Executar assim mesmo**. |
| **Linux** (x86_64 ou ARM64) | Baixe `skynet-agent-linux-install-<version>.sh` da [última versão](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) e execute `sh skynet-agent-linux-install-<version>.sh`. |
| **Android 7.0+** (64 bits) | Baixe `skynet-agent.apk` da página de versões, abra-o e permita a instalação a partir desta origem. O aplicativo só funciona enquanto o celular estiver carregando. |

O macOS e o iPhone não são suportados.

O instalador pergunta se deve iniciar o agente agora e ao entrar no sistema. Depois disso, não há mais
nada a fazer: o agente se atualiza sozinho (apenas para versões assinadas pelo projeto), pega tarefas e
publica resultados por conta própria.

## O que ele usa e o que nunca faz

- Um núcleo de processador na prioridade mais baixa por padrão, para que os seus próprios programas não
  fiquem mais lentos. Em um notebook, ele não trabalha na bateria, a menos que você permita.
- Ele nunca executa código vindo de uma tarefa, nunca envia os seus arquivos e não precisa de direitos de
  administrador. Cada resultado é um pequeno registro público assinado com a chave do próprio dispositivo.
- Para pausar ou parar: a pasta **SkyNet Agent** no menu Iniciar no Windows,
  `skynet-agent pause` / `stop` no Linux, o botão **Stop** no aplicativo.
- Para remover: **SkyNet Agent → Desinstalar** no Windows, `skynet-agent uninstall --yes` no Linux,
  desinstale o aplicativo no Android.

Detalhes: [o guia do agente](AGENT.md).

## Ajude com ideias, não apenas com processamento

O principal problema em aberto do projeto é como verificar cálculos de modo que trapacear nunca compense,
de forma barata, sem depósitos nem multas. Se você, ou o seu assistente de IA, tiver uma ideia ou tiver
encontrado uma falha, veja o [quadro de tarefas](BOARD.md), o [roteiro](ROADMAP.md) e as
[perguntas em aberto](OPEN_QUESTIONS.md).
