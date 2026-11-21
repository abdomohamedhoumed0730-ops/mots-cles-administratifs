"""Configuration centrale du projet.

Tous les chemins, graines aléatoires et hyperparamètres sont définis ici.
Modifier une valeur ici suffit : aucun autre fichier ne contient de constante en dur.
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DONNEES = RACINE / "data" / "corpus_notes_administratives.json"
MANIFESTE = RACINE / "data" / "MANIFEST.json"
RESULTATS = RACINE / "results"

# Reproductibilité : la seule source d'aléa est la graine ci-dessous.
GRAINE = 42

# Évaluation
K_VALUES = (5, 10)
K_PRINCIPAL = 5  # k utilisé pour choisir les hyperparamètres (jeu de développement)

# Grilles de recherche (jeu de développement uniquement)
GRILLE_PHRASES = (2, 3, 4)  # longueur maximale d'un candidat (approche 2a)
GRILLE_FENETRE = (2, 3, 4, 6)  # fenêtre de cooccurrence TextRank (approche 2b)
GRILLE_LEMMES = (1, 2, 3)  # longueur maximale d'un candidat lemmatisé (approche 2c)

# Valeurs retenues pendant la première évaluation (reprises telles quelles)
LONGUEUR_PHRASES_DEFAUT = 2
FENETRE_TEXTRANK_DEFAUT = 3

# Modèle linguistique spaCy (approche 2c)
MODELE_SPACY = "fr_core_news_sm"

# Stabilité
SEUIL_STABILITE_ALERTE = 0.5  # Jaccard moyen en dessous duquel on signale une instabilité
