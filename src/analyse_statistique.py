"""Incertitude des résultats : intervalles de confiance par bootstrap apparié.

Pourquoi : avec 10 à 20 notes, un écart de F1 peut être du hasard. On rééchantillonne
les notes avec remise (bootstrap), on recalcule la différence de F1 moyen entre deux
méthodes à chaque tirage, et on lit l'intervalle à 95 % dans la distribution obtenue.
Si l'intervalle contient 0, l'écart n'est pas établi.

Le rééchantillonnage est apparié : on tire les mêmes notes pour les deux méthodes,
ce qui réduit la variance de la différence.

Entrée : results/metriques_par_document.csv (produit par evaluate.py)
Sortie : results/intervalles_confiance.csv
Usage  : python src/analyse_statistique.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config as cfg

B = 2000  # nombre de rééchantillonnages
REFERENCE = "baseline_tfidf_mots"


def intervalle_difference(a: np.ndarray, b: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    """Différence moyenne a - b et intervalle à 95 % (bootstrap apparié)."""
    n = len(a)
    diffs = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        diffs[i] = a[idx].mean() - b[idx].mean()
    return float(a.mean() - b.mean()), float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def main() -> None:
    df = pd.read_csv(cfg.RESULTATS / "metriques_par_document.csv")
    df = df[df.correspondance == "souple"]
    rng = np.random.default_rng(cfg.GRAINE)
    lignes = []
    for split in ("eval", "test"):
        for k in cfg.K_VALUES:
            sous = df[(df.split == split) & (df.k == k)]
            pivot = sous.pivot(index="id", columns="methode", values="F1").sort_index()
            ref = pivot[REFERENCE].to_numpy()
            for methode in pivot.columns:
                if methode == REFERENCE:
                    continue
                diff, bas, haut = intervalle_difference(pivot[methode].to_numpy(), ref, rng)
                lignes.append({
                    "jeu": split, "k": k, "methode": methode, "reference": REFERENCE,
                    "difference_F1": round(diff, 3), "IC95_bas": round(bas, 3), "IC95_haut": round(haut, 3),
                    "ecart_etabli": "oui" if (bas > 0 or haut < 0) else "non",
                    "nb_notes": len(pivot),
                })
    sortie = pd.DataFrame(lignes)
    sortie.to_csv(cfg.RESULTATS / "intervalles_confiance.csv", index=False, encoding="utf-8")
    print(sortie.to_string(index=False))


if __name__ == "__main__":
    main()
