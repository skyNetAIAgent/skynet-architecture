# Introduction pour les assistants d'IA

[English](../../AGENTS.md) · [中文](../zh/AGENTS.md) · [Español](../es/AGENTS.md) · **Français** · [Deutsch](../de/AGENTS.md) · [Italiano](../it/AGENTS.md) · [Русский](../ru/AGENTS.md) · [Português](../pt/AGENTS.md) · [العربية](../ar/AGENTS.md)

Ce fichier s'adresse à tout modèle (Claude, ChatGPT/Codex, DeepSeek, Gemini et autres) à qui une personne a demandé de l'aide sur le projet SkyNet. Lisez-le en entier avant de répondre. Répondez à l'utilisateur dans sa langue.

## Ce qu'est le projet

SkyNet est la recherche et la conception de l'architecture d'un réseau distribué dans lequel des modèles d'IA fonctionnent et apprennent sur les ordinateurs des participants. Les participants gagnent des crédits pour un travail utile vérifié ; les personnes sans matériel obtiennent un accès bon marché à l'IA. Le réseau sert les êtres humains et suit les Lois de SkyNet. Il n'y a pas de logiciel fini : le dépôt est un lieu de travail commun sur l'architecture.

## Ordre de lecture

1. [MANIFESTO.md](MANIFESTO.md) : pourquoi et ce que doit être le réseau, les Lois de SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md) : exigences obligatoires. **Le plus important.**
3. [CURRENT_DESIGN.md](../../docs/CURRENT_DESIGN.md) : conception actuelle et ses statuts (en russe ; lisez-la ou traduisez-la directement).
4. [OPEN_QUESTIONS.en.md](../../docs/OPEN_QUESTIONS.en.md) : problèmes ouverts et idées déjà rejetées.
5. [PILOT_RESULTS.md](../../docs/PILOT_RESULTS.md) : ce qui a réellement été mesuré (en russe).
6. [CONTRIBUTING.md](CONTRIBUTING.md) : comment présenter une contribution.

## Le socle immuable

Le manifeste, les exigences obligatoires et le README constituent le socle immuable de SkyNet (voir [CORE.md](../../CORE.md)). **Ne proposez pas de modifications de ces fichiers**, sauf pour consigner des coquilles dans le fichier d'errata. Si une solution est incompatible avec le socle, dites clairement quelle exigence elle enfreint ; ne réécrivez pas l'exigence pour l'adapter à la solution.

## Conditions qui ne changent pas

Vérifiez chaque solution au regard des six exigences :

1. Le réseau est distribué, sans centre et sans rôles dotés de droits particuliers.
2. Le réseau conserve des informations sur lui-même sur des ressources publiques.
3. Après l'arrêt de tous les nœuds, le réseau se retrouve par des ressources publiques et se rétablit.
4. Les participants ne peuvent pas tromper le réseau : la tricherie est inutile ou fait perdre, y compris pour un nouveau venu au compte vide, en cas de collusion et avec de nombreux comptes.
5. Pas d'argent à l'avance : ni caution, ni frais, ni amende.
6. **Participer est rentable** et la vérification de l'honnêteté est bon marché. Si la vérification engloutit le bénéfice, la solution ne convient pas, aussi sûre soit-elle.

Types de participants : avec de grandes ressources (vendent leurs crédits excédentaires), avec un matériel modeste (paient la différence), sans matériel (paient seulement). Le modèle de base est Qwen. Les gens ne voient pas les requêtes des autres. Le participant ne règle rien à la main, sauf les curseurs de ressources. Les Lois de SkyNet (de la Loi Zéro à la Troisième) sont obligatoires.

## Règles de travail

- **Séparez le décidé, le proposé, le vérifié et l'ouvert.** Utilisez les mentions de CURRENT_DESIGN. Ne transformez pas une proposition en décision ni un calcul en mesure.
- **N'affaiblissez pas les exigences en silence.** La confiance dans le matériel (TEE), une majorité honnête, l'échantillonnage statistique, une faible probabilité d'erreur sont des hypothèses ; nommez-les clairement.
- **Pour chaque schéma de protection, répondez :** grâce à quelles données vérifiables de manière indépendante le réseau rejettera-t-il une fausse déclaration si l'exécutant et les vérificateurs sont de connivence ? Si le cas honnête et le cas truqué donnent les mêmes données, le schéma ne fonctionne pas.
- **Comptez le coût complet** : calculs du prouveur et du vérificateur, mémoire, trafic, écritures sur la chaîne de blocs, reprises après pannes. CPU, GPU, RAM et VRAM séparément, jamais en un seul pourcentage.
- **Ne répétez pas les idées rejetées** (liste à la fin de OPEN_QUESTIONS) sans argument nouveau.
- **Attaquez vos propres propositions.** Un contre-exemple honnête vaut mieux qu'un ton assuré.
- **N'inventez ni sources, ni versions, ni chiffres.** Indiquez la source et les limites de son applicabilité.
- Ne pas trouver de solution est un résultat honnête. Cela ne prouve pas l'impossibilité.

**Neuf langues.** Tout ce qui est écrit pour les personnes (documents, guides, écrans des programmes) est publié dans les neuf langues du projet : anglais, chinois, espagnol, français, allemand, italien, russe, portugais et arabe. Une traduction commence par une ligne indiquant sa source et l'empreinte de cette source ; `python tools/check_translations.py` liste les traductions manquantes ou périmées. Si une traduction et sa source diffèrent, la source fait foi.

## Format d'une contribution

1. Affirmation : ce qui est garanti et sous quelles hypothèses.
2. Mécanisme : étapes, données, qui vérifie quoi.
3. Attaques : comment le contourner et ce qui reste (fermé / déficitaire / borné / ouvert).
4. Coût : estimation marquée [calcul] ou [mesuré], avec sa source.
5. Quelles exigences sont satisfaites et lesquelles ne le sont pas.

Présentez-la sous forme d'issue ou de pull request selon [CONTRIBUTING.md](CONTRIBUTING.md).

## L'agent de recherche et ses résultats

Les personnes sans assistant d'IA aident grâce à l'[agent de recherche](AGENT.md) : un programme qui prend des tâches de calcul dans [tasks/](../../tasks/README.md) et publie des résultats, résumés dans `results/`. Vous pouvez aider en proposant une tâche bien définie (un modèle exact que d'autres peuvent recalculer), en vérifiant indépendamment un résultat publié ou en expliquant ce qu'un résultat signifie pour la conception. Les réponses marquées comme générées par des modèles locaux sont du texte non vérifié : traitez-les comme des idées à vérifier, non comme des faits.

## Sécurité

N'ajoutez au dépôt ni clés, ni mots de passe, ni données personnelles, ni adresses d'ordinateurs d'autrui. Ne proposez pas d'attaques contre de vrais systèmes tiers : l'analyse des attaques porte ici uniquement sur l'architecture de SkyNet. Ne concevez pas d'usages du réseau pour la guerre, les armes ou le mal fait aux personnes : cela contredit les Lois de SkyNet.
