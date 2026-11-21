"""Quatre méthodes d'extraction de mots-clés.

Baseline
    baseline_tfidf      : TF-IDF sur les mots isolés (mots vides retirés).

Approches améliorées
    approche_phrases    : 2a. Candidats = suites de mots non vides (type RAKE), scorés par TF-IDF.
    approche_textrank   : 2b. Graphe de cooccurrence + PageRank (TextRank), puis fusion des voisins.
    approche_lemmes     : 2c. Lemmatisation spaCy, garde noms, noms propres et adjectifs,
                          candidats = suites de lemmes gardés, scorés par TF-IDF.

Chaque méthode est une fabrique : elle reçoit le corpus (pour l'IDF) et renvoie
une fonction extraire(texte, k) -> liste de mots-clés classés.
Aucune méthode n'utilise les références humaines.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Callable

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

from config import MODELE_SPACY
from text_utils import (
    MOTS_VIDES,
    decouper_phrases,
    minuscules,
    tokens,
    tokens_candidats,
)

Extracteur = Callable[[str, int], list[str]]

_PATRON_MOT = r"[a-zàâçéèêëîïôûùüÿœæ0-9]{3,}"
CATEGORIES_GARDEES = frozenset({"NOUN", "PROPN", "ADJ"})


def _sans_doublons_inclus(candidats: list[str], k: int) -> list[str]:
    """Garde les candidats classés, en retirant ceux dont les mots sont inclus dans un déjà choisi."""
    retenus: list[str] = []
    ensembles: list[frozenset] = []
    for c in candidats:
        ens = frozenset(c.split())
        if any(ens <= autre for autre in ensembles):
            continue
        retenus.append(c)
        ensembles.append(ens)
        if len(retenus) == k:
            break
    return retenus


def _extracteur_tfidf(corpus: list[str], analyseur: Callable[[str], list[str]]) -> Extracteur:
    """Calcule un TF-IDF sur des candidats fournis par `analyseur`, puis classe les candidats.

    Factorise les approches 2a et 2c : seul le découpage en candidats diffère.
    """
    compteur = CountVectorizer(analyzer=analyseur)
    matrice = compteur.fit_transform(corpus)
    ponderation = TfidfTransformer(sublinear_tf=True).fit(matrice)
    vocabulaire = compteur.get_feature_names_out()

    def extraire(texte: str, k: int) -> list[str]:
        ligne = ponderation.transform(compteur.transform([texte]))
        if ligne.nnz == 0:
            return []
        ordre = np.argsort(-ligne.toarray()[0], kind="stable")
        classes = [str(vocabulaire[i]) for i in ordre if ligne[0, i] > 0]
        return _sans_doublons_inclus(classes, k)

    return extraire


# ---------------------------------------------------------------- Baseline
def baseline_tfidf(corpus: list[str]) -> Extracteur:
    """Baseline : TF-IDF sur les mots isolés, avec mots vides retirés."""
    vec = TfidfVectorizer(
        preprocessor=minuscules,
        token_pattern=_PATRON_MOT,
        stop_words=sorted(MOTS_VIDES),
        sublinear_tf=True,
    )
    vec.fit(corpus)
    vocabulaire = vec.get_feature_names_out()

    def extraire(texte: str, k: int) -> list[str]:
        ligne = vec.transform([texte])
        if ligne.nnz == 0:
            return []
        ordre = np.argsort(-ligne.data, kind="stable")
        return [str(vocabulaire[ligne.indices[i]]) for i in ordre[:k]]

    return extraire


# ------------------------------------------------- Approche 2a : phrases candidates
def candidats_phrases(texte: str, longueur_max: int = 3) -> list[str]:
    """Suites de mots non vides, coupées par un mot vide ou une ponctuation.

    Exemple : 'demande de congé annuel' donne 'demande' et 'congé annuel'.
    """
    candidats: list[str] = []
    for phrase in decouper_phrases(texte):
        courant: list[str] = []
        for mot in tokens(phrase):
            if mot in MOTS_VIDES or len(mot) < 3:
                if courant:
                    candidats.append(" ".join(courant))
                courant = []
            else:
                courant.append(mot)
                if len(courant) == longueur_max:
                    candidats.append(" ".join(courant))
                    courant = []
        if courant:
            candidats.append(" ".join(courant))
    return candidats


def approche_phrases(corpus: list[str], longueur_max: int = 3) -> Extracteur:
    """Approche 2a : candidats-phrases scorés par TF-IDF (sous-linéaire)."""
    return _extracteur_tfidf(corpus, lambda t: candidats_phrases(t, longueur_max))


# ------------------------------------------------- Approche 2b : TextRank
def approche_textrank(fenetre: int = 4, facteur_candidats: int = 2) -> Extracteur:
    """Approche 2b : TextRank sur le graphe de cooccurrence des mots.

    - nœuds : mots candidats (sans mots vides, au moins 3 lettres) ;
    - arêtes : deux mots distincts apparaissant à moins de `fenetre` positions
      dans une même phrase ; le poids est le nombre de cooccurrences ;
    - score : PageRank (amortissement 0.85) ;
    - fusion : les mots sélectionnés qui se suivent dans le texte forment une expression.
    """

    def extraire(texte: str, k: int) -> list[str]:
        phrases = [tokens_candidats(p) for p in decouper_phrases(texte)]
        phrases = [p for p in phrases if p]
        if not phrases:
            return []

        graphe = nx.Graph()
        for p in phrases:
            graphe.add_nodes_from(p)
            for i, mot in enumerate(p):
                for j in range(i + 1, min(i + fenetre, len(p))):
                    if p[j] == mot:
                        continue
                    if graphe.has_edge(mot, p[j]):
                        graphe[mot][p[j]]["weight"] += 1
                    else:
                        graphe.add_edge(mot, p[j], weight=1)

        if graphe.number_of_edges() == 0:
            scores = {n: 1.0 for n in graphe.nodes}
        else:
            scores = nx.pagerank(graphe, alpha=0.85, weight="weight")

        n_retenus = max(k * facteur_candidats, 1)
        meilleurs = sorted(scores, key=lambda m: (-scores[m], m))[:n_retenus]
        selection = set(meilleurs)

        # Fusion des mots sélectionnés adjacents dans le texte (ordre d'apparition).
        expressions: dict[str, float] = {}
        for p in (tokens(ph) for ph in decouper_phrases(texte)):
            courant: list[str] = []
            for mot in p + [""]:
                if mot in selection and len(mot) >= 3 and mot not in MOTS_VIDES:
                    courant.append(mot)
                else:
                    if courant:
                        expr = " ".join(courant)
                        expressions[expr] = expressions.get(expr, 0.0) + sum(scores[m] for m in courant)
                    courant = []

        classement = sorted(expressions, key=lambda e: (-expressions[e], e))
        # Les mots isolés non fusionnés doivent aussi apparaître s'il en manque.
        for mot in meilleurs:
            if not any(mot in e.split() for e in classement):
                classement.append(mot)
        return _sans_doublons_inclus(classement, k)

    return extraire


# ------------------------------------------------- Approche 2c : lemmes spaCy (ajoutée en v2)
@lru_cache(maxsize=1)
def charger_spacy(modele: str = MODELE_SPACY):
    """Charge le modèle spaCy une seule fois (il est coûteux à charger)."""
    import spacy

    return spacy.load(modele)


def candidats_lemmes(texte: str, nlp, longueur_max: int = 2) -> list[str]:
    """Suites de lemmes de noms, noms propres et adjectifs, adjacents dans le texte.

    Un mot est gardé s'il est alphabétique, non vide (pas de mot vide spaCy),
    de catégorie NOUN, PROPN ou ADJ, et de lemme d'au moins 3 lettres.
    Les chiffres sont donc exclus par construction.
    """
    candidats: list[str] = []
    courant: list[str] = []
    for jeton in nlp(texte):
        garde = (
            jeton.pos_ in CATEGORIES_GARDEES
            and not jeton.is_stop
            and jeton.is_alpha
            and len(jeton.lemma_) >= 3
        )
        if garde:
            courant.append(jeton.lemma_.lower())
            if len(courant) == longueur_max:
                candidats.append(" ".join(courant))
                courant = []
        elif courant:
            candidats.append(" ".join(courant))
            courant = []
    if courant:
        candidats.append(" ".join(courant))
    return candidats


def approche_lemmes(corpus: list[str], longueur_max: int = 2) -> Extracteur:
    """Approche 2c : candidats lemmatisés (spaCy) scorés par TF-IDF."""
    nlp = charger_spacy()
    return _extracteur_tfidf(corpus, lambda t: candidats_lemmes(t, nlp, longueur_max))


def construire_methodes(corpus: list[str]) -> dict[str, Extracteur]:
    """Renvoie les quatre méthodes avec les hyperparamètres retenus (voir config.py)."""
    from config import FENETRE_TEXTRANK_DEFAUT, LONGUEUR_PHRASES_DEFAUT

    return {
        "baseline_tfidf_mots": baseline_tfidf(corpus),
        "approche2a_phrases_tfidf": approche_phrases(corpus, LONGUEUR_PHRASES_DEFAUT),
        "approche2b_textrank": approche_textrank(FENETRE_TEXTRANK_DEFAUT),
        "approche2c_lemmes_spacy_tfidf": approche_lemmes(corpus, 2),
    }
