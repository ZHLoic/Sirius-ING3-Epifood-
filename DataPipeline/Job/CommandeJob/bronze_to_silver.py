from pymongo import MongoClient
from pymongo.errors import BulkWriteError


# ============================================================
# CONFIGURATION
# ============================================================

BRONZE_HOST = "172.31.249.120"
BRONZE_PORT = 27017

SILVER_HOST = "172.31.249.184"
SILVER_PORT = 27017

MONGO_USER = "admin"
MONGO_PASSWORD = "secret"

BRONZE_DB = "data_bronze"
BRONZE_COLLECTION = "raw_data"

SILVER_DB = "data_silver"
SILVER_COLLECTION = "cleaned_data"

BATCH_SIZE = 10_000

# True = seulement 100 lignes pour tester
# False = traitement complet
TEST_MODE = False

TEST_LIMIT = 100


# ============================================================
# CONNEXIONS
# ============================================================

bronze_client = MongoClient(
    BRONZE_HOST,
    BRONZE_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource="admin"
)

silver_client = MongoClient(
    SILVER_HOST,
    SILVER_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource="admin"
)

bronze_db = bronze_client[BRONZE_DB]
bronze_collection = bronze_db[BRONZE_COLLECTION]

silver_db = silver_client[SILVER_DB]
silver_collection = silver_db[SILVER_COLLECTION]


# ============================================================
# FONCTION DE TRANSFORMATION
# ============================================================

def transform_document(row, line_id):

    survey = row.get("Survey", "")

    # --------------------------------------------------------
    # Séparation Country / Year
    # Exemple :
    # "Brazil - 2008-2009"
    # ->
    # Country = Brazil
    # Year = 2008-2009
    # --------------------------------------------------------

    if " - " in survey:
        country, year = survey.rsplit(" - ", 1)
    else:
        country = survey
        year = None

    # --------------------------------------------------------
    # Conversion de Value
    # --------------------------------------------------------

    value = row.get("Value")

    try:
        value = float(value) if value not in (None, "") else None
    except (ValueError, TypeError):
        value = None

    # --------------------------------------------------------
    # Construction du document Silver
    # --------------------------------------------------------

    document = {
        "line_id": line_id,

        "Survey Code": row.get("Survey Code"),

        "Country": country,
        "Year": year,

        "Geographic Level": row.get("Geographic Level"),

        "Population Age Group": row.get("Population Age Group"),

        "Food Group Code": row.get("Food Group Code"),
        "Food Group": row.get("Food Group"),

        "Indicator Code": row.get("Indicator Code"),
        "Indicator": row.get("Indicator"),

        "Element": row.get("Element"),

        "Sex": row.get("Sex"),

        "Unit": row.get("Unit"),

        "Value": value
    }

    return document


# ============================================================
# TRAITEMENT
# ============================================================

print("Début Bronze → Silver")

# On commence avec un compteur basé sur les données existantes
# afin d'éviter de recommencer à 1 si le script est relancé.

existing_count = silver_collection.count_documents({})

print(f"Documents déjà présents en Silver : {existing_count:,}")

line_id = existing_count + 1

cursor = bronze_collection.find({})

batch = []
processed = 0


try:

    for row in cursor:

        document = transform_document(row, line_id)

        batch.append(document)

        line_id += 1
        processed += 1

        # ----------------------------------------------------
        # Mode test
        # ----------------------------------------------------

        if TEST_MODE and processed >= TEST_LIMIT:
            break

        # ----------------------------------------------------
        # Insertion par lots
        # ----------------------------------------------------

        if len(batch) >= BATCH_SIZE:

            silver_collection.insert_many(batch)

            print(
                f"{processed:,} lignes transformées et insérées"
            )

            batch = []

    # --------------------------------------------------------
    # Dernier batch
    # --------------------------------------------------------

    if batch:

        silver_collection.insert_many(batch)

        print(
            f"{processed:,} lignes transformées et insérées"
        )


except BulkWriteError as error:

    print("Erreur lors de l'insertion MongoDB :")
    print(error.details)


finally:

    cursor.close()
    bronze_client.close()
    silver_client.close()


print()
print("Traitement terminé.")
print(f"Nombre traité pendant cette exécution : {processed:,}")