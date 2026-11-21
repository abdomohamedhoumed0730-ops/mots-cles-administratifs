"""Logique de l'application TAL (sans interface) : extraction, contrôles, évaluation, mise en forme.

Séparée de l'écran Streamlit pour pouvoir être testée sans navigateur.
"""
from __future__ import annotations

import csv
import html
import io
import re
import time

from evaluate import metriques_document

VERSION = "1.1"

METHODES_AFFICHAGE = {
    "baseline_tfidf_mots": "Baseline TF-IDF",
    "approche2a_phrases_tfidf": "2a Expressions",
    "approche2b_textrank": "2b TextRank",
    "approche2c_lemmes_spacy_tfidf": "2c Lemmes spaCy",
}

# Description courte de chaque méthode, affichée dans l'interface.
DESCRIPTIONS_METHODES = {
    "baseline_tfidf_mots": (
        "Compte les mots et pondère chacun par sa rareté dans le corpus (TF-IDF). "
        "Référence de comparaison, sans aucun traitement linguistique."
    ),
    "approche2a_phrases_tfidf": (
        "Découpe le texte en expressions (suites de mots entre ponctuations ou mots vides), "
        "puis classe ces expressions par TF-IDF. Garde « congé annuel » au lieu de deux mots séparés."
    ),
    "approche2b_textrank": (
        "Construit un graphe où deux mots voisins sont reliés, puis classe les mots "
        "par l'algorithme PageRank. Ne dépend d'aucun corpus d'entraînement."
    ),
    "approche2c_lemmes_spacy_tfidf": (
        "Ramène chaque mot à sa forme de base (lemme) avec spaCy, ne garde que les noms, "
        "noms propres et adjectifs, puis classe par TF-IDF."
    ),
}

LIMITE_CARACTERES = 50_000
LIMITE_OCTETS_FICHIER = 200_000
MINIMUM_MOTS_CONSEILLE = 15

_PATRON_MOT_TEXTE = re.compile(r"\w+")


def controler_texte(texte: str) -> tuple[str | None, str | None]:
    """Vérifie un texte avant analyse.

    Renvoie (erreur, avertissement). Une erreur bloque l'analyse ; un avertissement
    ne bloque pas, il prévient seulement que le résultat sera peu fiable.
    """
    if not texte or not texte.strip():
        return "Le texte est vide. Collez une note ou choisissez une note du corpus.", None
    if len(texte) > LIMITE_CARACTERES:
        return (
            "Le texte dépasse 50 000 caractères. Découpez-le en plusieurs notes.",
            None,
        )
    nb_mots = len(_PATRON_MOT_TEXTE.findall(texte))
    if nb_mots < MINIMUM_MOTS_CONSEILLE:
        return None, (
            f"Le texte ne contient que {nb_mots} mot{'s' if nb_mots > 1 else ''}. Au-dessous de {MINIMUM_MOTS_CONSEILLE} mots, "
            "les mots-clés proposés sont peu fiables."
        )
    return None, None


def decoder_octets(donnees: bytes) -> tuple[str | None, str | None, str | None]:
    """Décode un fichier texte chargé par l'utilisateur.

    Renvoie (texte, encodage utilisé, erreur). Essaie UTF-8, puis Windows-1252
    (encodage courant des fichiers produits sous Windows en français).
    """
    if len(donnees) > LIMITE_OCTETS_FICHIER:
        return None, None, "Le fichier dépasse 200 Ko. Envoyez une note plus courte."
    for encodage in ("utf-8-sig", "cp1252"):
        try:
            return donnees.decode(encodage), encodage, None
        except UnicodeDecodeError:
            continue
    return None, None, "Encodage non reconnu. Enregistrez le fichier en UTF-8 puis rechargez-le."


def extraire_tous(extracteurs: dict, texte: str, k: int) -> dict[str, list[str]]:
    """Mots-clés de chaque méthode, classés, sans doublon de mots."""
    return {cle: extracteurs[cle](texte, k) for cle in METHODES_AFFICHAGE}


def extraire_chronometre(extracteurs: dict, texte: str, k: int) -> tuple[dict[str, list[str]], dict[str, float]]:
    """Comme extraire_tous, avec le temps de calcul de chaque méthode en millisecondes."""
    predictions, temps = {}, {}
    for cle in METHODES_AFFICHAGE:
        debut = time.perf_counter()
        predictions[cle] = extracteurs[cle](texte, k)
        temps[cle] = (time.perf_counter() - debut) * 1000
    return predictions, temps


def evaluer(predictions: dict[str, list[str]], references: list[str]) -> dict[str, dict[str, float]]:
    """Précision, rappel et F1 souples de chaque méthode, contre les références d'une note."""
    resultats = {}
    for cle, mots in predictions.items():
        p, r, f1 = metriques_document(mots, references, "souple")
        resultats[cle] = {"precision": p, "rappel": r, "f1": f1}
    return resultats


def echapper(texte: str) -> str:
    """Échappe un texte avant de l'insérer dans du HTML."""
    return html.escape(texte, quote=True)


def surligner(texte: str, mots: list[str]) -> str:
    """Texte échappé, où chaque mot-clé trouvé est entouré d'une balise <mark>.

    Une seule passe avec une alternative triée par longueur : « fiche technique »
    l'emporte sur « fiche », et une balise déjà posée n'est jamais recoupée.
    """
    expressions = sorted({m for m in mots if m}, key=len, reverse=True)
    echappe = html.escape(texte)
    if not expressions:
        return echappe.replace("\r\n", "\n").replace("\n", "<br>")
    motif = re.compile("|".join(re.escape(html.escape(m)) for m in expressions), re.IGNORECASE)
    surligne = motif.sub(lambda m: f'<mark class="mot-cle">{m.group(0)}</mark>', echappe)
    # Les lignes vides casseraient le bloc HTML dans le rendu Markdown de Streamlit :
    # on remplace chaque saut de ligne par une balise <br>, sans ligne vide.
    return surligne.replace("\r\n", "\n").replace("\n", "<br>")


def exporter_csv(predictions: dict[str, list[str]]) -> str:
    """Tableau CSV : un rang par ligne, une colonne par méthode (encodage UTF-8 avec BOM)."""
    tampon = io.StringIO()
    entetes = ["rang"] + [METHODES_AFFICHAGE[c] for c in METHODES_AFFICHAGE]
    ecrivain = csv.writer(tampon)
    ecrivain.writerow(entetes)
    k = max((len(v) for v in predictions.values()), default=0)
    for rang in range(k):
        ligne = [rang + 1]
        for cle in METHODES_AFFICHAGE:
            mots = predictions.get(cle, [])
            ligne.append(mots[rang] if rang < len(mots) else "")
        ecrivain.writerow(ligne)
    return "﻿" + tampon.getvalue()


def exporter_mesures_csv(resultats: dict[str, dict[str, float]]) -> str:
    """Précision, rappel et F1 de chaque méthode en CSV (UTF-8 avec BOM)."""
    tampon = io.StringIO()
    ecrivain = csv.writer(tampon)
    ecrivain.writerow(["methode", "precision", "rappel", "f1"])
    for cle, valeurs in resultats.items():
        ecrivain.writerow(
            [METHODES_AFFICHAGE[cle]] + [f"{valeurs[m]:.3f}" for m in ("precision", "rappel", "f1")]
        )
    return "﻿" + tampon.getvalue()
