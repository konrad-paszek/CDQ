import json
import random
import string
from pathlib import Path

from bson import ObjectId
from faker import Faker

from cdq.infra.mongodb import mongoclient

fake = Faker()


def fake_record():
    country_code = random.choice(["PL", "DE", "CH"])
    vat_number = f"{country_code}{''.join(random.choices(string.digits, k=8))}"
    return {
        "_id": str(ObjectId()),  # Generate a new MongoDB ObjectId
        "companyName": fake.company(),  # Fake company name
        "identifier": {"vatNumber": vat_number},
        "address": {
            "street": fake.street_address(),  # Fake street address
            "city": fake.city(),  # Fake city
            "zip": fake.zipcode(),  # Fake zip code
            "country": country_code,
        },
    }


def generate_test_data_file(size=100):
    storage_one_path = Path(__file__).parent / "data" / "storage_one.json"
    docs = [fake_record() for _ in range(size)]
    with open(storage_one_path.as_posix(), "w") as fd:
        json.dump(docs, fd, ensure_ascii=False)
    print(f"test file generated {str(storage_one_path)}")


def seed_mongo_from_file(file_path, db, collection):
    with mongoclient() as mongo:
        db = mongo.get_database(db)
        coll = db.get_collection(collection)
        with open(file_path, "r") as fd:
            docs = json.load(fd)
            coll.insert_many(docs)
            print("test database seeded")


def teardown_mongo():
    with mongoclient() as mongo:
        mongo.drop_database("BUSINESS_PARTNER_STORAGE")
        print("test database dropped")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if "--generate-test-data" in args:
        generate_test_data_file()
        sys.exit(0)
    if "--teardown" in args:
        teardown_mongo()
        sys.exit(0)
