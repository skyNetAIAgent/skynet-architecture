<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# Agente de pesquisa SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · **Português** · [العربية](../ar/ANDROID.md)

Um aplicativo Android que traz o mesmo [agente de pesquisa](../../agent/README.md) da versão para computador. É para quem não quer configurar o Termux: instale um arquivo, aperte Iniciar. Nesta etapa não há recompensas.

**Status: experimental.** Em 22 de novembro de 2026 o aplicativo foi verificado em um emulador Android 14 (x86_64) contra um repositório de teste local assinado com uma chave de teste: ele instalou, iniciou, conferiu as assinaturas, calculou sem erros todas as 7 porções das tarefas de teste, esperou enquanto o emulador estava fora do carregador, continuou trabalhando em segundo plano, guardou um token e com ele chegou à API real do GitHub, e parou e iniciou de novo mantendo o seu estado. Uma compilação apenas para ARM (`arm64-v8a`) fez o mesmo nesse emulador por meio da sua tradução de ARM. A parte em Python também passa nos testes em um computador. **Ainda não foi verificado em um telefone real**, no Android 7–13, em execuções longas nem contra os economizadores de bateria dos fabricantes de telefones. Executar o agente no [Termux](../../agent/README.md#install) continua sendo a outra forma.

## Para participantes

1. Baixe `skynet-agent.apk` da página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra o arquivo. O Android pede que você permita instalar aplicativos do seu navegador ou gerenciador de arquivos.
3. Abra "SkyNet Agent" e aperte **Iniciar**. Uma notificação permanente mostra que ele está em execução.

O que saber:

- Ele só trabalha enquanto o dispositivo está carregando, a menos que você marque "Trabalhar também na bateria". O carregador é verificado entre porções de trabalho: uma porção já iniciada (em geral menos de um minuto) é concluída mesmo se você desconectar o dispositivo.
- Ele não inicia sozinho depois que o dispositivo reinicia: abra o aplicativo e aperte Iniciar de novo.
- No Android 13 e mais recentes, se você recusar as notificações, o aplicativo continua funcionando; o Android passa a mostrá-lo apenas na lista de aplicativos em execução.
- Para publicar resultados ele precisa de um token do GitHub: no GitHub abra Settings → Developer settings → Personal access tokens, crie um token que possa escrever issues de repositórios públicos e cole-o no aplicativo. O token fica guardado apenas dentro do aplicativo. Sem token, os resultados esperam no dispositivo (até 300, e então o aplicativo para de calcular).
- Android 7.0 ou mais recente, dispositivo de 64 bits, cerca de 40 MB.
- O modo de IA opcional não está disponível no aplicativo.
- Para removê-lo, desinstale o aplicativo; nada mais fica no dispositivo.

## Como ele difere do agente para computador

| | Computador | Aplicativo Android |
|---|---|---|
| Código do agente | `agent/skynet_agent` | o mesmo pacote, embutido no APK |
| Trabalho | processos separados de baixa prioridade | uma porção por vez dentro do processo em segundo plano do aplicativo |
| Limite de tempo | o processo de trabalho é encerrado | um vigia encerra o processo em segundo plano; o Android o reinicia e a tarefa fica para dispositivos mais rápidos |
| Atualizações do agente | versão assinada do repositório | a mesma versão assinada, conferida pelo código embutido no APK: a assinatura, cada arquivo, nenhum arquivo fora da lista assinada, nunca abaixo da versão mais alta que já funcionou aqui. Uma versão nova tem três tentativas para chegar ao repositório; caso contrário, o aplicativo volta ao código embutido |
| O próprio aplicativo | lançador e instalador | muda apenas com um novo APK |
| Publicação | login no GitHub CLI | um token colado no aplicativo |

Limites, com honestidade. O APK é assinado com uma chave que está com os mantenedores do projeto; o Android só aceita uma atualização do aplicativo se ela estiver assinada com a mesma chave. A chave de lançamento (para o código do agente e as listas de tarefas) e essa chave do APK são dois pontos únicos de confiança que a rede SkyNet alvo não deve ter. O aplicativo carrega código Python assinado em tempo de execução, o que as regras do Google Play não permitem, por isso ele é distribuído como um arquivo.

## Compile você mesmo

Você precisa de JDK 17, do Android SDK (plataforma 34, build-tools 34), do Gradle 8.7 e do Python 3.12 no computador de compilação.

```sh
cd android
gradle assembleRelease
```

O resultado é `app/build/outputs/apk/release/app-release-unsigned.apk`. Assine-o com a sua própria chave (`zipalign` e depois `apksigner sign`) antes de instalar. Um APK que você mesmo assina não pode ser instalado por cima do APK do projeto, nem o contrário.

Compile o aplicativo apenas a partir de um commit em que `agent/skynet_agent/trust.py` liste a chave de lançamento: um agente sem chave de lançamento não aceita tarefas. Nesse caso, a compilação de release para com um erro; `-PallowNoReleaseKey` compila mesmo assim esse APK, apenas para testes.

A parte em Python do aplicativo é [`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py). Ela é testada em um computador por [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py). O Python é embutido com [Chaquopy](https://chaquo.com/chaquopy/) (licença MIT).

## Licença

MIT, como o agente: [agent/LICENSE](../../agent/LICENSE).
