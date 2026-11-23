<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Installateur Windows x64

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · **Français** · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Téléchargez l'EXE et le fichier `.exe.sha256` correspondant depuis la même publication du
projet. Dans PowerShell, ouvrez le dossier de téléchargement et comparez la somme de contrôle.
[Publications GitHub](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Ouvrez l'EXE vérifié. SmartScreen peut afficher **Windows a protégé votre ordinateur** parce que
l'installateur n'a pas de signature de code. Choisissez **Informations complémentaires**,
vérifiez le nom du fichier, puis choisissez **Exécuter quand même**. L'installation se fait pour
l'utilisateur actuel. Décochez l'une ou l'autre des cases de démarrage automatique pour changer
le moment où l'agent s'exécute.

L'agent accepte les mises à jour signées de ses propres fichiers. Un installateur plus récent
met à jour le Python intégré. Installez par-dessus la copie existante pour conserver l'identité
de l'appareil et les résultats en attente. Le désinstallateur du menu Démarrer les conserve lui
aussi par défaut. Sa case facultative de suppression des données inclut la boîte d'envoi et les
enregistrements signés en attente.

## Compilation et test

Utilisez une copie propre du dépôt avec des fins de ligne LF pour les fichiers signés. À la
racine du dépôt, sous Windows x64, exécutez PowerShell 7 avec un nouveau dossier de compilation.
La compilation vérifie la présence d'Inno Setup 6.3.3 ou plus récent dans PATH ou à son
emplacement habituel. Elle utilise Chocolatey pour installer 6.3.3 si le compilateur est absent.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` doit contenir la version de correctif 3.12 exacte et le SHA-256 à 64 chiffres de
son fichier officiel `python-<version>-embed-amd64.zip`. Pour épingler une nouvelle version,
authentifiez l'archive à l'aide des instructions et du paquet Sigstore liés depuis la page de
publication de Python, puis notez son SHA-256. Une valeur épinglée vide ou non valide arrête la
compilation avant le téléchargement. [Publication de Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

La compilation vérifie l'archive avant de l'extraire. L'interpréteur intégré ne copie que les
fichiers indiqués dans le manifeste de publication authentifié. Au moment de l'installation, il
vérifie de nouveau le paquet, y compris sa liste de fichiers, avant d'exécuter le candidat. Le
fichier `python312._pth` d'origine fournit la bibliothèque standard. Le lanceur et la
vérification du candidat ajoutent le dossier de publication sélectionné à `sys.path` avec
l'option `-I`.

Sur un profil Windows jetable sans installation SkyNet existante, exécutez le test de fumée. Il
s'installe en silence, vérifie l'enregistrement du démarrage à l'ouverture de session et la CLI
sans Python système dans PATH, puis se désinstalle et vérifie les données conservées.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

Sinon, exécutez **Actions → Installateur Windows → Exécuter le workflow**. Une fois le test de
fumée réussi, téléchargez l'artefact `SkyNetAgentSetup-x64`. Ses fichiers
`SkyNetAgentSetup-<version>.exe` et `.exe.sha256` sont les deux éléments à joindre manuellement
à la publication GitHub correspondante.
