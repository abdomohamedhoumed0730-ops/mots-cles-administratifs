# Guide 04 · Créer le dépôt GitHub

**Objectif.** Avoir une adresse GitHub où le code est stocké, nécessaire pour le déploiement.

## Prérequis
- Un compte GitHub (gratuit). Si vous n'en avez pas : github.com, « Sign up ».

## Étapes

1. Connectez-vous à **github.com**.
2. Cliquez sur le **+** en haut à droite, puis **New repository**.
3. Remplissez :
   - **Repository name** : `mots-cles-administratifs` (sans espaces).
   - **Visibility** : **Public** (indispensable pour le déploiement gratuit sur Streamlit Community Cloud).
   - **Ne cochez rien** d'autre : pas de README, pas de .gitignore, pas de licence (le projet en contient déjà).
4. Cliquez sur **Create repository**.
5. Gardez la page ouverte : elle affiche l'adresse du dépôt, du type `https://github.com/votre-nom/mots-cles-administratifs.git`.

## Vérification
La page du dépôt vide s'affiche, avec le titre `mots-cles-administratifs`.

## Important : ce qui ne doit pas être publié
Le fichier `.gitignore` exclut déjà la clé de l'évaluation humaine (`results/cle_methodes_PRIVEE.csv`) et le formulaire rempli. Ne les retirez pas de cette liste avant la soutenance.
