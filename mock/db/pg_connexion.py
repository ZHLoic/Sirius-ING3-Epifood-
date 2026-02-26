from psycopg2.extras import RealDictCursor
import psycopg2

def get_connexion():
    conn = psycopg2.connect(
        host="172.31.252.17",
        database="gold",
        user="mock_user",
        password="epifooding3"
    )
    return conn

def recuperer_recettes(conn):
    """
    Récupère toutes les recettes depuis PostgreSQL
    """
    cur = conn.cursor()  # simple cursor pour éviter blocage
    try:
        print("[DEBUG] Avant execute SQL")
        cur.execute("""
            SELECT order_id, category, name, description, price,
                   start_order_time, prep_time, end_time_prep, status
            FROM "goldRecipies" LIMIT 100000;
        """)
        print("[DEBUG] Après execute SQL")

        recettes = cur.fetchall()
        print(f"[DEBUG] fetchall OK, {len(recettes)} recettes récupérées")
        return recettes

    except Exception as e:
        print(f"[ERROR] Exception dans recuperer_recettes: {e}")
        return []

    finally:
        cur.close()