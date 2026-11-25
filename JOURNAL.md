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
| `Jeton inattendu « PS »` |

## Brief API REST (FastAPI)

### 1. Collection Postman enregistrée au mauvais endroit
- **Erreur :** la collection a été enregistrée dans un fichier nommé `postman`, alors que le brief demande `postman/collection.json`.
- **Solution :** création du dossier `postman`, puis `git mv` pour déplacer et renommer le fichier.

### 2. `pymysql`, `Request` et `logger` soulignés dans `main.py`
- **Erreur :** j'ai ajouté les gestionnaires d'erreurs en bas du fichier, mais oublié les imports en haut. Python ne connaissait pas ces noms.
- **Solution :** ajout de `import pymysql`, `from fastapi import Request`, `from fastapi.responses import JSONResponse` et `logger = logging.getLogger("api")`.

### 3. FastAPI ne peut pas renvoyer directement mes objets `Societe`
- **Problème :** ma couche d'accès renvoie des objets (dataclass), pas des dictionnaires.
- **Solution :** `vars(objet)` transforme l'objet en dictionnaire, que FastAPI envoie en JSON.

### 4. Pas de fonction pour modifier ou supprimer une société
- **Problème :** le brief demande PUT et DELETE, mais ma couche d'accès ne savait que lire et ajouter.
- **Solution :** ajout de `remplacer_societe`, `supprimer_societe` et `compter_bilans` dans `depot.py`, sans toucher aux fonctions existantes. Les routes ne contiennent toujours aucun SQL.

### 5. Supprimer une société effaçait ses bilans sans prévenir
- **Problème :** la table `bilan` a `ON DELETE CASCADE`. Le brief demande un 409 si la société a encore des bilans.
- **Solution :** la route DELETE appelle `compter_bilans()` avant de supprimer. S'il reste des bilans, elle répond 409.

### 6. La route des cours demande des dates
- **Problème :** `lister_cours()` a besoin d'une date de début et d'une date de fin.
- **Solution :** deux paramètres facultatifs, `date_debut` et `date_fin`, avec des valeurs par défaut très larges.

### 7. Ne pas montrer d'erreur technique
- **Problème :** une erreur imprévue (base arrêtée…) pourrait afficher une trace ou un nom de table.
- **Solution :** un gestionnaire global renvoie seulement « Erreur interne du serveur » (500). Le détail reste dans le terminal.

### Point d'attention : la connexion à la base
Chaque fonction de `depot.py` ouvre sa connexion et la ferme toujours (`with` ou `finally`), même en cas d'erreur. Une demande qui appelle plusieurs fonctions ouvre et ferme donc plusieurs connexions de suite, mais aucune ne reste ouverte.
