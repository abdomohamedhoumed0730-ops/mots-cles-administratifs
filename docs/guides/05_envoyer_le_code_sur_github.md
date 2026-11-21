# Guide 05 · Envoyer le code sur GitHub

**Objectif.** Copier le projet local sur GitHub, avec un historique.

## Prérequis
- Guide 04 terminé : vous avez l'adresse du dépôt.
- Git installé (`git --version` doit afficher une version).

## Étapes

1. Dans le dossier du projet, première fois seulement, configurez votre identité :
   ```bash
   git config --global user.name "Votre Nom"
   git config --global user.email "votre-email@exemple.com"
   ```

2. Initialisez le dépôt local et faites le premier enregistrement :
   ```bash
   git init
   git add .
   git status
   ```
   **Relisez la liste `git status`.** Elle ne doit contenir ni `cle_methodes_PRIVEE.csv`, ni `formulaire_evaluation_humaine.csv`, ni `.venv`. Si l'un d'eux apparaît, ne continuez pas : vérifiez le `.gitignore`.

3. Enregistrez :
   ```bash
   git commit -m "Version 4 : application Streamlit et documentation"
   ```

4. Reliez au dépôt GitHub (remplacez l'adresse par la vôtre) :
   ```bash
   git branch -M main
   git remote add origin https://github.com/votre-nom/mots-cles-administratifs.git
   git push -u origin main
   ```
   Git peut demander de vous connecter : suivez la fenêtre qui s'ouvre, ou utilisez un jeton personnel si GitHub le demande.

## Vérification
Rafraîchissez la page du dépôt sur GitHub : les dossiers `app`, `src`, `data`, `docs` et les fichiers `requirements.txt` et `README.md` sont visibles.

## En cas de problème
- **« Permission denied » ou demande de mot de passe** : GitHub n'accepte plus le mot de passe seul. Créez un jeton dans Settings › Developer settings › Personal access tokens, et utilisez-le à la place du mot de passe.
- **Le dépôt contient des fichiers inutiles** : `git rm --cached -r .venv`, puis un nouveau commit.
