"""Démonstration : extraction de mots-clés sur une note administrative.

Usage (depuis la racine du projet) :
    python demo/demo_mots_cles.py                    # exemple intégré
    python demo/demo_mots_cles.py ma_note.txt        # votre propre texte (UTF-8)
    python demo/demo_mots_cles.py --k 8 ma_note.txt  # nombre de mots-clés

Les quatre méthodes sont comparées côte à côte. L'IDF est appris sur le corpus
synthétique de data/ (hors notes de test) ; sans ce corpus, les scores TF-IDF n'ont pas de sens.
"""
import argparse
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from evaluate import charger_corpus  # noqa: E402
from methods import construire_methodes  # noqa: E402

EXEMPLE = (
    "Objet : demande d'achat de matériel informatique. Le service de la scolarité sollicite "
    "le remplacement de trois ordinateurs qui ne peuvent plus faire tourner le logiciel de gestion "
    "des notes. Le coût estimé est de 2 400 000 francs djiboutiens. Une fiche technique détaillée "
    "et deux devis sont joints à la présente demande."
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mots-clés d'une note administrative")
    parser.add_argument("fichier", nargs="?", help="fichier texte UTF-8 (sinon exemple intégré)")
    parser.add_argument("--k", type=int, default=5, help="nombre de mots-clés (5 à 10 recommandé)")
    args = parser.parse_args()

    texte = Path(args.fichier).read_text(encoding="utf-8") if args.fichier else EXEMPLE
    # Même corpus d'apprentissage de l'IDF que l'évaluation : les notes de test en sont exclues.
    corpus = [d["texte"] for d in charger_corpus() if d["split"] != "test"]
    methodes = construire_methodes(corpus)

    print("Texte analysé :\n" + texte.strip() + "\n")
    for nom, extracteur in methodes.items():
        print(f"== {nom} (top {args.k})")
        for rang, mot in enumerate(extracteur(texte, args.k), start=1):
            print(f"   {rang:>2}. {mot}")
        print()


if __name__ == "__main__":
    main()
