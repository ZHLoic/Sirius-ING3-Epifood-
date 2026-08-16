from pymongo import MongoClient


# ============================================================
# CONFIGURATION
# ============================================================

SILVER_HOST = "172.31.249.184"
SILVER_PORT = 27017

GOLD_HOST = "172.31.249.249"
GOLD_PORT = 27017

MONGO_USER = "admin"
MONGO_PASSWORD = "secret"

SILVER_DB = "data_silver"
SILVER_COLLECTION = "cleaned_data"

GOLD_DB = "data_gold"
GOLD_COLLECTION = "food_consumption"


# ============================================================
# CONNEXIONS
# ============================================================

silver_client = MongoClient(
    SILVER_HOST,
    SILVER_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource="admin"
)

gold_client = MongoClient(
    GOLD_HOST,
    GOLD_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource="admin"
)

silver_collection = silver_client[
    SILVER_DB
][SILVER_COLLECTION]

gold_collection = gold_client[
    GOLD_DB
][GOLD_COLLECTION]

print("Nettoyage de la collection Gold...")
gold_collection.delete_many({})

# ============================================================
# PIPELINE MONGODB
# ============================================================

pipeline = [

    # --------------------------------------------------------
    # 1. Exclusion des lignes Sex = Total
    # --------------------------------------------------------

    {
        "$match": {
            "Sex": {
                "$ne": "Total"
            }
        }
    },

    # --------------------------------------------------------
    # 2. Regroupement + sommation
    # --------------------------------------------------------

    {
        "$group": {

            "_id": {
                "Country": "$Country",
                "Year": "$Year",
                "Geographic Level": "$Geographic Level",
                "Population Age Group": "$Population Age Group",
                "Food Group Code": "$Food Group Code",
                "Food Group": "$Food Group",
                "Indicator Code": "$Indicator Code",
                "Indicator": "$Indicator",
                "Element": "$Element",
                "Unit": "$Unit"
            },

            "Value": {
                "$sum": "$Value"
            }
        }
    },

    # --------------------------------------------------------
    # 3. Remise à plat du document
    # --------------------------------------------------------

    {
        "$project": {
            "_id": 0,

            "Country": "$_id.Country",
            "Year": "$_id.Year",
            "Geographic Level": "$_id.Geographic Level",
            "Population Age Group": "$_id.Population Age Group",
            "Food Group Code": "$_id.Food Group Code",
            "Food Group": "$_id.Food Group",
            "Indicator Code": "$_id.Indicator Code",
            "Indicator": "$_id.Indicator",
            "Element": "$_id.Element",
            "Unit": "$_id.Unit",

            "Value": 1
        }
    }
]


# ============================================================
# EXECUTION
# ============================================================

print("Début Silver → Gold")

print("Exécution de l'agrégation MongoDB...")

results = silver_collection.aggregate(
    pipeline,
    allowDiskUse=True
)


# ============================================================
# INSERTION GOLD
# ============================================================

batch = []
batch_size = 5000

total = 0

for document in results:

    batch.append(document)

    if len(batch) >= batch_size:

        gold_collection.insert_many(batch)

        total += len(batch)

        print(
            f"{total:,} lignes insérées dans Gold"
        )

        batch = []


# Dernier batch

if batch:

    gold_collection.insert_many(batch)

    total += len(batch)

    print(
        f"{total:,} lignes insérées dans Gold"
    )


# ============================================================
# FIN
# ============================================================

print()
print("Transformation Silver → Gold terminée.")
print(f"Nombre de lignes Gold : {total:,}")


silver_client.close()
gold_client.close()