# Extraction de mots-clés dans des documents administratifs

Projet de fin de module TALN, Master 2 IAMD, Université de Djibouti. Sujet n° 6.

Le projet propose 5 à 10 mots-clés pour une note administrative, avec quatre méthodes comparées
sur un protocole sans fuite de données, et des résultats présentés avec leur incertitude.

## Pour commencer en cinq minutes

```bash
make install          # dépendances Python et modèle spaCy français
make tout             # validation, tests, évaluation, statistiques, rapport, diapositives
make demo             # démonstration sur un exemple
make streamlit        # application Streamlit (écran principal de la soutenance)
make app              # interface Gradio alternative : colle une note, obtiens le tableau
```

Sans `make` (Windows par exemple) :

```bash
pip install -r requirements-dev.txt
python -m spacy download fr_core_news_sm
python src/valider_donnees.py
python -m pytest -q tests
python src/evaluate.py
python src/analyse_statistique.py
python demo/demo_mots_cles.py --k 5
```

## Guides pas à pas

Les étapes d'installation, de déploiement, d'annotation et de soutenance sont dans `docs/guides/` : un guide par étape, avec la vérification qui clôt chacune.

## Où trouver quoi

| Je cherche… | Document |
|---|---|
| Comprendre le projet et les mots techniques | `docs/01_objectif_et_glossaire.md` |
| Savoir comment le code est organisé et pourquoi | `docs/02_architecture.md` |
| Savoir comment la démarche a été menée | `docs/03_methodologie.md` |
| Savoir ce que contiennent les données | `docs/04_fiche_donnees.md` |
| Savoir ce que valent les méthodes, et leurs limites | `docs/05_fiche_modele.md` |
| Savoir comment le code est testé | `docs/06_strategie_tests.md` |
| Préparer les questions du jury | `docs/07_questions_jury_et_guide.md` |
| Suivre les guides pas à pas (déploiement, soutenance) | `docs/guides/README.md` |
| Savoir ce qui reste à faire | `docs/08_checklist_rubrique.md` |
| Savoir ce qui a changé entre les versions | `docs/09_journal_modifications.md` |
| Préparer la soutenance | `docs/10_plan_soutenance.md` |

## Les quatre méthodes

1. **Baseline TF-IDF** : mots isolés qui reviennent dans la note et sont rares dans le corpus.
2. **Approche 2a** : expressions de deux mots maximum, scorées par TF-IDF.
3. **Approche 2b (TextRank)** : mots reliés par leur proximité dans le texte, classés par PageRank.
4. **Approche 2c** : lemmes de noms, noms propres et adjectifs (spaCy), scorés par TF-IDF.

Détail et choix : `docs/02_architecture.md` et `docs/05_fiche_modele.md`.

## Résultat principal, en une phrase

Sur le jeu de test gelé de 10 notes, aucune méthode ne bat nettement la baseline à k = 5, et
TextRank est nettement meilleure à k = 10. La variante 2c, qui semblait meilleure sur le jeu
d'évaluation, ne le confirme pas sur le test. Les chiffres complets, avec leurs intervalles de
confiance, sont dans `docs/05_fiche_modele.md`.

## Structure du dépôt

```
data/            corpus synthétique (40 notes), empreinte SHA-256, fiche de données
docs/            documentation par public (voir le tableau ci-dessus)
src/             code de production : config, prétraitement, méthodes, évaluation, statistiques, validation, inférence
app/             interface de démonstration Gradio (tableau de mots-clés par méthode)
models/          modèle sauvegardé (joblib), créé par l'inférence
tests/           61 tests (unitaires, intégration, non-régression, qualité des données)
demo/            démonstration en ligne de commande
results/         sorties générées (ne pas modifier à la main)
rapport/         rapport au format LaTeX et PDF
slides/          diapositives de soutenance et script de génération
.github/         intégration continue (non exécutée dans l'environnement de travail)
Makefile         commandes à lancer
```

## Application Streamlit

```bash
make streamlit        # ouvre http://localhost:8501
```

Trois sources de texte : une note du corpus (avec mesure contre ses références), un texte collé, ou un fichier `.txt` en UTF-8. Le tableau se télécharge en CSV.

### Déploiement public (Streamlit Community Cloud)

1. Pousser le dépôt sur GitHub (dépôt public ou privé relié au compte).
2. Sur share.streamlit.io, créer une application : dépôt, branche `main`, fichier principal `app/streamlit_app.py`.
3. Le fichier `requirements.txt` installe les dépendances, dont le modèle spaCy français (lien direct vers la version 3.8.0).
4. Vérifier avant la soutenance : l'application répond, le chargement prend quelques secondes, et une note du corpus donne un tableau.

Le déploiement se fait avec votre compte : ce dépôt ne contient aucun identifiant.

## Évaluation humaine (à réaliser)

```bash
make formulaire                              # crée le formulaire aveugle (396 lignes)
# Remplir la colonne 'pertinent' de results/formulaire_evaluation_humaine.csv (1 ou 0)
python src/annotation_humaine.py analyser    # calcule la précision humaine par méthode
```

Ne pas ouvrir `results/cle_methodes_PRIVEE.csv` avant la fin de la notation.

## Reproductibilité

- Une seule graine (`GRAINE = 42` dans `src/config.py`).
- Les hyperparamètres retenus sont écrits dans `results/parametres_retenus.json`.
- Le jeu de données est vérifié par empreinte SHA-256 (`data/MANIFEST.json`).
- Un test de non-régression fixe les scores de la première version.

## Limites à connaître

Corpus synthétique, références rédigées par un seul auteur, jeu de test de dix notes, évaluation
humaine non encore réalisée. Liste complète dans `docs/05_fiche_modele.md`, section 5.7 et 5.8.
