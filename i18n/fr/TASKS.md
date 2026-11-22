<!-- translation of tasks/README.md, source sha256: f0685cfe87baef739cff7ff9121f8ab2fd0aed86866b5638fd79dcdd347c1916 -->

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

## Proposer une tâche

Ouvrez un ticket intitulé `[Task] …` et indiquez :

1. la question à laquelle répond le calcul et la question ouverte à laquelle elle appartient ;
2. le modèle exact, afin qu'il puisse être recalculé de façon indépendante ;
3. quel noyau et quels paramètres le feraient, ou ce qu'un nouveau noyau doit calculer ;
4. comment un résultat faux ou falsifié serait remarqué.

Les mainteneurs vérifient la tâche avec `tools/sign_tasks.py --check`, l'ajoutent à `index.json` et signent
la liste. Seul le détenteur de la clé de publication peut signer ; voir
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
