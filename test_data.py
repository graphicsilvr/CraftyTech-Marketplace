import unittest
from peewee import SqliteDatabase
from models import Tag, Transaction, Product, User, ProductTag, UserProduct
from main import (
    add_tag_to_product,
    list_products_per_tag,
    add_product_to_catalog,
    purchase_product,
    search,
    list_user_products,
    User,
    Product,
    remove_tag_from_product,
    create_product_tag,
    create_transaction,
    remove_product, 
    update_tag,
    delete_tag,
    user_purchases,
)

# Use an in-memory SQLite database for testing
betsy_db = SqliteDatabase("betsy.db")


class TestMain(unittest.TestCase):
    def test_my_function(self):
        # Call my_function with some input
        result = my_function("input")
        
        # Check that the output is what we expect
        self.assertEqual(result, "expected_output")

    def setUp(self):
        # Bind the test database to the models
        User._meta.database = betsy_db
        Product._meta.database = betsy_db
        # Create the tables
        User.create_table()
        Product.create_table()

    def tearDown(self):
        # Drop the tables after each test
        User.drop_table()
        Product.drop_table()

    def test_create_user(self):
        """
        Test creating a user
        """
        user = create_user(
            username="testuser",
            name="Test User",
            address="123 Main St",
            zipcode="12345",
            city="Test City",
            state="Test State",
            country="Test Country",
            billing_name="Test Billing Name",
            billing_account="1234567890",
            password="testpassword",
            email="test@example.com",
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.zipcode, "12345")
        self.assertEqual(user.city, "Test City")
        self.assertEqual(user.state, "Test State")
        self.assertEqual(user.country, "Test Country")
        self.assertEqual(user.billing_name, "Test Billing Name")
        self.assertEqual(user.billing_account, "1234567890")
        self.assertEqual(user.password, "testpassword")
        self.assertEqual(user.email, "test@example.com")

    def test_create_product(self):
        """
        Test creating a product
        """
        product = create_product(
            name="Test Product",
            description="Test product description",
            price_per_unit=9.99,
            quantity_in_stock=100,
        )

        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test product description")
        self.assertEqual(product.price_per_unit, 9.99)
        self.assertEqual(product.quantity_in_stock, 100)
        
class TestCreateTransactions(unittest.TestCase):
    def setUp(self):
        # Bind the test database to the Transaction model
        Transaction.bind(betsy_db, bind_refs=False, bind_backrefs=False)
        betsy_db.create_tables([Transaction])

    def tearDown(self):
        # Drop the tables after each test
        betsy_db.drop_tables([Transaction])

    def test_create_transactions(self):
        # Call the create_transactions function
        create_transactions()

        # Check that the transactions were created correctly
        transactions = Transaction.select()
        self.assertEqual(transactions.count(), 4)

        transaction1 = transactions.where(Transaction.description == "Salary").get()
        self.assertEqual(transaction1.amount, 1000.00)
        self.assertEqual(transaction1.category, "salary_category")
        self.assertEqual(transaction1.account, "bank_account")
        self.assertEqual(transaction1.date, datetime(2022, 3, 31))

        transaction2 = transactions.where(Transaction.description == "Groceries").get()
        self.assertEqual(transaction2.amount, -100.00)
        self.assertEqual(transaction2.category, "groceries_category")
        self.assertEqual(transaction2.account, "bank_account")
        self.assertEqual(transaction2.date, datetime.date(2022, 4, 1))

        transaction3 = transactions.where(Transaction.description == "Dinner with friends").get()
        self.assertEqual(transaction3.amount, -50.00)
        self.assertEqual(transaction3.category, "entertainment_category")
        self.assertEqual(transaction3.account, "credit_card_account")
        self.assertEqual(transaction3.date, datetime.date(2022, 4, 2))

        transaction4 = transactions.where(Transaction.description == "New shoes").get()
        self.assertEqual(transaction4.amount, -200.00)
        self.assertEqual(transaction4.category, "clothing_category")
        self.assertEqual(transaction4.account, "credit_card_account")
        self.assertEqual(transaction4.date, datetime.date(2022, 4, 4))
        
class TestUserProducts(unittest.TestCase):
    """
    Test user_products as a unittest.TestCase subclass
    """

    def setUp(self):
        self.test_user = User.create(username="test_user")
        self.test_product = Product.create(name="test_product")
        self.test_purchase = Purchase.create(
            user=self.test_user, product=self.test_product, quantity=1
        )
        self.user_id = 1
        self.tag_name = "Test Tag"

    def test_search(self):
        """
        Test the search function
        """
        results = search("test")
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        for product in results:
            self.assertIsInstance(product, Product)

    def test_catalog(self):
        """
        Test the catalog function
        """
        user = User.create(username="test_user")


class TestData(unittest.TestCase):
    """
    Test data as a unittest.TestCase subclass
    """

    def setUp(self):
        self.test_user = User.create(username="test_user")
        self.test_product = Product.create(name="test_product")
        self.test_purchase = Purchase.create(
            user=self.test_user, product=self.test_product, quantity=1
        )
        self.user_id = 1
        self.tag_name = "Test Tag"

    def test_search(self):
        """
        Test the search function
        """
        results = search("test")
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        for product in results:
            self.assertIsInstance(product, Product)

    def test_catalog(self):
        """
        Test the catalog function
        """
        user = User.create(username="test_user")
        product = Product.create(name="test_product")
        catalog_product = CatalogProduct.create(product=product)
        catalog = Catalog.create(user=user, products=[catalog_product])
        self.assertIsNotNone(catalog)
        self.assertIsInstance(catalog, Catalog)
        self.assertIsInstance(catalog.products, list)
        self.assertIsInstance(catalog.tags, list)

    def test_user_purchases(self):
        """
        Test the user purchases function
        """
        results = []
        for purchase in self.test_user.purchases:
            results.append(purchase.product)
        self.assertEqual(len(results), len(self.test_user.purchases))

    def test_list_user_products(self):
        """
        Test the list_user_products function
        """
        products = list_user_products(self.user_id)
        self.assertFalse(len(products) > 0)
        for product in products:
            self.assertIsInstance(product, Product)

    def test_add_product_to_catalog(self):
        """
        Test the add_product_to_catalog function
        """
        # Create a new Product object
        new_product = Product(name="Test Product", price=19.99)
        # Add the new product to the catalog
        add_product_to_catalog(self.user_id, new_product)
        # Assert that the new product has a non-None value for its id attribute
        self.assertIsNotNone(new_product.id)
        self.assertListEqual(list(new_product.tags), [])

    def test_remove_product_from_catalog(self):
        """
        Test the remove_product_from_catalog function
        """
        # Get the product with the id of the new product
        product = Product.get(Product.id == self.test_product.id)
        # Delete the product
        self.test_product.delete_instance()
        self.assertRaises(
            Product.DoesNotExist, Product.get, Product.id == self.test_product.id
        )

    def test_add_tag_to_product(self):
        """
        Test the add_tag_to_product function
        """
        add_tag_to_product(self.test_product.id, self.tag_name)
        updated_product = Product.get(Product.id == self.test_product.id)
        self.assertTrue(self.tag_name in [tag.name for tag in updated_product.tags])

    def test_remove_tag_from_product(self):
        """
        Test the remove_tag_from_product function
        """
        self.test_product.tags.remove(self.tag_name)
        updated_product = Product.get(Product.id == self.test_product.id)
        self.assertFalse(self.tag_name in [tag.name for tag in updated_product.tags])

    def test_update_product(self):
        """
        Test updating a product
        """
        self.test_product.name = "Updated Product"
        self.test_product.description = "This is an updated product"
        self.test_product.price = 20.00
        self.test_product.save()
        updated_product = Product.get(Product.id == self.test_product.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.description, "This is an updated product")
        self.assertEqual(updated_product.price, 20.00)

    def test_delete_tag(self):
        """
        Test deleting a tag
        """
        tag = Tag.create(name=self.tag_name)
        tag.delete_instance()
        with self.assertRaises(Tag.DoesNotExist):
            Tag.get(Tag.id == tag.id)

    def test_list_products_per_tag(self):
        """
        Test the list_products_per_tag function
        """
        products = list_products_per_tag(self.tag_name)
        self.assertGreater(len(products), 0)
        for product in products:
            self.assertIsInstance(product, Product)

    def test_update_stock(self):
        """
        Test the update_stock function
        """
        new_quantity = 20
        update_stock(self.test_product.id, new_quantity)
        updated_product = Product.get(Product.id == self.test_product.id)
        self.assertGreater(new_quantity, updated_product.quantity)

    def test_purchase_product(self):
        """
        Test the purchase_product function
        """
        # Define the test data
        buyer_id = 1
        quantity = 2
        new_quantity = self.test_product.quantity - quantity

        # Test the purchase_product function
        purchase_product(self.test_product.id, buyer_id, quantity)

        # Assert that the product quantity has been updated correctly
        updated_product = Product.get(Product.id == self.test_product.id)
        self.assertEqual(updated_product.quantity, new_quantity)

    def test_user_products(self):
        """
        Test the list_user_products function
        """
        products = list_user_products(self.user_id)
        self.assertGreaterEqual(len(products), 0)
        for product in products:
            self.assertIsInstance(product, Product)

    # Tests that a transaction can be retrieved by its ID
    def test_retrieve_transaction_by_id(self):
        # Create a user and product
        user = User.create(
            username="test_user",
            name="Test User",
            address="123 Test St",
            zipcode="12345",
            city="Test City",
            state="CA",
            country="United States",
            billing_name="Test User",
            billing_account="1234567890",
            password="password",
            email="test@example.com",
        )
        product = Product.create(
            name="Test Product",
            description="A test product",
            price_per_unit=9.99,
            quantity_in_stock=10,
        )

        # Create a transaction
        transaction = Transaction.create(
            user=user,
            product=product,
            quantity=2,
            amount=19.98,
            description="Test transaction",
            category="Test category",
            account="Test account",
            date=date.today(),
        )

        # Retrieve the transaction by its ID
        retrieved_transaction = Transaction.get_by_id(transaction.id)

        # Assert that the retrieved transaction matches the original transaction
        assert retrieved_transaction.user == user
        assert retrieved_transaction.product == product
        assert retrieved_transaction.quantity == 2
        assert retrieved_transaction.amount == 19.98
        assert retrieved_transaction.description == "Test transaction"
        assert retrieved_transaction.category == "Test category"
        assert retrieved_transaction.account == "Test account"
        assert retrieved_transaction.date == date.today()


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests")
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed.")
