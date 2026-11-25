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