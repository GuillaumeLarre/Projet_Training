# Carnet d'entraînement musculation

Application Python en ligne de commande pour suivre ses séances de musculation, analyser sa progression, et comparer ses volumes hebdomadaires aux recommandations scientifiques.

Projet personnel développé pour mettre en pratique la programmation orientée objet, la persistance de données, et les bonnes pratiques de développement (tests automatiques, type hints, modules)

---

## Fonctionnalités

- **Catalogue d'exercices** personnalisable avec groupe musculaire, muscles ciblés et type de matériel
- **Saisie de séances** détaillées (date, durée, exercices, séries avec poids/reps/échauffement)
- **Modification et suppression** d'une séance ou de ses composants individuels
- **Stats d'entraînement** :
  - Volume total par groupe musculaire
  - Nombre de séries par groupe et par muscle cible, par semaine
  - Fréquence d'entraînement par groupe et par muscle
  - 1RM estimé par exercice (formule d'Epley)
  - Comparaison aux fourchettes scientifiques (insuffisant / fourchette basse / optimum / fourchette haute)
  - Évolution des charges dans le temps
  - Records par exercice
- **Récapitulatif hebdomadaire** automatique sur la semaine en cours
- **Persistance JSON** rétrocompatible

---

## Architecture
Projet-Training/

├── models/                     # Classes du domaine

│   ├── Serie.py

│   ├── Exercice.py

│   ├── ExerciceRealise.py

│   ├── Seance.py

│   └── CarnetEntrainement.py

├── stats/

│   └── stats.py                # Fonctions d'analyse statistique

├── interface/

│   └── interface.py            # Interface utilisateur (CLI)

├── constantes/

│   └── constantes.py           # Listes de référence (muscles, matériels, fourchettes scientifiques)

├── fonctions_utiles/

│   └── fonctions.py            # Helpers (validation date, accord, saisie)

├── tests/                      # Suite pytest

│   ├── test_serie.py

│   ├── test_exercice_realise.py

│   └── test_stats.py

├── seed.py                     # Catalogue d'exercices initial

├── seances_seed.py             # Séances de démonstration

├── main.py                     # Point d'entrée

└── conftest.py                 # Configuration pytest

Chaque classe suit le pattern POO suivant :
- Constructeur avec validation des paramètres
- Properties pour les calculs dérivés (volume, nb_series, etc.)
- Méthodes `to_dict()` / `from_dict()` pour la sérialisation JSON

---

## Installation

```bash
# Cloner le repo
git clone https://github.com/GuillaumeLarre/Projet_Training.git
cd Projet_Training

# (Optionnel) créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate    # macOS/Linux

# Installer les dépendances
pip install -r requirements.txt
```

---

## Utilisation

```bash
# Initialiser le catalogue d'exercices (à faire une fois)
python seed.py

# (Optionnel) charger des séances de démonstration
python seances_seed.py

# Lancer l'application
python main.py
```

Le menu principal propose 10 options pour saisir, consulter, analyser ou modifier ses entraînements.

---

## Tests

Suite de tests automatiques avec pytest (20 tests couvrant les classes principales et les stats).

```bash
pytest
```

---

## Technologies

- **Python 3.11+**
- **pytest** pour les tests automatiques
- **JSON** pour la persistance des données
- Annotations de types (PEP 484/604) vérifiées par Pylance/mypy

---

## Roadmap

- [x] Architecture POO et persistance JSON
- [x] Stats d'entraînement complètes
- [x] Modification/suppression de séances individuelles
- [x] Tests pytest
- [x] Type hints sur toute la base
- [ ] Migration vers SQLite (SQLAlchemy)
- [ ] Logging structuré
- [ ] Interface web (Flask)
- [ ] Visualisations graphiques (matplotlib)
- [ ] Progressive Web App (PWA) pour mobile

---

## Auteur

Guillaume LARRE — étudiant en bachelor informatique.

Projet en cours d'évolution dans le cadre d'un apprentissage continu des bonnes pratiques de développement Python.