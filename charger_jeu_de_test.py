from pathlib import Path
import pymysql
from connexion import get_connexion

FICHIER_SQL = Path(__file__).parent / "sql" / "jeu_de_test.sql"


def charger():
    texte = FICHIER_SQL.read_text(encoding="utf-8")
    instructions = [i.strip() for i in texte.split(";") if i.strip()]
    conn = get_connexion()
    try:
        with conn.cursor() as cur:
            for instruction in instructions:
                cur.execute(instruction)
        conn.commit()
        print(f"Jeu de test charge : {len(instructions)} instructions executees.")
    except pymysql.MySQLError as erreur:
        conn.rollback()
        print("Erreur, aucune modification enregistree :", erreur)
    finally:
        conn.close()


if __name__ == "__main__":
    charger()