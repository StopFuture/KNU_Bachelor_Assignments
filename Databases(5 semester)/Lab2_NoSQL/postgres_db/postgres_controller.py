import csv
import subprocess

import psycopg2
import random
from faker import Faker
import uuid
import datetime


class PostgresController:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.dbname = db_name
        self.user = db_user
        self.password = db_password
        self.host = db_host
        self.port = db_port

        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.faker = Faker()

    def generate_product(self):
        return {
            "id": str(uuid.uuid4()),
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
            "created_by": self.get_random_staff_account_id(),  # Random UUID
            "updated_by": self.get_random_staff_account_id()  # Random UUID
        }

    def insert_countries(self):
        with self.conn.cursor() as cur:
            for country_id in range(10001):  # From 0 to 10000
                iso = self.faker.country_code()
                name = self.faker.country()
                upper_name = name.upper()
                iso3 = self.faker.country_code(representation="alpha-3")
                num_code = random.randint(0, 999)
                phone_code = random.randint(1, 999)

                cur.execute("""
                    INSERT INTO countries (id, iso, name, upper_name, iso3, num_code, phone_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """, (country_id, iso, name, upper_name, iso3, num_code, phone_code))
            self.conn.commit()

    def generate_coupon(self):
        return {
            "id": str(uuid.uuid4()),
            "code": self.faker.bothify(text='????-###'),
            "discount_value": round(random.uniform(5, 50), 2),
            "discount_type": random.choice(["percentage", "amount"]),
            "times_used": random.randint(0, 50),
            "max_usage": random.randint(1, 100) if self.faker.boolean() else None,
            "order_amount_limit": round(random.uniform(50, 500), 2) if self.faker.boolean() else None,
            "coupon_start_date": datetime.datetime.now(),
            "coupon_end_date": datetime.datetime.now() + datetime.timedelta(days=30),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": self.get_random_staff_account_id(),  # Random UUID
            "updated_by": self.get_random_staff_account_id()  # Random UUID
        }

    def generate_category(self):
        return {
            "id": str(uuid.uuid4()),
            "parent_id": str(uuid.uuid4()) if self.faker.boolean() else None,
            "category_name": self.faker.word(),
            "category_description": self.faker.text(),
            "icon": self.faker.image_url(),
            "placeholder": self.faker.image_url(),
            "active": self.faker.boolean(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": self.get_random_staff_account_id(),
            "updated_by": self.get_random_staff_account_id()
        }

    def generate_supplier(self):
        return {
            "id": str(uuid.uuid4()),
            "supplier_name": self.faker.company(),
            "company": self.faker.company_suffix(),
            "phone_number": self.faker.phone_number(),
            "address_line1": self.faker.street_address(),
            "address_line2": self.faker.secondary_address(),
            "country_id": random.randint(1, 100),  # Assuming country_id is an integer
            "city": self.faker.city(),
            "note": self.faker.text(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": self.get_random_staff_account_id(),
            "updated_by": self.get_random_staff_account_id()
        }

    def generate_tag(self):
        return {
            "id": str(uuid.uuid4()),
            "tag_name": self.faker.word(),
            "icon": self.faker.image_url(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": self.get_random_staff_account_id(),
            "updated_by": self.get_random_staff_account_id()
        }

    def generate_customer(self):
        return {
            "id": str(uuid.uuid4()),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.unique.email(),
            "password_hash": self.faker.sha256(raw_output=False),  # Example hash
            "active": self.faker.boolean(),
            "registered_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }

    def insert_customer(self):
        customer = self.generate_customer()
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO customers (id, first_name, last_name, email, password_hash, 
                                       active, registered_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                customer["id"], customer["first_name"], customer["last_name"], customer["email"],
                customer["password_hash"], customer["active"], customer["registered_at"],
                customer["updated_at"]
            ))
            self.conn.commit()

    def generate_notification(self):
        return {
            "id": str(uuid.uuid4()),
            "account_id": self.get_random_customer_account_id(),  # Random UUID, replace with actual reference if needed
            "title": self.faker.sentence(),
            "content": self.faker.text(),
            "seen": self.faker.boolean(),
            "created_at": datetime.datetime.now(),
            "receive_time": datetime.datetime.now(),
            "notification_expiry_date": datetime.datetime.now() + datetime.timedelta(days=30)
        }

    def generate_staff_account(self):
        return {
            "id": str(uuid.uuid4()),
            "role_id": random.randint(1, 5),  # Assuming you have 5 roles, modify as needed
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone_number": self.faker.phone_number(),
            "email": self.faker.email(),
            "password_hash": self.faker.sha256(raw_output=False),  # Example hash
            "active": self.faker.boolean(),
            "placeholder": self.faker.sentence() if self.faker.boolean() else None,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "created_by": None,  # Initial entry will have no creator
            "updated_by": None  # Initial entry will have no updater
        }

    def get_random_staff_account_id(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM staff_accounts LIMIT 1 OFFSET floor(random()* (SELECT COUNT(*) FROM staff_accounts));")
            result = cur.fetchone()
            return result[0] if result else None  # Return None if staff_accounts is empty

    def insert_staff_account(self):
        staff_account = self.generate_staff_account()
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO staff_accounts (id, role_id, first_name, last_name, 
                                            phone_number, email, password_hash, 
                                            active, placeholder, created_at, 
                                            updated_at, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                staff_account["id"], staff_account["role_id"], staff_account["first_name"],
                staff_account["last_name"], staff_account["phone_number"], staff_account["email"],
                staff_account["password_hash"], staff_account["active"], staff_account["placeholder"],
                staff_account["created_at"], staff_account["updated_at"],
                staff_account["created_by"], staff_account["updated_by"]
            ))
            self.conn.commit()

    def insert_product(self):
        product = self.generate_product()
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (id, slug, product_name, price, quantity, 
                                      short_description, product_description, 
                                      product_type, published, created_at, 
                                      updated_at, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                product["id"], product["slug"], product["product_name"],
                product["price"], product["quantity"], product["short_description"],
                product["product_description"], product["product_type"],
                product["published"], product["created_at"], product["updated_at"],
                product["created_by"], product["updated_by"]
            ))
            self.conn.commit()

    def get_random_product_id(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM products ORDER BY RANDOM() LIMIT 1;")
            result = cur.fetchone()
            return result[0] if result else None

    def insert_coupon(self):
        coupon = self.generate_coupon()
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO coupons (id, code, discount_value, discount_type, 
                                     times_used, max_usage, order_amount_limit, 
                                     coupon_start_date, coupon_end_date, 
                                     created_at, updated_at, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                coupon["id"], coupon["code"], coupon["discount_value"],
                coupon["discount_type"], coupon["times_used"], coupon["max_usage"],
                coupon["order_amount_limit"], coupon["coupon_start_date"],
                coupon["coupon_end_date"], coupon["created_at"], coupon["updated_at"],
                coupon["created_by"], coupon["updated_by"]
            ))
            self.conn.commit()



    def insert_category(self):
        category = self.generate_category()
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO categories (id, parent_id, category_name, category_description, 
                                                icon, placeholder, active, created_at, updated_at, 
                                                created_by, updated_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                category["id"], category["id"], category["category_name"],
                category["category_description"], category["icon"], category["placeholder"],
                category["active"], category["created_at"], category["updated_at"],
                category["created_by"], category["updated_by"]
            ))
            self.conn.commit()

    def insert_supplier(self):
        supplier = self.generate_supplier()
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO suppliers (id, supplier_name, company, phone_number, 
                                               address_line1, address_line2, country_id, city, 
                                               note, created_at, updated_at, created_by, updated_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                supplier["id"], supplier["supplier_name"], supplier["company"],
                supplier["phone_number"], supplier["address_line1"], supplier["address_line2"],
                supplier["country_id"], supplier["city"], supplier["note"],
                supplier["created_at"], supplier["updated_at"],
                supplier["created_by"], supplier["updated_by"]
            ))
            self.conn.commit()

    def insert_tag(self):
        tag = self.generate_tag()
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO tags (id, tag_name, icon, created_at, updated_at, 
                                          created_by, updated_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                tag["id"], tag["tag_name"], tag["icon"], tag["created_at"],
                tag["updated_at"], tag["created_by"], tag["updated_by"]
            ))
            self.conn.commit()

    def insert_notification(self):
        notification = self.generate_notification()
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO notifications (id, account_id, title, content, seen, 
                                                   created_at, receive_time, notification_expiry_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                notification["id"], notification["account_id"], notification["title"],
                notification["content"], notification["seen"], notification["created_at"],
                notification["receive_time"], notification["notification_expiry_date"]
            ))
            self.conn.commit()

    def get_random_customer_account_id(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM customers LIMIT 1 OFFSET floor(random()* (SELECT COUNT(*) FROM customers));")
            result = cur.fetchone()
            return result[0] if result else None

    def update_product(self):
        product_id = self.get_random_product_id()
        if product_id is None:
            return 0  # No products to update

        # Generate random update data
        updated_data = {
            "price": round(random.uniform(10, 1000), 2),
            "quantity": random.randint(1, 100),
            "product_name": self.faker.word(),
            "short_description": self.faker.text(max_nb_chars=165)
            # Add other fields as needed
        }

        with self.conn.cursor() as cur:
            # Constructing the SQL query with dynamic fields
            query = "UPDATE products SET "
            query += ", ".join([f"{key} = %s" for key in updated_data])
            query += " WHERE id = %s"

            # Values for the query, ensuring the product ID is last
            values = list(updated_data.values()) + [product_id]

            cur.execute(query, values)
            self.conn.commit()
            return cur.rowcount

    # Returns the number of rows updated

    def delete_product(self):
        product_id = self.get_random_product_id()
        if product_id is None:
            return 0  # No products to delete

        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.conn.commit()
            return cur.rowcount  # Returns the number of rows deleted

    def read_product(self):
        product_id = self.get_random_product_id()
        if product_id is None:
            return None  # No products to read

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cur.fetchone()  # Returns a single product record or None

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

    def export_table_to_csv(self, table_name="products", output_file="new_import_postgres.csv"):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")

            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            with open(output_file, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(columns)  # Write the column headers
                csv_writer.writerows(rows)

    def backup_postgres_messages(self, backup_file):
        command = f"pg_dump -h {self.host} -p {self.port} -U {self.user} -F c -b -v -f {backup_file} {self.dbname}"
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Backup completed successfully. The backup file is {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while backing up PostgreSQL: {e}")

    def backup_postgres(self, backup_file):
        command = f"pg_dump -h {self.host} -p {self.port} -U {self.user} -F c -b -f {backup_file} {self.dbname}"
        try:
            subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"Backup completed successfully. The backup file is {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while backing up PostgreSQL: {e}")


