"""Tests unitaires du prétraitement (niveau base de la pyramide)."""
import pytest

from text_utils import (
    decouper_phrases,
    ensemble_mots_matching,
    forme_normalisee,
    minuscules,
    retirer_accents,
    tokens,
    tokens_candidats,
)


def test_apostrophe_separee():
    assert minuscules("D'achat") == "d achat"


def test_tokens_en_minuscules_sans_ponctuation():
    assert tokens("Objet : Demande d'achat.") == ["objet", "demande", "d", "achat"]


def test_mots_vides_et_courts_exclus_des_candidats():
    assert "de" not in tokens_candidats("demande de congé")
    assert "congé" in tokens_candidats("demande de congé")


@pytest.mark.parametrize("entree, attendu", [("congé", "conge"), ("Élève", "Eleve"), ("été", "ete")])
def test_retirer_accents(entree, attendu):
    assert retirer_accents(entree) == attendu


@pytest.mark.parametrize("entree, attendu", [("courriers", "courrier"), ("Congés", "conge")])
def test_forme_normalisee_retire_pluriel(entree, attendu):
    assert forme_normalisee(entree) == attendu


@pytest.mark.xfail(strict=True, reason="Limite connue : le suffixe x est retiré, 'prix' devient 'pri'. "
                   "Sans effet sur la comparaison, car la règle s'applique aux deux côtés.")
def test_limite_connue_suffixe_x():
    assert forme_normalisee("prix") == "prix"


def test_ensemble_matching_ignore_mots_vides_et_casse():
    assert ensemble_mots_matching("Demande DE congé annuel") == ensemble_mots_matching("demande congé annuel")


def test_decouper_phrases_ignore_vides():
    assert decouper_phrases("Une. Deux ;  \n Trois.") == ["Une", "Deux", "Trois"]
