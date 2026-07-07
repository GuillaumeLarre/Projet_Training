# Carnet d'entraînement musculation

Application Python en ligne de commande pour suivre ses séances de musculation, analyser sa progression et comparer ses volumes hebdomadaires à des fourchettes de référence.

Projet personnel développé pour mettre en pratique une architecture en couches, une base `SQLite` pilotée par l'ORM `SQLAlchemy`, le pattern Repository, les tests automatisés, les annotations de types et les bonnes pratiques de développement Python.

---

## Fonctionnalités

* **Catalogue d'exercices** personnalisable avec groupe musculaire, muscles ciblés et type de matériel
* **Saisie de séances** détaillées :

  * date ;
  * durée ;
  * exercices réalisés ;
  * séries avec poids, répétitions et échauffement.
* **Modification et suppression** d'une séance ou de ses composants individuels :

  * date ;
  * durée ;
  * exercice réalisé ;
  * série ;
  * séance complète.
* **Base SQLite** avec contraintes d'intégrité :

  * clés étrangères ;
  * contraintes `UNIQUE` ;
  * contraintes `CHECK` ;
  * valeurs par défaut ;
  * suppressions en cascade avec `ON DELETE CASCADE`.
* **Stats d'entraînement** :

  * volume total par groupe musculaire ;
  * nombre de séries par groupe et par muscle cible, par semaine ;
  * fréquence d'entraînement par groupe et par muscle ;
  * 1RM estimé par exercice avec la formule d'Epley ;
  * comparaison aux fourchettes scientifiques ;
  * évolution des charges dans le temps ;
  * records par exercice.
* **Récapitulatif hebdomadaire** automatique sur la semaine en cours

---

## Architecture

```text
Projet_Training/

├── database/
│   ├── engine.py                 # Création de l'engine
│   ├── models.py                 # Création des classes ORM
│   ├── exercices_repository.py   # Accès base pour le catalogue d'exercices
│   └── seances_repository.py     # Accès base pour les séances, exercices réalisés et séries
│
├── interface/
│   └── interface.py              # Interface utilisateur en ligne de commande
│
├── stats/
│   └── stats.py                  # Fonctions d'analyse statistique
│
├── constantes/
│   └── constantes.py             # Listes de référence : muscles, matériels, fourchettes
│
├── fonctions_utiles/
│   └── fonctions.py              # Helpers : validation de date, accord, saisies contrôlées
│
├── tests/
│   ├── test_exercices_repository.py
│   ├── test_seances_repository.py
│   └── test_stats.py
│
├── seed.py                       # Initialisation du catalogue d'exercices
├── seances_seed.py               # Séances de démonstration
├── main.py                       # Point d'entrée de l'application
└── conftest.py                   # Configuration et fixtures pytest
```

L'application est organisée en couches :

* `database/` isole l'accès aux données via l'ORM SQLAlchemy et le pattern Repository ;
* `interface/` gère l'orchestration, les menus et les saisies utilisateur ;
* `stats/` contient la logique d'analyse et de calcul ;
* `constantes/` centralise les listes de référence utilisées par l'application.

La base SQLite est créée automatiquement si elle n'existe pas encore.

Les suppressions dépendantes sont gérées par SQLite grâce aux clés étrangères et aux règles `ON DELETE CASCADE`. Par exemple, la suppression d'une séance entraîne automatiquement la suppression des exercices réalisés et des séries associés.

---

## Installation

```bash
# Cloner le repo
git clone https://github.com/GuillaumeLarre/Projet_Training.git
cd Projet_Training

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# Installer les dépendances
pip install -r requirements.txt
```

---

## Utilisation

```bash
# Initialiser le catalogue d'exercices
python seed.py

# Charger des séances de démonstration
python seances_seed.py

# Lancer l'application
python main.py
```

La base SQLite est créée automatiquement au premier lancement si elle n'existe pas encore.

Le menu principal permet de saisir, consulter, analyser, modifier ou supprimer des entraînements.

---

## Tests

Le projet utilise `pytest` pour les tests automatisés.
Suite de 18 tests automatisés.

Les tests repository utilisent des fixtures et une base SQLite en mémoire afin d'isoler les tests et d'éviter de modifier la base réelle.

```bash
pytest
```

Les tests couvrent notamment :

* le repository des exercices ;
* le repository des séances ;
* les ajouts, modifications et suppressions ;
* le chargement d'une séance complète ;
* les fonctions statistiques.

---

## Technologies

* **Python 3.11+**
* **SQLite**
* **SQLAlchemy 2.0.51**
* **pytest**
* **Logging**
* **Annotations de types** avec la syntaxe moderne Python
* **Pylance** pour l'aide au typage dans VS Code

---

## Roadmap

* [x] Architecture POO initiale
* [x] Stats d'entraînement complètes
* [x] Modification et suppression de séances individuelles
* [x] Type hints sur la base de code
* [x] Logging structuré
* [x] Migration vers SQLite avec `sqlite3`
* [x] Pattern Repository pour isoler l'accès aux données
* [x] Contraintes d'intégrité SQL et suppressions en cascade
* [x] Suite de tests pytest avec fixtures et base en mémoire
* [x] Refactorisation des repositories vers SQLAlchemy (ORM)
* [ ] Exposition de l'application via une API Flask ou FastAPI
* [ ] Frontend HTML/CSS responsive
* [ ] Progressive Web App (PWA) installable sur mobile
* [ ] Visualisations graphiques des stats

---

## Choix techniques et apprentissages

Ce projet a été l'occasion d'expérimenter plusieurs décisions d'architecture significatives :

* **Pattern Repository** : les accès à la base sont isolés dans `database/`, ce qui sépare l'accès aux données du reste du code. Cette séparation a rendu la migration vers SQLAlchemy possible sans toucher à la logique métier ni à l'interface (ce qui s'est vérifié : les 18 tests sont passés sans modification).

* **Cascade SQL plutôt que cascade Python** : les suppressions imbriquées (séance → exercices réalisés → séries) sont  déclarées au niveau des modèles ORM (ondelete="CASCADE") et appliquées par SQLite via les clés étrangères. Avantage : ajouter une nouvelle table enfant n'oblige pas à modifier les fonctions de suppression existantes, la règle est portée par la FK elle-même.

* **Stats sur dicts plutôt que sur objets** : les fonctions d'analyse ont été refactorisées pour opérer sur les données brutes retournées par les repositories (listes de dicts) au lieu d'un arbre d'objets en mémoire. Cette approche est cohérente avec une future migration vers une architecture web, où chaque requête HTTP est isolée et ne maintient pas d'état global.

* **Tests avec fixtures pytest et base SQLite en mémoire** : chaque test reçoit une base fraîche grâce à une fixture, ce qui garantit l'isolation et la rapidité (les 18 tests s'exécutent en moins de 100 ms). Cette approche permet de tester des comportements complexes (contraintes, cascades) sans nécessiter de configuration externe.

* **Atomicité des opérations métier** : la fonction `enregistrer_seance_complete` regroupe en une seule transaction l'enregistrement d'une séance, de ses exercices et de ses séries. Cela évite de laisser des données partielles en base en cas d'interruption.

* **Migration vers SQLAlchemy 2.x (ORM)** : les repositories, initialement écrits en sqlite3 pur, ont été réécrits avec l'ORM SQLAlchemy en préservant les mêmes signatures et formes de sortie (dicts), ce qui a permis de ne toucher ni à l'interface, ni aux stats, ni à la logique des tests. Points techniques notables : gestion des identifiants auto-générés en cascade via flush(), injection de la session en argument des fonctions (testabilité), et base de test isolée en mémoire.

## Auteur

Guillaume LARRE — étudiant en bachelor informatique.

Projet en cours d'évolution dans le cadre d'un apprentissage progressif des bonnes pratiques de développement Python, SQL et architecture logicielle.
