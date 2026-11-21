# 2. Architecture et décisions techniques

Public visé : développeurs et ingénieurs qui reprennent le code, et jury qui pose des questions de conception.

## 2.1 Vue d'ensemble du flux de données

```
data/corpus_notes_administratives.json (40 notes, 3 jeux)
        │
        ▼
src/valider_donnees.py ──► results/validation_donnees.md
        │                  data/MANIFEST.json (empreinte SHA-256)
        ▼
src/text_utils.py  ─────►  prétraitement : minuscules, apostrophes, mots vides, formes normalisées
        │
        ▼
src/methods.py     ─────►  4 extracteurs : baseline, 2a, 2b, 2c   (paramètres : src/config.py)
        │
        ├──► src/evaluate.py ──────► results/*.csv, parametres_retenus.json
        │         │
        │         └──► src/analyse_statistique.py ──► results/intervalles_confiance.csv
        │
        ├──► src/annotation_humaine.py ──► formulaire aveugle (évaluation humaine)
        │
        └──► demo/demo_mots_cles.py  (démonstration en ligne de commande)
```

## 2.2 Responsabilités des modules

| Module | Rôle | Dépend de |
|---|---|---|
| `src/config.py` | Toutes les constantes : chemins, graine, grilles, hyperparamètres retenus | rien |
| `src/text_utils.py` | Fonctions pures de prétraitement, sans état | rien |
| `src/methods.py` | Les quatre extracteurs, sur le même contrat `extraire(texte, k)` | `config`, `text_utils`, scikit-learn, networkx, spaCy |
| `src/evaluate.py` | Sélection sur dev, mesures, stabilité, erreurs | `config`, `methods`, `text_utils` |
| `src/analyse_statistique.py` | Bootstrap apparié sur les différences de F1 | `config` |
| `src/valider_donnees.py` | Contrôles de qualité et de vie privée sur le jeu de données | `config`, `text_utils` |
| `src/annotation_humaine.py` | Formulaire aveugle et calcul de la précision humaine | `config`, `evaluate`, `methods` |
| `demo/demo_mots_cles.py` | Interface en ligne de commande | `evaluate`, `methods` |

**Règle de dépendance.** Les modules bas (`config`, `text_utils`) n'importent rien du projet.
Les modules de haut niveau (évaluation, démo) ne sont pas importés par les méthodes.

## 2.3 Contrat commun des méthodes

Toutes les méthodes sont des **fabriques** : elles reçoivent le corpus une fois (pour apprendre l'IDF),
puis renvoient une fonction `extraire(texte, k) -> list[str]`.
Ce contrat permet à `evaluate.py` de traiter les quatre méthodes de la même manière.

## 2.4 Décisions d'architecture (format court)

Chaque décision indique le contexte, le choix, la raison et le compromis accepté.

### D1 — Pas de dépendance réseau à l'exécution
- **Contexte.** Le téléchargement de modèles (Hugging Face) n'était pas garanti.
- **Choix.** Tout tourne hors ligne, sauf l'installation initiale du modèle spaCy.
- **Compromis.** Pas d'embeddings de phrases. C'est une extension identifiée.

### D2 — Méthodes classiques plutôt qu'un grand modèle de langage
- **Contexte.** Le sujet valorise la rigueur, pas la taille du modèle.
- **Choix.** TF-IDF, graphe, lemmatisation.
- **Compromis.** Des performances plafonnées, et des erreurs lexicales visibles.

### D3 — L'IDF est appris hors notes de test
- **Contexte.** Le vocabulaire du test ne doit influencer aucun paramètre appris.
- **Choix.** Le corpus d'apprentissage de l'IDF exclut les 10 notes de test.
- **Compromis.** Le corpus d'apprentissage est un peu plus petit (30 notes).

### D4 — Hyperparamètres choisis sur le développement seulement
- **Contexte.** Éviter l'optimisme induit par le réglage sur le test.
- **Choix.** Grilles dans `config.py`, sélection sur dev (F1 souple, k = 5), égalité départagée par la plus petite valeur.
- **Compromis.** Avec 10 notes de dev, la sélection est elle-même bruitée.

### D5 — Correspondance souple comme mesure principale
- **Contexte.** Une baseline à mots isolés ne peut pas produire une expression complète.
- **Choix.** Inclusion d'ensembles de mots normalisés. La stricte est calculée en complément.
- **Compromis.** La règle est généreuse : « service » correspond à « service du personnel ».

### D6 — Approche 2c ajoutée après la première évaluation (divulgué)
- **Contexte.** La lemmatisation spaCy est vue en cours. Les erreurs de la version 1 (nombres,
  verbes conjugués) motivaient son filtrage par nature de mot.
- **Choix.** Ajout de 2c, évalué sur le même protocole, puis contrôlé sur un jeu de test gelé.
- **Compromis assumé.** La conception de 2c a utilisé les erreurs observées sur eval. Le test gelé
  corrige le biais : sur test, 2c n'est pas meilleure que la baseline à k = 5 (voir `05_fiche_modele.md`).
  Ce point est présenté tel quel au jury.

### D7 — Résultats reproductibles, graine unique
- **Contexte.** Exigence de reproductibilité du module.
- **Choix.** Une seule graine (`GRAINE = 42`) dans `config.py`. Les paramètres retenus sont écrits dans
  `results/parametres_retenus.json`. Le test `test_non_regression.py` fixe les valeurs de la version 1.
- **Compromis.** Le bootstrap utilise la même graine : les intervalles sont reproductibles, mais pas
  une estimation indépendante.

### D8 — Validation des données comme étape bloquante
- **Contexte.** Une donnée mal formée fausse toutes les mesures en silence.
- **Choix.** `valider_donnees.py` renvoie un code d'erreur en cas d'échec. Les tests le rejouent.
- **Compromis.** La couverture lexicale des références est un avertissement, pas un blocage :
  une référence peut être une forme dérivée (« rattrapage ») absente du texte.

## 2.5 Points d'extension prévus

| Extension | Où elle s'insère | Condition préalable |
|---|---|---|
| Embeddings de phrases multilingues | nouvelle fonction dans `methods.py`, même contrat | modèle téléchargé, mesuré sur test gelé |
| Classement d'archivage | nouveau module, classifieur sur les mots-clés | corpus annoté suffisant (plusieurs centaines de notes) |
| Interface web | nouveau dossier `app/`, appelle `methods.py` | aucune modification des méthodes |
