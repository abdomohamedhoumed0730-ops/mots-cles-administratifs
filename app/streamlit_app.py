"""Mots-clés d'une note administrative : comparaison de quatre méthodes de TAL.

Application Streamlit. Lancer en local :  streamlit run app/streamlit_app.py
La logique (extraction, contrôles, évaluation) est dans src/appli.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from appli import (  # noqa: E402
    DESCRIPTIONS_METHODES,
    METHODES_AFFICHAGE,
    VERSION,
    controler_texte,
    decoder_octets,
    echapper,
    evaluer,
    exporter_csv,
    exporter_mesures_csv,
    extraire_chronometre,
    surligner,
)
from evaluate import charger_corpus  # noqa: E402
from methods import construire_methodes  # noqa: E402

st.set_page_config(
    page_title="Mots-clés administratifs",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root {
  --primaire: #1F2328; --accent: #D9622B; --accent-doux: #FBE1CF; --sable: #F5F3EE;
  --texte: #1F2328; --gris: #5B616B; --bord: #DEDAD2; --surlignage: #FCD9B6;
}
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px;}
h1, h2, h3 {letter-spacing: -0.01em; color: var(--texte);}
.bandeau {background: var(--primaire); color: #FFFFFF; border-radius: 16px; padding: 28px 32px;
  border-bottom: 4px solid var(--accent); display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; margin-bottom: 14px;}
.bandeau h1 {color: #FFFFFF; margin: 0; font-size: 2rem; font-weight: 700;}
.bandeau p {color: #D8DCE1; margin: 8px 0 0 0; font-size: 1.02rem; line-height: 1.5; max-width: 760px;}
.version {background: rgba(255,255,255,.12); color: #FFFFFF; border-radius: 999px; padding: 4px 12px;
  font-size: .8rem; white-space: nowrap;}
.etapes {display: flex; gap: 10px; flex-wrap: wrap; margin: 0 0 18px 0;}
.etape {background: #FFFFFF; border: 1px solid var(--bord); border-radius: 999px; padding: 6px 14px;
  font-size: .9rem; color: var(--gris);}
.etape b {color: var(--accent);}
.carte {background: #FFFFFF; border: 1px solid var(--bord); border-radius: 14px; padding: 20px 22px; margin-bottom: 16px;}
.carte-methode {background: #FFFFFF; border: 1px solid var(--bord); border-left: 4px solid var(--accent);
  border-radius: 12px; padding: 16px 18px; margin-bottom: 14px;}
.carte-methode h4 {margin: 0 0 6px 0; color: var(--primaire);}
.carte-methode p {margin: 0; color: var(--texte); line-height: 1.55;}
.etiquette {font-size: .76rem; letter-spacing: .08em; text-transform: uppercase; color: var(--gris); margin: 0 0 10px 0; font-weight: 600;}
.pastille {display: inline-block; background: var(--accent-doux); color: var(--primaire); border-radius: 999px;
  padding: 6px 14px; margin: 4px 6px 4px 0; font-weight: 600;}
.pastille span {color: var(--gris); font-weight: 400; font-size: .8rem; margin-right: 6px;}
mark.mot-cle {background: var(--surlignage); color: var(--texte); border-radius: 4px; padding: 0 3px;}
.texte-note {line-height: 1.75; font-size: 1.02rem;}
.legende {font-size: .85rem; color: var(--gris); margin-bottom: 10px;}
.avertissement {background: #FDF0E7; border-left: 4px solid var(--accent); border-radius: 8px; padding: 12px 16px; color: var(--texte); margin-bottom: 14px;}
.info {background: var(--sable); border-left: 4px solid var(--primaire); border-radius: 8px; padding: 12px 16px; color: var(--texte); margin-bottom: 14px;}
.definition {color: var(--texte); line-height: 1.6; font-size: .95rem;}
.pied {color: var(--gris); font-size: .85rem; margin-top: 28px; line-height: 1.5;}
.accueil {text-align: center; color: var(--gris); padding: 48px 12px;}
</style>
"""


@st.cache_resource(show_spinner="Préparation des méthodes…")
def charger_methodes():
    """IDF appris hors notes de test, comme dans l'évaluation."""
    notes = charger_corpus()
    corpus = [n["texte"] for n in notes if n["split"] != "test"]
    return construire_methodes(corpus), notes


def bandeau() -> None:
    st.markdown(
        '<div class="bandeau"><div>'
        "<h1>Mots-clés d'une note administrative</h1>"
        "<p>Quatre méthodes de traitement automatique du langage sont appliquées au même texte. "
        "Vous voyez leurs mots-clés côte à côte, et, si la note a des références, leur précision mesurée.</p>"
        f'</div><span class="version">Version {VERSION}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="etapes">'
        '<span class="etape"><b>1</b> Choisir ou coller la note</span>'
        '<span class="etape"><b>2</b> Lancer l\'extraction</span>'
        '<span class="etape"><b>3</b> Lire et comparer les résultats</span>'
        "</div>",
        unsafe_allow_html=True,
    )


def reglages(notes: list[dict]) -> tuple[int, str, str]:
    with st.sidebar:
        st.markdown("### Réglages")
        k = st.slider("Nombre de mots-clés (k)", 5, 10, 5, help="Entre 5 et 10 mots-clés par méthode.")
        principale = st.selectbox(
            "Méthode principale",
            list(METHODES_AFFICHAGE),
            format_func=METHODES_AFFICHAGE.get,
            help="Ses mots-clés sont surlignés dans la note.",
        )
        source = st.radio("Source du texte", ["Note du corpus", "Coller un texte", "Charger un fichier .txt"])
        st.markdown("---")
        st.markdown(
            f"**Version {VERSION}**  \nCorpus de référence : {len(notes)} notes fictives. "
            "Les notes de test ne servent pas à calibrer les méthodes."
        )
    return k, principale, source


def saisir_texte(notes: list[dict], source: str) -> tuple[str, list[str], str | None]:
    """Renvoie (texte, mots de référence, avertissement de source)."""
    if source == "Note du corpus":
        choix = st.selectbox("Note à analyser", notes, format_func=lambda n: f"{n['id']} · {n['titre']}")
        return choix["texte"], choix["mots_cles_reference"], None
    if source == "Coller un texte":
        texte = st.text_area("Collez la note ici", height=200, placeholder="Objet : …")
        return texte, [], None
    fichier = st.file_uploader("Fichier texte (.txt), 200 Ko au maximum", type=["txt"])
    if fichier is None:
        return "", [], None
    texte, encodage, erreur = decoder_octets(fichier.getvalue())
    if erreur:
        st.error(erreur)
        return "", [], None
    return texte, [], f"Fichier lu avec l'encodage {encodage}."


def lancer_extraction(texte: str, k: int, principale: str, references: list[str], extracteurs: dict) -> None:
    predictions, temps = extraire_chronometre(extracteurs, texte, k)
    st.session_state["resultat"] = {
        "texte": texte,
        "k": k,
        "principale": principale,
        "predictions": predictions,
        "temps": temps,
        "references": references,
    }


def afficher_mots_cles(res: dict) -> None:
    mots = res["predictions"][res["principale"]]
    nom = METHODES_AFFICHAGE[res["principale"]]
    pastilles = "".join(
        f'<span class="pastille"><span>{rang}</span>{echapper(m)}</span>' for rang, m in enumerate(mots, 1)
    )
    st.markdown(
        f'<div class="carte"><div class="etiquette">Mots-clés · {echapper(nom)}</div>'
        f"{pastilles or 'Aucun mot-clé trouvé.'}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="carte"><div class="etiquette">Note surlignée</div>'
        '<div class="legende">Les expressions surlignées sont les mots-clés de la méthode principale.</div>'
        f'<div class="texte-note">{surligner(res["texte"], mots)}</div></div>',
        unsafe_allow_html=True,
    )


def afficher_comparaison(res: dict) -> None:
    k, predictions, temps = res["k"], res["predictions"], res["temps"]
    st.markdown('<div class="etiquette">Mots-clés par méthode</div>', unsafe_allow_html=True)
    tableau = pd.DataFrame(
        {"Rang": list(range(1, k + 1))}
        | {METHODES_AFFICHAGE[c]: predictions[c] + [""] * (k - len(predictions[c])) for c in METHODES_AFFICHAGE}
    )
    st.dataframe(tableau, hide_index=True, width="stretch")

    col_temps, col_csv = st.columns([2, 1])
    with col_temps:
        st.markdown('<div class="etiquette">Temps de calcul</div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(
                [{"Méthode": METHODES_AFFICHAGE[c], "Temps (ms)": round(temps[c], 1)} for c in METHODES_AFFICHAGE]
            ),
            hide_index=True,
            width="stretch",
        )
    with col_csv:
        st.markdown('<div class="etiquette">Export</div>', unsafe_allow_html=True)
        st.download_button(
            "Télécharger le tableau (CSV)",
            data=exporter_csv(predictions).encode("utf-8"),
            file_name="mots_cles.csv",
            mime="text/csv",
        )


def afficher_mesure(res: dict) -> None:
    refs = res["references"]
    if not refs:
        st.markdown(
            '<div class="info">Cette note n\'a pas de références : aucune mesure n\'est affichée. '
            "Une note libre ne permet pas de calculer la précision ni le rappel.</div>",
            unsafe_allow_html=True,
        )
        return
    resultats = evaluer(res["predictions"], refs)
    lignes = [
        {
            "Méthode": METHODES_AFFICHAGE[c],
            "Précision": r["precision"],
            "Rappel": r["rappel"],
            "F1": r["f1"],
        }
        for c, r in resultats.items()
    ]
    st.markdown('<div class="etiquette">Mesure contre les références de cette note</div>', unsafe_allow_html=True)
    st.dataframe(
        pd.DataFrame(lignes),
        hide_index=True,
        width="stretch",
        column_config={c: st.column_config.NumberColumn(format="%.2f") for c in ("Précision", "Rappel", "F1")},
    )
    st.download_button(
        "Télécharger les mesures (CSV)",
        data=exporter_mesures_csv(resultats).encode("utf-8"),
        file_name="mesures.csv",
        mime="text/csv",
    )
    st.markdown(
        '<div class="carte"><div class="etiquette">Comment lire ces chiffres</div>'
        '<p class="definition">'
        "<b>Précision</b> : part des mots proposés qui correspondent à une référence.<br>"
        "<b>Rappel</b> : part des références retrouvées parmi les mots proposés.<br>"
        "<b>F1</b> : moyenne de la précision et du rappel ; elle reste basse si l'un des deux l'est.<br>"
        "<b>Correspondance souple</b> : un mot proposé compte comme juste s'il contient une référence "
        "ou est contenu dans une référence, après retrait des accents et des pluriels simples."
        "</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='avertissement'>Références de cette note : {echapper(', '.join(refs))}. "
        "Une seule note ne permet pas de conclure. La mesure sérieuse porte sur l'ensemble du jeu "
        "de données, présenté dans le rapport.</div>",
        unsafe_allow_html=True,
    )


def afficher_methodes() -> None:
    for cle, nom in METHODES_AFFICHAGE.items():
        st.markdown(
            f'<div class="carte-methode"><h4>{echapper(nom)}</h4>'
            f"<p>{echapper(DESCRIPTIONS_METHODES[cle])}</p></div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="carte"><div class="etiquette">Limites connues</div>'
        '<p class="definition">'
        "• Les scores sont des classements, pas des probabilités : un mot classé haut n'est pas forcément juste.<br>"
        "• La liste de mots vides est volontairement courte. Certains mots de liaison peuvent donc sortir "
        "(par exemple « afin »). Ce défaut est mesuré et discuté dans le rapport.<br>"
        "• Le corpus compte 40 notes fictives. Les résultats ne se transposent pas tels quels à de vraies archives.<br>"
        "• Une seule note ne suffit pas à juger une méthode."
        "</p></div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    bandeau()
    extracteurs, notes = charger_methodes()
    k, principale, source = reglages(notes)

    with st.container(border=True):
        st.markdown('<div class="etiquette">Texte à analyser</div>', unsafe_allow_html=True)
        texte, references, info_source = saisir_texte(notes, source)
        if info_source:
            st.caption(info_source)
        erreur, avertissement = controler_texte(texte)
        if erreur and texte:
            st.error(erreur)
        elif avertissement:
            st.warning(avertissement)
        lancer = st.button(
            "Extraire les mots-clés",
            type="primary",
            disabled=bool(erreur) or not texte.strip(),
        )

    if lancer and not erreur:
        lancer_extraction(texte, k, principale, references, extracteurs)

    res = st.session_state.get("resultat")
    if res is None:
        st.markdown(
            '<div class="accueil">Choisissez une note, puis cliquez sur « Extraire les mots-clés ».</div>',
            unsafe_allow_html=True,
        )
    else:
        if res["k"] != k or res["principale"] != principale:
            st.markdown(
                "<div class='info'>Les réglages ont changé. Relancez l'extraction pour les appliquer.</div>",
                unsafe_allow_html=True,
            )
        onglets = st.tabs(["Mots-clés", "Comparaison", "Mesure", "Méthodes et limites"])
        with onglets[0]:
            afficher_mots_cles(res)
        with onglets[1]:
            afficher_comparaison(res)
        with onglets[2]:
            afficher_mesure(res)
        with onglets[3]:
            afficher_methodes()

    st.markdown(
        "<div class='pied'>Les mots-clés proposés sont des suggestions, à relire avant tout usage.</div>",
        unsafe_allow_html=True,
    )


main()
