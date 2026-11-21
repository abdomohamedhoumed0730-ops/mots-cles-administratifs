# Guide 08 · Annoter les 20 notes (évaluation humaine)

**Objectif.** Mesurer la précision des méthodes avec un jugement humain, sans savoir quelle méthode a produit quel mot. C'est la seule partie du projet qu'aucun programme ne peut faire à votre place.

## Principe
Pour chaque note, vous voyez une liste de mots-clés proposés par les méthodes, dans un ordre mélangé. Vous indiquez pour chacun s'il est **pertinent (1)** ou **non pertinent (0)**. La clé, qui dit quelle méthode a produit quoi, reste cachée jusqu'à la fin.

## Étapes

1. **Générer le formulaire.** Dans le dossier du projet :
   ```bash
   make formulaire
   ```
   Cela crée `results/formulaire_evaluation_humaine.csv` (396 lignes) et `results/documents_a_annoter.md`.

2. **Lire les consignes.** Ouvrez `results/documents_a_annoter.md`. Il contient les 20 notes (10 du jeu de test, 10 du jeu d'évaluation) et la consigne de notation.

3. **Annoter.** Ouvrez `results/formulaire_evaluation_humaine.csv` dans Excel ou LibreOffice. Pour chaque ligne, remplissez la colonne **pertinent** avec **1** ou **0**. Règle simple : un mot-clé est pertinent s'il décrit le sujet de la note, même s'il ne figure pas dans les références.

4. **Ne rien toucher d'autre.** Les autres colonnes servent au calcul. Ne triez pas le fichier et ne supprimez aucune ligne.

5. **Enregistrer** au format CSV (UTF-8 si le logiciel le demande).

6. **Calculer le résultat** :
   ```bash
   python src/annotation_humaine.py analyser
   ```
   Le résultat s'affiche et est écrit dans `results/resultats_evaluation_humaine.csv`.

## Vérification
- Les 396 lignes ont une valeur 0 ou 1 dans la colonne **pertinent**. Aucune case vide.
- La commande d'analyse se termine sans erreur et affiche une précision par méthode.

## Honnêteté
- Annotez **sans** ouvrir `results/cle_methodes_PRIVEE.csv`. Ce fichier révèle quelle méthode a produit chaque mot. Il est exclu de GitHub : gardez-le ainsi.
- Si vous hésitez, ne forcez pas : notez 0 et signalez dans le rapport le nombre de cas douteux.
- Reportez le résultat dans le rapport, à la section « Limites ». Un résultat humain annoncé est une force ; un résultat omis est une faiblesse.

## En cas de problème
- **Accents cassés à l'ouverture** : dans LibreOffice, utilisez « Données » › « Importer », encodage UTF-8.
- **Erreur à l'analyse** : une case est vide ou contient autre chose que 0 ou 1. Corrigez et relancez.
