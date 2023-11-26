import json
import random
import subprocess

from faker import Faker
from pymongo import MongoClient
from bson import ObjectId
import datetime


class MongoController:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.uri = uri
        self.db = self.client[db_name]
        self.faker = Faker()

    def generate_product(self):
        return {
            "slug": self.faker.slug(),
            "product_name": self.faker.word(),
            "price": round(random.uniform(10, 1000), 2),
            "quantity": random.randint(1, 100),
            "short_description": self.faker.text(max_nb_chars=165),
            "product_description": self.faker.text(),
            "product_type": self.faker.word(),
            "published": self.faker.boolean(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": ObjectId(),  # Random ObjectId
            "updated_by": ObjectId()  # Random ObjectId
        }

    def generate_coupon(self):
        return {
            "code": self.faker.bothify(text='????-###'),
            "discount_value": round(random.uniform(5, 50), 2),
            "discount_type": random.choice(["percentage", "amount"]),
            "times_used": random.randint(0, 50),
            "max_usage": random.randint(1, 100) if self.faker.boolean() else None,
            "order_amount_limit": round(random.uniform(50, 500), 2) if self.faker.boolean() else None,
            "coupon_start_date": datetime.datetime.now(),
            "coupon_end_date": datetime.datetime.now(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": ObjectId(),
            "updated_by": ObjectId()
        }

    def generate_category(self):
        return {
            "parent_id": ObjectId() if self.faker.boolean() else None,
            "category_name": self.faker.word(),
            "category_description": self.faker.text(),
            "icon": self.faker.image_url(),
            "placeholder": self.faker.image_url(),
            "active": self.faker.boolean(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": ObjectId(),
            "updated_by": ObjectId()
        }

    def generate_supplier(self):
        return {
            "supplier_name": self.faker.company(),
            "company": self.faker.company_suffix(),
            "phone_number": self.faker.phone_number(),
            "address_line1": self.faker.street_address(),
            "address_line2": self.faker.secondary_address() if self.faker.boolean() else "",
            "country_id": ObjectId(),
            "city": self.faker.city(),
            "note": self.faker.text(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": ObjectId(),
            "updated_by": ObjectId()
        }

    def generate_tag(self):
        return {
            "tag_name": self.faker.word(),
            "icon": self.faker.image_url(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": ObjectId(),
            "updated_by": ObjectId()
        }

    def generate_notification(self):
        return {
            "account_id": ObjectId(),
            "title": self.faker.sentence(nb_words=6),
            "content": self.faker.text(),
            "seen": self.faker.boolean(),
            "created_at": datetime.datetime.now(),
            "receive_time": datetime.datetime.now(),
            "notification_expiry_date": datetime.datetime.now() + datetime.timedelta(days=30)
        }

    def insert_product(self):
        self.db.products.insert_one(self.generate_product())

    def insert_coupon(self):
        self.db.coupons.insert_one(self.generate_coupon())

    def insert_category(self):
        self.db.categories.insert_one(self.generate_category())

    def insert_supplier(self):
        self.db.suppliers.insert_one(self.generate_supplier())

    def insert_tag(self):
        self.db.tags.insert_one(self.generate_tag())

    def insert_notification(self):
        self.db.notifications.insert_one(self.generate_notification())

    def delete_product(self):
        random_product = self.db.products.find_one()  # Get a random product
        if random_product:
            self.db.products.delete_one({"_id": random_product["_id"]})

    def read_product(self):
        return self.db.products.find_one()  # Returns a random product document

    def update_product(self):
        random_product = self.db.products.find_one()  # Get a random product
        if random_product:
            updated_data = {
                "price": round(random.uniform(10, 1000), 2),
                "quantity": random.randint(1, 100)
                # Add other fields as needed
            }
            self.db.products.update_one(
                {"_id": random_product["_id"]},
                {"$set": updated_data}
            )

    def insert_into_all(self):
        self.insert_product()
        # self.insert_coupon()
        # self.insert_category()
        # self.insert_supplier()
        # self.insert_tag()
        # self.insert_notification()

    def crud_all(self):
        self.insert_into_all()
        self.read_product()
        self.update_product()
        self.delete_product()

    def export_collection_to_json(self, output_file="mongo_export.json"):
        collection = self.db['products']
        data = list(collection.find())

        with open(output_file, 'w') as file:
            json.dump(data, file, default=str)

    def backup_mongodb_messages(self, backup_path):
        try:
            subprocess.run(['mongodump', '--uri', self.uri, '--out', backup_path], check=True)
            print(f"Backup completed successfully. Files are stored in {backup_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while backing up MongoDB: {e}")

    def backup_mongodb(self, backup_path):
        try:
            subprocess.run(['mongodump', '--uri', self.uri, '--out', backup_path], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"Backup completed successfully. Files are stored in {backup_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while backing up MongoDB: {e}")