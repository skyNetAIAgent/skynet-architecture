# Comment contribuer

[English](../../CONTRIBUTING.md) · [中文](../zh/CONTRIBUTING.md) · [Español](../es/CONTRIBUTING.md) · **Français** · [Deutsch](../de/CONTRIBUTING.md) · [Italiano](../it/CONTRIBUTING.md) · [Русский](../ru/CONTRIBUTING.md) · [Português](../pt/CONTRIBUTING.md) · [العربية](../ar/CONTRIBUTING.md)

Merci de vouloir aider. Ici compte la précision, pas le volume : une faille trouvée avec un scénario concret vaut plus que dix pages de considérations générales.

## Quoi apporter

- **Une attaque contre la conception actuelle.** Un scénario : qui agit, ce qu'il fait, ce qu'il obtient, pourquoi le réseau ne s'en aperçoit pas. Indiquez la section de [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md).
- **Une solution à une [question ouverte](../../docs/OPEN_QUESTIONS.en.md).**
- **Une source** : un article, un protocole ou un projet qui résout une partie d'un problème, avec version, date et ce qu'il ne **prouve pas** pour notre cas.
- **Un calcul de coût** ou une correction d'un calcul existant.
- **Une correction de traduction** : une imprécision dans une traduction du socle (via le fichier d'errata).
- **Une tâche pour l'agent de recherche** : un calcul qui répondrait à une partie d'une question ouverte (voir [tasks/README.md](../../tasks/README.md)).
- **De la puissance de calcul** : si vous n'avez ni assistant d'IA ni le temps d'écrire, lancez l'[agent de recherche](AGENT.md) sur votre ordinateur ou votre téléphone.

## Comment la présenter

Ouvrez une issue dont le titre commence par une étiquette :

| Étiquette | Pour |
|---|---|
| `[Attack]` | Un moyen de tromper ou de perturber le réseau |
| `[Q<N>]` | Une proposition pour la question ouverte N |
| `[Source]` | Un article ou un projet utile |
| `[Cost]` | Une estimation de coût ou une correction de chiffres |
| `[Translation]` | Une imprécision de traduction |
| `[Task]` | Un calcul pour l'agent de recherche |

Dans le texte, indiquez :

1. Ce qui est garanti et sous quelles hypothèses.
2. Le mécanisme.
3. Les attaques connues et ce qui reste.
4. Le coût, marqué [calcul] ou [mesuré].
5. Lesquelles des six [exigences](REQUIREMENTS.md) sont satisfaites et lesquelles ne le sont pas.

Les pull requests sur les documents de travail (`docs/`) sont bienvenues. Si vous changez le statut d'un point, expliquez pourquoi. Les issues et pull requests peuvent être rédigées dans n'importe quelle langue du dépôt.

## Règles

- **Le socle ne change pas.** Une pull request qui modifie le manifeste, les exigences, le README ou leurs empreintes ne sera pas acceptée. Voir [CORE.md](../../CORE.md).
- Un calcul n'est pas présenté comme une mesure, ni une proposition comme une décision.
- Ne publiez ni clés, ni mots de passe, ni données personnelles, ni adresses d'ordinateurs.
- Soyez courtois et allez à l'essentiel. Critiquez les idées, pas les personnes.

Si vous travaillez avec un assistant d'IA, donnez-lui [AGENTS.md](AGENTS.md). L'auteur d'une issue est responsable de l'exactitude de son texte.
