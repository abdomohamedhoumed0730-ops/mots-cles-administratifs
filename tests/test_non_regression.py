"""Test de non-régression : les méthodes v1 doivent garder les mêmes scores sur le jeu d'évaluation.

Les valeurs attendues sont celles de la première version (F1 souple, moyenne sur 20 notes).
Si elles changent, c'est qu'un choix de méthode a été modifié : il faut alors le documenter.
"""
import pytest

from config import RESULTATS
from evaluate import charger_corpus, metriques_document
from methods import approche_phrases, approche_textrank, baseline_tfidf

ATTENDU_K5 = {"baseline": 0.432, "2a": 0.480, "2b": 0.425}
TOLERANCE = 1e-3


@pytest.fixture(scope="module")
def corpus():
    return charger_corpus()


def _f1_moyen_eval(extracteur, corpus, k=5):
    evalu = [d for d in corpus if d["split"] == "eval"]
    scores = [metriques_document(extracteur(d["texte"], k), d["mots_cles_reference"], "souple")[2] for d in evalu]
    return sum(scores) / len(scores)


def test_baseline_non_regression(corpus):
    tous = [d["texte"] for d in corpus if d["split"] != "test"]
    assert _f1_moyen_eval(baseline_tfidf(tous), corpus) == pytest.approx(ATTENDU_K5["baseline"], abs=TOLERANCE)


def test_approche_2a_non_regression(corpus):
    tous = [d["texte"] for d in corpus if d["split"] != "test"]
    assert _f1_moyen_eval(approche_phrases(tous, 2), corpus) == pytest.approx(ATTENDU_K5["2a"], abs=TOLERANCE)


def test_approche_2b_non_regression(corpus):
    assert _f1_moyen_eval(approche_textrank(3), corpus) == pytest.approx(ATTENDU_K5["2b"], abs=TOLERANCE)


def test_resultats_publies_coherents_avec_le_code():
    """Le fichier de résultats doit correspondre aux valeurs attendues (évite un rapport périmé)."""
    import pandas as pd

    resume = pd.read_csv(RESULTATS / "metriques_resume.csv")
    lig = resume[(resume.split == "eval") & (resume.k == 5) & (resume.correspondance == "souple")]
    valeurs = dict(zip(lig.methode, lig.F1.round(3)))
    assert valeurs["baseline_tfidf_mots"] == ATTENDU_K5["baseline"]
    assert valeurs["approche2a_phrases_tfidf"] == ATTENDU_K5["2a"]
    assert valeurs["approche2b_textrank"] == ATTENDU_K5["2b"]
