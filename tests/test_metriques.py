"""Tests unitaires des mesures d'évaluation (correspondances, précision, rappel, F1)."""
import pytest

from evaluate import correspond, jaccard, metriques_document


def test_correspondance_souple_mot_inclus_dans_expression():
    assert correspond("congé", "demande de congé annuel", "souple")


def test_correspondance_stricte_refuse_mot_isole():
    assert not correspond("congé", "demande de congé annuel", "stricte")


def test_correspondance_stricte_accepte_meme_expression_reformulee():
    assert correspond("congé annuel", "annuel congé", "stricte")


def test_metriques_exemple_connu():
    # 1 prédiction sur 1 correcte, 1 référence sur 2 retrouvée :
    # précision = 1, rappel = 0.5, F1 = 2 * 1 * 0.5 / 1.5 = 0.6667
    p, r, f1 = metriques_document(["congé"], ["demande de congé annuel", "dossier de passation"], "souple")
    assert p == pytest.approx(1.0)
    assert r == pytest.approx(0.5)
    assert f1 == pytest.approx(2 / 3)


def test_metriques_sans_prediction_sont_nulles():
    assert metriques_document([], ["x"], "souple") == (0.0, 0.0, 0.0)


def test_f1_nul_si_aucune_correspondance():
    assert metriques_document(["zèbre"], ["congé annuel"], "souple")[2] == 0.0


def test_jaccard_identiques_et_disjoints():
    assert jaccard(["congé annuel"], ["congé annuel"]) == 1.0
    assert jaccard(["congé"], ["paiement"]) == 0.0
