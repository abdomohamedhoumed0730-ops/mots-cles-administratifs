# Commandes du projet. Lancer depuis la racine : make <cible>
PY ?= python3
export PYTHONPATH := src

.PHONY: install valider evaluer stats tester demo formulaire rapport slides tout nettoyer

install:
	pip install -r requirements-dev.txt
	$(PY) -m spacy download fr_core_news_sm

valider:
	$(PY) src/valider_donnees.py

evaluer: valider
	$(PY) src/evaluate.py

stats: evaluer
	$(PY) src/analyse_statistique.py

tester:
	$(PY) -m pytest -q tests

demo:
	$(PY) demo/demo_mots_cles.py --k 5

formulaire:
	$(PY) src/annotation_humaine.py generer

rapport:
	cd rapport && pdflatex -interaction=nonstopmode rapport.tex && pdflatex -interaction=nonstopmode rapport.tex

slides:
	$(PY) slides/build_slides.py

tout: tester stats rapport slides

nettoyer:
	find . -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .pytest_cache rapport/*.aux rapport/*.log rapport/*.out

.PHONY: app
app:
	python app/app_gradio.py

.PHONY: streamlit
streamlit:
	streamlit run app/streamlit_app.py
