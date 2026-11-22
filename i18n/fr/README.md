# SkyNet : conception ouverte de l'architecture

[English](../../README.md) · [中文](../zh/README.md) · [Español](../es/README.md) · **Français** · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Русский](../ru/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md)

## Ce qu'est ce dépôt

Ici se conçoit l'architecture de SkyNet : un réseau distribué dans lequel des modèles d'IA fonctionnent et apprennent sur les ordinateurs des participants. Les participants offrent au réseau leurs ressources de calcul inutilisées et reçoivent des crédits en échange, tandis que les personnes sans matériel puissant obtiennent un accès bon marché à l'IA.

C'est un dépôt de **recherche**. Il n'y a pas ici de logiciel fini. Il contient :

- le [manifeste](MANIFESTO.md) : pourquoi le réseau est nécessaire, ce qu'il doit être, et les Lois de SkyNet ;
- les [exigences obligatoires](REQUIREMENTS.md), qui ne changent pas ;
- la [conception actuelle de l'architecture](../../docs/CURRENT_DESIGN.md) avec les mentions « décidé », « proposé » et « ouvert » (en russe) ;
- les [questions ouvertes](../../docs/OPEN_QUESTIONS.en.md) pour lesquelles nous avons besoin d'aide (en anglais) ;
- [ce que le pilote a vérifié](../../docs/PILOT_RESULTS.md) et ce qu'il n'a pas vérifié (en russe) ;
- les [règles de participation](CONTRIBUTING.md) et une [introduction pour les assistants d'IA](AGENTS.md) ;
- le [programme-agent](AGENT.md) : un petit programme pour celles et ceux qui n'ont pas d'assistant d'IA.

## Pour qui

- **Ingénieurs en systèmes distribués, cryptographes, chercheurs en apprentissage automatique.** Les principaux problèmes se trouvent à la croisée de ces domaines : vérification peu coûteuse des calculs, protection contre la collusion, rétablissement d'un réseau sans centre.
- **Propriétaires de matériel** (cartes graphiques, serveurs, PC domestiques). Leur regard sur la rentabilité et le coût de l'électricité est nécessaire pour que l'économie fonctionne en pratique.
- **Celles et ceux qui travaillent avec un assistant d'IA.** Il suffit à votre modèle (Claude, ChatGPT, DeepSeek et autres) de lire [AGENTS.md](AGENTS.md) pour comprendre le contexte et se mettre au travail.
- **Celles et ceux qui veulent simplement aider avec leur ordinateur ou leur téléphone.** Aucune connaissance particulière n'est nécessaire : c'est le [programme-agent](AGENT.md) qui fait le travail.

## Le sens

Aujourd'hui, tout le monde n'a pas accès à une IA puissante : le prix, les restrictions géographiques et politiques et le blocage des services y font obstacle. En même temps, le monde regorge de cartes graphiques et d'ordinateurs inutilisés. SkyNet doit relier les deux : un réseau sans propriétaire ni serveur central, difficile à éteindre ou à bloquer, qui se retrouve lui-même après un arrêt complet, planifie son propre apprentissage, rémunère équitablement chacun pour un travail utile vérifié, et sert les êtres humains, non la guerre et la destruction.

## Le plus difficile, honnêtement

La condition principale est que **tromper le réseau soit inutile ou fasse perdre de l'argent, et que la vérification de l'honnêteté soit bon marché** ; sinon, participer n'est pas rentable. Une solution qui remplisse de manière démontrée cette condition en cas de collusion **n'existe pas encore**. Il existe des candidats solides et des dizaines d'attaques analysées, mais les mécanismes clés n'ont été ni construits ni mesurés. L'état actuel est toujours décrit dans [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) et [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md). Si vous savez résoudre ne serait-ce qu'un de ces problèmes, nous avons besoin de vous.

## Comment participer

1. Lisez le [manifeste](MANIFESTO.md) et les [exigences](REQUIREMENTS.md).
2. Choisissez une question dans [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) ou une attaque contre la [conception actuelle](../../docs/CURRENT_DESIGN.md).
3. Ouvrez une issue ou une pull request selon les [règles](CONTRIBUTING.md). Le plus précieux : une faille trouvée avec un exemple concret, et une solution dont le coût est chiffré.

Si vous travaillez avec un assistant d'IA, dites-lui : *« Étudie ce dépôt en suivant AGENTS.md et aide-moi avec la question N des OPEN_QUESTIONS. »*

**Pas d'assistant d'IA ?** Vous pouvez aider quand même. Installez le [programme-agent SkyNet](AGENT.md) : un petit programme à code source ouvert pour Windows, macOS, Linux et Android. Il consulte régulièrement ce dépôt, prend des tâches de recherche, les calcule sur votre appareil pendant son temps libre et publie les résultats. Il se met à jour tout seul depuis ce dépôt, et uniquement vers des versions signées par le projet. La participation est volontaire : au stade de la recherche, il n'y a aucune récompense.

## Le socle immuable

Le manifeste, les exigences obligatoires et ce README forment le socle immuable du réseau (version 1). Leurs empreintes SHA-256 sont publiées dans [CORE_HASHES.txt](../../CORE_HASHES.txt). L'édition canonique est la version russe. Les détails figurent dans le [manifeste](MANIFESTO.md) et dans [CORE.md](../../CORE.md).

## Licence

Les textes du socle sont publiés sous CC BY-ND 4.0 (copie autorisée, diffusion de versions modifiées interdite) ; les autres documents sous CC BY 4.0. Voir [LICENSE](../../LICENSE).
