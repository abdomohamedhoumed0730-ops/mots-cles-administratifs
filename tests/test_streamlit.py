"""Test de fumée de l'application Streamlit : elle se lance sans exception."""
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from streamlit.testing.v1 import AppTest  # noqa: E402


def test_application_se_lance_sans_exception():
    appli = AppTest.from_file(str(RACINE / "app" / "streamlit_app.py"), default_timeout=120)
    appli.run()
    assert not appli.exception


def test_clic_extraire_affiche_le_tableau():
    appli = AppTest.from_file(str(RACINE / "app" / "streamlit_app.py"), default_timeout=120)
    appli.run()
    appli.button[0].click().run()
    assert not appli.exception
    assert len(appli.dataframe) >= 1


def test_texte_court_affiche_un_avertissement_sans_bloquer():
    appli = AppTest.from_file(str(RACINE / "app" / "streamlit_app.py"), default_timeout=120)
    appli.run()
    appli.sidebar.radio[0].set_value("Coller un texte").run()
    appli.text_area[0].input("Demande de congé.").run()
    assert not appli.exception
    assert len(appli.warning) >= 1
    assert not appli.button[0].disabled


def test_resultats_restent_apres_une_nouvelle_execution():
    appli = AppTest.from_file(str(RACINE / "app" / "streamlit_app.py"), default_timeout=120)
    appli.run()
    appli.button[0].click().run()
    assert len(appli.dataframe) >= 1
    appli.run()  # simule un clic sur un téléchargement : le script se relance
    assert not appli.exception
    assert len(appli.dataframe) >= 1
