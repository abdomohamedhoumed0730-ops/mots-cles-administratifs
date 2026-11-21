# Guide 01 · Installer le projet sur votre ordinateur

**Objectif.** Avoir le projet qui tourne chez vous, avec toutes les dépendances.

## Ce qu'il vous faut
- Python 3.11 (3.10 ou 3.12 fonctionnent probablement, mais 3.11 est celui de la chaîne d'intégration).
- Le dossier du projet (le zip décompressé).
- Une connexion internet pour la première installation.

## Étapes

1. **Ouvrir un terminal dans le dossier du projet.**
   - Windows : ouvrez le dossier dans l'Explorateur, tapez `cmd` dans la barre d'adresse, Entrée.
   - macOS / Linux : clic droit sur le dossier, « Ouvrir dans le terminal ».

2. **Créer un environnement isolé (recommandé).**
   ```bash
   python -m venv .venv
   ```
   Activez-le :
   - Windows : `.venv\Scripts\activate`
   - macOS / Linux : `source .venv/bin/activate`

   Le début de la ligne de commande doit afficher `(.venv)`.

3. **Installer les dépendances de développement.**
   ```bash
   pip install -r requirements-dev.txt
   ```
   Cette commande installe aussi le modèle spaCy français, grâce à la ligne du fichier `requirements.txt`.

4. **Vérifier l'installation.**
   ```bash
   python -c "import spacy, streamlit, sklearn; print('OK')"
   ```
   Vous devez voir `OK`.

## Vérification
Le message `OK` s'affiche, sans erreur rouge.

## En cas de problème
- **« pip n'est pas reconnu »** : utilisez `python -m pip install -r requirements-dev.txt`.
- **Erreur sur `fr_core_news_sm`** : lancez `python -m spacy download fr_core_news_sm`.
- **Erreur de compilation sous Windows** : installez la version à jour de Python depuis python.org, puis recommencez dans un nouveau `.venv`.
