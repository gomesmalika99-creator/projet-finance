import pymysql
from db import get_connexion
from modeles import Societe, Bilan, Cours

# ===== Toutes les requetes SQL (avec parametres %s) =====
SQL_LISTER_SOCIETES = "SELECT id, nom, secteur, devise FROM societe ORDER BY nom"
SQL_LISTER_SOCIETES_SECTEUR = "SELECT id, nom, secteur, devise FROM societe WHERE secteur = %s ORDER BY nom"
SQL_LIRE_SOCIETE = "SELECT id, nom, secteur, devise FROM societe WHERE id = %s"
SQL_AJOUTER_SOCIETE = "INSERT INTO societe (nom, secteur) VALUES (%s, %s)"
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


def ajouter_societe(nom, secteur):
    conn = get_connexion()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_AJOUTER_SOCIETE, (nom, secteur))
            nouvel_id = cur.lastrowid
        conn.commit()
        return Societe(nouvel_id, nom, secteur)
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