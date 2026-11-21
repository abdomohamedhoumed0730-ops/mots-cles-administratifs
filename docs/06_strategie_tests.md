# 6. Stratégie de tests et d'assurance qualité

Principe : beaucoup de tests rapides en bas, quelques tests lents en haut.
Le projet compte 61 tests (60 réussis, 1 attendu en échec).

```
           /  Chaîne complète (make tout)     quelques, lente
          /  Intégration (méthodes, données)  quelques, moyenne
         /  Unitaires (texte, mesures)        nombreux, rapide
```

## 6.1 Ce qui est testé

| Fichier | Niveau | Ce qu'il vérifie |
|---|---|---|
| `tests/test_text_utils.py` | unitaire | apostrophes, accents, pluriel, mots vides, découpage |
| `tests/test_metriques.py` | unitaire | correspondances strictes et souples, précision, rappel, F1, Jaccard, exemple chiffré connu |
| `tests/test_methodes.py` | intégration | respect de k, absence de doublons inclus, expressions, déterminisme, exclusion des nombres et verbes en 2c |
| `tests/test_donnees.py` | qualité des données | validation sans erreur, répartition 10/20/10, identifiants uniques, absence de données personnelles, six références distinctes |
| `tests/test_non_regression.py` | non-régression | les méthodes v1 gardent leurs scores publiés ; le fichier de résultats est cohérent avec le code |

## 6.2 Ce qui n'est pas testé, et pourquoi

- **Le script de démonstration** : il est court et sert à présenter ; il est exécuté à la main.
  Un test d'intégration serait utile avant la soutenance.
- **Le formulaire d'évaluation humaine** : il dépend de saisies humaines. Son calcul est simple.
- **Les performances** : le temps par note est mesuré, mais aucun seuil n'est imposé.
- **Le rapport et les diapositives** : vérifiés à l'œil, pas automatiquement.

## 6.3 Cas limites couverts

- Texte vide : renvoie une liste vide, sans erreur.
- Texte composé uniquement de mots vides : renvoie une liste vide.
- Aucune prédiction : précision, rappel et F1 valent 0.
- Une seule phrase : la perturbation par suppression ne retire rien (garde-fou).

## 6.4 Test marqué comme limite connue

`test_limite_connue_suffixe_x` est en `xfail` strict : il échoue volontairement, car la règle de
normalisation transforme « prix » en « pri ». Si la règle est un jour corrigée, ce test deviendra
un succès, et pytest le signalera.

## 6.5 Intégration continue

Le fichier `.github/workflows/ci.yml` lance, à chaque modification, la validation des données,
les tests et l'évaluation. **Il n'a pas été exécuté dans l'environnement de travail** : il faut
le pousser sur un dépôt GitHub pour vérifier qu'il passe.

## 6.6 Lancer les tests

```bash
make tester           # équivalent : python -m pytest -q tests
```

## 6.7 Résultat du dernier passage

42 tests réussis, 1 test attendu en échec (`xfail`).
