<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# Ce qui a été vérifié dans le pilote

[English](../../docs/PILOT_RESULTS.en.md) · [中文](../zh/PILOT_RESULTS.md) · [Español](../es/PILOT_RESULTS.md) · **Français** · [Deutsch](../de/PILOT_RESULTS.md) · [Italiano](../it/PILOT_RESULTS.md) · [Русский](../../docs/PILOT_RESULTS.md) · [Português](../pt/PILOT_RESULTS.md) · [العربية](../ar/PILOT_RESULTS.md)

Avant de choisir l'architecture sans coordinateurs, le projet a construit un **pilote de confiance** avec un serveur central
et plusieurs prototypes de recherche sur la vérification. Voici ce qui a réellement été exécuté et mesuré,
et où se situent les limites de ces résultats. Le code source du pilote ne fait pas partie de ce dépôt.

Le pilote est un système fermé avec un opérateur de confiance. Il n'est pas protégé contre la triche dans un réseau ouvert
et n'implémente pas l'architecture cible. Tous les paiements y sont fictifs (TEST_CREDIT, sans retrait).

## Inférence et comptabilisation

| Quoi | Résultat |
|---|---|
| Circuit serveur | API, file d'attente, PostgreSQL, agent, vérification séparée du résultat et crédit fictif dans une seule transaction. Un nouvel envoi ne produit pas de second crédit, une location de tâche périmée est rejetée |
| GPU faible | Qwen2.5-0.5B-Instruct Q4_K_M via llama.cpp (Vulkan) sur le GPU intégré Intel Arrow Lake-P : tâche acceptée, substitution de réponse rejetée |
| Deuxième GPU | Qwen3-4B-Instruct-2507 Q4_K_M sur RTX 2060 6 Go : toutes les couches sur le GPU, environ 2,4 Gio de VRAM, médiane de 73,8 jetons/s sur un profil court |
| Modèle sur plusieurs ordinateurs | Les couches de Qwen3-4B ont été réparties sur le réseau local entre la RTX 2060 et le GPU d'un participant (RTX 4070 Laptop, puis Intel Arrow Lake-P). Le participant ne recevait en mémoire que la partie des poids qui lui était assignée. La paire RTX 2060 + RTX 4070 Laptop a donné environ 38–40 jetons/s contre 69,5 sur une seule RTX 2060 : davantage de mémoire ne garantit pas d'accélération |
| Récupération | Pause, reprise et récupération automatique du groupe après une coupure du tunnel |

La vérification dans le pilote consiste à répéter la génération sur **le même** GPU **de confiance**. Ce n'est pas une preuve
de l'honnêteté d'un nœud inconnu.

## Prototypes de vérification des calculs

| Quoi | Résultat | Limite |
|---|---|---|
| Groth16 pour deux matmul d'entiers + vérificateur Solidity | De vraies preuves et un paiement unique dans une EVM locale | Petite tâche sur CPU |
| RISC Zero pour une ligne de la projection Q4_K de Qwen sur des données réelles | Preuve en 22 min 10 s, vérification en 117 ms, entrées de 11,7 Ko | Une seule ligne, pas tout le graphe ; loin du budget |
| Lot de huit lignes dans une zkVM | 350 ms d'exécution contre 19,8 µs en natif (~17 700×) | Sans construction de preuve |
| Cartesi : contestation du résultat de Qwen | La substitution d'un bit a été détectée ; contestation en 93 transactions, 5,8–6,3 millions de gas | Nécessite un contestataire honnête qui intervient à temps |
| Rejeu complet de l'arithmétique de la ligne dans l'EVM | 14,1 millions de gas par soumission | Une seule ligne |
| Auditeurs automatiques | Un auditeur tiers a réfuté un faux vecteur alors que deux autres étaient d'accord | Sans observateur, l'erreur passait selon la règle optimiste |
| Collusion de l'exécutant et du vérificateur | Ont reçu un paiement pour un résultat incorrect | Montre pourquoi le vote des vérificateurs n'est pas une garantie |

## Ce qui n'a pas eu lieu

- Pas d'apprentissage distribué.
- Pas de quotas matériels stricts CPU/GPU/RAM/VRAM.
- Pas de paiements en argent réel.
- Pas de vérification sur du matériel indépendant dans un réseau ouvert.
- Pas de mesure d'énergie.
- Pas d'expériences sur la nouvelle architecture sans coordinateurs : elle n'est pour l'instant que conçue.
