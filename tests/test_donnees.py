"""Tests de qualité des données (contrôles de la validation, rejoués par pytest)."""
import json

import pytest

from config import DONNEES
from valider_donnees import PATRONS_DONNEES_PERSONNELLES, valider


@pytest.fixture(scope="module")
def notes():
    with open(DONNEES, encoding="utf-8") as f:
        return json.load(f)


def test_validation_sans_erreur_bloquante(notes):
    rapport = valider(notes)
    assert rapport.ok, rapport.erreurs


def test_quarante_notes_reparties_10_20_10(notes):
    compte = {s: sum(n["split"] == s for n in notes) for s in ("dev", "eval", "test")}
    assert compte == {"dev": 10, "eval": 20, "test": 10}


def test_identifiants_uniques(notes):
    ids = [n["id"] for n in notes]
    assert len(ids) == len(set(ids))


def test_aucune_donnee_personnelle_probable(notes):
    for n in notes:
        for nom, patron in PATRONS_DONNEES_PERSONNELLES.items():
            assert not patron.search(n["texte"]), f"{n['id']} : {nom}"


def test_six_references_distinctes_par_note(notes):
    for n in notes:
        refs = n["mots_cles_reference"]
        assert len(refs) == 6 and len(set(refs)) == 6, n["id"]
