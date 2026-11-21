"""Évaluation humaine aveugle des mots-clés proposés par chaque méthode.

Échantillon : 20 notes = les 10 notes de test + les 10 premières notes d'évaluation (N11 à N20).

Étape 1 - generer :
    python src/annotation_humaine.py generer
  Produit :
    results/documents_a_annoter.md              les 20 notes, sans références
    results/formulaire_evaluation_humaine.csv   une ligne par mot-clé, méthode masquée
    results/cle_methodes_PRIVEE.csv             correspondance lettre -> méthode (ne pas ouvrir avant la notation)

Étape 2 - analyser (après saisie de la colonne 'pertinent' : 1 = pertinent, 0 = non) :
    python src/annotation_humaine.py analyser
  Produit results/resultats_evaluation_humaine.csv (précision humaine par méthode, à k = 5).

Les annotateurs ne voient ni le nom des méthodes ni les mots-clés de référence.
"""
from __future__ import annotations

import random
import sys

import pandas as pd

import config as cfg
from evaluate import charger_corpus
from methods import construire_methodes

K = cfg.K_PRINCIPAL


def echantillon(corpus: list[dict]) -> list[dict]:
    test = [d for d in corpus if d["split"] == "test"]
    eval_debut = [d for d in corpus if d["split"] == "eval"][:10]
    return test + eval_debut


def generer() -> None:
    corpus = charger_corpus()
    tous = [d["texte"] for d in corpus if d["split"] != "test"]
    methodes = construire_methodes(tous)
    annotes = echantillon(corpus)

    rng = random.Random(cfg.GRAINE)
    noms = list(methodes)
    lettres = list("ABCD")
    rng.shuffle(lettres)
    correspondance = dict(zip(noms, lettres))

    lignes, documents = [], []
    for d in annotes:
        documents.append(f"## {d['id']} – {d['titre']}\n\n{d['texte']}\n")
        melange = []
        for nom, extracteur in methodes.items():
            for mot in extracteur(d["texte"], K):
                melange.append({"id": d["id"], "lettre": correspondance[nom], "mot_cle": mot})
        rng.shuffle(melange)
        for m in melange:
            lignes.append({**m, "pertinent": "", "commentaire": ""})

    cfg.RESULTATS.mkdir(exist_ok=True)
    (cfg.RESULTATS / "documents_a_annoter.md").write_text(
        f"# Documents à annoter ({len(annotes)} notes)\n\n"
        "Pour chaque mot-clé du formulaire, indiquer 1 s'il est pertinent pour la note, 0 sinon.\n\n"
        + "\n".join(documents), encoding="utf-8")
    pd.DataFrame(lignes).to_csv(cfg.RESULTATS / "formulaire_evaluation_humaine.csv", index=False, encoding="utf-8")
    pd.DataFrame([{"lettre": v, "methode": k} for k, v in correspondance.items()]).to_csv(
        cfg.RESULTATS / "cle_methodes_PRIVEE.csv", index=False, encoding="utf-8")
    print(f"Formulaire généré : {len(lignes)} lignes à noter pour {len(annotes)} notes.")


def analyser() -> None:
    formulaire = pd.read_csv(cfg.RESULTATS / "formulaire_evaluation_humaine.csv", dtype={"pertinent": "Int64"})
    cle = pd.read_csv(cfg.RESULTATS / "cle_methodes_PRIVEE.csv")
    notes = formulaire.dropna(subset=["pertinent"])
    if notes.empty:
        print("Aucune note saisie : remplir la colonne 'pertinent' (0 ou 1), puis relancer.")
        sys.exit(1)
    fusion = notes.merge(cle, on="lettre")
    resume = (fusion.groupby("methode")["pertinent"].agg(["mean", "count"])
              .rename(columns={"mean": "precision_humaine_k5", "count": "nb_notes_annotees"}).reset_index())
    resume.to_csv(cfg.RESULTATS / "resultats_evaluation_humaine.csv", index=False, encoding="utf-8")
    print(resume.to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"generer", "analyser"}:
        print(__doc__)
        sys.exit(0)
    generer() if sys.argv[1] == "generer" else analyser()
