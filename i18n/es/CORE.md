<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# El fundamento inmutable de SkyNet

[English](../../CORE.md) · [中文](../zh/CORE.md) · **Español** · [Français](../fr/CORE.md) · [Deutsch](../de/CORE.md) · [Italiano](../it/CORE.md) · [Русский](../ru/CORE.md) · [Português](../pt/CORE.md) · [العربية](../ar/CORE.md)

**Qué pertenece al fundamento (versión 1, 22 de noviembre de 2026):** el README, el manifiesto y los
requisitos obligatorios, en todos los idiomas de este repositorio:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (inglés);
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  para `ru zh es fr de it pt ar`.

La edición canónica es la rusa (`i18n/ru/`). Cuando las traducciones difieran, prevalece esta.

**Cómo se fija el fundamento:**

1. **Huellas.** La huella SHA-256 de cada archivo del fundamento figura en
   [CORE_HASHES.txt](../../CORE_HASHES.txt). Cualquiera puede comprobar una copia:
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) o comparar con `Get-FileHash` (Windows).
2. **Etiqueta `core-v1`.** El commit con la versión 1 del fundamento está marcado con la etiqueta `core-v1`.
3. **Comprobación automática.** Cada pull request y cada push ejecutan una comprobación que falla si cualquier archivo del fundamento o
   `CORE_HASHES.txt` difiere de la versión 1.
4. **Licencia.** Los textos del fundamento están bajo CC BY-ND 4.0: se pueden copiar y compartir textualmente,
   pero las versiones modificadas no pueden distribuirse.
5. **Programa futuro de la red.** La huella del fundamento debe escribirse en el núcleo inmutable
   del registro de la red, y el programa debe negarse a funcionar bajo reglas que lo contradigan.
   Es un requisito para el programa futuro; aún no existe.
6. **Copias.** Cada bifurcación, clon y archivo conserva los textos originales y sus huellas, de modo que un cambio
   en cualquier sitio puede detectarse por comparación.

**Límite honesto.** Técnicamente nadie puede prohibir a los propietarios de una organización de GitHub cambiar
la configuración del repositorio, y cualquiera puede bifurcar los textos y editar su copia. Lo que sí se puede garantizar es
distinto: cualquier cambio en el fundamento es **visible**, porque rompe las huellas publicadas,
y un proyecto con un fundamento distinto no es SkyNet. Las erratas y los errores de traducción se registran
en [ERRATA.md](ERRATA.md) sin tocar los archivos del fundamento.
