import datetime
from datetime import date


from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    DecimalField,
    IntegerField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    DateField,
)

db = SqliteDatabase("betsy.db")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    name = CharField()
    address = CharField()
    zipcode = CharField()
    city = CharField()
    state = CharField()
    country = CharField()
    billing_name = CharField()
    billing_account = CharField()
    password = CharField()
    email = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Product(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    price_per_unit = DecimalField()
    quantity_in_stock = IntegerField()


class Tag(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    color = CharField(null=True)
    parent = ForeignKeyField('self', null=True, related_name='children')


class ProductTag(BaseModel):
    tag = ForeignKeyField(Tag)
    product = ForeignKeyField(Product)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    description = CharField(null=True)


class Transaction(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity = IntegerField()
    amount = DecimalField(max_digits=10, decimal_places=2)
    description = CharField()
    category = CharField()
    account = CharField()
    date = DateField(default=datetime.date.today)


class UserProduct(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)


def create_database():
    with db.atomic():
        db.create_tables([User, Product, Tag, ProductTag, Transaction, UserProduct])


def create_user(username, name, address, zipcode, city, state, country, billing_name, billing_account, password, email):
    try:
        # Check if a user with the given username already exists
        existing_user = User.get(User.username == username)
        return existing_user
    except User.DoesNotExist:
        # Create a new user with the given information
        return User.create(
            username=username,
            name=name,
            address=address,
            zipcode=zipcode,
            city=city,
            state=state,
            country=country,
            billing_name=billing_name,
            billing_account=billing_account,
            password=password,
            email=email,
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        return None


def create_product(name, description, price_per_unit, quantity_in_stock):
    try:
        return Product.create(
            name=name,
            description=description,
            price_per_unit=price_per_unit,
            quantity_in_stock=quantity_in_stock,
        )
    except Exception as e:
        print(f"Error creating product: {e}")
        return None


def create_tag(name):
    try:
        return Tag.create(name=name)
    except Exception as e:
        print(f"Error creating tag: {e}")
        return None


# Create other users, similar to the above pattern

def populate_test_database():
    create_database()

    emma = create_user(
        username="emma1",
        name="Emma",
        address="123 Oak St",
        zipcode="12345",
        city="San Francisco",
        state="CA",
        country="United States",
        billing_name="Emma Stone",
        billing_account="1234567890",
        password="password",
        email="emma@example.com",
    )

    if emma:
        emma.name = "Emma Stone"
        emma.address = "456 Pine St"
        emma.zipcode = "54321"
        emma.city = "San Francisco"
        emma.state = "CA"
        emma.country = "USA"
        emma.billing_name = "Emma Stone"
        emma.billing_account = "1234509876"
        emma.password = "newpassword"
        emma.save()

    max, created = User.get_or_create(
        username="max1",
        defaults={
            "name": "Max",
            "address": "789 Pine St",
            "zipcode": "67890",
            "city": "Los Angeles",
            "state": "CA",
            "country": "United States",
            "billing_name": "Max Johnson",
            "billing_account": "5432167890",
            "password": "password",
            "email": "max@example.com",
        },
    )
    if not created:
        max.name = "Max Johnson"
        max.address = "567 Oak St"
        max.zipcode = "98765"
        max.city = "San Francisco"
        max.state = "CA"
        max.country = "USA"
        max.billing_name = "Max J."
        max.billing_account = "0987654321"
        max.password = "newpassword"
        max.save()

    dan, created = User.get_or_create(
        username="dan1",
        defaults={
            "name": "Dan",
            "address": "890 Maple Ave",
            "zipcode": "54321",
            "city": "San Diego",
            "state": "CA",
            "country": "United States",
            "billing_name": "Dan Brown",
            "billing_account": "0987654321",
            "password": "password",
            "email": "dan@example.com",
        },
    )
    if not created:
        dan.name = "Dan Brown"
        dan.address = "987 Elm St"
        dan.zipcode = "12345"
        dan.city = "San Diego"
        dan.state = "CA"
        dan.country = "United States"
        dan.billing_name = "Dan B."
        dan.billing_account = "0987654321"
        dan.password = "newpassword"
        dan.save()

    alice, created = User.get_or_create(
        username="alice1",
        defaults={
            "name": "Alice",
            "address": "875 Brons St",
            "zipcode": "153836",
            "city": "Boston",
            "state": "MA",
            "country": "United States",
            "billing_name": "Alice Smith",
            "billing_account": "1234567890",
            "password": "password",
            "email": "alice@example.com",
        },
    )
    if not created:
        alice.name = "Alice Smith"
        alice.address = "123 Main St"
        alice.zipcode = "12345"
        alice.city = "Boston"
        alice.state = "MA"
        alice.country = "United States"
        alice.billing_name = "Alice S."
        alice.billing_account = "1234509876"
        alice.password = "newpassword"
        alice.save()

    bob, created = User.get_or_create(
        username="bob1",
        defaults={
            "name": "Bob",
            "address": "874 Jefferson lane",
            "zipcode": "98874",
            "city": "New York",
            "state": "NY",
            "country": "United States",
            "billing_name": "Bob Johnson",
            "billing_account": "5432909833",
            "password": "password",
            "email": "bob@example.com",
        },
    )
    if not created:
        bob.name = "Bob Johnson"
        bob.address = "456 Main St"
        bob.zipcode = "54321"
        bob.city = "New York"
        bob.state = "NY"
        bob.country = "United States"
        bob.billing_name = "Bob J."
        bob.billing_account = "5432167890"
        bob.password = "newpassword"
        bob.save()

    product1, created = Product.get_or_create(
    name="iPhone 13",
    defaults={
            "description": "Apple iPhone 13 with 128GB of storage",
            "price_per_unit": 799.00,
            "quantity_in_stock": 10,            
        },
    )
    print(f"Product 1 created: {created}")

    if not created:
        product1.description = "Apple iPhone 13 with 256GB of storage"
        product1.price_per_unit = 899.00
        product1.quantity_in_stock = 20
        product1.save()

    product2, created = Product.get_or_create(
        name="AirPods Pro",
        defaults={
                "description": "Apple AirPods Pro with wireless charging case",
                "price_per_unit": 249.00,
                "quantity_in_stock": 5,        
        },
    )
    print(f"Product 2 created: {created}")

    if not created:
        product2.description = "Apple AirPods Pro with noise cancellation"
        product2.price_per_unit = 299.00
        product2.quantity_in_stock = 10
        product2.save()

    product3, created = Product.get_or_create(
        name="MacBook Pro",
        defaults={
            "description": "Apple MacBook Pro with M1 chip and 512GB SSD",
            "price_per_unit": 1499.00,
            "quantity_in_stock": 2,
        },
    )
    print(f"Product 3 created: {created}")

    if not created:
        product3.description = "Apple MacBook Pro with M1 chip and 1TB SSD"
        product3.price_per_unit = 1699.00
        product3.quantity_in_stock = 5
        product3.save()

    product4, created = Product.get_or_create(
        name="airpods",
        defaults={
            "description": "Apple AirPods with wireless charging case",
            "price_per_unit": 159.00,
            "quantity_in_stock": 5,
        },
    )
    print(f"Product 4 created: {created}")

    if not created:
        product4.description = "Apple AirPods next generation with noise cancellation"
        product4.price_per_unit = 199.00
        product4.quantity_in_stock = 10
        product4.save()

    electronics, created = Tag.get_or_create(name="Electronics")
    if not created:
        electronics.name = "Electronics. Updated"
        print(f"Tag Electronics updated: {created}")

    apple, created = Tag.get_or_create(name="Apple")
    if not created:
        apple.name = "Apple. Updated"
        print(f"Tag Apple updated: {created}")

    headphones, created = Tag.get_or_create(name="Headphones")
    if not created:
        headphones.name = "Headphones. Updated"
        print(f"Tag Headphones updated: {created}")

    laptops, created = Tag.get_or_create(name="Laptops")
    if not created:
        laptops.name = "Laptops. Updated"
        print(f"Tag Laptops updated: {created}")
        
def create_product_tag(tag_name, product_name):
    try:
        tag = Tag.get(Tag.name == tag_name)
        product = Product.get(Product.name == product_name)
        product_tag, created = ProductTag.get_or_create(tag=tag, product=product)
        if created:
            logging.Logger.info(f"ProductTag created: {product_tag}")
            print(f"ProductTag created: {product_tag}")
        else:
            logging.logger.info(f"ProductTag already exists: {product_tag}")
            print(f"ProductTag already exists: {product_tag}")
        return True
    except Exception as e:
        logging.logger.error(f"Error creating product tag: {e}")
        print(f"Error creating product tag: {e}")
        return False
        print(f"product_tag.__dict__: {product_tag.__dict__}")

    # Define a list of tag-product pairs to create ProductTag instances for
    tag_product_pairs = [
        ("Red", "Apple"),
        ("Electronics", "iPhone"),
        ("Apple", "iPhone"),
        ("Electronics", "AirPods"),
        ("Headphones", "AirPods"),
        ("Electronics", "MacBook"),
        ("Laptops", "MacBook"),
    ]

    # Loop through the tag-product pairs and create ProductTag instances
    for tag_name, product_name in tag_product_pairs:
        create_product_tag(tag_name, product_name)

    # Define a dictionary to map tags to products
    tag_map = {
        "electronics": ["iPhone", "AirPods", "MacBook"],
        "apple": ["iPhone", "AirPods", "MacBook"],
        "iphone": ["iPhone"],
        "ipad": ["MacBook"],
        "macbook": ["MacBook"],
        "airpods": ["AirPods"],
        "apple_watch": ["MacBook"],
    }

    # Iterate over the tags and products and create the corresponding product tags
    for tag_name, product_names in tag_map.items():
        tag, _ = Tag.get_or_create(name=tag_name)  # Retrieve or create the tag
        for product_name in product_names:
            product = Product.get(name=product_name)  # Retrieve the product
            product_tag, created = ProductTag.get_or_create(tag=tag, product=product)
            if created:
                logger.info(f"ProductTag created: {product_tag}")
                print(f"ProductTag created: {product_tag}")
            else:
                logger.info(f"ProductTag already exists: {product_tag}")
                print(f"ProductTag already exists: {product_tag}")

    # check if the product instances with the names specified in the tag_map exist in the database
    for product_name in set(product_names for product_names in tag_map.values()):
        try:
            Product.get(Product.name == product_name)
        except Product.DoesNotExist:
            print(f"{product_name} does not exist in the database")

    # check if the product tag instances where created and exist in the database
    for tag_name, product_names in tag_map.items():
        tag = Tag.get(Tag.name == tag_name)
        for product_name in product_names:
            try:
                ProductTag.get(
                    ProductTag.tag == tag, ProductTag.product == product_name
                )
            except ProductTag.DoesNotExist:
                print(f"Product tag for {product_name} and {tag.name} does not exist in the database")

def create_transactions():
    Transaction.create(
        amount=1000.00,
        description="Salary",
        category="salary_category",
        account="bank_account",
        date=datetime(2022, 3, 31),
    )
    Transaction.create(
        amount=-100.00,
        description="Groceries",
        category="groceries_category",
        account="bank_account",
        date=datetime.date(2022, 4, 1),
    )
    Transaction.create(
        amount=-50.00,
        description="Dinner with friends",
        category="entertainment_category",
        account="credit_card_account",
        date=datetime.date(2022, 4, 2),
    )
    Transaction.create(
        amount=-200.00,
        description="New shoes",
        category="clothing_category",
        account="credit_card_account",
        date=datetime.date(2022, 4, 4),
    )

    # Create the transactions
    create_transactions()

def create_user_product(user_id, product_id):
    try:
        user = User.get(id=user_id)
        product = Product.get(id=product_id)
        user_product = UserProduct.create(user=user, product=product)
        user_product.save()
        return True
    except Exception as e:
        logging.logger.error(f"Error creating user product: {e}")
        return False
        print(f"user_product.__dict__: {user_product.__dict__}")

    # Create the users and products
    dan = User.create(name="Dan")
    emma = User.create(name="Emma")
    max = User.create(name="Max")
    apple = Product.create(name="Apple", price_per_unit=0.5)
    orange = Product.create(name="Orange", price_per_unit=0.3)
    print("Users and products created successfully.")

    # Create the UserProduct records
    UserProduct.get_or_create(user=dan, product=apple)
    UserProduct.get_or_create(user=dan, product=orange)
    UserProduct.get_or_create(user=emma, product=orange)
    UserProduct.get_or_create(user=max, product=apple)
    print("UserProduct records created successfully.")


create_database()
populate_test_database()
print("Test database created and populated successfully.")
print(db.database)


