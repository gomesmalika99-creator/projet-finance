import pymysql
from db import get_connexion
from modeles import Societe, Bilan, Cours

# ===== Toutes les requetes SQL (avec parametres %s) =====
SQL_LISTER_SOCIETES = "SELECT id, nom, secteur, devise, symbole FROM societe ORDER BY nom"
SQL_LISTER_SOCIETES_SECTEUR = "SELECT id, nom, secteur, devise, symbole FROM societe WHERE secteur = %s ORDER BY nom"
SQL_LIRE_SOCIETE = "SELECT id, nom, secteur, devise, symbole FROM societe WHERE id = %s"
SQL_AJOUTER_SOCIETE = "INSERT INTO societe (nom, secteur, symbole) VALUES (%s, %s, %s)"
SQL_LISTER_BILANS = (
    "SELECT id, societe_id, annee, chiffre_affaires, resultat_net, actifs_courants, "
    "passifs_courants, dettes_totales, capitaux_propres "
    "FROM bilan WHERE societe_id = %s ORDER BY annee"
)
SQL_LISTER_COURS = (
    "SELECT id, societe_id, date_cours, cloture FROM cours "
    "WHERE societe_id = %s AND date_cours BETWEEN %s AND %s ORDER BY date_cours"
)


# ===== Fonctions d'acces aux donnees =====
def lister_societes(secteur=None):
    with get_connexion() as conn:
        with conn.cursor() as cur:
            if secteur is None:
                cur.execute(SQL_LISTER_SOCIETES)
            else:
                cur.execute(SQL_LISTER_SOCIETES_SECTEUR, (secteur,))
            return [Societe(**ligne) for ligne in cur.fetchall()]


def lire_societe(id_societe):
    with get_connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL_LIRE_SOCIETE, (id_societe,))
            ligne = cur.fetchone()
            return Societe(**ligne) if ligne else None


def ajouter_societe(nom, secteur, symbole):
    conn = get_connexion()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_AJOUTER_SOCIETE, (nom, secteur, symbole))
            nouvel_id = cur.lastrowid
        conn.commit()
        return Societe(nouvel_id, nom, secteur, symbole=symbole)
    except pymysql.MySQLError:
        conn.rollback()
        raise
    finally:
        conn.close()


def lister_bilans(id_societe):
    with get_connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL_LISTER_BILANS, (id_societe,))
            return [Bilan(**ligne) for ligne in cur.fetchall()]


def lister_cours(id_societe, date_debut, date_fin):
    with get_connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL_LISTER_COURS, (id_societe, date_debut, date_fin))
            return [Cours(**ligne) for ligne in cur.fetchall()]


# ===== Ajouts pour l'API (étape 5) =====
SQL_REMPLACER_SOCIETE = "UPDATE societe SET nom = %s, secteur = %s, symbole = %s WHERE id = %s"
SQL_SUPPRIMER_SOCIETE = "DELETE FROM societe WHERE id = %s"
SQL_COMPTER_BILANS = "SELECT COUNT(*) AS nb FROM bilan WHERE societe_id = %s"
SQL_SYMBOLE_PRIS = "SELECT COUNT(*) AS nb FROM societe WHERE symbole = %s AND id <> %s"


def remplacer_societe(id_societe, nom, secteur, symbole):
    conn = get_connexion()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_REMPLACER_SOCIETE, (nom, secteur, symbole, id_societe))
        conn.commit()
    except pymysql.MySQLError:
        conn.rollback()
        raise
    finally:
        conn.close()


def supprimer_societe(id_societe):
    conn = get_connexion()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_SUPPRIMER_SOCIETE, (id_societe,))
        conn.commit()
    except pymysql.MySQLError:
        conn.rollback()
        raise
    finally:
        conn.close()


def compter_bilans(id_societe):
    with get_connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL_COMPTER_BILANS, (id_societe,))
            return cur.fetchone()["nb"]


def symbole_existe(symbole, sauf_id=0):
    """Vrai si une autre société (que sauf_id) utilise déjà ce symbole."""
    with get_connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL_SYMBOLE_PRIS, (symbole, sauf_id))
            return cur.fetchone()["nb"] > 0
