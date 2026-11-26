# Projet finance - Accès aux données

## Installation

1. Créer l'environnement : `python -m venv .venv`
2. L'activer : `.venv\Scripts\activate`
3. Installer les dépendances : `pip install -r requirements.txt`
4. Copier `.env.example` en `.env` et renseigner le mot de passe du compte `app_finance`.

## Base de données (avec le compte root, dans HeidiSQL)

1. Créer la base `finance`, les tables et le compte dédié `app_finance` avec `sql/000_creation_base.sql` (droits SELECT, INSERT, UPDATE, DELETE uniquement sur `finance`).
   Attention : ce script commence par `DROP DATABASE IF EXISTS finance`. Il sert uniquement à la première installation et ne doit jamais être lancé sur une base qui contient de vraies données.
2. Appliquer la migration : `sql/002_ajout_devise.sql`

## Utilisation

- Recharger le jeu de test (`sql/001_jeu_de_test.sql`) : `python charger_jeu_de_test.py`
- Lancer la démonstration : `python demo.py`
- Tester les indicateurs : `python test_indicateurs.py`
- Tester l'injection SQL : `python test_injection.py`

Le journal des erreurs et le résultat du test d'injection sont dans `JOURNAL.md`.

## Lancer l'API

```
pip install -r requirements.txt
uvicorn main:app --reload
```

- Documentation : http://127.0.0.1:8000/docs
- Tests : importer `postman/collection.json` dans Postman, puis faire **Run collection**.
## Front web

Une interface web est servie directement par l'API : http://127.0.0.1:8000/app/

- Liste des sociétés avec recherche, fiche détaillée de chaque société
- Indicateurs calculés depuis le dernier bilan (chiffre d'affaires, résultat net, marge, liquidité, endettement)
- Graphique des cours de clôture (1 mois, 6 mois, 1 an ou tout)
- Création, modification et suppression d'une société, avec affichage du code de réponse de l'API (201, 200, 204, 404, 409, 422)
- Mode démo (fausses données) pour la tester sans API

Le code est dans `frontend/index.html` (HTML, CSS et JavaScript, sans bibliothèque externe). Il a été réalisé avec l'aide d'une IA (Claude).
