import json
import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_food_list(headers, data):
    """
    Fetches a list of dish names for various types of restaurants in JSON format.

    This function sends a POST request to the URL specified in the environment variable "OLLAMA_URL" with the provided headers and data.
    The data should include a prompt asking for an extensive list of dish names for various types of restaurants, structured as JSON.
    The function expects a JSON response containing the list of dishes.

    Args:
        headers (dict): The headers to include in the POST request.
        data (dict): The data to include in the POST request. Must contain a "prompt" key.

    Returns:
        dict: A dictionary where keys are restaurant types and values are lists of dish names.

    Raises:
        Exception: If the response cannot be parsed as JSON or if the request fails.
    """
    data["prompt"] = (
        'Write and extensive list of dish names for various tyes of restaurants. Structure your answer as JSON in the format of `"restaurant_type": [<dishes>]`. Provide only the JSON response. Do not include any other text. Double check that it is valid JSON.'
    )
    response = requests.post(
        os.getenv("OLLAMA_URL"), headers=headers, data=json.dumps(data)
    )
    try:
        food_data = json.loads(response.text)["response"].replace("`", "")
        food_data = json.loads(food_data)
        return food_data
    except:
        return _get_food_list(headers, data)


def _get_resturant_name(headers, data, restaurant_type):
    """
    Generates a fitting name for a restaurant based on the given type.

    Args:
        headers (dict): The headers to include in the POST request.
        data (dict): The data to include in the POST request. This dictionary will be modified to include the prompt.
        restaurant_type (str): The type of restaurant for which to generate a name.

    Returns:
        str: The generated restaurant name.
    """
    data["prompt"] = (
        f"Generate a fitting name for a {restaurant_type} restaurant. Make sure to return only the name in the form of <name>, no extra text."
    )
    response = requests.post(
        os.getenv("OLLAMA_URL"), headers=headers, data=json.dumps(data)
    )
    name = json.loads(response.text)["response"]
    return name


def populate_tables(cursor):
    """
    Populates the database tables with restaurant and menu data.

    Args:
        cursor (psycopg2.cursor): A cursor object to execute database operations.

    The function performs the following steps:
    1. Retrieves a list of food items categorized by restaurant type.
    2. For each restaurant type, it fetches or generates a restaurant name.
    3. Inserts the restaurant name and type into the 'restaurants' table and retrieves the restaurant ID.
    4. For each dish in the restaurant's menu:
        - Checks if the dish already exists in the 'menu_items' table.
        - If it exists, retrieves the item ID.
        - If it does not exist, inserts the dish into the 'menu_items' table and retrieves the new item ID.
    5. Collects all menu item IDs for the restaurant and inserts them into the 'menus' table.

    Note:
        - The function assumes the existence of helper functions `_get_food_list` and `_get_resturant_name`.
        - The function uses environment variables and random values for some operations.
    """
    headers = {
        "Content-Type": "application/json",
    }
    data = {"model": os.getenv("OLLAMA_MODEL"), "stream": False}
    food_data = _get_food_list(headers, data)
    for restaurant_type, dishes in food_data.items():
        name = _get_resturant_name(headers, data, restaurant_type)
        cursor.execute(
            f"INSERT INTO restaurants (name, type, rating, address, average_time, price_range, image) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ID;",
            (
                name,
                restaurant_type,
                random.randint(155, 500) / 100,
                "",
                5 * round(random.randint(15, 60) / 5),
                random.randint(1, 4),
                requests.get("https://foodish-api.com/api/").json()["image"],
            ),
        )
        restaurant_id = cursor.fetchone()[0]
        restaurant_menu_ids = []
        for dish in dishes:
            item_id = None
            cursor.execute("SELECT id FROM menu_items WHERE name = %s;", (dish,))
            if cursor.fetchone():
                item_id = cursor.fetchone()
            else:
                price = round(random.uniform(7.60, 15.80), 2)
                cursor.execute(
                    "INSERT INTO menu_items (name, price, image) VALUES (%s, %s, %s) RETURNING ID;",
                    (
                        dish,
                        price,
                        requests.get("https://foodish-api.com/api/").json()["image"]
                    ),
                )
                item_id = cursor.fetchone()[0]
            restaurant_menu_ids.append(item_id)
        cursor.execute(
            "INSERT INTO menus (restaurant_id, items) VALUES (%s, %s) RETURNING ID;",
            (restaurant_id, restaurant_menu_ids),
        )
