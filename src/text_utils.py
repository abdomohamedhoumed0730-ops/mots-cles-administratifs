"""Outils de prétraitement du texte (français).

Ce module ne fait que préparer le texte : il ne choisit aucun mot-clé.
"""
import re
import unicodedata

# Liste de mots vides français (écrite à la main, volontairement courte et lisible).
# Un mot vide est un mot très fréquent qui porte peu de sens à lui seul
# (articles, prépositions, pronoms...).
MOTS_VIDES_FR = set("""
a au aux avec ce ces cet cette ceci cela ça celui celle ceux celles dans de des du
elle elles en entre et eux il ils je j l la le les leur leurs lui ma mais me même
mes moi mon ne ni nos notre nous on ou où par pas pour qu que quel quelle quels
quelles qui sa sans se ses si son sont sur ta te tes toi ton tu un une vos votre
vous y est être été sera seront sont était étaient avoir a ont avait ont fait
faire plus moins très aussi alors donc car comme dont lors leurs chaque tout tous
toute toutes autre autres après avant depuis pendant sous vers chez selon ainsi
peut peuvent doit doivent doit cela cet cette ici là
""".split())

# Mots très fréquents dans les documents administratifs mais peu discriminants.
# Ils sont retirés uniquement pour les candidats mots-clés, pas pour l'évaluation.
MOTS_ADMIN_GENERIQUES = set("""
objet merci bien ci dessous présente présent présentes note notes date
""".split())

MOTS_VIDES = MOTS_VIDES_FR | MOTS_ADMIN_GENERIQUES

_TOKEN_RE = re.compile(r"[a-zàâçéèêëîïôûùüÿœæ0-9]+")


def minuscules(texte: str) -> str:
    """Passe en minuscules et remplace les apostrophes par des espaces.

    Exemple : "d'achat" devient "d achat". Les formes élidées sont ainsi séparées.
    """
    return texte.lower().replace("’", " ").replace("'", " ")


def tokens(texte: str) -> list[str]:
    """Découpe un texte en mots (sans ponctuation), en minuscules."""
    return _TOKEN_RE.findall(minuscules(texte))


def tokens_candidats(texte: str) -> list[str]:
    """Mots utilisables comme mots-clés : pas de mots vides, au moins 3 lettres."""
    return [t for t in tokens(texte) if t not in MOTS_VIDES and len(t) >= 3]


def decouper_phrases(texte: str) -> list[str]:
    """Découpe grossière en phrases (point, point-virgule, deux-points, saut de ligne)."""
    morceaux = re.split(r"[.;:!?\n]+", texte)
    return [m.strip() for m in morceaux if m.strip()]


def retirer_accents(texte: str) -> str:
    """Supprime les accents : 'congé' devient 'conge'."""
    decompose = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in decompose if not unicodedata.combining(c))


def forme_normalisee(mot: str) -> str:
    """Forme simple pour la comparaison : minuscules, sans accent, pluriel 's' ou 'x' retiré.

    C'est un 'stemming' très simplifié, suffisant pour rapprocher 'courrier'/'courriers'.
    Ce n'est pas une lemmatisation complète, et cela doit être dit dans le rapport.
    """
    mot = retirer_accents(mot.lower())
    if len(mot) > 3 and mot[-1] in "sx":
        mot = mot[:-1]
    return mot


def ensemble_mots_matching(expression: str) -> frozenset:
    """Ensemble de formes normalisées (sans mots vides) d'une expression, pour l'évaluation."""
    mots = [forme_normalisee(t) for t in tokens(expression) if t not in MOTS_VIDES_FR]
    return frozenset(m for m in mots if len(m) >= 2)
