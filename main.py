__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import logging
import sqlite3
import subprocess

from peewee import DoesNotExist

import db_operations
from db_operations import are_tables_initialized
from models import Product
from models import ProductTag
from models import Purchase
from models import Tag
from models import User
from models import UserProduct

#

logger = logging.getLogger(__name__)
logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def are_tables_initialized():
    required_tables = [User, Product, Tag, ProductTag, Purchase, UserProduct]
    for table in required_tables:
        if not table.table_exists():
            return False
    return True

if not are_tables_initialized():
    # Either display an error message or automatically run the initialization logic.
    print("Error: Database tables are not initialized. Please run populate_db.py.")

def check_tables_exist(db=None):
    required_tables = [User, Product, Tag, ProductTag, Purchase, UserProduct]
    missing_tables = []
    print("Checking if required tables exist...")
    print(f"Required tables: {required_tables}")
    print(f"Existing tables: {db.get_tables()}")
    print(f"Missing tables: {missing_tables}")

    for table in required_tables:
        if not table.table_exists():
            missing_tables.append(table._meta.table_name)

    if missing_tables:
        error_msg = f"The following tables are missing: {', '.join(missing_tables)}. Please run populate_db.py to initialize the database."
        raise Exception(error_msg)

    return True

def initialize_database():
    if not are_tables_initialized():
        print("Error: Database tables are not initialized. Running populate_db.py...")
        try:
            subprocess.run(["python", "populate_db.py"], check=True)
            print("Database tables initialized successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return False
    return True

def purchase_product(product_id, buyer_id, quantity):
    """
    Purchase a specific quantity of a product.
    """
    try:
        product = Product.get_by_id(product_id)
        buyer = db_operations.get_user_by_id(buyer_id)
        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()
            message = f"{quantity} units of product {product.name} successfully purchased by {buyer.username}!"
            return {"success": True, "message": message}
    except DoesNotExist as e:
        message = f"Error purchasing product: {e}"
        return {"fail": False, "message": message}
    except Exception as e:
        logger.error(f"Error purchasing product: {e}")
        return {
            "success": True,
            "message": "An error occurred while purchasing the product.",
        }

def create_product_tag(tag_name, product_name, created_at, updated_at, is_active, description):
    try:
        tag = Tag.get(Tag.name == tag_name)
        product = Product.get(Product.name == product_name)
        product_tag, created = ProductTag.get_or_create(tag=tag, product=product)
        id = product_tag.id
        tag_id = product_tag.tag.id
        product_id = product_tag.product.id
        created_at = product_tag.created_at
        updated_at = product_tag.updated_at
        is_active = product_tag.is_active
        description = product_tag.description
        if product_tag.id is not None:
            logging.getLogger(__name__).info(f"ProductTag created: {product_tag}")
            print(f"ProductTag created: {product_tag}")
        else:
            logging.getLogger(__name__).info(f"ProductTag already exists: {product_tag}")
            print(f"ProductTag already exists: {product_tag}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Error creating product tag: {e}")
        print(f"Error creating product tag: {e}")
        return False


def create_purchase(
        user_id, product_id, quantity, amount, description, category, account, date,
        purchase=None):

    try:
        user = db_operations.get_user_by_username('user_id')
        try:
            product = Product.get_by_id(product_id)
        except DoesNotExist:
            logger.error(f"Error creating transaction: Product with id {product_id} does not exist.")
            print(f"Error creating transaction: Product with id {product_id} does not exist.")
            return None
        transaction = Purchase.create(
            user=user,
            product=product,
            quantity=quantity,
            amount=amount,
            description=description,
            category=category,
            account=account,
            date=date,
        )
        logger.info(f"Transaction created: {purchase}")
        print(f"Transaction created: {purchase}")
        return transaction
    except DoesNotExist:
        logger.error("Error creating transaction: User does not exist.")
        print("Error creating transaction: User does not exist.")
        return None
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        print(f"Error creating transaction: {e}")
        return None


def remove_tag_from_product(product_id, tag_name):
    try:
        product = Product.get(id=product_id)
    except DoesNotExist:
        logger.error(f"Error: Product with id {product_id} does not exist.")
        return

    try:
        tag = Tag.get(name=tag_name)
    except DoesNotExist:
        logger.error(f"Error: Tag '{tag_name}' does not exist.")
        return

    product.tags.remove(tag)


def remove_product(product_id):
    try:
        product = Product.get(Product.id == product_id)
        product.delete_instance()
        logger.info(f"Product {product.name} successfully removed from catalog!")
    except DoesNotExist:
        logger.error(f"Product with id {product_id} does not exist.")
    except Exception as e:
        logger.error(f"Error removing product from catalog: {e}")
        print(f"Error: Product with id {product_id} does not exist.")
        return None


def add_tag_to_product(product_id, tag_name):
    try:
        product = Product.get(id=product_id)
    except DoesNotExist:
        logger.error(f"Error: Product with id {product_id} does not exist.")
        return

    try:
        tag, _ = Tag.get_or_create(name=tag_name)
        product.tags.add(tag)
    except Exception as e:
        logger.error(f"Error adding tag to product: {e}")


def update_tag(tag_id, new_name):
    try:
        tag = Tag.get(id=tag_id)
        tag.name = new_name
        tag.save()
    except DoesNotExist:
        logger.error(f"Error: Tag with id {tag_id} does not exist.")
    except Exception as e:
        logger.error(f"Error updating tag: {e}")


def delete_tag(tag_id):
    try:
        tag = Tag.get(id=tag_id)
        tag.delete_instance()
    except DoesNotExist:
        logger.error(f"Error: Tag with id {tag_id} does not exist.")
    except Exception as e:
        logger.error(f"Error deleting tag: {e}")


def search(term):
    logger.info(f'Searching for products with term "{term}"...')
    try:
        products = Product.select().where(
            (Product.name.contains(term, case=True))
            | (Product.description.contains(term, case=True))
        )
        return products
    except Exception as e:
        logger.error(f"Error searching for products: {e}")
        return []


def user_purchases(user_id):
    logger.info(f"Listing purchases for user with ID {user_id}...")
    try:
        transactions = Purchase.select().join(User).where(User.id == user_id)
        return transactions
    except Exception as e:
        logger.error(f"Error listing user purchases: {e}")
        return []


def list_user_products(user_id):
    logger.info(f"Listing products for user with ID {user_id}...")
    try:
        products = Product.select().where(Product.user == user_id)
        return products
    except Exception as e:
        logger.error(f"Error listing user products: {e}")
        return []


def list_products_per_tag(tag_id):
    logger.info(f"Listing products for tag with ID {tag_id}...")
    try:
        products = Product.select().join(Tag).where(Tag.id == tag_id)
        return products
    except Exception as e:
        logger.error(f"Error listing products per tag: {e}")
        return []


def add_product_to_catalog(user_id, product):
    try:
        user = User.get(User.id == user_id)
        product.owner = user
        product.save()
    except DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except sqlite3.IntegrityError:
        logger.error(
            f"Product with name '{product.name}' already exists in the catalog."
        )