<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# Das unveränderliche Fundament von SkyNet

[English](../../CORE.md) · [中文](../zh/CORE.md) · [Español](../es/CORE.md) · [Français](../fr/CORE.md) · **Deutsch** · [Italiano](../it/CORE.md) · [Русский](../ru/CORE.md) · [Português](../pt/CORE.md) · [العربية](../ar/CORE.md)

**Was zum Fundament gehört (Version 1, 22. November 2026):** das README, das Manifest und die
verbindlichen Anforderungen, in jeder Sprache dieses Repositorys:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (Englisch);
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  für `ru zh es fr de it pt ar`.

Die kanonische Fassung ist die russische (`i18n/ru/`). Wo Übersetzungen abweichen, gilt sie.

**Wie das Fundament festgeschrieben ist:**

1. **Fingerabdrücke.** Der SHA-256-Fingerabdruck jeder Fundamentdatei ist aufgeführt in
   [CORE_HASHES.txt](../../CORE_HASHES.txt). Jeder kann eine Kopie prüfen:
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) oder mit `Get-FileHash` (Windows) vergleichen.
2. **Tag `core-v1`.** Der Commit mit Version 1 des Fundaments ist mit dem Tag `core-v1` markiert.
3. **Automatische Prüfung.** Jeder Pull Request und jeder Push führt eine Prüfung aus, die fehlschlägt,
   wenn eine Fundamentdatei oder `CORE_HASHES.txt` von Version 1 abweicht.
4. **Lizenz.** Die Fundamenttexte stehen unter CC BY-ND 4.0: Sie dürfen unverändert kopiert und geteilt
   werden, veränderte Versionen dürfen jedoch nicht verbreitet werden.
5. **Künftige Netzsoftware.** Der Fingerabdruck des Fundaments soll in den unveränderlichen Kern
   des Netz-Ledgers geschrieben werden, und die Software muss sich weigern, unter Regeln zu laufen,
   die ihm widersprechen. Das ist eine Anforderung an die künftige Software; sie existiert noch nicht.
6. **Kopien.** Jeder Fork, jeder Klon und jedes Archiv behält die Originaltexte und ihre Fingerabdrücke,
   sodass eine Änderung irgendwo durch Vergleich erkannt werden kann.

**Ehrliche Grenze.** Technisch kann niemand den Eigentümern einer GitHub-Organisation verbieten,
die Repository-Einstellungen zu ändern, und jeder kann die Texte forken und seine Kopie bearbeiten.
Garantieren lässt sich etwas anderes: Jede Änderung am Fundament ist **sichtbar**, weil sie die
veröffentlichten Fingerabdrücke bricht, und ein Projekt mit einem anderen Fundament ist nicht
SkyNet. Tippfehler und Übersetzungsfehler werden in [ERRATA.md](ERRATA.md) festgehalten, ohne
die Fundamentdateien anzutasten.
