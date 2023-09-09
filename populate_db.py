import bcrypt
from models import TagError
from peewee import IntegrityError
from peewee import fn


from models import db, User, Product, Tag, ProductTag, Purchase, UserProduct


def populate_test_database(electronics=None, apple=None):
    create_database()
    """
    Creates the database tables.
    """
    with db:
        db.create_tables([User, Product, Tag, ProductTag, Purchase, UserProduct])

def hash_password(password):
    """Hashes the given password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def create_database():
    with db.atomic():
        db.create_tables([User, Product, Tag, ProductTag, Purchase, UserProduct])


def create_user(username, name, address, zipcode, city, state, country, billing_name, billing_account, password, email):
    try:
        # Check if a user with the given username already exists
        existing_user = User.select().where(User.username == username).first()
        if existing_user:
            return existing_user
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

def display_all_users():
    # Sample logic to retrieve all users from database
    users = User.select()

    print("All Users:")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    print("\n")

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

def display_all_products():
    # Sample logic to retrieve all products from database
    products = Product.select()

    print("All Products:")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price_per_unit}")
    print("\n")

def create_tag(name):
    try:
        tag_name = Tag.select().where(Tag.name == name).first()
        tag = Tag.create(name=name)
        tag.save()
        return tag
    except IntegrityError as e:
        print(f"Error creating tag: {e}")
        return None

def display_all_tags():
    # Sample logic to retrieve all tags from the database
    tags = Tag.select()
    
    print("All Tags:")
    for tag in tags:
        print(f"ID: {tag.id}, Name: {tag.name}")
    print("\n")


def display_products_by_tag(tag_name: str):
    if not tag_name:
        raise TagError("Tag name cannot be empty")
    try:
        products = (Product
                    .select()
                    .join(ProductTag)
                    .join(Tag)
                    .where(Tag.name == tag_name))
        print(f"Products with tag: {tag_name}")
        for product in products:
            print(product.name)
        print("\n")  # For better formatting
    except Exception as e:
        raise TagError(f"Error displaying products by tag: {e}") 

def display_all_products_by_tag(tags: str):
    # Convert the tags string into a list
    tag_list = [tag.strip() for tag in tags.split(",")]
    
    # If only one tag is provided, use the display_products_by_tag function
    if len(tag_list) == 1:
        display_products_by_tag(tag_list[0])
        return

    # Logic for multiple tags
    try:
        products = (Product
                    .select()
                    .join(ProductTag)
                    .join(Tag)
                    .where(Tag.name.in_(tag_list))
                    .group_by(Product.id)
                    .having(fn.count(Product.id) == len(tag_list)))
        
        print(f"Products with tags: {', '.join(tag_list)}")
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}")
        print("\n")  # For better formatting
    except Exception as e:
        raise TagError(f"Error displaying products by tags: {e}")
    

def create_user_product(user_id, product_id, logger=None):
    try:
        user = User.get(id=user_id)
        product = Product.get(id=product_id)
        user_product = UserProduct.create(user=user, product=product)
        user_product.save()

        # Return a dictionary containing information about the created UserProduct object
        return {
            'id': user_product.id,
            'user_id': user_product.user.id,
            'product_id': user_product.product.id,
            'user_username': user_product.user.username,
            'product_name': user_product.product.name,
            'product_price': user_product.product.price,
            'quantity': user_product.quantity,
            'created_at': user_product.created_at,
            'updated_at': user_product.updated_at,
            'is_active': user_product.is_active,
            'description': user_product.description,
        }

    except Exception as e:
        logger.error(f"Error creating user product: {e}")
        return None
    
def display_all_user_products():
    try:
        user_products = (UserProduct
                         .select()
                         .join(User)
                         .switch(Product))
        for user_product in user_products:
            print(user_product.user.username, user_product.product.name, user_product.quantity)
    except Exception as e:
        print(f"Error displaying user products: {e}")


def create_purchase(user_id, product_id, quantity, logger=None):
    try:
        user = User.get(id=user_id)
        product = Product.get(id=product_id)
        
        # Compute the amount
        total_amount = product.price_per_unit * quantity
        
        purchase = Purchase.create(
            user=user, 
            product=product, 
            quantity=quantity,
            amount=total_amount  # Here's where you'd calculate the total amount
        )
        purchase.save()

        # Return a dictionary containing information about the created Purchase object
        return {
            'id': purchase.id,
            'user_id': purchase.user.id,
            'product_id': purchase.product.id,
            'user_username': purchase.user.username,
            'product_name': purchase.product.name,
            'product_price': purchase.product.price,
            'quantity': purchase.quantity,
            'created_at': purchase.created_at,
            'updated_at': purchase.updated_at,
            'is_active': purchase.is_active,
            'description': purchase.description,
        }

    except Exception as e:
        if logger:
            logger.error(f"Error creating purchase: {e}")
        else:
            print(f"Error creating purchase: {e}")
        return None

    
def display_all_purchases():
    # Sample logic to retrieve all purchases from database
    purchases = Purchase.select()
    
    print("All Purchases:")
    for purchase in purchases:
        print(f"Purchase ID: {purchase.id}, Product ID: {purchase.product_id}, Quantity: {purchase.quantity}")
    print("\n")

"""

def display_all_purchases():
    try:
        purchases = (Purchase
                     .select(Purchase, User, Product)
                     .join(User, on=(Purchase.user == User.id))
                     .switch(Purchase)
                     .join(Product, on=(Purchase.product == Product.id)))
        for purchase in purchases:
            print(purchase.user.username, purchase.product.name, purchase.quantity, purchase.created_at)
    except Exception as e:
        print(f"Error displaying purchases: {e}")

"""


def display_all_purchases():
    try:
        purchases = (Purchase
                     .select(Purchase, User, Product)
                     .join(User, on=(Purchase.user == User.id))
                     .switch(Purchase)
                     .join(Product, on=(Purchase.product == Product.id)))
        print("All Purchases:")
        for purchase in purchases:
            print(f"Purchase ID: {purchase.id}, User: {purchase.user.username}, Product: {purchase.product.name}, Quantity: {purchase.quantity}, Price: {purchase.product.price_per_unit}, Total: {purchase.amount}")
        print("\n")
    except Exception as e:
        print(f"Error displaying purchases: {e}")

# Create other users, similar to the above pattern

def populate_test_database(electronics=None, apple=None):
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
            "tags": ["airpods", "wireless"],
            "category": "electronics",
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
            "tags": ["electronics, apple"],
            "categories": ["electronics, apple"],
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
            "tags": ["airpods", "wireless"],
            "category": "electronics",
        },
    )
    print(f"Product 4 created: {created}")

    if not created:
        product4.description = "Apple AirPods next generation with noise cancellation"
        product4.price_per_unit = 199.00
        product4.quantity_in_stock = 10
        product4.save()

    product5, created = Product.get_or_create(
        name="macbook",
        defaults={
            "description": "Apple MacBook Pro with M1 chip and 512GB SSD",
            "price_per_unit": 1499.00,
            "quantity_in_stock": 2,
            "tags": [electronics, apple],
            "categories": [electronics, apple],
        },
    )
    print(f"Product 5 created: {created}")
    if not created:
        product5.description = "Apple MacBook Pro with M1 chip and 1TB SSD"
        product5.price_per_unit = 1699.00
        product5.quantity_in_stock = 5
        product5.save()

    

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

    iphone, created = Tag.get_or_create(name="iPhone")
    if not created:
        iphone.name = "iPhone. Updated"
        print(f"Tag iPhone updated: {created}")

    airpods, created = Tag.get_or_create(name="AirPods")
    if not created:
        airpods.name = "AirPods. Updated"
        print(f"Tag AirPods updated: {created}")

    wireless, created = Tag.get_or_create(name="Wireless")
    if not created:
        wireless.name = "Wireless. Updated"
        print(f"Tag Wireless updated: {created}")


    # Sample data to create purchases
    # User emma buys an iPhone 13
    create_purchase(emma.id, product1.id, 1)

    # User dan buys AirPods Pro
    create_purchase(dan.id, product2.id, 2)

    # User bob buys MacBook Pro
    create_purchase(bob.id, product3.id, 1)

    # User alice buys airpods
    create_purchase(alice.id, product4.id, 2)


    # Tagging products
    product_tag1, created = ProductTag.get_or_create(product=product1, tag=iphone, name="ProductTag 1")
    print(f"ProductTag 1 created: {created}")

    product_tag2, created = ProductTag.get_or_create(product=product2, tag=airpods, name="ProductTag 2")
    print(f"ProductTag 2 created: {created}")

    product_tag3, created = ProductTag.get_or_create(product=product2, tag=wireless, name="ProductTag 3")
    print(f"ProductTag 3 created: {created}")

    product_tag4, created = ProductTag.get_or_create(product=product3, tag=laptops, name="ProductTag 4")
    print(f"ProductTag 4 created: {created}")

    product_tag5, created = ProductTag.get_or_create(product=product3, tag=apple, name="ProductTag 5")
    print(f"ProductTag 5 created: {created}")

    product_tag6, created = ProductTag.get_or_create(product=product4, tag=airpods, name="ProductTag 6")
    print(f"ProductTag 6 created: {created}")

    product_tag7, created = ProductTag.get_or_create(product=product4, tag=wireless, name="ProductTag 7")
    print(f"ProductTag 7 created: {created}")

    product_tag8, created = ProductTag.get_or_create(product=product5, tag=laptops, name="ProductTag 8")
    print(f"ProductTag 8 created: {created}")

    product_tag9, created = ProductTag.get_or_create(product=product5, tag=apple, name="ProductTag 9")
    print(f"ProductTag 9 created: {created}")


    # Users owning products
    user_product1, created = UserProduct.get_or_create(user=emma, product=product1, quantity=1)
    print(f"UserProduct 1 created: {created}")

    user_product2, created = UserProduct.get_or_create(user=dan, product=product2, quantity=2)
    print(f"UserProduct 2 created: {created}")

    user_product3, created = UserProduct.get_or_create(user=bob, product=product3, quantity=1)
    print(f"UserProduct 3 created: {created}")

    user_product4, created = UserProduct.get_or_create(user=alice, product=product4, quantity=3)
    print(f"UserProduct 4 created: {created}")

    user_product5, created = UserProduct.get_or_create(user=max, product=product5, quantity=1)
    print(f"UserProduct 5 created: {created}")


# Call database
create_database()


# Call the populate function to populate the database
populate_test_database()


# Call the display_all_users function to display all users in the database
display_all_users()


# Call display all products
display_all_products()


# Call all purchases
display_all_purchases()


# call all tags 
display_all_tags()


# Call all products by tag
display_all_products_by_tag("Electronics, Apple, Wireless, AirPods, Headphones, Laptops, iPhone, AirPods Pro, MacBook Pro")


# Call all user products
display_all_user_products()


print("Test database created and populated successfully.")
