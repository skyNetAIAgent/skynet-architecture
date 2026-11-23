<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Instalador para Windows x64

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · **Português** · [العربية](../ar/WINDOWS_INSTALLER.md)

Baixe o EXE e o `.exe.sha256` correspondente no mesmo lançamento do projeto. No
PowerShell, abra a pasta de downloads e compare o checksum. [Releases do GitHub](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Abra o EXE verificado. O SmartScreen pode mostrar **O Windows protegeu seu PC**
(*Windows protected your PC*) porque o instalador não tem assinatura de código. Escolha
**Mais informações** (*More info*), confirme o nome do arquivo e depois escolha
**Executar assim mesmo** (*Run anyway*). A instalação é feita para o usuário atual.
Desmarque qualquer uma das caixas de seleção de inicialização para mudar quando o agente
roda.

O agente aceita atualizações assinadas dos próprios arquivos. Um instalador mais novo
atualiza o Python incluído. Instale por cima da cópia existente para manter a identidade
do dispositivo e os resultados em espera. O desinstalador do menu Iniciar também os
mantém por padrão. A sua caixa de seleção opcional de exclusão de dados inclui a caixa de
saída e os registros assinados pendentes.

## Compilação e teste

Use uma cópia limpa do repositório, com finais de linha LF nos arquivos assinados. Na
raiz do repositório, em um Windows x64, execute o PowerShell 7 com uma pasta de
compilação nova. A compilação verifica se há o Inno Setup 6.3.3 ou mais recente no PATH
ou no local habitual. Se o compilador não estiver presente, ela usa o Chocolatey para
instalar a versão 6.3.3.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

O `python.lock` deve conter a versão de correção 3.12 exata e o SHA-256 de 64 dígitos do
`python-<version>-embed-amd64.zip` oficial. Para fixar uma nova versão, autentique o
arquivo usando as instruções e o pacote Sigstore indicados na página de lançamento do
Python e depois registre o seu SHA-256. Uma versão fixada vazia ou inválida interrompe a
compilação antes do download. [Lançamento do Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

A compilação verifica o arquivo antes de extraí-lo. O interpretador incluído prepara
apenas os arquivos do manifesto do lançamento autenticado. No momento da instalação, ele
verifica o pacote de novo, inclusive a lista de arquivos, antes de executar o candidato.
O `python312._pth` original fornece a biblioteca padrão. O lançador e a verificação do
candidato adicionam a pasta do lançamento selecionado ao `sys.path` em modo `-I`.

Em um perfil do Windows descartável, sem nenhuma instalação da SkyNet existente, execute
o teste de fumaça. Ele instala em silêncio, verifica o registro de login e a CLI sem
Python do sistema no PATH, depois desinstala e verifica os dados mantidos.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

Como alternativa, execute **Ações → Instalador do Windows → Executar fluxo de trabalho**.
Depois que o teste de fumaça passar, baixe o artefato `SkyNetAgentSetup-x64`. O
`SkyNetAgentSetup-<version>.exe` e o `.exe.sha256` dele são os dois arquivos a anexar
manualmente ao lançamento correspondente no GitHub.
