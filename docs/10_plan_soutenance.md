# 10. Plan de soutenance (24 novembre)

Format prévu, à confirmer avec l'enseignant : 10 min de présentation, 3 min de démonstration, 5 min de questions, 2 min de transition.
Plan recommandé par le sujet : contexte, question, données, pipeline, baseline, modèle, résultats, erreurs,
démonstration, limites et perspectives.

## 10.1 Répartition

| Temps | Partie | Diapositives | Qui |
|---|---|---|---|
| 1 min | Contexte et question | 2 | Personne A |
| 2 min | Données et protocole (dev, eval, test) | 3 | Personne A |
| 2 min | Pipeline et approches | 4, 5 | Personne B |
| 2,5 min | Résultats et incertitude | 6, 7 | Personne B |
| 1,5 min | Analyse d'erreurs | 8 | Personne A |
| 1 min | Limites, perspectives, conclusion | 9 | Personne A |
| 3 min | Démonstration | — | Personne B |
| 2 min | Transition et notation (incluse dans le format) | — | — |

Présentation : 10 min (1 + 2 + 2 + 2,5 + 1,5 + 1). Démonstration : 3 min. Questions : 5 min.

## 10.2 Phrases à dire, dans cet ordre

1. « Nous cherchons 5 à 10 mots-clés pour une note administrative, avec une méthode mesurable. »
2. « Nous avons séparé les données en trois : développement pour régler, évaluation pour mesurer,
   test gelé pour conclure. »
3. « La baseline est un TF-IDF sur les mots. Nous avons trois améliorations : expressions, TextRank,
   et lemmatisation. »
4. « Sur le jeu gelé, aucune méthode ne bat nettement la baseline à k = 5. TextRank est meilleure à k = 10. »
5. « Un écart n'est établi que si son intervalle de confiance ne contient pas zéro. »
6. « La lemmatisation 2c semblait meilleure sur l'évaluation, mais elle a été conçue à partir de ces
   données. Le test gelé ne le confirme pas. Nous le disons. »

## 10.3 Démonstration (3 minutes, à répéter)

```bash
python demo/demo_mots_cles.py --k 5
```

Avant la soutenance, tester une fois sur la machine qui sera utilisée. Préparer un texte de secours
en cas de problème (`ma_note.txt`).

## 10.4 Questions probables

Voir `07_questions_jury_et_guide.md`. Répondre en s'appuyant sur les chiffres de `results/`,
pas sur la mémoire.

## 10.5 Erreurs à éviter

- Dire que le système « comprend » le texte.
- Présenter 0,50 comme une précision garantie : c'est une moyenne sur 10 ou 20 notes synthétiques.
- Affirmer qu'une méthode est meilleure sans regarder l'intervalle de confiance.
- Lire les diapositives. Expliquer les chiffres.
