# 3. Méthodologie de projet

Ce document décrit la démarche suivie, étape par étape, comme un projet de data science bien conduit.
Il s'inspire du cycle CRISP-DM (compréhension, données, préparation, modélisation, évaluation, déploiement).

## 3.1 Compréhension du problème

- **Question.** Produire 5 à 10 mots-clés pertinents pour une note administrative.
- **Critère de succès.** Un F1 supérieur à la baseline, établi par un intervalle de confiance,
  sur un jeu de test non utilisé pour choisir.
- **Contraintes.** Calendrier (lancement 11 novembre, dépôt 23 novembre, soutenance 24 novembre), aucune donnée réelle disponible, reproductibilité,
  méthodes expliquables au jury.

## 3.2 Données

1. Création d'un corpus synthétique de 40 notes (voir `04_fiche_donnees.md`).
2. Validation automatique : schéma, unicité, équilibre, vie privée, couverture (`valider_donnees.py`).
3. Empreinte SHA-256 enregistrée, pour détecter toute modification silencieuse.

## 3.3 Préparation

- Minuscules, apostrophes séparées, mots vides retirés (liste écrite à la main).
- Formes normalisées pour la comparaison : sans accent, pluriel retiré.
- Pour 2c : lemmatisation et filtrage par nature de mot, avec spaCy.

## 3.4 Modélisation

Quatre méthodes, du plus simple au plus riche :

| Ordre | Méthode | Pourquoi elle est là |
|---|---|---|
| 1 | Baseline TF-IDF | référence obligatoire, la plus simple à expliquer |
| 2 | Approche 2a | ajouter des expressions de plusieurs mots |
| 3 | Approche 2b (TextRank) | méthode sans corpus d'entraînement, vue en cours |
| 4 | Approche 2c | lemmatisation et filtrage grammatical, vue en cours |

Chaque méthode a au plus un hyperparamètre, choisi sur le jeu de développement.

## 3.5 Évaluation

1. **Sélection** des hyperparamètres sur dev (10 notes), critère F1 souple à k = 5.
2. **Mesure** sur eval (20 notes), à k = 5 et k = 10.
3. **Mesure finale** sur test (10 notes), une seule fois, méthodes figées.
4. **Incertitude** par bootstrap apparié, 2 000 tirages, IC à 95 %.
5. **Stabilité** : contrôle par mélange d'ordre, perturbation par suppression d'une phrase.
6. **Erreurs** : mots-clés parasites et références absentes du top-5, classées par cause.
7. **Évaluation humaine** : formulaire aveugle sur 20 notes (à réaliser par le binôme).

## 3.6 Itérations et divulgation

Le projet a connu deux versions. Ce qui a changé est listé dans `09_journal_modifications.md`.
Règle suivie : tout ajout de méthode après une première mesure est signalé comme tel, et évalué
sur un jeu que la conception n'a pas utilisé.

## 3.7 Déploiement

Le livrable est une chaîne de commandes (`make`), une démonstration en ligne de commande, et une
documentation. Il n'y a pas de service en production. Une mise en production demanderait :
un service web, une surveillance de la précision humaine, et un filtrage des données personnelles.

## 3.8 Limites de la démarche

- Un seul auteur pour les références.
- Un corpus synthétique.
- Un jeu de test de 10 notes : les intervalles sont larges.
- Pas de test sur de vraies archives.
