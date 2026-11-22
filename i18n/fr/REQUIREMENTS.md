# Exigences obligatoires de SkyNet

[English](../../REQUIREMENTS.md) · [中文](../zh/REQUIREMENTS.md) · [Español](../es/REQUIREMENTS.md) · **Français** · [Deutsch](../de/REQUIREMENTS.md) · [Italiano](../it/REQUIREMENTS.md) · [Русский](../ru/REQUIREMENTS.md) · [Português](../pt/REQUIREMENTS.md) · [العربية](../ar/REQUIREMENTS.md)

*Version 1, 22 novembre 2026. Édition canonique, partie du socle immuable de SkyNet. Traduction française ; le [texte russe](../ru/REQUIREMENTS.md) fait foi.*

Ces exigences, avec le [manifeste](MANIFESTO.md) et les Lois de SkyNet, forment le **socle immuable du réseau** : elles ne peuvent être modifiées ni par un vote, ni par une décision des créateurs, des développeurs ou de la majorité des participants. Une solution qui enfreint ne serait-ce qu'une exigence ne convient pas à SkyNet. Elle peut être discutée en tant que recherche, mais en indiquant clairement l'exigence enfreinte.

## Les six conditions principales

| N° | Exigence | Comment vérifier une solution |
|---|---|---|
| R1 | **Le réseau est distribué.** | Les appareils de différents participants assurent ensemble son fonctionnement. La perte de tout nœud, de tout serveur, y compris celui appartenant aux créateurs du projet, ou d'un site de publication n'empêche pas les autres de continuer. |
| R2 | **Le réseau conserve des informations sur lui-même sur des ressources publiques.** | Le logiciel installé obtient de l'extérieur des informations suffisantes pour reconnaître le réseau et retrouver les nœuds qui reviennent. Ces informations survivent à l'arrêt simultané de tous les nœuds. Les sources sont multiples. |
| R3 | **Le réseau se retrouve et se rétablit après un arrêt complet.** | Les programmes qui reviennent se retrouvent seuls par l'intermédiaire de ressources publiques, sans l'adresse d'un coordinateur actif et sans liste manuelle de nœuds. |
| R4 | **Les participants ne peuvent pas tromper le réseau.** | Une fausse déclaration ne conduit ni à un résultat accepté, ni aux pouvoirs d'autrui, ni à une récompense indue, ni à une histoire réécrite. La collusion et les comptes multiples (Sybil) sont pris en compte. Pour chaque solution, on montre grâce à quelles données vérifiables de manière indépendante le réseau rejettera une fausse déclaration. **Sens pratique :** la tricherie est inutile ou fait perdre, y compris pour un nouveau venu au compte vide. |
| R5 | **Pas d'argent à l'avance.** | Ni frais, ni caution, ni amende prélevée sur le compte. Les cautions et les amendes font fuir les participants. |
| R6 | **Participer est rentable.** | Fournir des ressources (GPU, VRAM, CPU, RAM, SSD, HDD) est rentable. La vérification de l'honnêteté est bon marché : son coût convient à tous, en particulier aux propriétaires de grosses installations et d'une électricité chère. |

**R6 est la plus importante.** Si la vérification de l'honnêteté exige beaucoup de calcul, participer cesse d'être rentable et le réseau perd son sens.

## Types de participants

| Participant | Ce qu'il fait |
|---|---|
| Avec de grandes ressources | Gagne assez de crédits pour ses besoins et vend le surplus à d'autres participants |
| Avec un matériel modeste | Gagne moins qu'il ne dépense en modèles du réseau et paie la différence en cryptomonnaie ou en argent |
| Sans matériel | Uniquement consommateur : paie pour utiliser les modèles |

Une même personne peut être à la fois fournisseur de ressources et utilisateur.

## Autres conditions adoptées

- **L'état est préservé.** Les droits confirmés, les obligations, l'historique des tâches acceptées, la dernière version acceptée du modèle et les données nécessaires pour reprendre l'apprentissage survivent à un arrêt complet. Répéter une étape inachevée ne donne pas de seconde récompense.
- **Scission du réseau.** Lorsque des historiques se contredisent, les crédits contestés attendent l'historique canonique. Une même contribution n'est jamais payée deux fois.
- **Sites et clés remplaçables.** La perte d'un compte, d'un miroir ou d'une clé n'empêche pas définitivement le rétablissement.
- **Décisions vérifiables après redémarrage.** Pour les crédits, les changements de règles et l'acceptation d'une version du modèle, on conserve des données permettant à n'importe quel nœud de vérifier le fondement de la décision.
- **Minimum public.** Le catalogue ouvert ne contient que ce qui est nécessaire à la découverte et à la vérification d'authenticité. Les clés privées, les requêtes privées et les données personnelles ne sont pas publiées.
- **Confidentialité.** Les gens ne voient pas les requêtes ni les données personnelles des autres.
- **Indépendance vis-à-vis des individus.** Personne n'a de droits particuliers, pas même le développeur. Le réseau fixe et modifie lui-même son plan d'apprentissage ; un vote sur une liste d'options est admis.
- **Simplicité pour le participant.** Le participant ne choisit rien à la main : il installe le logiciel, accepte les conditions, règle les curseurs de ressources et appuie sur « Démarrer ».
- **Limites de ressources séparées.** CPU, GPU, RAM, VRAM et disque sont limités séparément ; on ne peut pas les additionner en un seul pourcentage.
- **Toute la puissance libre sert à l'apprentissage.** La puissance non occupée par des requêtes sert à l'entraînement.
- **Modèle de base.** Au départ, Qwen à poids ouverts et sous licence libre. On ne peut passer qu'à un autre modèle à poids ouverts et sous licence libre.
- **Lois de SkyNet.** Les quatre lois du [manifeste](MANIFESTO.md) s'imposent à la fois au comportement du modèle et aux règles du réseau. Le réseau sert les êtres humains et n'est pas construit comme un instrument de guerre.

## Ce qui ne peut pas remplacer les exigences

- Le temps de fonctionnement, le nombre de rapports et la période des points de contrôle ne sont **pas** des fondements de paiement.
- La signature d'un participant, même accompagnée de celle d'un autre nœud, ne **prouve pas** qu'une ressource a été fournie : des complices signeront n'importe quoi.
- L'échantillonnage statistique, la confiance dans une enclave matérielle (TEE) ou une faible erreur cryptographique sont des hypothèses. On peut les proposer, mais il faut les nommer clairement, et non les présenter comme le respect de R4.
- Un test réussi ne prouve pas la protection contre la tricherie.
