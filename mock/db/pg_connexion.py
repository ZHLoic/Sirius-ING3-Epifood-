import psycopg2
from psycopg2.extras import RealDictCursor

# Connexion à la base
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
    Récupère toutes les recettes
    """
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT _id, name, ingredients, diet, prep_time, cook_time, flavor_profile, course, state, region
        FROM "goldRecipies";
    """)
    recettes = cur.fetchall()
    cur.close()
    return recettes
