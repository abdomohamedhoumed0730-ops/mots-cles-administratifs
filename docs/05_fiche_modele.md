# 5. Fiche des méthodes (*model card*)

Format inspiré des « model cards ». Ces méthodes ne sont pas des modèles entraînés au sens strict :
ce sont des procédures à faible apprentissage (IDF, PageRank, lemmatisation pré-entraînée).

## 5.1 Vue d'ensemble

| Méthode | Principe | Apprentissage | Paramètre retenu |
|---|---|---|---|
| Baseline TF-IDF | score TF-IDF des mots isolés | IDF sur le corpus hors test | — |
| Approche 2a | candidats = suites de mots non vides, scorés par TF-IDF | IDF sur candidats | longueur max 2 |
| Approche 2b (TextRank) | graphe de cooccurrence + PageRank | aucun | fenêtre 3 |
| Approche 2c | lemmes de noms, noms propres et adjectifs, scorés par TF-IDF | IDF + modèle spaCy `fr_core_news_sm` | longueur max 2 |

## 5.2 Usage prévu

- Proposer des mots-clés candidats pour une note administrative, à valider par un humain.
- Servir de base de comparaison pour de futures méthodes.

## 5.3 Usages non prévus

- Classement automatique sans validation humaine.
- Traitement de données personnelles réelles sans analyse d'impact.
- Décisions administratives ou juridiques.
- Documents hors français, ou fortement scannés (aucune gestion de l'OCR).

## 5.4 Résultats (F1 souple, moyenne par note, avec intervalle à 95 % vs baseline)

Les intervalles sont obtenus par bootstrap apparié sur les notes (2 000 tirages).

**Jeu de test gelé (10 notes)**

| Méthode | F1 k=5 | F1 k=10 | Écart vs baseline, k=5 | Écart vs baseline, k=10 |
|---|---|---|---|---|
| Baseline | 0,483 | 0,488 | — | — |
| 2a | 0,323 | 0,407 | −0,161 [−0,275 ; −0,047] **établi** | −0,081 [−0,164 ; +0,003] |
| 2b | 0,455 | 0,621 | −0,029 [−0,239 ; +0,162] | +0,133 [+0,021 ; +0,236] **établi** |
| 2c | 0,456 | 0,460 | −0,027 [−0,163 ; +0,127] | −0,028 [−0,098 ; +0,064] |

**Jeu d'évaluation (20 notes, a guidé la conception de 2c)**

| Méthode | F1 k=5 | F1 k=10 | Écart vs baseline, k=5 | Écart vs baseline, k=10 |
|---|---|---|---|---|
| Baseline | 0,432 | 0,572 | — | — |
| 2a | 0,480 | 0,531 | +0,048 [−0,032 ; +0,120] | −0,041 [−0,088 ; +0,008] |
| 2b | 0,425 | 0,514 | −0,007 [−0,104 ; +0,089] | −0,058 [−0,138 ; +0,019] |
| 2c | 0,499 | 0,726 | +0,067 [+0,003 ; +0,128] **établi** | +0,153 [+0,089 ; +0,216] **établi** |

**Lecture.** Sur le jeu gelé, aucune méthode ne domine la baseline de manière robuste.
Les deux écarts établis sur le test ne sont pas confirmés sur eval : 2a à k=5 est même légèrement
meilleure sur eval (+0,048, non établi) alors qu'elle est nettement moins bonne sur test ;
2b à k=10 est légèrement moins bonne sur eval (−0,058, non établi) alors qu'elle est meilleure sur test.
Le gain de 2c sur eval est optimiste : cette méthode a été conçue à partir des erreurs de ce jeu.
Avec douze comparaisons et dix notes de test, quelques écarts « établis » peuvent être dus au hasard.

## 5.5 Stabilité

Suppression d'une phrase au hasard, Jaccard moyen entre les top-5 :
baseline 0,64 ; 2a 0,67 ; 2b 0,60 ; 2c 0,64 (minimum 0,11 pour 2c).
Aucune méthode n'est stable face à une perte d'information. Le contrôle par mélange d'ordre donne 1,00
pour les quatre méthodes, comme attendu.

## 5.6 Coût

Temps moyen par note, machine de travail : baseline 2,3 ms, 2b 3,1 ms, 2a 9,5 ms, 2c 20,3 ms.
Tous les coûts sont négligeables pour une note administrative.

## 5.7 Limites connues

- **Erreurs de lemmatisation (2c).** « fiche » devient « fich », « ressources humaines » devient
  « ressource humain ». Le modèle `fr_core_news_sm` est le plus léger de spaCy.
- **Ambiguïté grammaticale (2c).** « cours » (formation ou cours d'eau), « compte » (compte rendu). Sur le test, 2c retient « cours » (N31) et « compte » (N33).
- **Noms de personnes.** Un nom propre est retenu comme mot-clé (« hassan »). Pour un archivage réel,
  il faut décider d'exclure les noms de personnes : c'est une question de confidentialité.
- **Expressions coupées (2a, 2c).** « guichet de paiement » ne peut pas sortir en entier, car « de »
  est un mot vide.
- **Nombres (2a, 2b).** Les montants et numéros peuvent être retenus. Le filtre de 2c les exclut.
- **Normalisation.** La règle qui retire le « s » ou le « x » final transforme « prix » en « pri ». Elle
  est appliquée aux deux côtés de la comparaison, donc sans effet sur les écarts, mais elle reste une
  approximation (test marqué `xfail`).

## 5.8 Risques et biais

- **Biais de référence.** Les mots-clés de référence sont écrits par un seul auteur, donc ils reflètent
  son découpage du sujet. Une évaluation humaine indépendante est prévue (voir `docs/08_checklist`).
- **Biais de sélection.** Le corpus est synthétique et régulier. Les performances sur de vraies notes
  (fautes, scans, tableaux) seront probablement plus basses.
- **Confidentialité.** Le corpus ne contient pas de données personnelles réelles, mais l'extraction
  sur de vraies notes peut faire remonter des noms, des montants ou des données sensibles.
  Un filtrage est nécessaire avant tout usage réel.

## 5.9 Surveillance et maintenance

Pour un usage réel, il faudrait : rejouer `make tout` après chaque changement de données, suivre
la précision humaine sur un échantillon régulier, et tenir à jour la liste de mots vides et des noms
à exclure.
