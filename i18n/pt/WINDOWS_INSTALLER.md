<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Instalador para desktop do Windows

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · **Português** · [العربية](../ar/WINDOWS_INSTALLER.md)

Escolha o instalador amd64 ou arm64 para o seu computador. Verifique o SHA-256 dele usando um checksum obtido por um canal confiável. A instalação coloca o lançamento nativo assinado no perfil do usuário atual. A instalação inicia o agente imediatamente e a cada início de sessão do Windows; ambas as opções podem ser desmarcadas na página de tarefas. Os atalhos do menu Iniciar chamam o lançador permanente.

O desinstalador mantém a identidade, as filas e o histórico de lançamentos por padrão. Selecione a opção de exclusão de dados para removê-los. Durante a migração, a ponte Python assinada anterior e o interpretador dela são mantidos para reversão.

## Compilação e teste

Use Python 3.9+ e Inno Setup 6 na máquina de compilação. Prepare o manifesto do lançamento e a assinatura destacada em `agent/v2`, e os binários do lançamento correspondente em `dist`. Use uma pasta de compilação nova. O teste de fumaça precisa de uma conta do Windows descartável.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
