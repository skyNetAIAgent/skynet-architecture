<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# Le socle immuable de SkyNet

[English](../../CORE.md) · [中文](../zh/CORE.md) · [Español](../es/CORE.md) · **Français** · [Deutsch](../de/CORE.md) · [Italiano](../it/CORE.md) · [Русский](../ru/CORE.md) · [Português](../pt/CORE.md) · [العربية](../ar/CORE.md)

**Ce qui appartient au socle (version 1, 22 novembre 2026) :** le README, le manifeste et les
exigences obligatoires, dans chaque langue de ce dépôt :

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (anglais) ;
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  pour `ru zh es fr de it pt ar`.

L'édition canonique est la russe (`i18n/ru/`). En cas de divergence entre les traductions, c'est elle
qui prévaut.

**Comment le socle est fixé :**

1. **Empreintes.** L'empreinte SHA-256 de chaque fichier du socle figure dans
   [CORE_HASHES.txt](../../CORE_HASHES.txt). N'importe qui peut vérifier une copie :
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) ou comparer avec `Get-FileHash` (Windows).
2. **Balise `core-v1`.** Le commit de la version 1 du socle est marqué avec la balise `core-v1`.
3. **Vérification automatique.** Chaque pull request et chaque push déclenchent une vérification
   qui échoue si un fichier du socle ou `CORE_HASHES.txt` diffère de la version 1.
4. **Licence.** Les textes du socle sont sous CC BY-ND 4.0 : ils peuvent être copiés et partagés
   textuellement, mais les versions modifiées ne peuvent pas être distribuées.
5. **Futur logiciel du réseau.** L'empreinte du socle doit être écrite dans le cœur immuable du
   registre du réseau, et le logiciel doit refuser de fonctionner selon des règles qui contredisent
   le socle. C'est une exigence pour le futur logiciel ; il n'existe pas encore.
6. **Copies.** Chaque fork, clone et archive conserve les textes d'origine et leurs empreintes, de
   sorte qu'un changement, où qu'il soit, peut être détecté par comparaison.

**Limite honnête.** Personne ne peut techniquement empêcher les propriétaires d'une organisation
GitHub de modifier les réglages du dépôt, et n'importe qui peut forker les textes et modifier sa
copie. Ce qui peut être garanti est différent : tout changement apporté au socle est **visible**,
car il casse les empreintes publiées, et un projet dont le socle est différent n'est pas SkyNet.
Les fautes de frappe et les erreurs de traduction sont consignées dans [ERRATA.md](ERRATA.md) sans
toucher aux fichiers du socle.
