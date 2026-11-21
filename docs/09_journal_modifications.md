# 9. Journal des modifications

Ce journal rend visible ce qui a changé entre les versions, et pourquoi.

## Version 2 (20 novembre 2026, soir)

### Ajouts
- **Approche 2c** : lemmatisation spaCy, filtrage par nature de mot, scoring TF-IDF.
  *Ajoutée après la première évaluation* (divulgué, voir décision D6).
- **Jeu de test gelé** de 10 notes (N31 à N40), rédigé après la conception de 2c, mesuré une seule fois.
- **Intervalles de confiance** par bootstrap apparié (`analyse_statistique.py`).
- **Validation des données** bloquante, avec contrôle de vie privée et empreinte SHA-256.
- **Configuration centrale** (`config.py`) : plus aucune constante en dur dans les modules.
- **Suite de tests** : 61 tests (dont 7 pour l'inférence et l'interface), dont un test de non-régression.
- **Outillage** : `Makefile`, `requirements.txt` complété, `.gitignore`, workflow CI (non exécuté).
- **Documentation** par public : `docs/`.

### Corrections
- **IDF apprise hors test.** La version 1 n'avait pas de jeu de test. Le choix est désormais explicite et appliqué aux trois jeux.
- **Démonstration** : utilise le même corpus d'apprentissage que l'évaluation.
- **Formulaire d'évaluation humaine** : couvre les quatre méthodes, sur 20 notes (10 test, 10 eval).
- **Tie-break** : en cas d'égalité sur dev, la plus petite valeur est retenue, de façon explicite.
- **Tests** : correction de deux attendus écrits à tort (accents, pluriel), sans changement du code. Un cas limite est documenté en `xfail`.

### Changements de résultats
- Aucun résultat de la version 1 n'a changé pour les trois méthodes d'origine (test de non-régression).
- Nouveau : 2c (voir `results/metriques_resume.csv`).
- Nouveau : jeu test (lignes `split = test` dans les mêmes fichiers).

### Corrections apportées au rapport v1 (à relire avant soutenance)
- Le rapport v1 concluait que l'approche 2a était la meilleure à k = 5. Sur le jeu gelé, ce n'est pas le cas.
- Le rapport v1 disait « pas de test statistique ». Il existe maintenant (intervalles de confiance).

## Version 1 (20 novembre 2026, début de soirée)

- Corpus de 30 notes (dev 10, eval 20).
- Trois méthodes : baseline TF-IDF, 2a phrases candidates, 2b TextRank.
- Évaluation souple et stricte, stabilité par mélange d'ordre et suppression, analyse de douze erreurs.
- Rapport de six pages, neuf diapositives.
- Évaluation humaine préparée, non réalisée.

## Ce qui reste ouvert

Voir `08_checklist_rubrique.md`, section 8.2.
- **Application v1.1** : résultats conservés entre deux clics (le téléchargement ne les efface plus) ; contrôles de saisie (texte vide, texte trop long, texte très court, fichier trop lourd, encodage) ; interface en quatre onglets (mots-clés, comparaison avec temps de calcul, mesure, méthodes et limites) ; export des mesures en CSV ; barre d'outils Streamlit réduite et détails d'erreur masqués. Les chiffres publiés n'ont pas changé.
