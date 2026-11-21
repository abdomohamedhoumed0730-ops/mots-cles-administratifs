"""Interface de démonstration (Gradio) : mots-clés d'une note administrative.

Lancer :  python app/app_gradio.py   puis ouvrir l'adresse affichée (http://127.0.0.1:7860).

L'utilisateur colle une note, choisit k, et obtient un tableau : une colonne par méthode,
une ligne par rang. La logique (analyser) est séparée de l'interface pour être testée.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from evaluate import charger_corpus  # noqa: E402
from methods import construire_methodes  # noqa: E402

COLONNES = {
    "baseline_tfidf_mots": "Baseline TF-IDF",
    "approche2a_phrases_tfidf": "2a Expressions",
    "approche2b_textrank": "2b TextRank",
    "approche2c_lemmes_spacy_tfidf": "2c Lemmes spaCy",
}

EXEMPLE = (
    "Objet : demande d'achat de matériel informatique. Le service de la scolarité sollicite "
    "le remplacement de trois ordinateurs qui ne peuvent plus faire tourner le logiciel de gestion "
    "des notes. Le coût estimé est de 2 400 000 francs djiboutiens. Une fiche technique détaillée "
    "et deux devis sont joints à la présente demande."
)


def construire_extracteurs():
    """IDF appris hors notes de test, comme dans l'évaluation."""
    corpus = [d["texte"] for d in charger_corpus() if d["split"] != "test"]
    return construire_methodes(corpus)


def analyser(extracteurs: dict, texte: str, k: int) -> pd.DataFrame:
    """Renvoie un tableau : Rang, puis une colonne par méthode."""
    k = int(k)
    if not texte or not texte.strip():
        return pd.DataFrame({"Message": ["Collez une note administrative pour obtenir des mots-clés."]})
    colonnes = {"Rang": list(range(1, k + 1))}
    for cle, titre in COLONNES.items():
        mots = extracteurs[cle](texte, k)
        colonnes[titre] = mots + [""] * (k - len(mots))
    return pd.DataFrame(colonnes)


def construire_interface(extracteurs: dict):
    import gradio as gr

    with gr.Blocks(title="Mots-clés administratifs – M2 IAMD") as demo:
        gr.Markdown(
            "## Mots-clés d'une note administrative\n"
            "Quatre méthodes, un même texte. Les colonnes sont classées par rang. "
            "Les scores ne sont pas des probabilités : ce sont des classements."
        )
        texte = gr.Textbox(label="Note administrative", value=EXEMPLE, lines=6)
        k = gr.Slider(minimum=5, maximum=10, value=5, step=1, label="Nombre de mots-clés (k)")
        bouton = gr.Button("Extraire", variant="primary")
        tableau = gr.Dataframe(label="Mots-clés par méthode", interactive=False)
        bouton.click(lambda t, n: analyser(extracteurs, t, n), inputs=[texte, k], outputs=tableau)
    return demo


if __name__ == "__main__":
    construire_interface(construire_extracteurs()).launch()
