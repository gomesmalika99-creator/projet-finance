# Journal du projet

## Test de la saisie piégée

Saisie testée : `' OR '1'='1`

Commande : `python test_injection.py`

Résultat :
- lister_societes(piege) -> [] (aucune donnée)
- lire_societe(piege) -> None (aucune donnée)

Explication : toutes les requêtes utilisent des paramètres `%s`. PyMySQL envoie la saisie
comme une simple valeur texte, jamais comme du code SQL. L'attaque ne peut donc pas modifier la requête.

## Erreurs rencontrées et solutions

| Erreur | Cause | Solution |
|---|---|---|
| `Python est introuvable` | Python n'était pas installé | Installer Python depuis python.org |
| `git n'est pas reconnu` | VS Code n'avait pas vu la nouvelle installation | Redémarrer l'ordinateur |
| `Jeton inattendu « PS »` | J'avais collé le début de ligne `(.venv) PS ...` avec la commande | Copier seulement la commande |
| `fatal: not a git repository` | Commande tapée dans une autre fenêtre (UCRT64) | Toujours utiliser le terminal de VS Code, dans le dossier du projet |
| Fichier `env` sans le point, marqué U | Mauvais nom : Git allait envoyer le mot de passe | Renommer en `.env` (ignoré par .gitignore) |
| `Table 'societe' already exists` | Script SQL lancé deux fois | Ajouter `DROP DATABASE IF EXISTS finance;` en début de script |
| `ImportError` / `NameError` | Fichier pas enregistré | Ctrl + S, puis activer File > Auto Save |