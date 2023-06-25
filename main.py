__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


import sqlite3
import logging

from peewee import DoesNotExist

from models import Product
from models import User
from models import Tag
from models import ProductTag
from models import Transaction

logger = logging.getLogger(__name__)
logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def purchase_product(product_id, buyer_id, quantity):
    """
    Purchase a specific quantity of a product.
    """
    try:
        product = Product.get_by_id(product_id)
        buyer = User.get_by_id(buyer_id)
        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()
            message = f"{quantity} units of product {product.name} successfully purchased by {buyer.username}!"
            return {"success": True, "message": message}
    except DoesNotExist as e:
        message = f"Error purchasing product: {e}"
        return {"success": False, "message": message}
    except Exception as e:
        logger.error(f"Error purchasing product: {e}")
        return {
            "success": False,
            "message": "An error occurred while purchasing the product.",
        }


def create_product_tag(tag_name, product_name):
    try:
        tag = Tag.get(Tag.name == tag_name)
        product = Product.get(Product.name == product_name)
        product_tag = ProductTag.create(tag=tag, product=product)
        product_tag.save()
        return True
    except Exception as e:
        logger.error(f"Error creating product tag: {e}")
        return False

def create_transaction(
    user_id, product_id, quantity, amount, description, category, account, date
):
    try:
        user = User.get(User.id == user_id)
        product = Product.get(Product.id == product_id)
        transaction = Transaction.create(
            user=user,
            product=product,
            quantity=quantity,
            amount=amount,
            description=description,
            category=category,
            account=account,
            date=date,
        )
        logger.info(f"Transaction created: {transaction}")
        print(f"Transaction created: {transaction}")
        return transaction
    except DoesNotExist:
        logger.error("Error creating transaction: User or product does not exist.")
        print("Error creating transaction: User or product does not exist.")
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
        product = Product.get(id=product_id)
        product.delete_instance()
        logger.info(f"Product {product.name} successfully removed from catalog!")
    except Product.DoesNotExist:
        logger.error(f"Product with id {product_id} not found!")
    except Exception as e:
        logger.error(f"Error removing product from catalog: {e}")


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
            (Product.name.contains(term, case=False))
            | (Product.description.contains(term, case=False))
        )
        return products
    except Exception as e:
        logger.error(f"Error searching for products: {e}")
        return []


def user_purchases(user_id):
    logger.info(f"Listing purchases for user with ID {user_id}...")
    try:
        transactions = Transaction.select().join(User).where(User.id == user_id)
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




