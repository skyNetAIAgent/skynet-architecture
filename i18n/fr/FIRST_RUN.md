<!-- translation of results/FIRST_RUN.md, source sha256: 786aa2e462922d0a3a2ec06d0da0e26d246a2563867e215a11cfbf5a799bfe0a -->

# Premier lancement de la première liste de tâches (un seul ordinateur, pas encore confirmé)

[English](../../results/FIRST_RUN.md) · [中文](../zh/FIRST_RUN.md) · [Español](../es/FIRST_RUN.md) · **Français** · [Deutsch](../de/FIRST_RUN.md) · [Italiano](../it/FIRST_RUN.md) · [Русский](../ru/FIRST_RUN.md) · [Português](../pt/FIRST_RUN.md) · [العربية](../ar/FIRST_RUN.md)

Le 22 novembre 2026, chaque unité de la liste de tâches numéro 1 a été calculée une fois sur un
seul ordinateur Windows avec le même code que les agents exécutent : 702 unités, 15,5 heures CPU,
aucun échec. Un seul ordinateur n'est pas une confirmation. Les nombres ci-dessous ne deviennent
des résultats du projet que lorsque d'autres participants publient les mêmes empreintes (voir
[README.md](RESULTS.md)).

## Partir avec de faux résultats (kernel `exit-scam-a@1`, variante A de la conception)

Un participant disposant d'un montant H0 « en attente » soumet de faux résultats en quelques vagues
rapides et part. S'il partait simplement, il obtiendrait H0. Le tableau donne la plus petite part de
vérificateurs complices à partir de laquelle une stratégie de la famille examinée a un gain espéré
supérieur à H0. Le modèle exact figure en haut de
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py).

| Tâche | Stratégies examinées | Part de collusion à partir de laquelle c'est rentable | Meilleur gain espéré à ce niveau |
|---|---:|---|---|
| `exit-a-honest-check` : pas de collusion, taille de tâche quelconque, deux vagues | 92,169,600 | jamais | 0.980 × H0 |
| `exit-a-uniform-h399` : petites tâches égales, 399 prix en attente, une vague | 7,600 | 0.892 (pas à 0.890) | 1.0066 × H0 |
| `exit-a-uniform-h1200` : petites tâches égales, 1200 prix en attente, une vague | 22,800 | 0.908 (pas à 0.906) | 1.0117 × H0 |
| `exit-a-uniform-cap-h399` : petites tâches égales, trois vagues, « au plus un tiers en cours » | 71,772,196 | 0.890 (pas à 0.888) | 1.0059 × H0 |
| `exit-a-sizes-cap` : taille de tâche quelconque, trois vagues, « au plus un tiers en cours » | 1,190,974,992 | 0.875 (pas à 0.870) | 1.00004 × H0 ; 1.034 × H0 à 0.880 |
| `exit-a-sizes-nocap` : taille de tâche quelconque, deux vagues, sans cette limite | 69,148,800 | 0.800 (pas à 0.780) | 1.218 × H0 ; 4.91 × H0 à 0.850 |

Ce que cela suggère :

- L'estimation de la conception « tricher est perdant tant que les complices détiennent moins
  d'environ 91% » provient de la moyenne sur un seul faux. Elle ne tient pas compte du fait qu'un
  participant ne peut pas perdre plus que le montant en attente (il n'y a ni dépôts ni amendes).
  Pour quelqu'un qui part, la perte est plafonnée et le gain ne l'est pas, ce qui abaisse le seuil
  à environ 87,5–89%.
- La règle proposée « au plus un tiers du montant en attente en cours à la fois » est nécessaire.
  Sans elle, les récompenses non vérifiées de la première vague augmentent le montant en attente et
  permettent des tâches plus grandes dans la deuxième vague, et le seuil tombe à environ 80%.
- Sans collusion, aucun moyen rentable de partir avec de faux résultats n'a été trouvé.

Limites : il s'agit d'un calcul dans un modèle formel des règles, pas d'une mesure ; la recherche
ne couvre que les familles listées ; la grille des parts de collusion a des pas de 0,002 à 0,02.

## Ne payer que les tâches vérifiées (kernel `lottery-b@1`, variante B de la conception)

Probabilité que le revenu d'une période soit inférieur au coût du travail effectué pendant cette
période, lorsqu'une tâche est vérifiée avec une probabilité de 1/P et qu'une tâche vérifiée est
payée P prix. Sommes binomiales exactes.

| Tâches par mois | Vérifiée | Coût / prix | Mois perdants | Trimestres perdants |
|---:|---|---:|---:|---:|
| 600 | 1 sur 10 | 95% | 32.20% | 22.91% |
| 6,000 | 1 sur 100 | 95% | 33.10% | 24.02% |
| 6,000 | 1 sur 100 | 80% | 4.84% | |
| 60,000 | 1 sur 100 | 95% | 10.47% | 1.55% |
| 200,000 | 1 sur 100 | 95% | 1.15% | |
| 200,000 | 1 sur 100 | 98% | 18.15% | |
| 600 | 1 sur 100 | 95% | 44.49% | |

Avec 600 tâches par mois et 1 sur 100 vérifiée, rien du tout n'est payé dans 0,24% des mois. Le
tableau complet compte 360 cellules ; il apparaîtra dans `summary.json` une fois que les agents
l'auront publié.
