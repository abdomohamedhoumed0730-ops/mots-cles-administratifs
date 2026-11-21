"""Tests de la logique de l'interface (sans lancer le serveur Gradio)."""
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "app"))
sys.path.insert(0, str(RACINE / "src"))

from app_gradio import COLONNES, EXEMPLE, analyser, construire_extracteurs  # noqa: E402


@pytest.fixture(scope="module")
def extracteurs():
    return construire_extracteurs()


def test_tableau_a_k_lignes_et_une_colonne_par_methode(extracteurs):
    tableau = analyser(extracteurs, EXEMPLE, 5)
    assert len(tableau) == 5
    assert list(tableau.columns) == ["Rang"] + list(COLONNES.values())


def test_texte_vide_ne_plante_pas(extracteurs):
    tableau = analyser(extracteurs, "   ", 5)
    assert "Message" in tableau.columns


def test_pas_de_mot_manquant_sans_case_vide_inattendue(extracteurs):
    tableau = analyser(extracteurs, EXEMPLE, 10)
    assert len(tableau) == 10
