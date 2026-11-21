"""Inférence : sauvegarde, rechargement et prédiction de mots-clés (baseline TF-IDF).

Pourquoi ce module ? Un prototype doit pouvoir être sauvegardé, rechargé et utilisé
sans réentraîner. Les méthodes de methods.py sont des fermetures non sérialisables ;
ici, l'artefact est un TfidfVectorizer scikit-learn, sauvegardé avec joblib.

Honnêteté sur le score : c'est un score TF-IDF, pas une probabilité. Il sert à classer,
il ne mesure pas une certitude.

Usage :
    from inference import entrainer_et_sauvegarder, charger, predire_mots_cles
"""
from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from config import RACINE
from methods import _PATRON_MOT
from text_utils import MOTS_VIDES, minuscules

CHEMIN_MODELE = RACINE / "models" / "baseline_tfidf.joblib"


def entrainer(corpus: list[str]) -> TfidfVectorizer:
    """Apprend l'IDF sur le corpus fourni (à passer SANS les notes de test)."""
    vec = TfidfVectorizer(
        preprocessor=minuscules,
        token_pattern=_PATRON_MOT,
        stop_words=sorted(MOTS_VIDES),
        sublinear_tf=True,
    )
    vec.fit(corpus)
    return vec


def entrainer_et_sauvegarder(corpus: list[str], chemin: Path = CHEMIN_MODELE) -> Path:
    """Entraîne le vectoriseur puis l'écrit sur disque."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(entrainer(corpus), chemin)
    return chemin


def charger(chemin: Path = CHEMIN_MODELE) -> TfidfVectorizer:
    """Recharge le vectoriseur sauvegardé."""
    return joblib.load(chemin)


def predire_mots_cles(vec: TfidfVectorizer, texte: str, k: int = 5) -> list[tuple[str, float]]:
    """Renvoie les k mots-clés les mieux notés, avec leur score TF-IDF."""
    ligne = vec.transform([texte])
    if ligne.nnz == 0:
        return []
    vocabulaire = vec.get_feature_names_out()
    ordre = np.argsort(-ligne.data, kind="stable")[:k]
    return [(str(vocabulaire[ligne.indices[i]]), float(ligne.data[i])) for i in ordre]
