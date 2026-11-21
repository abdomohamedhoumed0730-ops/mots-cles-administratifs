"""Génère la présentation de soutenance (version 2) avec python-pptx.

Usage : python slides/build_slides.py
Sortie : slides/soutenance_binome6.pptx

Les chiffres sont recopiés depuis results/ (dernier passage de make tout).
Ils ne sont pas recalculés ici : si results/ change, mettre ce fichier à jour.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

SORTIE = Path(__file__).resolve().parent / "soutenance_binome6.pptx"

# Palette : anthracite, orange brûlé, sable clair (aucune couleur du rapport PDF).
FOND = RGBColor(0xF5, 0xF3, 0xEE)
PRIMAIRE = RGBColor(0x1F, 0x23, 0x28)
ACCENT = RGBColor(0xD9, 0x62, 0x2B)
SECONDAIRE = RGBColor(0xFB, 0xE1, 0xCF)
TEXTE = RGBColor(0x1F, 0x23, 0x28)
GRIS = RGBColor(0x5B, 0x61, 0x6B)

prs = Presentation()
prs.slide_width = Emu(12192000)   # 16:9
prs.slide_height = Emu(6858000)
VIDE = prs.slide_layouts[6]


def nouvelle_diapositive(titre, sous_titre=None):
    diap = prs.slides.add_slide(VIDE)
    fond = diap.background.fill
    fond.solid()
    fond.fore_color.rgb = FOND
    bandeau = diap.shapes.add_shape(1, 0, 0, prs.slide_width, Emu(120000))
    bandeau.fill.solid()
    bandeau.fill.fore_color.rgb = ACCENT
    bandeau.line.fill.background()
    zone = diap.shapes.add_textbox(Emu(600000), Emu(380000), Emu(10900000), Emu(900000))
    cadre = zone.text_frame
    cadre.word_wrap = True
    p = cadre.paragraphs[0]
    p.text = titre
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = PRIMAIRE
    if sous_titre:
        p2 = cadre.add_paragraph()
        p2.text = sous_titre
        p2.font.size = Pt(15)
        p2.font.color.rgb = GRIS
    return diap


def ajouter_puces(diap, elements, x=600000, y=1550000, largeur=10900000, hauteur=4900000, taille=18):
    zone = diap.shapes.add_textbox(Emu(x), Emu(y), Emu(largeur), Emu(hauteur))
    cadre = zone.text_frame
    cadre.word_wrap = True
    for i, texte in enumerate(elements):
        p = cadre.paragraphs[0] if i == 0 else cadre.add_paragraph()
        p.text = "•  " + texte
        p.font.size = Pt(taille)
        p.font.color.rgb = TEXTE
        p.space_after = Pt(10)


def ajouter_tableau(diap, entetes, lignes, x=600000, y=1600000, largeur=10900000, taille=14):
    nb_l, nb_c = len(lignes) + 1, len(entetes)
    forme = diap.shapes.add_table(nb_l, nb_c, Emu(x), Emu(y), Emu(largeur), Emu(420000 * nb_l))
    tableau = forme.table
    for j, titre in enumerate(entetes):
        cellule = tableau.cell(0, j)
        cellule.text = titre
        cellule.fill.solid()
        cellule.fill.fore_color.rgb = PRIMAIRE
        for par in cellule.text_frame.paragraphs:
            par.font.bold = True
            par.font.size = Pt(taille)
            par.font.color.rgb = FOND
    for i, ligne in enumerate(lignes, start=1):
        for j, valeur in enumerate(ligne):
            cellule = tableau.cell(i, j)
            cellule.text = valeur
            cellule.fill.solid()
            cellule.fill.fore_color.rgb = SECONDAIRE if i % 2 else FOND
            for par in cellule.text_frame.paragraphs:
                par.font.size = Pt(taille)
                par.font.color.rgb = TEXTE
                if j > 0:
                    par.alignment = PP_ALIGN.CENTER
    return tableau


def pied(diap, texte):
    zone = diap.shapes.add_textbox(Emu(600000), Emu(6250000), Emu(10900000), Emu(400000))
    p = zone.text_frame.paragraphs[0]
    zone.text_frame.word_wrap = True
    p.text = texte
    p.font.size = Pt(12)
    p.font.color.rgb = GRIS


# 1. Titre
diap = prs.slides.add_slide(VIDE)
diap.background.fill.solid()
diap.background.fill.fore_color.rgb = PRIMAIRE
zone = diap.shapes.add_textbox(Emu(900000), Emu(2200000), Emu(10400000), Emu(2400000))
cadre = zone.text_frame
cadre.word_wrap = True
p = cadre.paragraphs[0]
p.text = "Extraction de mots-clés dans des documents administratifs"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = FOND
p2 = cadre.add_paragraph()
p2.text = "Peut-on proposer des mots-clés fiables pour une note administrative, et comment le mesurer ?"
p2.space_before = Pt(18)
p2.font.size = Pt(20)
p2.font.color.rgb = SECONDAIRE
p3 = cadre.add_paragraph()
p3.text = "TALN, Master 2 IAMD, Université de Djibouti. Binôme 6 : Abdo Mohamed Houmed et Magdi Ali."
p3.font.size = Pt(16)
p3.font.color.rgb = SECONDAIRE

# 2. Données et protocole
diap = nouvelle_diapositive("Données et protocole", "Un corpus synthétique, trois jeux séparés")
ajouter_tableau(
    diap,
    ["Jeu", "Notes", "Usage"],
    [
        ["Développement", "10 (N01 à N10)", "Choix des hyperparamètres"],
        ["Évaluation", "20 (N11 à N30)", "Mesure ; a guidé la conception de 2c"],
        ["Test gelé", "10 (N31 à N40)", "Mesure finale, une seule fois"],
    ],
)
ajouter_puces(
    diap,
    [
        "40 notes fictives, 36 à 67 mots, six mots-clés de référence chacune.",
        "Références rédigées par un seul auteur : limite assumée.",
        "L'IDF est appris hors notes de test. Aucune donnée personnelle réelle.",
    ],
    y=3900000,
    taille=18,
)

# 3. Méthodes
diap = nouvelle_diapositive("Quatre méthodes", "De la référence la plus simple à la plus riche")
ajouter_puces(
    diap,
    [
        "Baseline TF-IDF : mots isolés, pondérés par fréquence dans la note et rareté dans le corpus.",
        "Approche 2a : expressions de deux mots maximum, scorées par TF-IDF.",
        "Approche 2b (TextRank) : graphe de cooccurrence et PageRank, sans entraînement.",
        "Approche 2c : lemmes de noms, noms propres et adjectifs (spaCy), scorés par TF-IDF. Ajoutée après la première évaluation.",
    ],
    taille=20,
)

# 4. Mesures
diap = nouvelle_diapositive("Mesurer et conclure avec prudence")
ajouter_puces(
    diap,
    [
        "Mesure principale : F1 souple (précision et rappel), moyenné par note, à k = 5 et k = 10.",
        "Souple : l'ensemble des mots de l'une des expressions est inclus dans l'autre.",
        "Incertitude : bootstrap apparié, 2 000 tirages, intervalle à 95 %.",
        "Un écart est établi seulement si son intervalle ne contient pas zéro.",
        "Stabilité : suppression d'une phrase, coefficient de Jaccard entre les top-5.",
    ],
    taille=20,
)

# 5. Résultats test
diap = nouvelle_diapositive("Résultats sur le jeu de test gelé", "F1 souple, écart vs baseline avec intervalle à 95 %")
ajouter_tableau(
    diap,
    ["Méthode", "F1 k = 5", "Écart k = 5", "F1 k = 10", "Écart k = 10"],
    [
        ["Baseline", "0,483", "-", "0,488", "-"],
        ["2a", "0,323", "-0,161 établi", "0,407", "-0,081"],
        ["2b (TextRank)", "0,455", "-0,029", "0,621", "+0,133 établi"],
        ["2c", "0,456", "-0,027", "0,460", "-0,028"],
    ],
    taille=16,
)
pied(diap, "Intervalles complets dans le rapport. « établi » : intervalle à 95 % sans zéro.")

# 6. Résultats évaluation et point de conception
diap = nouvelle_diapositive("Sur le jeu d'évaluation, 2c semblait gagnante", "Mais ce jeu a guidé sa conception")
ajouter_tableau(
    diap,
    ["Méthode", "F1 k = 5", "Écart k = 5", "F1 k = 10", "Écart k = 10"],
    [
        ["Baseline", "0,432", "-", "0,572", "-"],
        ["2a", "0,480", "+0,048", "0,531", "-0,041"],
        ["2b (TextRank)", "0,425", "-0,007", "0,514", "-0,058"],
        ["2c", "0,499", "+0,067 établi", "0,726", "+0,153 établi"],
    ],
    taille=16,
)
ajouter_puces(
    diap,
    [
        "2c a été conçue à partir des erreurs observées sur ce jeu : le gain est optimiste.",
        "Sur le test gelé, 2c n'est pas meilleure que la baseline.",
    ],
    y=4300000,
    taille=18,
)

# 7. Stabilité et coût
diap = nouvelle_diapositive("Stabilité et coût", "Aucune méthode n'est stable face à la perte d'une phrase")
ajouter_tableau(
    diap,
    ["Méthode", "Jaccard moyen (suppression d'une phrase)", "Temps par note"],
    [
        ["Baseline", "0,64", "2,3 ms"],
        ["2a", "0,67", "9,5 ms"],
        ["2b (TextRank)", "0,60", "3,1 ms"],
        ["2c", "0,64", "20,3 ms"],
    ],
    taille=16,
)
pied(diap, "Contrôle par mélange d'ordre : 1,00 pour toutes, par construction (c'est un contrôle, non une preuve).")

# 8. Analyse d'erreurs
diap = nouvelle_diapositive("Analyse d'erreurs", "Cas réels relevés dans les fichiers de sortie")
ajouter_puces(
    diap,
    [
        "Mots génériques : « heures » (N11, baseline), « annexe » (N20).",
        "Nombres : « 400 » tiré de « 400 000 francs djiboutiens » (N24, baseline).",
        "Référence absente : « maintenance des climatiseurs » (N14, baseline et 2b).",
        "Nom de personne : « hassan » (N21, 2c, rang 5). Filtrage à décider avant tout usage réel.",
        "Lemmatisation : « ressource humain » (N31, 2c), « fich » pour « fiche ».",
        "Polysémie : « cours » (N31) et « compte » (N33), en 2c sur le test.",
    ],
    taille=18,
)

# 9. Ce qui est fait et ce qui reste
diap = nouvelle_diapositive("Ce qui est fait, ce qui reste")
ajouter_puces(
    diap,
    [
        "Fait : protocole sans fuite, intervalles de confiance, 61 tests (60 réussis, 1 attendu en échec), chaîne reproductible (make tout).",
        "Fait : analyse d'erreurs documentée, limites écrites, journal des versions.",
        "Reste : évaluation humaine aveugle (20 notes, 396 lignes), non réalisée à ce jour.",
        "Reste : données réelles, si l'administration l'autorise, et exclusion des noms de personnes.",
    ],
    taille=18,
)

# 10. Conclusion
diap = nouvelle_diapositive("Conclusion")
ajouter_puces(
    diap,
    [
        "Sur le test gelé, aucune méthode ne bat nettement la baseline à k = 5.",
        "TextRank est nettement meilleure à k = 10 : seul résultat établi sur le test à ce seuil.",
        "2c, meilleure sur l'évaluation, ne se confirme pas sur le test. Nous le disons.",
        "Un jury doit retenir des conclusions modestes et vérifiables plutôt qu'un gagnant fragile.",
    ],
    taille=20,
)

prs.save(SORTIE)
print(f"Présentation écrite : {SORTIE} ({len(prs.slides)} diapositives)")
