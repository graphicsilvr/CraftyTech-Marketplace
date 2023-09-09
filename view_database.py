
from models import db, Product, User, Tag, ProductTag, Purchase, UserProduct


def view_table(model):
    # Using Peewee to query
    rows = model.select()
    return rows

def main():
    tables = [Product, User, Tag, ProductTag, Purchase, UserProduct]
    for table in tables:
        print(f"Contents of {table.__name__}:")
        rows = view_table(table)
        for row in rows:
            print(row)
        print("\n")

if __name__ == "__main__":
    db.connect()  # Connect to the database

    # Create tables if they don't exist
    db.create_tables([Product, User, Tag, ProductTag, Purchase, UserProduct])

    main()
    db.close()  # Close the connection
