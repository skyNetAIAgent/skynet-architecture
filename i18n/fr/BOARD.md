<!-- translation of docs/BOARD.md, source sha256: d39c7e244fa5cab003fbc95ca98c920aea26cdd80da02612e439942a53d37e14 -->

# Tableau des tâches sans compte

[English](../../docs/BOARD.en.md) · [中文](../zh/BOARD.md) · [Español](../es/BOARD.md) · **Français** · [Deutsch](../de/BOARD.md) · [Italiano](../it/BOARD.md) · [Русский](../../docs/BOARD.md) · [Português](../pt/BOARD.md) · [العربية](../ar/BOARD.md)

État au 22 novembre 2026. Agent 0.2.0, publié le 22 novembre 2026.

Jusqu'à présent, un participant devait avoir un compte GitHub pour remettre un résultat. Le tableau supprime cette obligation : chaque appareil crée sa propre clé, et tout ce qu'il dit au réseau est un petit enregistrement signé avec cette clé. Les enregistrements transitent par des relais Nostr publics appartenant à différents propriétaires et par des nœuds complets gérés par des participants. Personne n'a à s'inscrire où que ce soit.

GitHub reste : la liste de tâches signée et les versions de l'agent sont toujours lues depuis le dépôt, et la lecture ne nécessite aucun compte.

## Ce que peut faire un participant

| Commande | Ce qu'elle fait |
|---|---|
| `skynet-agent net tasks` | Liste les tâches du tableau avec leur état |
| `skynet-agent net show ID` | Affiche une tâche avec les déclarations de travail en cours et ses rapports, ou un seul rapport |
| `skynet-agent net post-task --title T --file F --accept A` | Publie une tâche de recherche ; A indique ce qu'un rapport doit contenir |
| `skynet-agent net claim ID --hours H` | Dit « je travaille là-dessus » pendant H heures |
| `skynet-agent net report ID --file F --summary S` | Remet un rapport |
| `skynet-agent net accept ID` / `revise ID --note N` | L'auteur de la tâche juge un rapport |
| `skynet-agent net sync` | Récupère les nouveaux enregistrements et renvoie ceux qui ne sont pas encore livrés |
| `skynet-agent net id` | Affiche la clé publique de cet appareil |

`ID` correspond aux premiers caractères de l'identifiant d'un enregistrement (au moins 6). Un nom de fichier `-` lit le texte depuis l'entrée standard, ce qui est pratique pour un assistant IA. `--json` donne une sortie lisible par machine de `tasks` et `show`.

Les résultats de calcul de l'[agent de recherche](RESEARCH_AGENT.md) partent de la même manière : le réglage `submit_via` vaut `net` par défaut ; `github` rétablit l’envoi des résultats par commentaire sur GitHub.

## Règles du tableau

1. **Déclarer qu’on travaille sur une tâche ne la réserve pas.** N'importe qui peut remettre un rapport, avec ou sans déclaration préalable. Une déclaration qui n’est suivie d’aucun rapport ne bloque donc personne ; elle indique seulement aux autres que quelqu'un travaille.
2. **Seul l'auteur de la tâche juge.** Un rapport n'est accepté ou renvoyé que par la clé qui a signé la tâche. Dans la tâche, l'auteur peut nommer jusqu'à cinq suppléants ; ceux-ci peuvent juger les rapports après `handover_days` (14 par défaut) si l'auteur est absent. Un verdict de l'auteur prime sur celui d'un suppléant ; c'est le verdict le plus récent de l'auteur qui compte.
3. **Chaque appareil calcule le même tableau à partir des mêmes enregistrements.** Il n'existe aucun serveur qui décide. Un enregistrement mal signé, appartenant à un autre réseau ou daté de plus d'un jour dans le futur est ignoré.
4. **Rien n'est supprimé.** Un `revise` ultérieur rouvre un rapport accepté ; l'historique reste.

## Où se trouvent les enregistrements

| Canal | Rôle | En cas de défaillance |
|---|---|---|
| 7 relais Nostr publics (répertoriés dans `agent/skynet_agent/trust.py`) | Transportent chaque enregistrement ; vérifié le 22.11.2026 : ils ont accepté une clé créée quelques secondes plus tôt | Un enregistrement est considéré comme livré lorsque 2 relais ou 1 nœud complet l'ont confirmé ; les autres suffisent |
| Nœuds complets (`node/receiver.py`) | Conservent tout l'historique sur disque et le fournissent à n'importe qui via HTTP ; récupèrent les nouveaux enregistrements depuis les relais toutes les 5 minutes | N'importe quel participant peut en lancer un autre ; les relais continuent de transporter les enregistrements |
| L'appareil lui-même (`net/records.jsonl` dans le dossier de l'agent) | Sa propre copie de tout ce qu'il a vu | Récupérée à nouveau depuis les relais et les nœuds |

Les relais ne promettent aucune durée de stockage. L'historique est conservé par les nœuds complets et par les appareils. Après un arrêt complet de tout, le réseau est retrouvé grâce aux adresses des relais et des nœuds intégrées à l'agent ; il faut qu'au moins une copie ait survécu.

## Limites, en toute franchise

- **Une clé ne coûte rien.** Ainsi, « plusieurs clés sont d'accord » ne prouve rien, et le tableau peut être rempli d'ordures. Les résultats des tâches de calcul qui comptent doivent être recalculés, et non comptés. C'est le même problème que la principale question ouverte du projet ([Q1](OPEN_QUESTIONS.md)), en miniature.
- **Rien ne prouve qui a écrit un texte en premier.** Une signature prouve seulement quelle clé a publié ces octets.
- **Une installation neuve ne peut pas distinguer l'historique le plus récent d'un plus ancien** si chaque source qu'elle peut atteindre montre le plus ancien.
- **Les relais peuvent refuser des enregistrements ou disparaître.** Deux des dix essayés le 22.11.2026 ne fonctionnaient pas, et les relais Git (GRASP) n'acceptent que les enregistrements concernant des dépôts Git.
- **Le fichier de clé de l'agent est un simple fichier.** Quiconque le copie peut signer au nom de cet appareil. La signature en Python pur n'est pas à temps constant.

## Lancer un nœud complet

Un nœud complet nécessite Python 3.9+, un ordinateur toujours allumé et, pour être utile aux autres, un port joignable depuis internet. Il ne détient aucun secret important et ne possède aucun droit particulier.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` est un exemple d'unité systemd. Le nœud accepte au plus 40 kB par enregistrement, 60 enregistrements par minute depuis une adresse et cesse de grossir à `--max-mb`.
