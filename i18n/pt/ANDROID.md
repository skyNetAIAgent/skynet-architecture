<!-- translation of android/README.md, source sha256: e6e5eb4a3358a14712c3c5b2e0efee2cd483b0009e7378ef16b31cc789c0d054 -->

# Agente de pesquisa SkyNet para Android (experimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · **Português** · [العربية](../ar/ANDROID.md)

Um aplicativo Android que traz os mesmos [kernels de computação em Go](../../agent-go/README.md) da versão
para computador. Instale um arquivo e aperte Iniciar. Por padrão, o agente assina cada
resultado no dispositivo e o publica sem conta ou token.
Nesta etapa não há recompensas.

**Experimental.** O shell 0.3.0 inclui o agente Go 1.0.0 (versão 7 do motor) no APK. A instalação
por cima da 0.2.0, o ciclo de vida do serviço e a reinicialização ainda precisam ser testados no Android.

## Para participantes

1. Baixe `skynet-agent.apk` da
   página [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Abra o arquivo. O Android pede que você permita instalar aplicativos do seu navegador ou gerenciador de arquivos.
3. Abra "SkyNet Agent" e aperte **Iniciar**. Uma notificação permanente mostra que ele está em execução.

- Ele só trabalha enquanto o dispositivo está carregando, a menos que você marque "Trabalhar também na bateria".
  Desconectar cancela a porção atual e a deixa disponível para uma execução posterior.
- Para continuar depois de reiniciar o dispositivo, ative **Iniciar após reiniciar**. Vem desativado
  por padrão. Apertar **Parar** mantém o agente parado após um reinício.
- No Android 13 e mais recentes, se você recusar as notificações, o aplicativo continua funcionando; o Android passa a mostrá-lo apenas na lista de aplicativos em execução.
- Se um perfil existente usa `submit_via=github`, os resultados dele ficam na fila. Esta versão
  oferece publicação por meio de registros de rede assinados.
- Android 7.0 ou mais recente em arm64-v8a ou x86_64.
- O modo de IA opcional não está disponível no aplicativo.
- Para removê-lo, desinstale o aplicativo; nada mais fica no dispositivo.

## Atualizando o aplicativo

Instale a 0.3.0 por cima do aplicativo existente com a mesma assinatura de pacote para manter a identidade
do seu dispositivo, as configurações, o progresso e os resultados na fila. A partir da 0.2.0, abrir a tela
verifica se há um novo APK. O Android também agenda uma verificação diária quando há uma rede
disponível, mesmo que o agente esteja parado. Restrições de bateria podem atrasar essa verificação.

O aplicativo verifica o manifesto da versão, assinado com a chave embutida no APK. Para uma versão
compatível mais recente, ele baixa o arquivo da versão para o cache privado e confere o tamanho
e o SHA-256. Toque no botão de atualização ou na notificação para instalá-la. No Android 8 e mais
recentes, permita a instalação pelo SkyNet Agent se for solicitado, volte ao aplicativo e
confirme no instalador do Android. Com as notificações desativadas, use o botão na tela principal.

## Agente e atualizações

O serviço em primeiro plano inicia o executável extraído no diretório de bibliotecas nativas.
Ele executa um worker de baixa prioridade por vez e mantém um wake lock durante a computação. Um
worker que excede o tempo limite é encerrado e o agente pula temporariamente essa tarefa. Novas
tarefas chegam pelo índice de tarefas assinado. Novo código executável chega com uma atualização do aplicativo.

O Android verifica o certificado de assinatura do APK durante a instalação. A chave de lançamento
separada autentica o índice de tarefas e o manifesto de download do APK. O aplicativo confere o
tamanho, o SHA-256, o nome do pacote e o código de versão do APK antes de abrir o instalador.

## Compile você mesmo

No Linux, instale o Go 1.27.4 com os fontes, Bash, GNU patch, coreutils, file e readelf
(binutils). Para compilar o APK também são necessários JDK 17, Gradle 8.7 e Android SDK 34.

```sh
cd android
gradle assembleRelease
```

O Gradle chama `./build-go.sh`. Execute esse script diretamente para compilar apenas os dois
executáveis `app/src/main/jniLibs/<abi>/libskynet.so`. Ele usa `GOOS=android`,
`CGO_ENABLED=0` e PIE para as duas ABIs. A compilação para arm64 usa o Go padrão. Para a
compilação para o emulador x86_64, o script ativa a linkedição interna em uma cópia temporária das
ferramentas de compilação do host do Go 1.27.4. Ele verifica a arquitetura, o ponto de entrada e
o interpretador `/system/bin/linker64` antes de instalar qualquer um dos arquivos.

O APK de release é `app/build/outputs/apk/release/app-release-unsigned.apk`. Use
`zipalign` e depois `apksigner sign` com a mesma chave do APK anterior para atualizações
no local. Gere e assine `android/latest.json` a partir do APK assinado final com
`tools/make_apk_manifest.py`.

## Licença

MIT, como o agente: [agent/LICENSE](../../agent/LICENSE).
