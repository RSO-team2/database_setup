import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def make_tables():
    """
    Creates necessary tables for the database if they do not already exist.
    The tables created are:
    - menu_items: Stores menu items with id and name.
    - restaurants: Stores restaurant information with id, name, and type.
    - menus: Stores menus with id, restaurant_id, and items.
    - users: Stores user information with user_id, user_name, user_email, user_password, and user_address.
    - order_statuses: Stores order statuses with id and status.
    - orders: Stores order information with id, customer_id, order_date, total_amount, items, restaurant_id, status, and delivery_address.
    Inserts initial order statuses into the order_statuses table.
    Returns:
        tuple: A tuple containing the database connection and cursor.
    """
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    print("Creating items table...")
    cursor.execute("DROP TABLE IF EXISTS menu_items CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price DECIMAL(10, 2),
            image VARCHAR(255)
        );
        """
    )

    print("Creating restaurants table...")
    cursor.execute("DROP TABLE IF EXISTS restaurants CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS restaurants (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            type VARCHAR(255),
            rating DECIMAL(3, 2),
            address VARCHAR(255),
            average_time INT,
            price_range INT,
            image VARCHAR(255)
        );
        """
    )

    print("Creating menus table...")
    cursor.execute("DROP TABLE IF EXISTS menus CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS menus (
            id SERIAL PRIMARY KEY,
            restaurant_id INT references restaurants(id),
            items INT[]
        );
        """
    )

    print("Creating user types table...")
    cursor.execute("DROP TABLE IF EXISTS user_types CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_types (
            id SERIAL PRIMARY KEY,
            type VARCHAR(255)
        );
        """
    )

    cursor.execute(
        """
        INSERT INTO user_types (type) VALUES ('restaurant');
        INSERT INTO user_types (type) VALUES ('courier');
        INSERT INTO user_types (type) VALUES ('customer');
        """
    )

    print("Creating users table...")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_email VARCHAR(255) NOT NULL,
            user_password TEXT NOT NULL,
            user_address TEXT NOT NULL,
            user_type INT references user_types(id)
            );
        """
    )

    print("Creating order statuses table...")
    cursor.execute("DROP TABLE IF EXISTS order_statuses CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_statuses (
            id SERIAL PRIMARY KEY,
            status VARCHAR(255)
        );
        """
    )

    cursor.execute(
        """
        INSERT INTO order_statuses (status) VALUES ('pending');
        INSERT INTO order_statuses (status) VALUES ('processing');
        INSERT INTO order_statuses (status) VALUES ('delivered');
        """
    )

    print("Creating orders table...")
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_id INT references users(user_id),
            order_date TIMESTAMP,
            total_amount DECIMAL(10, 2),
            items INT[],
            restaurant_id INT references restaurants(id),
            status INT references order_statuses(id),
            delivery_address VARCHAR(255)
        );
        """
    )

    print("Creating reservation table...")
    cursor.execute("DROP TABLE IF EXISTS reservations CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id SERIAL PRIMARY KEY,
            customer_id INT references users(user_id),
            restaurant_id INT references restaurants(id),
            make_date TIMESTAMP,
            reservation_date TIMESTAMP,
            num_persons INT,
            optional_message VARCHAR(255)
        );
        """
    )

    cursor.execute(
        "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
    )
    print("The databse cluster contains the following tables:")
    print(cursor.fetchall())

    return conn, cursor
