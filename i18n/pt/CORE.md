<!-- translation of CORE.md, source sha256: bf365ef474bbcbb38228177243cd54e909c8bf626180103b058e7126414cf4b4 -->

# A base imutável da SkyNet

[English](../../CORE.md) · [中文](../zh/CORE.md) · [Español](../es/CORE.md) · [Français](../fr/CORE.md) · [Deutsch](../de/CORE.md) · [Italiano](../it/CORE.md) · [Русский](../ru/CORE.md) · **Português** · [العربية](../ar/CORE.md)

**O que pertence à base (versão 1, 22 de novembro de 2026):** o README, o manifesto e os
requisitos obrigatórios, em todos os idiomas deste repositório:

- `README.md`, `MANIFESTO.md`, `REQUIREMENTS.md` (inglês);
- `i18n/<lang>/README.md`, `i18n/<lang>/MANIFESTO.md`, `i18n/<lang>/REQUIREMENTS.md`
  para `ru zh es fr de it pt ar`.

A edição canônica é a russa (`i18n/ru/`). Onde as traduções divergirem, ela prevalece.

**Como a base é fixada:**

1. **Impressões digitais.** A impressão digital SHA-256 de cada arquivo da base está listada em
   [CORE_HASHES.txt](../../CORE_HASHES.txt). Qualquer pessoa pode verificar uma cópia:
   `sha256sum -c CORE_HASHES.txt` (Linux/macOS) ou comparar com `Get-FileHash` (Windows).
2. **Tag `core-v1`.** O commit com a versão 1 da base está marcado com a tag `core-v1`.
3. **Verificação automática.** Cada pull request e cada push executam uma verificação que falha se
   qualquer arquivo da base ou `CORE_HASHES.txt` diferir da versão 1.
4. **Licença.** Os textos da base estão sob CC BY-ND 4.0: podem ser copiados e compartilhados
   na íntegra, mas as versões modificadas não podem ser distribuídas.
5. **Futuro programa da rede.** A impressão digital da base deverá ser gravada no núcleo imutável
   do livro-razão da rede, e o programa deverá se recusar a funcionar sob regras que o contradigam.
   Isso é um requisito para o programa futuro; ele ainda não existe.
6. **Cópias.** Cada fork, clone e arquivo mantém os textos originais e suas impressões digitais,
   de modo que qualquer alteração em qualquer lugar possa ser detectada por comparação.

**Limite honesto.** Tecnicamente, ninguém pode proibir os proprietários de uma organização do GitHub
de alterar as configurações do repositório, e qualquer pessoa pode fazer um fork dos textos e editar
a própria cópia. O que pode ser garantido é diferente: qualquer alteração na base é **visível**,
porque quebra as impressões digitais publicadas, e um projeto com uma base diferente não é a SkyNet.
Erros de digitação e de tradução são registrados em [ERRATA.md](ERRATA.md) sem tocar nos arquivos
da base.
