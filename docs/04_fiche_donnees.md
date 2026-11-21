# 4. Fiche de données

Format inspiré des « datasheets for datasets ». Public : étudiants, jury, quiconque réutilise le jeu.

## 4.1 Identité

- **Nom.** `corpus_notes_administratives.json`
- **Version.** 2 (40 notes). La version 1 comptait 30 notes ; les 10 notes du test ont été ajoutées ensuite.
- **Empreinte.** SHA-256 dans `data/MANIFEST.json`, recalculée par `src/valider_donnees.py`.
- **Langue.** Français.
- **Licence.** Rédigé pour ce projet, sans source externe. Réutilisable dans le cadre du module.

## 4.2 Origine et méthode de création

- **Provenance.** Aucun document administratif réel n'était fourni. Les notes ont été rédigées
  pour ce projet, en imitant les genres courants : note de service, convocation, avis de paiement,
  demande, procès-verbal, circulaire.
- **Données personnelles.** Aucune. Les noms de personnes qui apparaissent dans les notes sont fictifs. Montants, dates et numéros de dossier sont inventés. Le contrôle automatique vérifie
  l'absence d'e-mail, de numéro de téléphone et d'IBAN.
- **Sensibilité.** Le corpus évite les informations de santé. La note N31 (congé) a été reformulée
  pour cela : le motif est « raison personnelle ».

## 4.3 Contenu et structure

| Champ | Type | Contenu |
|---|---|---|
| `id` | texte | N01 à N40 |
| `split` | texte | `dev` (N01-N10), `eval` (N11-N30), `test` (N31-N40) |
| `titre` | texte | titre court de la note |
| `texte` | texte | corps de la note, de 36 à 67 mots |
| `mots_cles_reference` | liste de 6 textes | mots-clés de référence, rédigés par l'auteur |

## 4.4 Rôle de chaque jeu

| Jeu | Notes | Usage autorisé |
|---|---|---|
| dev | 10 | choix des hyperparamètres |
| eval | 20 | mesure ; a aussi guidé la conception de l'approche 2c |
| test | 10 | mesure finale, une seule fois, jamais pour choisir |

## 4.5 Qualité et limites connues

- **Annotation.** Les références ont été rédigées par un seul auteur, sans double annotation.
  Un mot-clé raisonnable absent de la liste est compté comme une erreur. Cela sous-estime les méthodes.
- **Représentativité.** Les notes sont plus régulières qu'une vraie archive : pas de fautes de saisie,
  pas de scans, pas de tableaux, pas d'en-têtes répétés.
- **Taille.** Quarante notes ne suffisent pas pour des conclusions robustes. Les intervalles de
  confiance sont larges (voir `results/intervalles_confiance.csv`).
- **Couverture.** Une référence peut être une forme dérivée absente du texte (« rattrapage » pour
  « rattraper »). La validation le signale comme avertissement.

## 4.6 Validation automatique (résultat du dernier passage)

- Statut : PASS, 40 notes, 0 avertissement.
- Les contrôles sont décrits dans `src/valider_donnees.py` et rejoués par `tests/test_donnees.py`.

## 4.7 Utilisation recommandée

- Démontrer une méthode de mots-clés, comparer des méthodes, enseigner l'évaluation.
- Ne pas utiliser pour juger des performances sur de vraies archives.
- Pour un usage réel, remplacer le fichier et relancer `make tout`.
