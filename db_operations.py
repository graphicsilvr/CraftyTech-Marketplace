import logging

import bcrypt
from peewee import IntegrityError

from models import ProductTag
from models import Purchase
from models import UserProduct
from models import db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_product(name, description, price, quantity):
    """
    Create a product with validations.
    """
    # Validate product name
    if not name or len(name.strip()) == 0 or len(name) > 255:
        raise ValueError("Invalid product name.")
    
    # Validate product description
    if not description or len(description.strip()) == 0 or len(description) > 1000:
        raise ValueError("Invalid product description.")
    
    # Validate product price
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Price must be a positive number.")
    
    # Validate product quantity
    if not isinstance(quantity, int) or quantity < 0:
        raise ValueError("Quantity must be a non-negative integer.")
    
    # Create the product in the database
    try:
        return Product.create(
            name=name,
            description=description,
            price_per_unit=price,
            quantity_in_stock=quantity,
        )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return None


def create_tag(name):
    try:
        return Tag.create(name=name)
    except IntegrityError as e:
        logger.error(f"Error creating tag: {e}")
        return None


def create_user_product(user_id, product_id):
    try:
        user = User.get(id=user_id)
        product = Product.get(id=product_id)
        user_product = UserProduct.create(user=user, product=product)
        user_product.save()
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
    
def create_bulk_user_products(users, product_name):
    for user_name in users:
        user = User.get(User.username == user_name)
        product = Product.get(Product.name == product_name)
        create_user_product(user.id, product.id)
        logger.info(f"UserProduct record created for user {user_name} and product {product_name}")

def create_database():
    with db.atomic():
        db.create_tables([User, Product, Tag, ProductTag, Purchase, UserProduct])


def list_user_products_by_user(user_id):
    user_products = UserProduct.select().where(UserProduct.user == user_id)
    for user_product in user_products:
        print(user_product.user.username, user_product.product.name, user_product.quantity)

def list_user_products_by_product(product_id):
    user_products = UserProduct.select().where(UserProduct.product == product_id)
    for user_product in user_products:
        print(user_product.user.username, user_product.product.name, user_product.quantity)

def add_product_to_catalog():
    product = create_product("Test Product", "This is a test product.", 10.99, 5)
    if product:
        print(f"Product {product.name} created")
    else:
        print("Error creating product")

def add_product_to_user(user_id, product_id, quantity):
    """
    Handle product purchase with validations.
    """
    # Validate user existence
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ValueError("User not found.")
    
    # Validate product existence
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        raise ValueError("Product not found.")
    
    # Validate purchase quantity
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Purchase quantity must be a positive integer.")
    
    # Check stock availability
    if product.quantity < quantity:
        raise ValueError("Requested quantity exceeds available stock.")
    
    # Create a new UserProduct entry
    user_product = UserProduct.create(
        user=user,
        product=product,
        quantity=quantity,
    )
    
    # Update the product quantity in the database
    product.quantity -= quantity
    product.save()
    
    return f"Successfully created UserProduct with ID {user_product.id}."

def create_product_tag(product_id, tag_id):
    # Importing necessary models and exceptions
    from models import Product, Tag, ProductTag
    from peewee import DoesNotExist

    # Checking if the product exists
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."

    # Checking if the tag exists
    try:
        tag = Tag.get_by_id(tag_id)
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."

    # Creating a new ProductTag entry
    product_tag = ProductTag.create(product=product, tag=tag, name=f"{product.name}_{tag.name}")

    return f"Successfully created ProductTag with ID {product_tag.id}."


def create_purchase(user_id, product_id, quantity):
    # Importing necessary models and exceptions
    from models import User, Product, Purchase
    from peewee import DoesNotExist

    # Checking if the user exists
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        return f"User with ID {user_id} does not exist."

    # Checking if the product exists and getting its price
    try:
        product = Product.get_by_id(product_id)
        product_price = product.price  # Assuming Product model has a price attribute
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."

    # Calculating the total amount for the purchase
    total_amount = product_price * quantity

    # Creating a new Purchase entry
    purchase_entry = Purchase.create(user=user, product=product, quantity=quantity, amount=total_amount)

    return f"Successfully created Purchase with ID {purchase_entry.id}."

def purchase_product(buyer_id, seller_id, product_id, quantity):
    """
    Handle product purchase with validations.
    """
    # Validate buyer existence
    buyer = User.get_or_none(User.id == buyer_id)
    if not buyer:
        raise ValueError("Buyer not found.")
    
    # Validate seller existence
    seller = User.get_or_none(User.id == seller_id)
    if not seller:
        raise ValueError("Seller not found.")
    
    # Validate product existence
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        raise ValueError("Product not found.")
    
    # Validate purchase quantity
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Purchase quantity must be a positive integer.")
    
    # Check stock availability
    if product.quantity < quantity:
        raise ValueError("Requested quantity exceeds available stock.")
    
    # Calculate the total amount for the purchase
    total_amount = product.price * quantity
    
    # Create a new Purchase entry
    purchase_entry = Purchase.create(
        buyer=buyer,
        seller=seller,
        product=product,
        quantity=quantity,
        amount=total_amount,
    )
    
    # Update the product quantity in the database
    product.quantity -= quantity
    product.save()
    
    return f"Successfully created Purchase with ID {purchase_entry.id}."


def remove_tag_from_product(product_id, tag_id):
    # Importing necessary models and exceptions
    from models import Product, Tag, ProductTag
    from peewee import DoesNotExist

    # Checking if the product exists
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."

    # Checking if the tag exists
    try:
        tag = Tag.get_by_id(tag_id)
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."

    # Checking if an association exists between the product and tag
    try:
        product_tag_association = ProductTag.get((ProductTag.product == product) & (ProductTag.tag == tag))
        product_tag_association.delete_instance()
        return f"Successfully removed association between Product {product_id} and Tag {tag_id}."
    except DoesNotExist:
        return f"No association exists between Product {product_id} and Tag {tag_id}."


def remove_product(product_id):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Checking if the product exists
    try:
        product = Product.get_by_id(product_id)
        product.delete_instance()
        return f"Successfully removed Product with ID {product_id}."
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."


def add_tag_to_product(product_id, tag_id):
    # Importing necessary models and exceptions
    from models import Product, Tag, ProductTag
    from peewee import DoesNotExist

    # Checking if the product exists
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."

    # Checking if the tag exists
    try:
        tag = Tag.get_by_id(tag_id)
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."

    # Checking if an association already exists between the product and tag
    try:
        existing_association = ProductTag.get((ProductTag.product == product) & (ProductTag.tag == tag))
        return f"Association already exists between Product {product_id} and Tag {tag_id}."
    except DoesNotExist:
        # Creating a new ProductTag entry
        product_tag = ProductTag.create(product=product, tag=tag, name=f"{product.name}_{tag.name}")
        return f"Successfully added tag {tag_id} to Product {product_id}."


def update_tag(tag_id, **tag_details):
    """
    Updates the details of a tag with the given ID using the provided arguments.
    """
    try:
        tag = Tag.get_by_id(tag_id)
        
        # Updating the tag details based on provided arguments
        for key, value in tag_details.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        tag.save()
        
        return f"Successfully updated Tag with ID {tag_id}."
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."


from models import Tag


def delete_tag(tag_id):
    """
    Deletes the tag with the given ID from the database.
    """
    try:
        tag = Tag.get_by_id(tag_id)
        tag.delete_instance()
        return f"Successfully deleted Tag with ID {tag_id}."
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."


def search(keyword):
    # Importing necessary models
    from models import Product

    # Searching for products with names containing the keyword
    matching_products = Product.select().where(Product.name.contains(keyword))

    # Returning the list of matching products or a message if no matches are found
    if matching_products:
        return [product.name for product in matching_products]
    else:
        return f"No products found matching the keyword '{keyword}'."


from models import Product


def get_product_details(product_id):
    """
    Retrieves the details of a product with the given ID from the database.
    """
    try:
        product = Product.get_by_id(product_id)
        product_details = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            # Other fields can be added as needed
        }
        return product_details
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."

    # Importing necessary models
    from models import Product

    # Querying the database to retrieve all products
    products = Product.select()
    
    # Creating a list of product details
    product_list = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]

    return product_list if product_list else "No products found in the database."


def get_user_purchases(user_id):
    # Importing necessary models and exceptions
    from models import User, Purchase
    from peewee import DoesNotExist

    # Checking if the user exists
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        return f"User with ID {user_id} does not exist."

    # Querying the database to retrieve all purchases made by this user
    user_purchases = Purchase.select().where(Purchase.user == user)
    
    # Creating a list of purchase details
    purchase_list = [
        {
            'purchase_id': purchase.id, 
            'product_id': purchase.product.id, 
            'product_name': purchase.product.name, 
            'quantity': purchase.quantity,
            'amount': purchase.amount
        } 
        for purchase in user_purchases
    ]

    return purchase_list if purchase_list else f"No purchases found for user with ID {user_id}."


def get_purchase_details(purchase_id):
    # Importing necessary models and exceptions
    from models import Purchase
    from peewee import DoesNotExist

    # Checking if the purchase exists and retrieving its details
    try:
        purchase = Purchase.get_by_id(purchase_id)
        purchase_details = {
            'id': purchase.id,
            'user_id': purchase.user.id,
            'user_name': purchase.user.name,
            'product_id': purchase.product.id,
            'product_name': purchase.product.name,
            'quantity': purchase.quantity,
            'amount': purchase.amount,
            # Other fields can be added as needed
        }
        return purchase_details
    except DoesNotExist:
        return f"Purchase with ID {purchase_id} does not exist."


def get_tag_details(tag_id):
    # Importing necessary models and exceptions
    from models import Tag
    from peewee import DoesNotExist

    # Checking if the tag exists and retrieving its details
    try:
        tag = Tag.get_by_id(tag_id)
        tag_details = {
            'id': tag.id,
            'name': tag.name,
            'description': tag.description,
            # Other fields can be added as needed
        }
        return tag_details
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."


def get_user_details(user_id):
    """
    Retrieves the details of a user with the given ID from the database.
    """
    try:
        user = User.get_by_id(user_id)
        user_details = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,  # Usually, we wouldn't return the password, but it's included here for completion
            # Other fields can be added as needed
        }
        return user_details
    except DoesNotExist:
        return f"User with ID {user_id} does not exist."

    # Importing necessary models
    from models import User

    # Querying the database to retrieve all users
    users = User.select()
    
    # Creating a list of user details
    user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]

    return user_list if user_list else "No users found in the database."


def delete_user(user_id):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    # Checking if the user exists
    try:
        user = User.get_by_id(user_id)
        user.delete_instance()
        return f"Successfully deleted User with ID {user_id}."
    except DoesNotExist:
        return f"User with ID {user_id} does not exist."


def update_user(user_id, **kwargs):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    # Checking if the user exists and updating its details
    try:
        user = User.get_by_id(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return f"Successfully updated User with ID {user_id}."
    except DoesNotExist:
        return f"User with ID {user_id} does not exist."
    except AttributeError:
        return f"Invalid field provided for update."


def add_product_to_user(user_id, product_id, quantity):
    """
    Associate a product with a user with validations.
    """
    # Validate user existence
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ValueError("User not found.")
    
    # Validate product existence
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        raise ValueError("Product not found.")
    
    # Validate quantity
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")
    
    # Check if the user already has the product in their inventory
    user_product = UserProduct.get_or_none(UserProduct.user == user, UserProduct.product == product)
    if user_product:
        # If the user already has the product, update the quantity
        user_product.quantity += quantity
        user_product.save()
        return f"Successfully updated UserProduct with ID {user_product.id}."
    else:
        # If the user does not have the product, create a new UserProduct entry
        user_product = UserProduct.create(user=user, product=product, quantity=quantity)
        return f"Successfully created UserProduct with ID {user_product.id}."


def delete_product(product_id):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Checking if the product exists and deleting it
    try:
        product = Product.get_by_id(product_id)
        product.delete_instance()
        return f"Successfully deleted Product with ID {product_id}."
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."


def update_product(product_id, **kwargs):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Checking if the product exists and updating its details
    try:
        product = Product.get_by_id(product_id)
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.save()
        return f"Successfully updated Product with ID {product_id}."
    except DoesNotExist:
        return f"Product with ID {product_id} does not exist."
    except AttributeError:
        return f"Invalid field provided for update."

    # Importing necessary models
    from models import Product

    # Querying the database to retrieve all products
    products = Product.select()
    
    # Creating a list of product details
    product_list = [
        {
            'id': product.id, 
            'name': product.name, 
            'description': product.description, 
            'price': product.price
        } 
        for product in products
    ]

    return product_list if product_list else "No products found in the database."


def add_tag(name, description):
    # Importing necessary models and exceptions
    from models import Tag

    # Adding the new tag to the database
    try:
        new_tag = Tag.create(name=name, description=description)
        return f"Successfully added new tag with ID {new_tag.id}."
    except Exception as e:
        return f"Error adding tag: {str(e)}."


def delete_tag(tag_id):
    # Importing necessary models and exceptions
    from models import Tag
    from peewee import DoesNotExist

    # Checking if the tag exists and deleting it
    try:
        tag = Tag.get_by_id(tag_id)
        tag.delete_instance()
        return f"Successfully deleted Tag with ID {tag_id}."
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."


def update_tag(tag_id, **kwargs):
    # Importing necessary models and exceptions
    from models import Tag
    from peewee import DoesNotExist

    # Checking if the tag exists and updating its details
    try:
        tag = Tag.get_by_id(tag_id)
        for key, value in kwargs.items():
            setattr(tag, key, value)
        tag.save()
        return f"Successfully updated Tag with ID {tag_id}."
    except DoesNotExist:
        return f"Tag with ID {tag_id} does not exist."
    except AttributeError:
        return f"Invalid field provided for update."


def list_tags():
    # Importing necessary models
    from models import Tag

    # Querying the database to retrieve all tags
    tags = Tag.select()
    
    # Creating a list of tag details
    tag_list = [{'id': tag.id, 'name': tag.name, 'description': tag.description} for tag in tags]

    return tag_list if tag_list else "No tags found in the database."


def add_product_tag(product_id, tag_id):
    # Importing necessary models and exceptions
    from models import Product, Tag, ProductTag
    from peewee import DoesNotExist

    # Associating the product with the tag
    try:
        # Checking if the product and tag exist
        product = Product.get_by_id(product_id)
        tag = Tag.get_by_id(tag_id)
        
        # Creating the association in the ProductTag table
        product_tag_association = ProductTag.create(product=product, tag=tag)
        
        return f"Successfully associated Product ID {product_id} with Tag ID {tag_id}."
    except DoesNotExist:
        return f"Either Product ID {product_id} or Tag ID {tag_id} does not exist."
    except Exception as e:
        return f"Error associating product with tag: {str(e)}."


def delete_product_tag(product_id, tag_id):
    # Importing necessary models and exceptions
    from models import Product, Tag, ProductTag
    from peewee import DoesNotExist

    # Removing the association between the product and the tag
    try:
        # Checking if the product and tag exist
        product = Product.get_by_id(product_id)
        tag = Tag.get_by_id(tag_id)
        
        # Finding and deleting the association in the ProductTag table
        product_tag_association = ProductTag.get((ProductTag.product == product) & (ProductTag.tag == tag))
        product_tag_association.delete_instance()
        
        return f"Successfully removed association of Product ID {product_id} with Tag ID {tag_id}."
    except DoesNotExist:
        return f"No association found between Product ID {product_id} and Tag ID {tag_id}."
    except Exception as e:
        return f"Error removing association between product and tag: {str(e)}."


def list_product_tags(product_id):
    # Importing necessary models and exceptions
    from models import Product, ProductTag, Tag
    from peewee import DoesNotExist

    # Retrieving a list of tags associated with the specified product
    try:
        product = Product.get_by_id(product_id)
        
        # Querying the ProductTag table for the associated tags
        associated_tags = (Tag.select()
                           .join(ProductTag)
                           .join(Product)
                           .where(Product.id == product_id))
        
        # Creating a list of tag details
        tag_list = [{'id': tag.id, 'name': tag.name, 'description': tag.description} for tag in associated_tags]

        return tag_list if tag_list else f"No tags found for Product ID {product_id}."
    except DoesNotExist:
        return f"Product ID {product_id} does not exist."


def login(username, password):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    # Attempting to authenticate the user
    try:
        user = User.get(User.username == username)
        if user.password == password:  # Note: This is insecure and just for demonstration.
            return f"Login successful for user: {username}."
        else:
            return f"Incorrect password for user: {username}."
    except DoesNotExist:
        return f"User with username {username} does not exist."


def register(username, password, email):
    # Importing necessary models and exceptions
    from models import User
    from peewee import IntegrityError

    # Attempting to register the user
    try:
        new_user = User.create(username=username, password=password, email=email)  # Insecure password storage
        return f"User {username} successfully registered."
    except IntegrityError:
        return f"User with username {username} or email {email} already exists."


def logout():
    # In this basic implementation, we'll assume there's an in-memory variable or cache that tracks the logged-in user.
    # This variable will be reset/cleared during logout.
    
    logged_in_user = None  # This is a placeholder. In a real-world application, this might be a global or context variable.
    
    if logged_in_user:
        logged_in_user = None
        return f"Successfully logged out."
    else:
        return f"No user is currently logged in."


def place_order(user_id, product_id, quantity):
    # Importing necessary models and exceptions
    from models import User, Product, Purchase
    from peewee import DoesNotExist, IntegrityError

    # Attempting to place the order
    try:
        user = User.get_by_id(user_id)
        product = Product.get_by_id(product_id)
        
        # Check if enough stock is available
        if product.stock < quantity:
            return f"Not enough stock for Product ID {product_id}. Available stock: {product.stock}"
        
        # Create the order record (using the Purchase model in this case)
        purchase = Purchase.create(user=user, product=product, quantity=quantity)
        
        # Deduct the stock of the product
        product.stock -= quantity
        product.save()
        
        return f"Order successfully placed for Product ID {product_id}. Quantity: {quantity}"
    except DoesNotExist:
        return f"Either User ID {user_id} or Product ID {product_id} does not exist."
    except IntegrityError as e:
        return f"Error placing order: {str(e)}."


def list_orders(user_id=None):
    # Importing necessary models and exceptions
    from models import User, Purchase
    from peewee import DoesNotExist

    # Attempting to list the orders
    try:
        # Base query for all orders
        orders_query = Purchase.select()
        
        # If a user_id is provided, filter orders for that user
        if user_id:
            user = User.get_by_id(user_id)
            orders_query = orders_query.where(Purchase.user == user)
        
        # Fetching the orders and associated details
        orders_list = []
        for order in orders_query:
            order_details = {
                'order_id': order.id,
                'user': order.user.username,
                'product': order.product.name,
                'quantity': order.quantity
            }
            orders_list.append(order_details)
        
        return orders_list if orders_list else f"No orders found for User ID {user_id}." if user_id else "No orders found."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error listing orders: {str(e)}."


def get_order_details(order_id):
    # Importing necessary models and exceptions
    from models import Purchase
    from peewee import DoesNotExist

    # Attempting to fetch the order details
    try:
        order = Purchase.get_by_id(order_id)
        order_details = {
            'order_id': order.id,
            'user': order.user.username,
            'product': order.product.name,
            'quantity': order.quantity
        }
        
        return order_details
    except DoesNotExist:
        return f"Order ID {order_id} does not exist."
    except Exception as e:
        return f"Error fetching order details: {str(e)}."


def add_stock(product_id, quantity):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Attempting to add stock to the specified product
    try:
        product = Product.get_by_id(product_id)
        product.stock += quantity
        product.save()
        
        return f"Stock successfully updated for Product ID {product_id}. New stock: {product.stock}."
    except DoesNotExist:
        return f"Product ID {product_id} does not exist."
    except Exception as e:
        return f"Error updating stock: {str(e)}."


def reduce_stock(product_id, quantity):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Attempting to reduce stock of the specified product
    try:
        product = Product.get_by_id(product_id)
        
        # Check if enough stock is available to reduce
        if product.stock < quantity:
            return f"Not enough stock for Product ID {product_id}. Available stock: {product.stock}"
        
        product.stock -= quantity
        product.save()
        
        return f"Stock successfully reduced for Product ID {product_id}. New stock: {product.stock}."
    except DoesNotExist:
        return f"Product ID {product_id} does not exist."
    except Exception as e:
        return f"Error reducing stock: {str(e)}."
    

def list_products():
    # Importing necessary models and exceptions
    from models import Product

    # Fetching the list of products
    products_query = Product.select()
    
    # Fetching the products and associated details
    products_list = []
    for product in products_query:
        product_details = {
            'product_id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        }
        products_list.append(product_details)
    
    return products_list if products_list else "No products available."

def get_product_details(product_id):
    # Importing necessary models and exceptions
    from models import Product
    from peewee import DoesNotExist

    # Attempting to fetch the product details
    try:
        product = Product.get_by_id(product_id)
        product_details = {
            'product_id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        }
        
        return product_details
    except DoesNotExist:
        return f"Product ID {product_id} does not exist."
    except Exception as e:
        return f"Error fetching product details: {str(e)}."

def get_user_details(user_id):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    # Attempting to fetch the user details
    try:
        user = User.get_by_id(user_id)
        user_details = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'password': '********',  # It's a good practice not to expose password details
            'admin': user.admin
        }
        
        return user_details
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error fetching user details: {str(e)}."

def list_users():
    # Importing necessary models
    from models import User

    # Fetching the list of users
    users_query = User.select()
    
    # Fetching the users and associated details
    users_list = []
    for user in users_query:
        user_details = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'admin': user.admin
        }
        users_list.append(user_details)
    
    return users_list if users_list else "No users available."

def authenticate_user(username, password):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    # Attempting to authenticate the user
    try:
        user = User.get(User.username == username)
        
        # Comparing the provided password with the stored one
        if user.password == password:
            return f"User {username} authenticated successfully."
        else:
            return f"Incorrect password for user {username}."
    except DoesNotExist:
        return f"User {username} does not exist."
    except Exception as e:
        return f"Error during authentication: {str(e)}."

def create_user(username, name, email, password, address, zipcode, city, state, country, billing_name, billing_account, admin=False):
    """
    Creates a new user with the given information.
    """
    hashed_password = hash_password(password)
    user_instance = User.create(
        username=username,
        name=name,
        email=email,
        password=hashed_password.decode('utf-8'),
        address=address,
        zipcode=zipcode,
        city=city,
        state=state,
        country=country,
        billing_name=billing_name,
        billing_account=billing_account,
        admin=admin
    )
    return user_instance


import inspect

# Importing necessary modules
from models import User
from peewee import DoesNotExist

def create_user(name, email, password):
    """
    Creates a new user with the given name, email, and password.
    """
    try:
        user = User.create(name=name, email=email, password=password)
        return f"Successfully created User with ID {user.id}."
    except Exception as e:
        return f"Error creating user: {str(e)}."

# Implementing the create_user function
def create_user(username, email, password, admin=False):
    try:
        # Checking if a user with the same username or email already exists
        existing_user = User.get((User.username == username) | (User.email == email))
        return "A user with the same username or email already exists."
    except DoesNotExist:
        # Hashing the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Creating a new user entry in the database
        new_user = User.create(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            admin=admin
        )
        return f"User {username} created successfully with ID {new_user.id}."
    except Exception as e:
        return f"Error creating user: {str(e)}."
    

# Implementing the update_user_password function
def update_user_password(user_id, new_password):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist
    import bcrypt

    try:
        # Querying the database to find the specified user
        user = User.get_by_id(user_id)
        
        # Hashing the new password using bcrypt
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Updating the user's password in the database
        user.password = hashed_new_password.decode('utf-8')
        user.save()
        
        return f"Password updated successfully for User ID {user_id}."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error updating password: {str(e)}."

db_operations_updated_content_list = [ "\n\n", inspect.getsource(create_user) ] 
db_operations_updated_content = "".join(db_operations_updated_content_list)
print(inspect.getsource(create_user))

# Displaying the implemented function for review
inspect.getsource(update_user_password)

def update_user_password(user_id, new_password):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist
    import bcrypt

    try:
        # Querying the database to find the specified user
        user = User.get_by_id(user_id)
        
        # Hashing the new password using bcrypt
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Updating the user's password in the database
        user.password = hashed_new_password.decode('utf-8')
        user.save()
        
        return f"Password updated successfully for User ID {user_id}."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error updating password: {str(e)}."

# Implementing the update_user_admin_status function
def update_user_admin_status(user_id, admin_status):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    try:
        # Querying the database to find the specified user
        user = User.get_by_id(user_id)
        
        # Updating the user's admin status in the database
        user.admin = admin_status
        user.save()
        
        admin_status_text = "admin" if admin_status else "non-admin"
        return f"Admin status updated to {admin_status_text} for User ID {user_id}."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error updating admin status: {str(e)}."

# Adding this function to the db_operations_updated_content
db_operations_updated_content += "\n\n" + inspect.getsource(update_user_admin_status)

# Displaying the implemented function for review
inspect.getsource(update_user_admin_status)

def update_user_admin_status(user_id, admin_status):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    try:
        # Querying the database to find the specified user
        user = User.get_by_id(user_id)
        
        # Updating the user's admin status in the database
        user.admin = admin_status
        user.save()
        
        admin_status_text = "admin" if admin_status else "non-admin"
        return f"Admin status updated to {admin_status_text} for User ID {user_id}."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error updating admin status: {str(e)}."

def delete_user(user_id):
    # Importing necessary models and exceptions
    from models import User
    from peewee import DoesNotExist

    try:
        # Querying the database to find the specified user
        user = User.get_by_id(user_id)
        
        # Deleting the user's entry from the database
        user.delete_instance()
        
        return f"User ID {user_id} deleted successfully."
    except DoesNotExist:
        return f"User ID {user_id} does not exist."
    except Exception as e:
        return f"Error deleting user: {str(e)}."
    

def initialize_database():
    db.connect()  # Connect to the database
    # Create tables if they don't exist with safe=True
    db.create_tables([User, Product, Tag, ProductTag, Purchase, UserProduct], safe=True)
    db.close()  # Close the connection

def are_tables_initialized():
    required_tables = [User, Product, Tag, ProductTag, Purchase, UserProduct]
    for table in required_tables:
        if not table.table_exists():
            return False
    return True


def get_user_by_id(buyer_id):
    return None


def get_user_by_id(buyer_id):
    return None


def get_user_by_username(param):
    return None