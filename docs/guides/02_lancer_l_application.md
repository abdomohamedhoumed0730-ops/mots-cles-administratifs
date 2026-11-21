# Guide 02 · Lancer l'application en local

**Objectif.** Voir l'application Streamlit tourner dans votre navigateur.

## Prérequis
Guide 01 terminé, environnement `.venv` activé.

## Étapes

1. Dans le dossier du projet, lancez :
   ```bash
   make streamlit
   ```
   Sans `make` (Windows, par exemple) :
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. Ouvrez votre navigateur à l'adresse affichée, en général **http://localhost:8501**.

3. Testez les trois sources :
   - **Note du corpus** : choisissez une note, cliquez sur « Extraire les mots-clés ». Un tableau de mesure apparaît.
   - **Coller un texte** : collez une note, cliquez sur « Extraire les mots-clés ». Les résultats sont dans quatre onglets (Mots-clés, Comparaison, Mesure, Méthodes et limites). Sans référence, l'onglet Mesure indique qu'aucune mesure n'est affichée : c'est normal.
   - **Charger un fichier .txt** : chargez un fichier UTF-8.

4. Pour arrêter le serveur, revenez au terminal et appuyez sur **Ctrl + C**.

## Vérification
- La page affiche le bandeau vert, la barre latérale, et un tableau après le clic.
- Le terminal ne montre pas de ligne rouge « Traceback ».

## En cas de problème
- **Page blanche ou erreur à l'ouverture** : relancez `make streamlit` et attendez la fin du chargement (la première fois, le modèle spaCy prend quelques secondes).
- **Port 8501 déjà utilisé** : `streamlit run app/streamlit_app.py --server.port 8502`.
- **Le navigateur ne s'ouvre pas** : ouvrez l'adresse à la main.
