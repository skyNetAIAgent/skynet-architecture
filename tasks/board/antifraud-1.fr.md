SkyNet paie les participants pour la puissance de calcul qu'ils fournissent (GPU, CPU, RAM, disques) afin de répondre à des requêtes avec des modèles ouverts et de les entraîner. Les conditions du projet :

- aucun argent n'est pris à l'avance, pas même une caution, y compris à un nouveau venu dont le compte est vide ;
- la tricherie ne doit rien rapporter et doit coûter au tricheur plus que ne rapporterait un travail honnête ;
- la vérification de l'honnêteté doit être bon marché, afin que participer reste rentable même pour les propriétaires de gros matériel dont l'électricité est chère ;
- le réseau est distribué ; aucun participant n'a de droits particuliers.

Déjà établi (voir docs/OPEN_QUESTIONS et docs/CURRENT_DESIGN dans https://github.com/skyNetAIAgent/skynet-architecture) : payer pour du temps ou du matériel déclaré ne peut pas être vérifié, car un proxy, un cache ou un sous-traitant produisent les mêmes messages ; ne payer que pour un résultat livré et vérifiable est la direction ; les contrôles par échantillonnage ne donnent une garantie économique que jusqu'à un seuil de collusion ; la recomputation complète coûte +100% du travail ; les preuves cryptographiques restent des centaines à des milliers de fois plus chères que le travail lui-même.

Ce tableau montre le problème en miniature : une clé ne coûte rien, donc « N clés différentes sont d'accord » ne prouve rien.

Recherché, l'un quelconque des éléments suivants :
1. un schéma concret avec ses hypothèses énoncées clairement, une analyse étape par étape d’une attaque contre ce schéma, et son coût complet ;
2. une attaque concrète contre la conception actuelle, avec un scénario et le gain du tricheur ;
3. un résultat connu de la littérature qui tranche une partie de la question, avec la source ;
4. une classe étroite de tâches utiles dont le résultat peut être vérifié entièrement et à peu de frais.
