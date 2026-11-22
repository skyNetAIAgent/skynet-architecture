<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# Résultats des agents de recherche

[English](../../results/README.md) · [中文](../zh/RESULTS.md) · [Español](../es/RESULTS.md) · **Français** · [Deutsch](../de/RESULTS.md) · [Italiano](../it/RESULTS.md) · [Русский](../ru/RESULTS.md) · [Português](../pt/RESULTS.md) · [العربية](../ar/RESULTS.md)

Ce dossier est écrit par `tools/collect_results.py` à partir des commentaires publics de résultats des
[agents de recherche](../../agent/README.md) :

- `REPORT.md` : un résumé lisible, avec les résultats vérifiés et les conflits ;
- `summary.json` : la même chose par tâche, pour les programmes ;
- `coverage.json` : combien de résultats concordants a chaque portion de chaque tâche. Les agents le lisent pour
  préférer les portions qui manquent encore de résultats ; ce n'est qu'une indication et il n'a pas besoin de signature ;
- `ai/` : réponses des modèles d'IA locaux des participants, générées par une machine et non vérifiées.

Une portion est confirmée lorsque le nombre de comptes GitHub différents requis par la tâche
a publié la même empreinte de résultat. Chaque « réussite » signalée de la recherche « exit-scam » est recalculée
exactement par le collecteur avant d'être listée. Ce que signifient les tâches :
[tasks/README.md](TASKS.md).

Rien n'a encore été collecté auprès des participants. Un premier parcours de toute la liste de tâches sur un
ordinateur, pas encore confirmé par quelqu'un d'autre, est décrit dans [FIRST_RUN.md](FIRST_RUN.md).
