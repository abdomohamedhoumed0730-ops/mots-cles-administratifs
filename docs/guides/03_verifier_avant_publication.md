# Guide 03 · Vérifier que tout passe avant publication

**Objectif.** Prouver que le projet fonctionne du début à la fin, avant de le mettre en ligne.

## Étapes

1. Dans le dossier du projet, lancez la chaîne complète :
   ```bash
   make tout
   ```
   Sans `make` :
   ```bash
   python src/valider_donnees.py
   python -m pytest -q tests
   python src/evaluate.py
   python src/analyse_statistique.py
   ```

2. Vérifiez les trois résultats clés :
   - La validation des données se termine par **PASS**.
   - Les tests affichent **60 passed, 1 xfailed** (le nombre peut varier de quelques unités ; l'essentiel est qu'il n'y ait aucun échec et exactement un test « xfailed »).
   - Le terminal se termine sans « Error ».

## Vérification
Les trois points ci-dessus sont vrais. Le test marqué **xfailed** est attendu : c'est une limite connue documentée, pas un bug.

## En cas de problème
- **Un test échoue (FAILED)** : ne publiez pas. Notez le nom du test, et relisez `docs/06_strategie_tests.md`.
- **La validation affiche FAIL** : le fichier de données a été modifié. Restaurez le fichier d'origine à partir du zip, car le manifeste garde l'empreinte d'origine.
