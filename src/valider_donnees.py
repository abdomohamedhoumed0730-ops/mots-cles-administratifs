"""Validation du jeu de données avant toute expérimentation.

Contrôles (inspirés des bonnes pratiques de qualité de données) :
  1. Schéma      : chaque note a les champs attendus, des types corrects, un texte non vide.
  2. Unicité     : identifiants et textes non dupliqués.
  3. Équilibre   : 10 notes de développement, 20 notes d'évaluation, 6 références par note.
  4. Références  : pas de doublon dans une liste de références.
  5. Vie privée  : aucun e-mail, numéro de téléphone ou IBAN dans les textes.
  6. Couverture  : part des mots des références présents dans le texte (signalement, pas blocage).
  7. Intégrité   : empreinte SHA-256 écrite dans data/MANIFEST.json.

Un échec bloquant (FAIL) arrête la chaîne : les tests et l'évaluation le détectent.

Usage : python src/valider_donnees.py
Sortie : results/validation_donnees.md et data/MANIFEST.json
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from config import DONNEES, MANIFESTE, RESULTATS
from text_utils import ensemble_mots_matching, forme_normalisee, tokens

CHAMPS_OBLIGATOIRES = {"id", "split", "titre", "texte", "mots_cles_reference"}
SPLITS_ATTENDUS = {"dev": 10, "eval": 20, "test": 10}
REFERENCES_PAR_NOTE = 6

PATRONS_DONNEES_PERSONNELLES = {
    "courriel": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "telephone_djibouti": re.compile(r"\+?253[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
}


@dataclass
class Rapport:
    erreurs: list[str] = field(default_factory=list)
    avertissements: list[str] = field(default_factory=list)
    couverture: dict[str, float] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.erreurs


def empreinte_sha256(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def valider(notes: list[dict]) -> Rapport:
    rapport = Rapport()

    # 1. Schéma
    for n in notes:
        manquants = CHAMPS_OBLIGATOIRES - set(n)
        if manquants:
            rapport.erreurs.append(f"{n.get('id', '?')} : champs manquants {sorted(manquants)}")
            continue
        if not isinstance(n["texte"], str) or not n["texte"].strip():
            rapport.erreurs.append(f"{n['id']} : texte vide")
        if not isinstance(n["mots_cles_reference"], list):
            rapport.erreurs.append(f"{n['id']} : références non listées")

    if rapport.erreurs:
        return rapport

    # 2. Unicité
    ids = [n["id"] for n in notes]
    if len(set(ids)) != len(ids):
        rapport.erreurs.append("identifiants dupliqués")
    textes = [n["texte"] for n in notes]
    if len(set(textes)) != len(textes):
        rapport.erreurs.append("textes dupliqués")

    # 3. Équilibre
    for split, attendu in SPLITS_ATTENDUS.items():
        n_split = sum(1 for n in notes if n["split"] == split)
        if n_split != attendu:
            rapport.erreurs.append(f"split '{split}' : {n_split} notes, {attendu} attendues")
    for n in notes:
        if len(n["mots_cles_reference"]) != REFERENCES_PAR_NOTE:
            rapport.erreurs.append(f"{n['id']} : {len(n['mots_cles_reference'])} références, {REFERENCES_PAR_NOTE} attendues")

    # 4. Références sans doublon
    for n in notes:
        refs = [r.strip().lower() for r in n["mots_cles_reference"]]
        if len(set(refs)) != len(refs):
            rapport.erreurs.append(f"{n['id']} : références en double")

    # 5. Vie privée
    for n in notes:
        for nom, patron in PATRONS_DONNEES_PERSONNELLES.items():
            if patron.search(n["texte"]):
                rapport.erreurs.append(f"{n['id']} : donnée personnelle probable ({nom})")

    # 6. Couverture lexicale des références (avertissement seulement)
    for n in notes:
        mots_texte = {forme_normalisee(t) for t in tokens(n["texte"])}
        couvertures = []
        for ref in n["mots_cles_reference"]:
            ens = ensemble_mots_matching(ref)
            if ens:
                couvertures.append(len(ens & mots_texte) / len(ens))
        taux = sum(couvertures) / len(couvertures) if couvertures else 0.0
        rapport.couverture[n["id"]] = taux
        if taux < 0.5:
            rapport.avertissements.append(
                f"{n['id']} : couverture lexicale faible ({taux:.2f}), références peu présentes dans le texte"
            )
    return rapport


def ecrire_rapport(rapport: Rapport, notes: list[dict], empreinte: str) -> None:
    RESULTATS.mkdir(exist_ok=True)
    statut = "PASS" if rapport.ok else "FAIL"
    lignes = [
        "# Validation du jeu de données",
        "",
        f"Statut : **{statut}**",
        f"Notes : {len(notes)}  |  SHA-256 : `{empreinte}`",
        "",
        "## Erreurs bloquantes",
        *([f"- {e}" for e in rapport.erreurs] or ["Aucune."]),
        "",
        "## Avertissements",
        *([f"- {a}" for a in rapport.avertissements] or ["Aucun."]),
        "",
        "## Couverture lexicale des références par note",
        "",
        "| Note | Split | Couverture |",
        "|---|---|---|",
    ]
    splits = {n["id"]: n["split"] for n in notes}
    for nid, taux in rapport.couverture.items():
        lignes.append(f"| {nid} | {splits.get(nid, '')} | {taux:.2f} |")
    (RESULTATS / "validation_donnees.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main() -> int:
    with open(DONNEES, encoding="utf-8") as f:
        notes = json.load(f)
    rapport = valider(notes)
    empreinte = empreinte_sha256(DONNEES)
    ecrire_rapport(rapport, notes, empreinte)
    MANIFESTE.write_text(
        json.dumps({"fichier": DONNEES.name, "sha256": empreinte, "nb_notes": len(notes)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    statut = "PASS" if rapport.ok else "FAIL"
    print(f"Validation : {statut} ({len(notes)} notes, {len(rapport.avertissements)} avertissement(s))")
    for e in rapport.erreurs:
        print(f"  ERREUR : {e}")
    return 0 if rapport.ok else 1


if __name__ == "__main__":
    sys.exit(main())
