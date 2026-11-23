<!-- translation of tasks/README.md, source sha256: 761301bce18193a8aa61cf3fb87ae267379898b5e4164ffab7e23094d1ec08b5 -->

# Tâches pour les agents de recherche

[English](../../tasks/README.md) · [中文](../zh/TASKS.md) · [Español](../es/TASKS.md) · **Français** · [Deutsch](../de/TASKS.md) · [Italiano](../it/TASKS.md) · [Русский](../ru/TASKS.md) · [Português](../pt/TASKS.md) · [العربية](../ar/TASKS.md)

Ce dossier contient le travail que prennent les [agents de recherche](../../agent/README.md) :

- [`index.json`](../../tasks/index.json) : la liste de tâches actuelle ;
- `index.json.sig` : sa signature (les agents ignorent une liste sans signature valide) ;
- [`context/`](../../tasks/context) : les textes figés que citent les questions d'IA.

Les résultats apparaissent comme des commentaires dans le ticket de suivi de chaque tâche et sont résumés dans
[`results/`](../../results) par `tools/collect_results.py`.

## Ce qu'est une tâche

Une tâche est une donnée : le nom d'un calcul intégré à l'agent (un « noyau »), ses
paramètres et le nombre de morceaux indépendants (« unités ») en lesquels le travail est
découpé. Une tâche ne peut pas transporter de code. Un nouveau type de calcul exige une
nouvelle version signée de l'agent.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

Il n'y a pas d'ordonnanceur. Chaque agent choisit au hasard une unité qu'il n'a pas encore
faite. Que plusieurs agents tombent sur la même unité est voulu : tous les noyaux de calcul
sont en arithmétique entière exacte, de sorte qu'un travail égal donne des chiffres égaux sur
chaque appareil, et une unité est considérée comme confirmée lorsque `redundancy` comptes
GitHub différents publient la même empreinte. Des empreintes différentes pour une même unité
sont un conflit qu'un mainteneur règle en la recalculant.

## Noyaux de l'agent 0.1

| Noyau | Ce qu'il calcule | Source |
|---|---|---|
| `selftest@1` | Une charge de travail fixe en nombres entiers ; chaque appareil doit renvoyer la même empreinte | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Gain attendu exact d'un participant qui soumet de faux résultats puis quitte, sur une famille de stratégies ; signale les stratégies qui battent un départ honnête | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Probabilité exacte d'un mois ou d'un trimestre perdant lorsque seules les tâches vérifiées sont payées | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Facultatif : une question pour un modèle d'IA local que fait tourner le participant | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

Chaque fichier source commence par le modèle exact qu'il implémente, afin que chacun puisse recalculer un résultat de façon indépendante.

## Les tâches publiées maintenant, et pourquoi

Toutes concernent la principale question ouverte du projet : peut-on rendre la triche inutile à peu de frais ([OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)).

| Tâche | Question |
|---|---|
| `selftest-1` | Le pipeline fonctionne-t-il sur votre appareil ? |
| `exit-a-honest-check` | Sans collusion, existe-t-il un moyen de profiter de faux résultats avant de quitter ? La conception dit que non |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | Avec de petites tâches égales : à partir de quelle part de vérificateurs complices le fait de quitter avec de faux résultats rapporte-t-il ? L'estimation de la conception est d'environ 91 % |
| `exit-a-uniform-cap-h399` | La même chose avec la limite proposée « au plus un tiers du montant en attente engagé dans des tâches en cours », en trois vagues |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | La même chose lorsque les tâches peuvent avoir n'importe quelle taille, avec et sans cette limite |
| `lottery-b-table` | Si seules les tâches vérifiées sont payées, à quelle fréquence un petit participant a-t-il un mois perdant ? |
| `ask-variant-b-attack` | Pour les modèles d'IA locaux : trouver une nouvelle attaque contre « le réseau ne paie que le travail vérifié » |

Ce sont des calculs sur les règles telles qu'écrites dans les documents de conception. Ce ne
sont ni des mesures de matériel ni des expériences sur le réseau. Les tâches de mesure (par
exemple, de savoir si l'inférence en nombres entiers donne les mêmes bits sur différentes
cartes graphiques) ne seront publiées qu'après que les mainteneurs du projet auront ouvert les
expériences.

## Quatre tâches de la liste 2

Ces tâches nécessitent la séquence de publications 5 de l'agent ou une version ultérieure. Les
neuf tâches d'origine conservent leurs identifiants afin que le travail déjà en cours puisse se
terminer. Chaque nouvelle unité renvoie des fractions exactes sous forme de chaînes décimales
telles que `3/10`.

| Tâche | Comment lire une unité |
|---|---|
| `exit-campaign-b-grid` | Un participant doit-il encaisser ou risquer sa somme en attente sur de faux résultats ? Chaque point indique le meilleur gain attendu au-delà de l'encaissement, combien de faux résultats soumettre d'abord (zéro signifie s'arrêter) et si le gain est positif. Comparer les parts de collusion pour une même somme en attente, une même part de vérification, un même nombre de vérificateurs, un même plafond de vagues et un même horizon. |
| `apprentice-seats-grid` | Combien les clés de la coalition peuvent-elles collecter sur un ensemble fixe de places d'apprenti ? Chaque ligne donne le nombre de clés de la coalition, les récompenses attendues pour une époque et pour toutes les époques, la part honnête des places pourvues et la probabilité qu'aucune clé honnête n'obtienne une place. |
| `lottery-adaptive-grid` | À quelle fréquence un participant honnête perd-il de l'argent lorsque les vérifications sont aussi peu fréquentes que la grille le permet ? Une unité réalisable indique la part de vérification, les probabilités d'une perte et d'une absence de paiement pour un mois et un trimestre, ainsi que la charge de travail mensuelle attendue des vérificateurs. Un point inatteignable signifie que même la part disponible la plus élevée donne moins de 60 vérifications attendues. |
| `token-certificate-grid` | Des bornes de groupe peuvent-elles certifier le jeton au meilleur score avec moins de multiplications ? Chaque unité vérifie les gagnants d'une matrice d'entiers à graine par rapport à un balayage complet et indique les multiplications et les lignes de poids lues, additionnées sur les vecteurs de requête. Le rapport vérification/complet est inférieur à un pour une économie et supérieur à un pour un travail supplémentaire. Il exclut la construction de l'index et la recherche du gagnant annoncé. Les matrices sont aléatoires, donc aucune économie n'est attendue (une première exécution a trouvé environ 0.8 % de travail en plus qu'un balayage complet) ; ces 20 unités sont une référence pour des exécutions ultérieures sur les poids d'un modèle réel. |

## Proposer une tâche

Ouvrez un ticket intitulé `[Task] …` et indiquez :

1. la question à laquelle répond le calcul et la question ouverte à laquelle elle appartient ;
2. le modèle exact, afin qu'il puisse être recalculé de façon indépendante ;
3. quel noyau et quels paramètres le feraient, ou ce qu'un nouveau noyau doit calculer ;
4. comment un résultat faux ou falsifié serait remarqué.

Les mainteneurs vérifient la tâche avec `tools/sign_tasks.py --check`, l'ajoutent à `index.json` et signent
la liste. Seul le détenteur de la clé de publication peut signer ; voir
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
