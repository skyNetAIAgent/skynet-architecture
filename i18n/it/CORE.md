<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# Il fondamento immutabile di SkyNet

[English](../../CORE.md) · [中文](../zh/CORE.md) · [Español](../es/CORE.md) · [Français](../fr/CORE.md) · [Deutsch](../de/CORE.md) · **Italiano** · [Русский](../ru/CORE.md) · [Português](../pt/CORE.md) · [العربية](../ar/CORE.md)

**Cosa appartiene al fondamento (versione 1, 22 novembre 2026):** il README, il manifesto e i
requisiti obbligatori, in ogni lingua di questo repository:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (inglese);
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  per `ru zh es fr de it pt ar`.

L'edizione canonica è quella russa (`i18n/ru/`). In caso di divergenza tra le traduzioni, prevale quella russa.

**Come viene fissato il fondamento:**

1. **Impronte.** L'impronta SHA-256 di ogni file del fondamento è elencata in
   [CORE_HASHES.txt](../../CORE_HASHES.txt). Chiunque può controllare una copia:
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) oppure confrontarla con `Get-FileHash` (Windows).
2. **Tag `core-v1`.** Il commit con la versione 1 del fondamento è contrassegnato con il tag `core-v1`.
3. **Controllo automatico.** Ogni pull request e ogni push esegue un controllo che fallisce se un file del fondamento o
   `CORE_HASHES.txt` differisce dalla versione 1.
4. **Licenza.** I testi del fondamento sono sotto CC BY-ND 4.0: possono essere copiati e condivisi alla lettera,
   ma le versioni modificate non possono essere distribuite.
5. **Software di rete futuro.** L'impronta del fondamento deve essere scritta nel nucleo immutabile
   del registro di rete, e il software deve rifiutarsi di funzionare in base a regole che lo contraddicono.
   È un requisito per il software futuro; non esiste ancora.
6. **Copie.** Ogni fork, clone e archivio conserva i testi originali e le loro impronte, così un cambiamento
   in qualunque punto può essere rilevato per confronto.

**Limite onesto.** Nessuno può tecnicamente vietare ai proprietari di un'organizzazione GitHub di cambiare
le impostazioni del repository, e chiunque può fare il fork dei testi e modificare la propria copia. Ciò che si può garantire è
diverso: ogni cambiamento del fondamento è **visibile**, perché rompe le impronte pubblicate,
e un progetto con un fondamento diverso non è SkyNet. I refusi e gli errori di traduzione vengono registrati
in [ERRATA.md](ERRATA.md) senza toccare i file del fondamento.
