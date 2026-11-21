# 1. Objectif du projet et glossaire

Ce document s'adresse à toute personne qui découvre le projet : étudiants du binôme, jury, lecteurs futurs.
Il répond à trois questions : pourquoi, quoi, et avec quels mots.

## 1.1 Pourquoi ce projet

Une administration reçoit et produit chaque jour des notes : demandes de congé, notes de service,
convocations, avis de paiement. Pour retrouver un document plus tard, il faut le classer.
Relire chaque note en entier prend du temps.

**Question centrale.** Peut-on demander à un programme de proposer 5 à 10 mots-clés qui résument
une note, avec une méthode simple, mesurable et reproductible ?

## 1.2 Ce que le projet produit

1. Un **programme** qui, pour une note, renvoie des mots-clés classés (`demo/demo_mots_cles.py`).
2. Un **protocole de mesure** : on compare les mots-clés proposés aux mots-clés de référence.
3. Des **résultats chiffrés**, avec leur incertitude, et une **analyse d'erreurs** honnête.
4. Une **chaîne reproductible** : une seule commande (`make tout`) reconstruit tout.

## 1.3 Ce que le projet ne fait pas

- Il ne traite pas de vrais documents : le corpus est synthétique (40 notes fictives).
- Il n'utilise pas de grand modèle de langage, par choix (voir `02_architecture.md`, décision D2).
- Il ne classe pas automatiquement les documents dans des dossiers d'archivage. C'est une extension
  possible, pas une fonctionnalité livrée.

---

## 1.4 Glossaire pédagogique

Chaque entrée suit le même plan : définition, explication, importance, exemple, erreur fréquente.

### Mot-clé
- **Définition.** Un mot ou une expression courte qui résume le sujet d'un texte.
- **Explication.** « demande de congé annuel » est un mot-clé ; « annuel » seul l'est moins.
- **Importance.** Il permet de classer et de retrouver un document sans le relire.
- **Exemple.** Pour une note d'achat de matériel, « matériel informatique » est un bon mot-clé.
- **Erreur fréquente.** Confondre mot-clé et mot fréquent. Un mot peut être fréquent sans être utile
  (« service » apparaît partout dans l'administration).

### Mot vide (*stop word*)
- **Définition.** Un mot très courant qui porte peu de sens seul : « le », « de », « et ».
- **Explication.** On les retire avant de chercher les mots-clés. Dans ce projet, la liste est écrite
  à la main (`src/text_utils.py`) et contient aussi des termes administratifs (« objet », « merci »).
- **Erreur fréquente.** Oublier que « de » coupe une expression : « guichet de paiement » devient
  deux morceaux.

### Lemme et lemmatisation
- **Définition.** Le lemme est la forme de base d'un mot (« étudiants » → « étudiant »).
  La lemmatisation consiste à trouver ce lemme.
- **Explication.** spaCy fait cette opération avec un modèle entraîné sur du français.
- **Importance.** « rattraper » et « rattrapage » deviennent comparables.
- **Limite observée.** Le modèle utilisé se trompe parfois : « fiche » devient « fich ».
  Ce défaut est documenté dans `05_fiche_modele.md`.

### Catégorie grammaticale (POS, *part of speech*)
- **Définition.** La nature d'un mot : nom (NOUN), nom propre (PROPN), adjectif (ADJ), verbe (VERB)…
- **Explication.** L'approche 2c ne garde que les noms, noms propres et adjectifs, car ce sont
  surtout eux qui portent le sujet d'un document.
- **Erreur fréquente.** Croire que le filtre est parfait. Un nom peut être pris pour un autre
  (« cours » au sens de cours d'eau ou de cours de formation).

### TF-IDF
- **Définition.** Un score qui donne plus de poids à un mot fréquent dans un document et rare dans le corpus.
- **Explication.** TF (*term frequency*) est la fréquence du mot dans la note. IDF (*inverse document
  frequency*) mesure sa rareté dans le corpus. Le score est leur produit.
  Dans le code, scikit-learn applique aussi une transformation sous-linéaire du TF : 1 + ln(tf).
- **Importance.** C'est la méthode de référence (baseline) en recherche d'information depuis Salton
  et Buckley (1988).
- **Exemple.** Dans la note N14 (avis de paiement), la référence contient « maintenance des climatiseurs ».
  Un score TF-IDF élevé sur « climatiseurs » serait cohérent avec cette référence ; le projet le mesure, il ne le suppose pas.
- **Erreur fréquente.** Penser que TF-IDF comprend le sens. Il compte des mots. Il peut donc retenir un
  nombre issu d'un montant : sur la note N24, la baseline propose « 400 ».

### Graphe de cooccurrence et TextRank
- **Définition.** Un graphe où les mots sont des nœuds, reliés s'ils apparaissent près l'un de l'autre.
- **Explication.** TextRank (Mihalcea et Tarau, 2004) applique PageRank à ce graphe. Un mot important
  est un mot lié à d'autres mots importants.
- **Importance.** Il ne demande aucun entraînement : il marche sur une seule note.
- **Erreur fréquente.** Croire que le mot le plus connecté est le plus thématique. « heures » peut être
  très connecté dans une note sur les horaires sans être le sujet.

### PageRank
- **Définition.** Algorithme qui classe les nœuds d'un graphe selon leur importance, en la répartissant
  entre voisins (Page et al., 1999).
- **Explication.** Ici, le poids d'une arête est le nombre de fois où deux mots se suivent de près.
  L'amortissement de 0,85 est la valeur classique.

### Précision, rappel, F1
- **Précision.** Parmi les mots-clés proposés, part de ceux qui correspondent à une référence.
- **Rappel.** Parmi les mots-clés de référence, part de ceux qui ont été trouvés.
- **F1.** Moyenne harmonique : F1 = 2 × P × R / (P + R).
- **Exemple.** P = 0,5 et R = 0,4 donnent F1 ≈ 0,44. La moyenne harmonique pénalise le déséquilibre.
- **Erreur fréquente.** Ne lire que la précision. Un système qui propose un seul mot juste a une
  précision parfaite et un rappel très faible.

### Correspondance stricte et souple
- **Stricte.** Les deux expressions ont les mêmes mots (après normalisation).
- **Souple.** L'ensemble des mots de l'une est inclus dans l'autre. « congé » correspond à
  « demande de congé annuel ».
- **Erreur fréquente.** Juger la baseline sur la stricte : un mot isolé ne peut pas égaler une
  expression de trois mots. La souple est la mesure principale.

### Coefficient de Jaccard
- **Définition.** Pour deux ensembles A et B : |A ∩ B| / |A ∪ B|. Il vaut 1 si les ensembles sont identiques.
- **Usage ici.** Mesurer si les mots-clés changent quand la note est légèrement modifiée (stabilité).

### Stabilité
- **Définition.** Capacité d'une méthode à donner les mêmes mots-clés face à une petite modification.
- **Attention.** Mélanger l'ordre des phrases ne change rien pour TF-IDF : le score est égal à 1 par
  construction. C'est un contrôle, pas une preuve. Le vrai test est la suppression d'une phrase.

### Intervalle de confiance par bootstrap
- **Définition.** Une fourchette qui dit où se trouve probablement la vraie différence entre deux méthodes.
- **Explication.** On tire les notes au hasard avec remise, 2 000 fois, et on recalcule l'écart à chaque
  tirage. On garde les bornes à 2,5 % et 97,5 %.
- **Lecture.** Si la fourchette contient 0, l'écart n'est pas établi.
- **Erreur fréquente.** Conclure d'un écart de 0,05 sur 10 notes. La fourchette est souvent plus large.

### Jeu de développement, d'évaluation et de test
- **Développement (dev, 10 notes).** On y choisit les hyperparamètres.
- **Évaluation (eval, 20 notes).** On y mesure, mais elle a aussi guidé la conception de 2c.
- **Test (test, 10 notes).** Jeu gelé, rédigé après la conception, mesuré une seule fois.
- **Erreur fréquente.** Choisir une méthode sur le jeu de test. C'est une fuite : le score devient optimiste.

### Fuite de données (*data leakage*)
- **Définition.** Information du jeu de test qui influence le modèle ou les choix avant la mesure finale.
- **Exemple dans ce projet.** Apprendre l'IDF sur les notes de test. Ce choix a été corrigé : l'IDF
  est appris hors test.

---

## Résumé à retenir

1. Un mot-clé résume une note ; le projet compare quatre façons de le trouver.
2. Les mesures sont la précision, le rappel et le F1, en correspondance souple.
3. Un écart n'a de valeur que s'il est établi par un intervalle de confiance.
4. Le jeu de test ne sert qu'à la mesure finale, jamais au choix d'une méthode.
