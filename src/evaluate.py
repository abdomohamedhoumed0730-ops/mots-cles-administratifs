"""Évaluation des quatre méthodes d'extraction de mots-clés.

Protocole (sans fuite) :
1. Le corpus est coupé en deux : 'dev' (10 notes, pour choisir les hyperparamètres)
   et 'eval' (20 notes, jamais utilisées pour choisir quoi que ce soit).
2. Les hyperparamètres des approches 2a, 2b et 2c sont choisis sur 'dev' seulement
   (F1 souple à k = K_PRINCIPAL). Les choix sont écrits dans results/selection_dev.csv.
3. Les méthodes figées sont mesurées sur 'eval' : précision, rappel, F1 à k = 5 et k = 10.
4. Stabilité : (a) mélange de l'ordre des phrases, contrôle d'invariance attendu à 1,0 ;
   (b) suppression d'une phrase au hasard, perturbation réelle mesurée en Jaccard.
5. Erreurs : mots-clés parasites et références absentes du top-5 (eval).

Deux correspondances avec la référence :
- stricte : mêmes ensembles de mots (sans mots vides, sans accent, pluriel retiré) ;
- souple : l'un des deux ensembles est inclus dans l'autre. Mesure principale.

Usage (depuis la racine) : python src/evaluate.py
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd

import config as cfg
from methods import approche_lemmes, approche_phrases, approche_textrank, baseline_tfidf, construire_methodes
from text_utils import decouper_phrases, ensemble_mots_matching


def charger_corpus() -> list[dict]:
    with open(cfg.DONNEES, encoding="utf-8") as f:
        return json.load(f)


def correspond(prediction: str, reference: str, mode: str) -> bool:
    ens_p = ensemble_mots_matching(prediction)
    ens_r = ensemble_mots_matching(reference)
    if not ens_p or not ens_r:
        return False
    if mode == "stricte":
        return ens_p == ens_r
    return ens_p <= ens_r or ens_r <= ens_p


def metriques_document(predictions: list[str], references: list[str], mode: str) -> tuple[float, float, float]:
    """Précision, rappel et F1 pour une note."""
    if not predictions:
        return 0.0, 0.0, 0.0
    precision_hits = sum(any(correspond(p, r, mode) for r in references) for p in predictions)
    rappel_hits = sum(any(correspond(p, r, mode) for p in predictions) for r in references)
    precision = precision_hits / len(predictions)
    rappel = rappel_hits / len(references) if references else 0.0
    f1 = 2 * precision * rappel / (precision + rappel) if precision + rappel else 0.0
    return precision, rappel, f1


def jaccard(a: list[str], b: list[str]) -> float:
    sa = {ensemble_mots_matching(x) for x in a}
    sb = {ensemble_mots_matching(x) for x in b}
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def melanger_phrases(texte: str, graine: int) -> str:
    """Contrôle d'invariance : change l'ordre des phrases, sans rien retirer."""
    phrases = decouper_phrases(texte)
    random.Random(graine).shuffle(phrases)
    return ". ".join(phrases) + "."


def supprimer_une_phrase(texte: str, graine: int) -> str:
    """Perturbation réelle : retire une phrase choisie au hasard (si le texte en a au moins 3)."""
    phrases = decouper_phrases(texte)
    if len(phrases) < 3:
        return texte
    retiree = random.Random(graine).randrange(len(phrases))
    del phrases[retiree]
    return ". ".join(phrases) + "."


def selection_hyperparametres(dev: list[dict], tous: list[str]) -> pd.DataFrame:
    """Grilles de choix, uniquement sur le jeu de développement."""
    lignes = []

    def score(extracteur) -> float:
        f1s = [metriques_document(extracteur(d["texte"], cfg.K_PRINCIPAL), d["mots_cles_reference"], "souple")[2] for d in dev]
        return float(np.mean(f1s))

    for longueur in cfg.GRILLE_PHRASES:
        lignes.append({"methode": "approche2a_phrases_tfidf", "parametre": f"longueur_max={longueur}",
                       "valeur": longueur, "F1_souple_k5_dev": score(approche_phrases(tous, longueur))})
    for fenetre in cfg.GRILLE_FENETRE:
        lignes.append({"methode": "approche2b_textrank", "parametre": f"fenetre={fenetre}",
                       "valeur": fenetre, "F1_souple_k5_dev": score(approche_textrank(fenetre))})
    for longueur in cfg.GRILLE_LEMMES:
        lignes.append({"methode": "approche2c_lemmes_spacy_tfidf", "parametre": f"longueur_max={longueur}",
                       "valeur": longueur, "F1_souple_k5_dev": score(approche_lemmes(tous, longueur))})
    return pd.DataFrame(lignes)


def meilleur(selection: pd.DataFrame, methode: str) -> int:
    """Valeur du paramètre ayant le meilleur F1 dev. En cas d'égalité, la plus petite valeur."""
    s = selection[selection.methode == methode].sort_values(["F1_souple_k5_dev", "valeur"], ascending=[False, True])
    return int(s.iloc[0]["valeur"])


def main() -> None:
    cfg.RESULTATS.mkdir(exist_ok=True)
    corpus = charger_corpus()
    # L'IDF est appris sans les notes de test, pour que le test n'influence rien (même sans étiquettes).
    tous = [d["texte"] for d in corpus if d["split"] != "test"]
    dev = [d for d in corpus if d["split"] == "dev"]
    evalu = [d for d in corpus if d["split"] == "eval"]
    print(f"Corpus : {len(corpus)} notes ({len(dev)} dev, {len(evalu)} eval)")

    # 1) Choix des hyperparamètres sur le dev seulement
    selection = selection_hyperparametres(dev, tous)
    selection.to_csv(cfg.RESULTATS / "selection_dev.csv", index=False, encoding="utf-8")
    l2a = meilleur(selection, "approche2a_phrases_tfidf")
    f2b = meilleur(selection, "approche2b_textrank")
    l2c = meilleur(selection, "approche2c_lemmes_spacy_tfidf")
    print(f"Hyperparamètres retenus (sur dev) : 2a longueur_max={l2a}, 2b fenetre={f2b}, 2c longueur_max={l2c}")

    # 2) Méthodes figées
    methodes = {
        "baseline_tfidf_mots": baseline_tfidf(tous),
        "approche2a_phrases_tfidf": approche_phrases(tous, l2a),
        "approche2b_textrank": approche_textrank(f2b),
        "approche2c_lemmes_spacy_tfidf": approche_lemmes(tous, l2c),
    }

    # 3) Métriques par document
    lignes_doc, temps = [], {}
    for nom, extracteur in methodes.items():
        debut = time.perf_counter()
        for d in corpus:
            for k in cfg.K_VALUES:
                preds = extracteur(d["texte"], k)
                for mode in ("souple", "stricte"):
                    p, r, f1 = metriques_document(preds, d["mots_cles_reference"], mode)
                    lignes_doc.append({"id": d["id"], "split": d["split"], "methode": nom, "k": k,
                                       "correspondance": mode, "precision": p, "rappel": r, "F1": f1})
        temps[nom] = (time.perf_counter() - debut) / len(corpus)
    df_doc = pd.DataFrame(lignes_doc)
    df_doc.to_csv(cfg.RESULTATS / "metriques_par_document.csv", index=False, encoding="utf-8")

    resume = (df_doc.groupby(["split", "methode", "k", "correspondance"])[["precision", "rappel", "F1"]]
              .mean().reset_index())
    resume.to_csv(cfg.RESULTATS / "metriques_resume.csv", index=False, encoding="utf-8")
    print("\nRésumé par jeu (moyenne par note) :")
    print(resume[resume.split.isin(["eval", "test"])].sort_values(["split", "k", "methode"]).round(3).to_string(index=False))

    # 4) Stabilité
    lignes_stab = []
    for nom, extracteur in methodes.items():
        js_ordre, js_suppr = [], []
        for d in evalu:
            avant = extracteur(d["texte"], cfg.K_PRINCIPAL)
            js_ordre.append(jaccard(avant, extracteur(melanger_phrases(d["texte"], cfg.GRAINE), cfg.K_PRINCIPAL)))
            js_suppr.append(jaccard(avant, extracteur(supprimer_une_phrase(d["texte"], cfg.GRAINE), cfg.K_PRINCIPAL)))
        lignes_stab.append({
            "methode": nom,
            "jaccard_ordre_phrases_moyen": round(float(np.mean(js_ordre)), 3),
            "jaccard_suppression_phrase_moyen": round(float(np.mean(js_suppr)), 3),
            "jaccard_suppression_phrase_min": round(float(np.min(js_suppr)), 3),
        })
    pd.DataFrame(lignes_stab).to_csv(cfg.RESULTATS / "stabilite.csv", index=False, encoding="utf-8")

    # 5) Temps moyen par note (indicatif)
    pd.DataFrame([{"methode": k, "secondes_par_note": v} for k, v in temps.items()]).to_csv(
        cfg.RESULTATS / "temps_execution.csv", index=False, encoding="utf-8")

    # 6) Prédictions et erreurs (eval)
    lignes_pred, lignes_err = [], []
    for nom, extracteur in methodes.items():
        for d in evalu:
            preds10 = extracteur(d["texte"], max(cfg.K_VALUES))
            for rang, mot in enumerate(preds10, start=1):
                ok = any(correspond(mot, r, "souple") for r in d["mots_cles_reference"])
                lignes_pred.append({"id": d["id"], "methode": nom, "rang": rang, "mot_cle": mot, "correspond_reference": ok})
            preds5 = preds10[:cfg.K_PRINCIPAL]
            for mot in preds5:
                if not any(correspond(mot, r, "souple") for r in d["mots_cles_reference"]):
                    lignes_err.append({"id": d["id"], "methode": nom, "type": "parasite (top-5 hors référence)",
                                       "mot_cle": mot, "reference_manquee": ""})
            for ref in d["mots_cles_reference"]:
                if not any(correspond(p, ref, "souple") for p in preds5):
                    lignes_err.append({"id": d["id"], "methode": nom, "type": "référence absente du top-5",
                                       "mot_cle": "", "reference_manquee": ref})
    pd.DataFrame(lignes_pred).to_csv(cfg.RESULTATS / "predictions_eval.csv", index=False, encoding="utf-8")
    pd.DataFrame(lignes_err).to_csv(cfg.RESULTATS / "erreurs_par_document.csv", index=False, encoding="utf-8")

    # 7) Paramètres effectivement utilisés (traçabilité)
    (cfg.RESULTATS / "parametres_retenus.json").write_text(json.dumps({
        "graine": cfg.GRAINE, "k_values": list(cfg.K_VALUES),
        "approche2a_longueur_max": l2a, "approche2b_fenetre": f2b, "approche2c_longueur_max": l2c,
    }, indent=2) + "\n", encoding="utf-8")
    print("\nFichiers écrits dans results/.")


if __name__ == "__main__":
    main()
