<!-- translation of installer/linux/README.md, source sha256: cabcf2237fcb61f3ccddb3e461306c5030f018a0db5353bfe00e7a5f55dd389f -->

# Instalador do Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · **Português** · [العربية](../ar/LINUX_INSTALLER.md)

O instalador off-line contém executáveis Go assinados para amd64, arm64 e ARMv7. Execute-o como o usuário do desktop. Uma instalação nova usa o diretório de dados por usuário e coloca o comando em `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

Use `--home DIR` para um perfil personalizado. A configuração inicia o agente imediatamente e o registra como serviço de usuário do systemd, para que ele inicie novamente após uma reinicialização; ela também tenta mantê-lo em execução após o logout (linger). Use `--no-autostart` para apenas instalar, ou `--linger` para exigir linger. A remoção do agente preserva a identidade e as filas. Adicionar `--purge` remove explicitamente os dados salvos do agente.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

O bootstrap on-line em `agent/install.sh` usa curl, jq, xxd, sha256sum e OpenSSL com suporte a Ed25519. Obtenha o script de um release confiável. Ele autentica o manifesto antes de executar o binário específico da arquitetura.

Para compilar o instalador off-line a partir de arquivos assinados, execute o seguinte na raiz do repositório. O manifesto e a assinatura ficam em `agent/v2`. O script de compilação verifica cada arquivo antes de empacotá-lo.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
