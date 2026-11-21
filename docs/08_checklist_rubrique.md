# 8. Checklist : grille du jury et ce qui reste à faire

Cette page confronte le projet à la grille de notation de 20 points (sujet de projet).
Pour chaque critère : ce qui est fait, la preuve, et ce qui manque encore.

**Légende.** ✅ fait et prouvé · 🟡 partiel · ❌ à faire (par le binôme).

## 8.1 Tableau récapitulatif

| Critère (points) | État | Preuve dans le projet | Ce qui manque |
|---|---|---|---|
| Problématique et cadrage (2) | ✅ | `docs/01`, section 1 | rien |
| Données et qualité (3) | 🟡 | `docs/04`, `valider_donnees.py`, empreinte SHA-256 | données réelles fournies par l'enseignant, si elles existent ; sinon, justifier le choix synthétique devant le jury |
| Baseline et méthodologie (3) | ✅ | `methods.py`, `docs/03`, dev/eval/test | rien |
| Modèle / approche améliorée (3) | 🟡 | trois approches améliorées dont une ajoutée après coup (D6) | le binôme doit savoir expliquer pourquoi 2c a été ajoutée et ce que le test gelé montre |
| Évaluation quantitative (3) | 🟡 | tableaux, IC bootstrap, jeu de test gelé | **évaluation humaine réelle** (❌, voir 8.2) |
| Analyse d'erreurs et limites (2) | ✅ | `results/erreurs_par_document.csv`, `docs/05`, rapport | rien |
| Reproductibilité et code (2) | ✅ | README, `requirements.txt`, `Makefile`, 61 tests, CI | exécuter `make install` puis `make tout` sur une machine propre |
| Présentation et démonstration (2) | 🟡 | diapositives, `demo_mots_cles.py`, `docs/07` | répétition chronométrée (❌, voir 8.2) |

**Score estimé si tout est fait :** 20/20. **Score aujourd'hui :** une grande partie est acquise ;
les deux points ouverts sont l'évaluation humaine et la répétition de la soutenance.

## 8.2 Ce qui reste à faire, par ordre de priorité

1. **❌ Évaluation humaine (critique).** Le formulaire est prêt : `make formulaire`.
   Le binôme annote 20 notes, soit 396 lignes, en mettant 1 ou 0 dans la colonne `pertinent`.
   Compter environ une heure. Puis `python src/annotation_humaine.py analyser`.
   Le résultat doit être ajouté au rapport : **sans lui, le rapport dit que l'évaluation humaine reste à faire**.
2. **❌ Répétition de la soutenance.** Trois répétitions chronométrées : 10 min de présentation,
   3 min de démonstration, 5 min de questions, 2 min de transition. Vérifier que chaque membre du
   binôme peut expliquer toutes les sections, pas seulement la sienne.
3. **❌ Maîtrise des notions.** Relire `docs/01` (glossaire) et `docs/07` (questions du jury) et
   répondre à voix haute à chaque question sans regarder.
4. **❌ Vérifier les noms et la date dans le rapport**, et les consignes exactes de l'enseignant
   (format, nombre de pages, emplacement du dépôt).
5. **❌ Installation sur une machine propre.** `make install`, puis `make tout`. Noter les difficultés.
6. **🟡 Données réelles.** Si l'enseignant fournit de vrais documents, remplacer le corpus, relancer
   `make tout`, et mettre à jour les chiffres. Ne pas mélanger les anciens et les nouveaux.
7. **🟡 Exécuter la CI.** Pousser le dépôt sur GitHub pour vérifier que le workflow passe.

## 8.3 Ce qui est acquis et démontrable

- Une question claire, un périmètre réaliste.
- Un protocole sans fuite : dev pour choisir, eval pour mesurer, test gelé pour conclure.
- Un test de non-régression qui empêche de changer un résultat publié sans le savoir.
- Des écarts présentés avec leur incertitude, et une conclusion qui n'est pas plus forte que les données.
- Une analyse d'erreurs qui cite des cas réels, avec leur cause probable.
- Une chaîne reproductible et documentée.

## 8.4 Ce qu'il faut assumer devant le jury

- La variante 2c a été ajoutée après une première évaluation. Le test gelé montre qu'elle n'apporte
  pas de gain robuste. C'est une bonne nouvelle pour la méthode : elle montre la discipline du protocole.
- Le corpus est synthétique et les références ont un seul auteur.
- Les écarts entre méthodes sont souvent du même ordre que l'incertitude.
