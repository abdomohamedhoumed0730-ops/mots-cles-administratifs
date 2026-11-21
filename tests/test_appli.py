"""Tests de la logique de l'application Streamlit (sans interface)."""
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from appli import METHODES_AFFICHAGE, evaluer, exporter_csv, extraire_tous, surligner  # noqa: E402
from inference import entrainer  # noqa: E402
from methods import construire_methodes  # noqa: E402
from evaluate import charger_corpus  # noqa: E402


@pytest.fixture(scope="module")
def extracteurs():
    corpus = [d["texte"] for d in charger_corpus() if d["split"] != "test"]
    return construire_methodes(corpus)


def test_extraire_tous_donne_une_liste_par_methode(extracteurs):
    res = extraire_tous(extracteurs, "Demande de congé annuel pour le service des finances.", 5)
    assert set(res) == set(METHODES_AFFICHAGE)
    assert all(len(v) <= 5 for v in res.values())


def test_evaluer_score_parfait_si_prediction_egale_reference():
    refs = ["demande de congé", "service des finances"]
    res = evaluer({"baseline_tfidf_mots": ["congé", "finances"]}, refs)
    assert res["baseline_tfidf_mots"]["precision"] == 1.0
    assert res["baseline_tfidf_mots"]["f1"] > 0


def test_surligner_echappe_le_html():
    sortie = surligner("<script>x</script> congé", ["congé"])
    assert "<script>" not in sortie
    assert '<mark class="mot-cle">congé</mark>' in sortie


def test_surligner_prefere_l_expression_la_plus_longue():
    sortie = surligner("fiche technique jointe", ["fiche", "fiche technique"])
    assert sortie.count("<mark") == 1


def test_exporter_csv_a_un_en_tete_et_un_rang_par_ligne():
    csv_txt = exporter_csv({"baseline_tfidf_mots": ["a", "b"], "approche2b_textrank": ["c", "d"]})
    lignes = csv_txt.lstrip("﻿").strip().splitlines()
    assert lignes[0].startswith("rang,")
    assert len(lignes) == 3


def test_surligner_pas_de_ligne_vide_dans_le_html():
    sortie = surligner("Premier paragraphe.\n\nDeuxième congé.", ["congé"])
    assert "\n" not in sortie
    assert "<br><br>" in sortie
    assert '<mark class="mot-cle">congé</mark>' in sortie


def test_controler_texte_bloque_le_vide_et_le_trop_long():
    from appli import LIMITE_CARACTERES, controler_texte

    assert controler_texte("   ")[0] is not None
    assert controler_texte("x " * LIMITE_CARACTERES)[0] is not None


def test_controler_texte_avertit_si_texte_tres_court_sans_bloquer():
    from appli import controler_texte

    erreur, avertissement = controler_texte("Demande de congé.")
    assert erreur is None
    assert avertissement is not None


def test_controler_texte_accepte_une_note_normale():
    from appli import controler_texte

    note = "Objet : demande de congé annuel. " * 3
    assert controler_texte(note) == (None, None)


def test_decoder_octets_accepte_utf8_et_windows_1252():
    from appli import decoder_octets

    texte, encodage, erreur = decoder_octets("Demande de congé".encode("utf-8"))
    assert texte == "Demande de congé" and encodage == "utf-8-sig" and erreur is None
    texte, encodage, erreur = decoder_octets("Demande de congé".encode("cp1252"))
    assert texte == "Demande de congé" and encodage == "cp1252" and erreur is None


def test_decoder_octets_refuse_un_fichier_trop_gros():
    from appli import LIMITE_OCTETS_FICHIER, decoder_octets

    texte, _, erreur = decoder_octets(b"a" * (LIMITE_OCTETS_FICHIER + 1))
    assert texte is None and erreur is not None


def test_extraire_chronometre_donne_un_temps_par_methode(extracteurs):
    from appli import extraire_chronometre

    predictions, temps = extraire_chronometre(
        extracteurs, "Demande de congé annuel pour le service des finances.", 5
    )
    assert set(temps) == set(METHODES_AFFICHAGE)
    assert all(t >= 0 for t in temps.values())
    assert set(predictions) == set(METHODES_AFFICHAGE)


def test_echapper_neutralise_le_html():
    from appli import echapper

    assert "<" not in echapper("<img src=x>")


def test_exporter_mesures_csv_a_quatre_colonnes():
    from appli import exporter_mesures_csv

    resultats = {c: {"precision": 0.5, "rappel": 0.25, "f1": 0.333} for c in METHODES_AFFICHAGE}
    lignes = exporter_mesures_csv(resultats).lstrip("﻿").strip().splitlines()
    assert lignes[0] == "methode,precision,rappel,f1"
    assert len(lignes) == 1 + len(METHODES_AFFICHAGE)
