# CraftyTech Marketplace (formerly Betsy Electronics)

## Introduction
CraftyTech Marketplace, originally known as Betsy Electronics, is a fictional online platform designed to cater to a wide spectrum of products ranging from consumer electronics. As the platform evolved, its vision expanded to become an intelligent, self-driving marketplace, setting the foundation to function as a PaaS or SaaS platform. Vendors can now offer a plethora of products, from digital software licenses and subscriptions from renowned marketplaces.

This project was initiated to test skills in function writing, SQL joins, and database modeling. It employs a database design for the marketplace using the peewee ORM, consisting of four models: User, Product, Tag, and Transaction.

## Prerequisites
- **Software & Hardware Requirements**:
  - Python 3.6 or higher
  - Peewee ORM library
  - SQLite database
  - Command-line interface or terminal

## SQL Database
CraftyTech uses a SQLite database to store information about users, products, transactions, and tags. Managed using the Peewee ORM, a lightweight ORM library for Python, it provides a simple and intuitive API for SQL database interactions, enabling database queries using Python code.

## Installation and Setup
1. Clone the project repository from GitHub.
2. Ensure Python 3.6 or higher is installed.
3. Install the Peewee ORM library using pip: 
   ```
   pip install peewee
   ```
4. Navigate to the project directory using a terminal or command-line interface.
5. Execute the `main.py` file to initiate the program: 
   ```
   python main.py
   ```

## Models
### User
- Contains name, address data, and billing information.
- A user can own multiple products and is the sole entity that can make purchases.
- Incorporates password management, indicating authentication mechanisms.

### Product and Related Models
- Product, UserProduct, and ProductTag models establish relationships between users, products, and tags.
- Enables functionalities like tagging products and associating products with users.

### Purchase
- Designed to record transactions with details about each purchase.

## Query Utilities
Available in `main.py` are several querying utilities, which include:
- Product search based on a term (case-insensitive).
- Viewing products associated with a user.
- Listing all products linked to a specific tag.
- Adding and removing a product to/from a user.
- Updating the stock quantity of a product.
- Handling transactions between a buyer and seller for a chosen product.

## Implemented Functionality
Based on the files you've provided, we can summarize the functionalities that have been implemented in the CraftyTech application:
- **User Management**: 
  - Register a new user with name, address, and billing information.
  - Retrieve a list of all users.
- **Product Management**: 
  - Create, retrieve, update, and delete products.
  - Each product has attributes like name, description, price per unit, and stock quantity.
- **Tag Management**: 
  - Tags can be associated with products.
  - Create, retrieve, update, and delete tags.
- **Transaction Management**: 
  - Handle purchases between a buyer and a seller for specific products.
  - Track the quantity of purchased items.

## Enhancements and Improvements
- **Enhanced Search**: Extend the search function to include product descriptions.
- **Error Handling**: Properly manage potential errors.
- **Database Connection Management**: Effectively manage database connections.
- **Password Management**: Ensure secure password storage.
- **Product Indexing**: Enhance search performance.
- **Search Autocorrect**: Improve search user experience.
- **Advanced DB Operations**: Ensure comprehensive CRUD operations.

## Debugging Process
The CraftyTech application underwent several iterations of development and debugging to enhance its functionality and ensure a seamless experience for users.

## Ongoing Improvements
The application continues to undergo improvements, focusing on:
- Enhanced logic for creating products, tags, purchases, and other entities.
- Improved error messages for clarity.
- Code updates to replace references from product.price to product.price_per_unit.

## Possible Future Iterations
To further refine the CraftyTech Marketplace, the following enhancements and features are being considered:
- **Frontend Development**: Integrate a web interface or GUI.
- **Enhanced Testing**: Comprehensive testing of all functionalities.
- **Optimization**: Address any performance bottlenecks.
- **Security Measures**: Implement robust security mechanisms.
- **Deployment**: Set up a deployment environment.
- **Documentation**: Create thorough documentation.

## License
Please refer to the [lisence.txt](./lisence.txt) file for details on the licensing of the CraftyTech Marketplace project.