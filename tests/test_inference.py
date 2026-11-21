"""Tests du module d'inférence : sauvegarde, rechargement, prédiction."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inference import charger, entrainer, entrainer_et_sauvegarder, predire_mots_cles  # noqa: E402

CORPUS = [
    "demande de congé annuel pour le service des finances",
    "demande d'achat de fournitures de bureau et matériel informatique",
    "convocation au comité de pilotage du projet de numérisation",
]


def test_round_trip_donne_le_meme_resultat(tmp_path):
    chemin = tmp_path / "modele.joblib"
    entrainer_et_sauvegarder(CORPUS, chemin)
    avant = predire_mots_cles(entrainer(CORPUS), CORPUS[1], k=5)
    apres = predire_mots_cles(charger(chemin), CORPUS[1], k=5)
    assert avant == apres
    assert len(apres) > 0


def test_scores_decroissants_et_positifs():
    resultat = predire_mots_cles(entrainer(CORPUS), CORPUS[0], k=5)
    scores = [s for _, s in resultat]
    assert all(s > 0 for s in scores)
    assert scores == sorted(scores, reverse=True)


def test_texte_vide_renvoie_liste_vide():
    assert predire_mots_cles(entrainer(CORPUS), "le de et", k=5) == []


def test_k_est_respecte():
    assert len(predire_mots_cles(entrainer(CORPUS), CORPUS[1], k=3)) <= 3
