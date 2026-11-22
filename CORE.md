# The immutable foundation of SkyNet / Неизменяемая основа SkyNet

**English** · [中文](i18n/zh/CORE.md) · [Español](i18n/es/CORE.md) · [Français](i18n/fr/CORE.md) · [Deutsch](i18n/de/CORE.md) · [Italiano](i18n/it/CORE.md) · [Русский](i18n/ru/CORE.md) · [Português](i18n/pt/CORE.md) · [العربية](i18n/ar/CORE.md)

## English

**What belongs to the foundation (version 1, 22 November 2026):** the README, the manifesto and the
mandatory requirements, in every language of this repository:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (English);
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  for `ru zh es fr de it pt ar`.

The canonical edition is Russian (`i18n/ru/`). Where translations differ, it prevails.

**How the foundation is fixed:**

1. **Fingerprints.** The SHA-256 fingerprint of every foundation file is listed in
   [CORE_HASHES.txt](CORE_HASHES.txt). Anyone can check a copy:
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) or compare with `Get-FileHash` (Windows).
2. **Tag `core-v1`.** The commit with version 1 of the foundation is marked with the tag `core-v1`.
3. **Automatic check.** Every pull request and push runs a check that fails if any foundation file or
   `CORE_HASHES.txt` differs from version 1.
4. **Licence.** The foundation texts are under CC BY-ND 4.0: they may be copied and shared verbatim,
   but modified versions may not be distributed.
5. **Future network software.** The fingerprint of the foundation is to be written into the immutable
   core of the network ledger, and the software must refuse to run under rules that contradict it.
   This is a requirement for the future software; it does not exist yet.
6. **Copies.** Every fork, clone and archive keeps the original texts and their fingerprints, so a change
   anywhere can be detected by comparison.

**Honest limit.** Nobody can technically forbid the owners of a GitHub organisation from changing
repository settings, and anyone can fork the texts and edit their copy. What can be guaranteed is
different: any change to the foundation is **visible**, because it breaks the published fingerprints,
and a project with a different foundation is not SkyNet. Typos and translation errors are recorded
in [ERRATA.md](ERRATA.md) without touching the foundation files.

## Русский

**Что входит в основу (версия 1, 22 ноября 2026 года):** README, манифест и обязательные требования
на всех языках репозитория:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (английский);
- `i18n/<язык>/README.md`, `i18n/<язык>/MANIFESTO.md`, `i18n/<язык>/REQUIREMENTS.md`
  для `ru zh es fr de it pt ar`.

Каноническая редакция — русская (`i18n/ru/`). При расхождении переводов действует она.

**Как закреплена основа:**

1. **Отпечатки.** Отпечаток SHA-256 каждого файла основы записан в [CORE_HASHES.txt](CORE_HASHES.txt).
   Любой может проверить свою копию: `sha256sum -c CORE_HASHES.txt` (Linux/macOS) или сравнить
   с `Get-FileHash` (Windows).
2. **Метка `core-v1`.** Коммит с версией 1 основы отмечен меткой `core-v1`.
3. **Автоматическая проверка.** Каждый pull request и каждая запись в репозиторий запускают проверку,
   которая падает, если файл основы или `CORE_HASHES.txt` отличается от версии 1.
4. **Лицензия.** Тексты основы распространяются по CC BY-ND 4.0: копировать и распространять
   дословно можно, распространять изменённые версии нельзя.
5. **Будущая программа сети.** Отпечаток основы должен быть записан в неизменяемое ядро журнала сети,
   а программа обязана отказываться работать по правилам, которые ей противоречат. Это требование
   к будущей программе; самой программы ещё нет.
6. **Копии.** Каждый форк, клон и архив сохраняет исходные тексты и их отпечатки, поэтому изменение
   где угодно обнаруживается сравнением.

**Честная граница.** Технически никто не может запретить владельцам организации на GitHub менять
настройки репозитория, а любой может скопировать тексты и править свою копию. Гарантировать можно
другое: любое изменение основы **видно**, потому что ломает опубликованные отпечатки, а проект
с другой основой — это не SkyNet. Опечатки и ошибки переводов записываются в [ERRATA.md](ERRATA.md),
не трогая файлы основы.
