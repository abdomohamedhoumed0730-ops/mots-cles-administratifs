"""Tests d'intégration des méthodes d'extraction (niveau milieu de la pyramide)."""
import pytest

from config import MODELE_SPACY
from methods import (
    approche_phrases,
    approche_textrank,
    baseline_tfidf,
    candidats_phrases,
)

CORPUS = [
    "Demande de congé annuel pour le service des finances. Dix jours ouvrables.",
    "Avis de paiement d'une facture de maintenance des climatiseurs.",
    "Procès-verbal du conseil d'administration. Budget révisé de l'exercice.",
]
TEXTE = CORPUS[0]


def test_baseline_respecte_k_et_renvoie_des_mots_isoles():
    extraire = baseline_tfidf(CORPUS)
    mots = extraire(TEXTE, 3)
    assert len(mots) <= 3
    assert all(" " not in m for m in mots)


def test_baseline_texte_vide_renvoie_liste_vide():
    assert baseline_tfidf(CORPUS)("", 5) == []


def test_candidats_phrases_coupe_aux_mots_vides():
    assert candidats_phrases("demande de congé annuel", 3) == ["demande", "congé annuel"]


def test_candidats_phrases_respecte_longueur_max():
    assert all(len(c.split()) <= 2 for c in candidats_phrases("congé annuel exceptionnel prolongé", 2))


def test_approche_phrases_produit_expressions():
    mots = approche_phrases(CORPUS, 2)(TEXTE, 5)
    assert mots, "au moins un candidat attendu"
    assert any(" " in m for m in mots), "au moins une expression de plusieurs mots attendue"


def test_textrank_renvoie_au_plus_k_expressions_sans_doublon_inclus():
    mots = approche_textrank(3)(TEXTE, 5)
    assert 0 < len(mots) <= 5
    for i, a in enumerate(mots):
        for b in mots[i + 1:]:
            assert not (set(a.split()) <= set(b.split()))


def test_textrank_texte_sans_contenu_renvoie_liste_vide():
    assert approche_textrank(3)("de la le", 5) == []


def test_methodes_deterministes():
    extraire = approche_phrases(CORPUS, 2)
    assert extraire(TEXTE, 5) == extraire(TEXTE, 5)


def test_approche_lemmes_exclut_chiffres_et_verbes():
    pytest.importorskip("spacy")
    from methods import approche_lemmes, charger_spacy

    try:
        charger_spacy(MODELE_SPACY)
    except OSError:
        pytest.skip(f"modèle {MODELE_SPACY} non installé")
    texte = "Le service a approuvé 312 500 francs pour la facture 2026 0457."
    mots = approche_lemmes(CORPUS, 2)(texte, 10)
    assert not any(any(ch.isdigit() for ch in m) for m in mots), "les nombres doivent être exclus"
    assert "approuver" not in mots, "les verbes doivent être exclus"
