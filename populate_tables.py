import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_food_list(headers, data):
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
    data["prompt"] = f"Generate a fitting name for a {restaurant_type} restaurant. Make sure to return only the name in the form of <name>, no extra text."
    response = requests.post(
        os.getenv("OLLAMA_URL"), headers=headers, data=json.dumps(data)
    )
    name = json.loads(response.text)["response"]
    return name


def populate_tables(conn, cursor):
    headers = {
        "Content-Type": "application/json",
    }
    data = {"model": os.getenv("OLLAMA_MODEL"), "stream": False}
    food_data = _get_food_list(headers, data)
    for restaurant_type, dishes in food_data.items():
        name = _get_resturant_name(headers, data, restaurant_type)
        cursor.execute(
            f"INSERT INTO restaurants (name, type) VALUES (%s, %s) RETURNING ID;", (name, restaurant_type)
        )
        restaurant_id = cursor.fetchone()[0]
        restaurant_menu_ids = []
        for dish in dishes:
            item_id = None
            cursor.execute("SELECT id FROM menu_items WHERE name = %s;", (dish,))
            if cursor.fetchone():
                item_id = cursor.fetchone()
            else:
                cursor.execute("INSERT INTO menu_items (name) VALUES (%s) RETURNING ID;", (dish,)
                )
                item_id = cursor.fetchone()[0]
            restaurant_menu_ids.append(item_id)
        cursor.execute(
            "INSERT INTO menus (restaurant_id, items) VALUES (%s, %s) RETURNING ID;",
            (restaurant_id, restaurant_menu_ids),
        )

