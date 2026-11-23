<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Instalador do Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · **Português** · [العربية](../ar/LINUX_INSTALLER.md)

Execute o arquivo único da página Releases do projeto com a sua própria conta.

```sh
sh skynet-agent-install.sh
```

O arquivo contém a versão assinada do agente. A instalação verifica a assinatura Ed25519 e os hashes dos arquivos sem conexão. Se houver Python 3.9 ou mais recente no seu PATH, a instalação usa esse interpretador. Caso contrário, ela precisa de uma compilação fixada de CPython com glibc para x86_64 ou aarch64. **Os dois hashes estão pendentes no momento. Esta compilação exige o Python do sistema.**

O instalador on-line usa o mesmo procedimento de instalação. Com uma versão fixada e verificada, ele consegue buscar o runtime correspondente no python-build-standalone e conferir o SHA-256 antes da extração. Os interpretadores portáteis ficam em `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normalmente `~/.local/share/skynet-agent/python/<sha256>`. O comando em `~/.local/bin` e o serviço de usuário do systemd usam o executável escolhido.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Iniciar e remover

Em um terminal, Enter no primeiro pedido inicia o serviço agora e ao entrar no sistema. Enter no segundo mantém o serviço ligado às sessões de login. Sem um terminal, a instalação pula os pedidos. Estes comandos fazem as escolhas de forma explícita.

```sh
sh skynet-agent-install.sh --autostart           # Executar agora e ao entrar no sistema
sh skynet-agent-install.sh --autostart --linger  # Também executar antes do login e depois do logout
sh skynet-agent-install.sh --no-autostart        # Instalar para uso manual
```

O serviço precisa de um gerenciador de usuário do systemd em execução. O gerador de serviço assinado 0.2.2 aceita caminhos com espaços. A instalação pede início manual se o caminho do interpretador ou do agente tiver aspas duplas, barra invertida, cifrão, sinal de porcentagem ou quebra de linha. Se a política local negar o lingering, a instalação informa isso e o serviço continua rodando durante as sessões de login. O lingering para toda a conta pode ser alterado à parte com `loginctl disable-linger "$(id -un)"`. Para uma instalação manual, comece o trabalho com `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

A remoção desativa o serviço, pede que ele pare e espera o bloqueio do agente. Sua chave de identidade, a caixa de saída, os registros de relay pendentes e as configurações ficam na pasta do agente para uma reinstalação. Para apagar também os dados salvos do agente, use `uninstall --yes --purge`. O lingering é uma configuração da conta inteira e continua valendo depois da remoção.

## Compilar e verificar

Na raiz do repositório, use Python 3.9 ou mais recente na máquina de compilação.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

O script de compilação autentica a versão com a chave pública em `agent/install.py` e gera `installer/linux/skynet-agent-install.sh`. Para habilitar o Python portátil, verifique cada arquivo upstream de forma independente e registre o seu SHA-256 em `python.lock` (um campo por linha). Apenas para uma entrada nula, a CI pode fornecer um digest verificado por meio de `SKYNET_PYTHON_SHA256_X86_64` ou `SKYNET_PYTHON_SHA256_AARCH64`. Estas são configurações do momento da compilação. O script de compilação verifica e incorpora cada arquivo fixado. Para compilar sem conexão usando versões fixadas, use `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

O fluxo de trabalho do instalador Linux executa o pacote como um usuário sem privilégios e com a rede desativada. O Ubuntu 24.04 testa o Python do sistema. O Debian 12 slim testa o interpretador portátil quando o digest x86_64 está disponível e verifica a recusa quando ele está pendente. As instalações bem-sucedidas executam o autoteste, informam a versão e testam os dois modos de remoção. O fluxo de trabalho envia o script como artefato de compilação para distribuição manual.
