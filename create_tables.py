import os

import psycopg2
from dotenv import load_dotenv


def make_tables():
    load_dotenv()

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    print("Creating items table...")
    cursor.execute("DROP TABLE IF EXISTS menu_items CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
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
            type VARCHAR(255)
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

    print("Creating users table...")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_email VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL
            );
        """
    )

    print("Creating order table...")
    cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_id INT references users(user_id),
            order_date DATE,
            total_amount DECIMAL(10, 2),
            items TEXT[],
            restaurant_id INT references restaurants(id),
            status INT
        );
    """
    )

    cursor.execute(
        "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
    )
    print("The databse cluster contains the following tables:")
    print(cursor.fetchall())

    return conn, cursor
