import csv
from pymongo import MongoClient

MONGO_HOST = "172.31.249.120"
MONGO_PORT = 27017
MONGO_USER = "admin"
MONGO_PASSWORD = "secret"

DATABASE_NAME = "data_bronze"
COLLECTION_NAME = "raw_data"

CSV_FILE = "/home/epifood/data/food_consumption.csv"

BATCH_SIZE = 10_000


client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource="admin"
)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
collection.delete_many({})
print("Collection Bronze vidée.")

total_inserted = 0

with open(CSV_FILE, mode="r", encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    batch = []

    for row in reader:
        batch.append(dict(row))

        if len(batch) >= BATCH_SIZE:
            collection.insert_many(batch)

            total_inserted += len(batch)

            print(f"{total_inserted:,} lignes insérées")

            batch = []

    # Insérer le dernier lot
    if batch:
        collection.insert_many(batch)
        total_inserted += len(batch)
        print(f"{total_inserted:,} lignes insérées")


client.close()

print(f"\nImport terminé : {total_inserted:,} lignes.")