# 7. Guide pour répondre au jury

Ce guide sert à préparer les questions, pas à les réciter. Pour chaque réponse, la question est de
savoir *pourquoi* on répond ainsi, et où se trouve la preuve dans `results/`.

Les chiffres cités viennent de la dernière exécution (`make tout`). Si les données changent, relire ce guide.

---

## 1. Résumé de l'argument en trente secondes

Nous cherchons 5 à 10 mots-clés pour une note administrative. Nous comparons quatre méthodes,
avec des jeux séparés pour régler, mesurer et conclure. Sur le jeu de test gelé, aucune méthode ne
bat nettement la baseline à k = 5, et TextRank est nettement meilleure à k = 10. Nos conclusions sont
donc prudentes, et nous les présentons avec leurs intervalles de confiance.

---

## 2. Questions sur le problème et la méthode

**Q : Pourquoi une baseline TF-IDF ?**
R : Elle est simple, rapide (2 ms par note) et facile à expliquer. Une méthode plus complexe doit
faire mieux qu'elle pour être justifiée. C'est précisément la question que notre test pose.

**Q : Qu'est-ce qu'un mot-clé, concrètement ?**
R : Une expression courte qui résume le sujet. « demande de congé annuel » en est un ; « annuel » seul
est moins utile. Voir le glossaire, `01_objectif_et_glossaire.md`.

**Q : Expliquez TF-IDF simplement.**
R : Un mot est important s'il revient souvent dans la note et rarement dans les autres notes.
Le score est le produit de la fréquence (TF) et de la rareté (IDF).

**Q : Comment fonctionne TextRank ?**
R : On construit un graphe où les mots sont reliés s'ils apparaissent près l'un de l'autre. On applique
PageRank : un mot est important s'il est lié à des mots importants. Il ne demande aucun entraînement.

**Q : Que fait la lemmatisation, et pourquoi l'utiliser ?**
R : Elle ramène un mot à sa forme de base (« étudiants » devient « étudiant »). Elle permet de comparer
des formes différentes. Elle a des limites : spaCy transforme parfois « fiche » en « fich ».

**Q : Pourquoi filtrer les noms, noms propres et adjectifs ?**
R : Ce sont surtout eux qui portent le sujet d'une note. Le filtre écarte les nombres et les verbes
conjugués, qui étaient des erreurs fréquentes dans la première version.

---

## 3. Questions sur les données

**Q : Pourquoi des données synthétiques ?**
R : Aucun document réel n'était fourni, et les documents administratifs contiennent des données
personnelles. Le corpus est fictif, sans données personnelles, et la validation automatique le vérifie.

**Q : Qui a écrit les références ?**
R : Nous, sans double annotation. C'est une limite : un mot-clé raisonnable absent de la liste est
compté comme une erreur. Nous avons prévu une évaluation humaine aveugle ; dites honnêtement si elle
n'est pas encore faite.

**Q : Pourquoi trois jeux (dev, eval, test) ?**
R : Le développement sert à régler les paramètres, l'évaluation à mesurer, le test à conclure.
Si l'on règle sur le test, le score est optimiste. C'est une fuite.

**Q : Pourquoi l'évaluation a-t-elle guidé la conception de 2c, et pourquoi cela pose-t-il problème ?**
R : Nous avons vu les erreurs de la version 1 sur ce jeu, et nous avons conçu un filtre pour les corriger.
Les résultats sur ce jeu sont donc optimistes. Le jeu de test, rédigé après la conception, est le
seul juge. Il ne confirme pas le gain de 2c. Nous le disons.

**Q : Pourquoi 40 notes seulement ?**
R : Le corpus a été créé pour ce projet. C'est une limite majeure. Les intervalles
de confiance sont larges, et nous les montrons.

---

## 4. Questions sur les résultats

**Q : Quelle est la meilleure méthode ?**
R : Ça dépend du jeu et de k. Sur le test à k = 5, aucune ne bat nettement la baseline. Sur le test à
k = 10, TextRank est nettement meilleure (+0,133, intervalle entre +0,021 et +0,236). Il n'y a pas de
gagnant unique et robuste. C'est la réponse honnête.

**Q : Que signifie « écart établi » ?**
R : Un écart est établi si son intervalle de confiance à 95 % ne contient pas zéro. L'intervalle
est obtenu par bootstrap apparié : on rééchantillonne les notes 2 000 fois.

**Q : Votre écart de 0,05 est-il significatif ?**
R : Pas au sens strict. Sur 10 ou 20 notes, les intervalles sont larges. Un écart de cet ordre
est une tendance.

**Q : Pourquoi l'approche 2c paraît-elle meilleure sur un jeu et pas sur l'autre ?**
R : Parce que la différence vient en partie du hasard d'un petit échantillon, et en partie de la
conception. Le jeu de test est le seul juge fiable ici, et il n'est pas favorable à 2c.

**Q : Pourquoi la correspondance souple ?**
R : Une baseline à mots isolés ne peut pas produire une expression entière. La stricte la pénaliserait
mécaniquement. Nous publions les deux, et la souple est la mesure principale.

**Q : Vos scores de stabilité sont-ils bons ?**
R : Non. Supprimer une seule phrase change en moyenne environ un tiers des mots-clés (Jaccard entre
0,60 et 0,67). Le contrôle par mélange d'ordre donne 1,00, mais ce n'est qu'un contrôle : TF-IDF
ne dépend pas de l'ordre.

**Q : Quelle est l'erreur la plus fréquente ?**
R : Le bruit lexical : verbes participes (« approuvé »), mots génériques (« heures », « annexe »),
et pour 2a, 2b et la baseline les nombres (« 400 », « 400 000 francs djiboutiens »). La lemmatisation de 2c produit ses propres erreurs.

---

## 5. Questions sur le code et la reproductibilité

**Q : Comment reproduire vos résultats ?**
R : `make install`, puis `make tout`. Tout est dans le dépôt : données, code, tests, résultats.

**Q : Comment savez-vous que les données n'ont pas changé ?**
R : Le fichier `data/MANIFEST.json` contient l'empreinte SHA-256. La validation vérifie qu'elle est
enregistrée et le test de données la contrôle.

**Q : Comment vous assurez-vous qu'un changement ne modifie pas les résultats publiés ?**
R : Le test de non-régression (`tests/test_non_regression.py`) fixe les scores de la version 1.
Si un changement les modifie, le test échoue.

**Q : Pourquoi pas de modèle de langage ?**
R : Le sujet valorise la rigueur, pas la taille. Un grand modèle demanderait des téléchargements
non garantis et rendrait les résultats plus difficiles à expliquer.

**Q : Votre code est-il prêt pour la production ?**
R : Non. Nous le disons clairement. Il manque un service web, une surveillance de la précision et un
filtrage des noms de personnes. Voir `03_methodologie.md`, section 3.7.

---

## 6. Questions sur la confidentialité

**Q : Le système pourrait-il retenir des noms de personnes ?**
R : Oui. Dans la version 2c, « hassan » a été retenu comme mot-clé. Pour un archivage réel, il faudrait
exclure les noms propres de personnes. C'est une décision à prendre avec l'administration.

**Q : Pourquoi ne pas utiliser de vraies notes ?**
R : Parce que les données personnelles et la confidentialité rendent leur usage impossible sans
autorisation et analyse d'impact.

---

## 7. Erreurs à éviter pendant la soutenance

- Dire que le système « comprend » le sens. Il compte, il relie, il lemmatise.
- Présenter 0,50 comme une précision garantie.
- Affirmer qu'une méthode est meilleure sans citer son intervalle.
- Affirmer que 2c est la meilleure méthode. Le jeu de test ne le confirme pas.
- Lire les diapositives au lieu d'expliquer les chiffres.
- Ne pas savoir répondre « nous ne savons pas ». C'est une réponse acceptable, à condition de dire
  comment on le vérifierait.

---

## 8. Un dernier conseil

Un jury préfère une conclusion modeste et bien justifiée à une conclusion spectaculaire et fragile.
Si une question vous surprend, reformulez-la, donnez l'hypothèse que vous retenez, et dites comment
la vérifier.
