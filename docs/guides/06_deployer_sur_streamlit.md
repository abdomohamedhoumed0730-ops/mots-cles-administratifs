# Guide 06 · Déployer sur Streamlit Community Cloud

**Objectif.** Obtenir une adresse publique (du type `https://…streamlit.app`) pour l'application.

## Prérequis
- Guide 05 terminé : le code est sur GitHub, dans la branche `main`.
- Dépôt **public** (guide 04).

## Étapes

1. Allez sur **share.streamlit.io**.
2. Cliquez sur **Sign in** et connectez-vous **avec votre compte GitHub** (le même que celui du dépôt).
3. Autorisez Streamlit à lire vos dépôts, si GitHub le demande.
4. Cliquez sur **Create app** (ou **New app**), puis sur l'option **Deploy a public app from GitHub** (le libellé peut légèrement varier).
5. Remplissez le formulaire :
   - **Repository** : `votre-nom/mots-cles-administratifs`
   - **Branch** : `main`
   - **Main file path** : `app/streamlit_app.py` (exactement ce chemin)
   - **App URL** (facultatif) : choisissez un nom court, par exemple `mots-cles-administratifs`.
6. Cliquez sur **Advanced settings**. Si l'option existe, choisissez **Python 3.11**.
7. Cliquez sur **Deploy**.
8. Attendez l'installation : elle peut prendre plusieurs minutes, car elle télécharge spaCy et le modèle français. Un journal défile : c'est normal.

## Vérification
L'application s'affiche avec le bandeau vert. Une note du corpus, choisie dans le menu, donne un tableau après le clic.

## En cas de problème
- **Erreur à l'installation** : ouvrez le journal, cherchez la ligne en rouge, et vérifiez que `requirements.txt` est bien à la racine du dépôt. Corrigez, validez, poussez (guide 05), puis cliquez sur **Reboot app**.
- **« No module named 'appli' »** : vérifiez que `src/appli.py` est bien sur GitHub. L'application ajoute `src` au chemin, donc elle n'a pas besoin d'être installée.
- **L'application se met en veille** : comportement normal du plan gratuit. Elle redémarre au premier accès, en quelques dizaines de secondes.
- **Installation qui échoue à cause de spaCy ou de scikit-learn** : dans les paramètres avancés, passez à Python 3.11, puis **Reboot app**.

## Ce que vous devez noter
Votre adresse publique : elle va dans le rapport et sur la première diapositive.
