# Standard library imports
import unittest
import pytest

# Third-party imports
from peewee import SqliteDatabase

import db_operations
from db_operations import add_product_to_user, create_product, create_user
from populate_db import populate_test_database

# Local module imports
from models import db
from models import Product
from models import ProductTag
from models import Purchase
from models import Tag
from models import User
from models import UserProduct

# Use an in-memory SQLite for tests
test_db = SqliteDatabase(':memory:')


def associate_product_with_user(user_id, product_id):
    """
    Associates the product with the user.
    """
    UserProduct.create(user=user_id, product=product_id)


class TestCreateProduct(unittest.TestCase):
    def test_create_product_success(self):
        # Test creating a product with valid inputs
        product = db_operations.create_product("Test Product", "This is a test product.", 10.99, 5)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "This is a test product.")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.quantity, 5)

    def test_create_product_invalid_name(self):
        # Test creating a product with an empty name
        with self.assertRaises(ValueError):
            db_operations.create_product("", "This is a test product.", 10.99, 5)

    def test_create_product_invalid_description(self):
        # Test creating a product with an empty description
        with self.assertRaises(ValueError):
            db_operations.create_product("Test Product", "", 10.99, 5)

    def test_create_product_invalid_price(self):
        # Test creating a product with a negative price
        with self.assertRaises(ValueError):
            db_operations.create_product("Test Product", "This is a test product.", -10.99, 5)

    def test_create_product_invalid_quantity(self):
        # Test creating a product with a negative quantity
        with self.assertRaises(ValueError):
            db_operations.create_product("Test Product", "This is a test product.", 10.99, -5)


# tests related to add_product_to_user in test_db_operations.py

def test_remove_tag_from_product(self):
    print("Testing remove_tag_from_product...")
    # Get the product with the id of the new product
    product = Product.get(Product.id == self.product_id)
    # Remove the tag from the product
    product.tags.remove(self.tag_id)
    # Assert that the product no longer has a tag with the id of the new
    # tag
    self.assertFalse(self.tag_id in [tag.id for tag in product.tags])


class TagError:
    pass


def list_products_per_tag(tag_id: int):
    try:
        # Get the tag with the specified ID
        tag = Tag.get(Tag.id == tag_id)

        # Get all products associated with the tag
        products = tag.products

        return products

    except Exception as e:
        raise TagError(f"Error listing products per tag: {e}")


# Tests removing a tag from a product.
@pytest.fixture
def test_remove_tag_from_product():
    # Get the product with the id of the new product
    product = Product.get(Product.id == self.product_id)
    # Remove the tag from the product
    product.tags.remove(self.tag_id)
    # Assert that the product no longer has a tag with the id of the new
    # tag
    assert self.tag_id not in [tag.id for tag in product.tags]


class TestCreateProduct(unittest.TestCase):

    def create_product(name, description, price, quantity):
        # Create a new product instance
        product = Product(name=name, description=description, price=price, quantity=quantity)

        # Save the product to the database
        product.save()

        # Return the product instance
        return product

    def test_create_product_invalid_name(self):
        # Test creating a product with an empty name
        with self.assertRaises(ValueError):
            create_product("", "This is a test product.", 10.99, 5)

    def test_create_product_invalid_description(self):
        # Test creating a product with an empty description
        with self.assertRaises(ValueError):
            db_operations.create_product("Test Product", "", 10.99, 5)

    def test_create_product_invalid_price(self):
        # Test creating a product with a negative price
        with self.assertRaises(ValueError):
            create_product("Test Product", "This is a test product.", -10.99, 5)

    def test_create_product_invalid_quantity(self):
        # Test creating a product with a negative quantity
        with self.assertRaises(ValueError):
            create_product("Test Product", "This is a test product.", 10.99, -5)


if __name__ == "__main__":
    unittest.main()

