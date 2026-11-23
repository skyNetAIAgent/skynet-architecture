<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# Agente de pesquisa SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · **Português** · [العربية](../ar/ANDROID.md)

Um aplicativo Android que traz o mesmo [agente de pesquisa](../../agent/README.md) da versão
para computador. Instale um arquivo e aperte Iniciar. Por padrão, o agente assina cada
resultado no dispositivo e o publica sem conta ou token.
Nesta etapa não há recompensas.

**Experimental.** O shell anterior foi testado em um emulador Android 14, em 22 de novembro
de 2026. Ele concluiu todas as sete porções de teste, esperou pelo carregamento e manteve o
seu estado entre paradas e inícios. O shell 0.2.0 inclui o agente 0.2.2. Os seus fluxos de
instalação e de reinício ainda precisam ser testados no Android.

## Para participantes

1. Baixe `skynet-agent.apk` da
   página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra o arquivo. O Android pede que você permita instalar aplicativos do seu navegador ou gerenciador de arquivos.
3. Abra "SkyNet Agent" e aperte **Iniciar**. Uma notificação permanente mostra que ele está em execução.

- Ele só trabalha enquanto o dispositivo está carregando, a menos que você marque "Trabalhar também na bateria".
  O carregador é verificado entre porções de trabalho: uma porção já iniciada (em geral menos de um
  minuto) é concluída mesmo se você desconectar o dispositivo.
- Para continuar depois de reiniciar o dispositivo, ative **Iniciar após reiniciar**. Vem desativado
  por padrão. Apertar **Parar** mantém o agente parado após um reinício.
- No Android 13 e mais recentes, se você recusar as notificações, o aplicativo continua funcionando; o Android passa a mostrá-lo apenas na lista de aplicativos em execução.
- Usuários avançados que selecionam `submit_via=github` podem inserir um token do GitHub na tela principal.
- Android 7.0 ou mais recente, dispositivo de 64 bits, cerca de 40 MB.
- O modo de IA opcional não está disponível no aplicativo.
- Para removê-lo, desinstale o aplicativo; nada mais fica no dispositivo.

## Atualizando o aplicativo

Se você tem a versão 0.1.0, instale a 0.2.0 da página Releases por cima do aplicativo existente
para manter as suas configurações e os resultados na fila. A partir da 0.2.0, abrir a tela
verifica se há um novo APK. O Android também agenda uma verificação diária quando há uma rede
disponível, mesmo que o agente esteja parado. Restrições de bateria podem atrasar essa verificação.

O aplicativo verifica o manifesto da versão, assinado com a chave embutida no APK. Para uma versão
compatível mais recente, ele baixa o arquivo da versão para o cache privado e confere o tamanho
e o SHA-256. Toque no botão de atualização ou na notificação para instalá-la. No Android 8 e mais
recentes, permita a instalação pelo SkyNet Agent se for solicitado, volte ao aplicativo e
confirme no instalador do Android. Com as notificações desativadas, use o botão na tela principal.

## Como ele difere do agente para computador

| | Computador | Aplicativo Android |
|---|---|---|
| Código do agente | `agent/skynet_agent` | o mesmo pacote, embutido no APK |
| Trabalho | processos separados de baixa prioridade | uma porção por vez dentro do processo em segundo plano do aplicativo |
| Limite de tempo | o processo de trabalho é encerrado | um vigia encerra o processo em segundo plano; o Android o reinicia e a tarefa fica para dispositivos mais rápidos |
| Atualizações do agente | versão assinada do repositório | o APK verifica os arquivos assinados e o número da versão. Um agente novo tem três inícios para passar em uma autoverificação local e concluir uma etapa do ciclo |
| O próprio aplicativo | lançador e instalador | um APK verificado instalado com a sua confirmação |
| Publicação | registros assinados por padrão | registros assinados por padrão |

Limites, com honestidade. O APK é assinado com uma chave que está com os mantenedores do projeto; o Android só aceita uma atualização do aplicativo se ela estiver assinada com a mesma chave. A chave de lançamento (para o código do agente e as listas de tarefas) e essa chave do APK são dois pontos únicos de confiança que a rede SkyNet alvo não deve ter. O aplicativo carrega código Python assinado em tempo de execução, o que as regras do Google Play não permitem, por isso ele é distribuído como um arquivo.

## Compile você mesmo

Você precisa de JDK 17, do Android SDK (plataforma 34, build-tools 34), do Gradle 8.7 e do Python 3.12 no computador de compilação.

```sh
cd android
gradle assembleRelease
```

O resultado é `app/build/outputs/apk/release/app-release-unsigned.apk`. Assine-o com a sua própria chave (`zipalign` e depois `apksigner sign`) antes de instalar. Um APK que você mesmo assina não pode ser instalado por cima do APK do projeto, nem o contrário.

Compile o aplicativo apenas a partir de um commit em que `agent/skynet_agent/trust.py` liste a chave de lançamento: um agente sem chave de lançamento não aceita tarefas. Nesse caso, a compilação de release para com um erro; `-PallowNoReleaseKey` compila mesmo assim esse APK, apenas para testes.

A ponte do agente e o verificador do APK têm testes de Python separados no computador.
[Testes do agente](../../agent/tests/test_android_glue.py) · [Testes de atualização do APK](../../agent/tests/test_apk_update.py)
O Python é embutido com [Chaquopy](https://chaquo.com/chaquopy/) (licença MIT).

## Licença

MIT, como o agente: [agent/LICENSE](../../agent/LICENSE).
