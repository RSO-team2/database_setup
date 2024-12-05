# Database Setup

This repository contains the Python script that sets up the databases for the project of other repositories in this organization. [^1]

To use the provided script the following steps are required:
1. Clone the repository
2. Install the required packages (ensure you have Python and Pip installed)
3. Configure your local `.env` file with the required environment variables:
   1. `DATABASE_URL` - Digital Ocean Managed Postgres Database URL
   2. `OLLAMA_URL` - Ollama URL (requires a local Ollama instance)
   3. `OLLAMA_MODEL` - Ollama model to use
4. Run the `setup.py` script.

## Created Tables

Below are the column definitions of the created tables (subject to change).

### `users`

| Column Name    | #   | Data type    | Identity | Collation | Not Null | Default                                    | 
|----------------|-----|--------------|----------|-----------|----------|--------------------------------------------|
| user_id        | 1   | serial4      | [NULL]   | [NULL]    | true     | nextval('users_user_id_seq'::regclass)     |
| user_name      | 2   | varchar(255) | [NULL]   | default   | true     | [NULL]                                     |
| user_email     | 3   | varchar(255) | [NULL]   | default   | true     | [NULL]                                     |
| user_password  | 5   | text         | [NULL]   | default   | false    | [NULL]                                     |


### `orders`

| Column Name       | #   | Data type       | Identity | Collation | Not Null | Default                           |
|-------------------|-----|-----------------|----------|-----------|----------|-----------------------------------|
| id                | 1   | serial4         | [NULL]   | [NULL]    | true     | nextval('orders_id_seq'::regclass)|
| customer_id       | 2   | int4            | [NULL]   | [NULL]    | false    | [NULL]                            |
| order_date        | 3   | timestamp       | [NULL]   | [NULL]    | false    | [NULL]                            |
| total_amount      | 4   | numeric(10, 2)  | [NULL]   | [NULL]    | false    | [NULL]                            |
| items             | 5   | _int4[]           | [NULL]   | default   | false    | [NULL]                            |
| restaurant_id     | 6   | int4            | [NULL]   | [NULL]    | false    | [NULL]                            |
| status            | 7   | int4            | [NULL]   | [NULL]    | false    | [NULL]                            |
| delivery_address  | 8   | varchar(255)    | [NULL]   | default   | false    | [NULL]                            |


### `order_statuses`

| Column Name | #   | Data type    | Identity | Collation | Not Null | Default                                    |
|-------------|-----|--------------|----------|-----------|----------|--------------------------------------------|
| id          | 1   | serial4      | [NULL]   | [NULL]    | true     | nextval('order_statuses_id_seq'::regclass) |
| status      | 2   | varchar(255) | [NULL]   | default   | false    | [NULL]                                     |


### `restaurants`

| Column Name | #   | Data type    | Identity | Collation | Not Null | Default                                    |
|-------------|-----|--------------|----------|-----------|----------|--------------------------------------------|
| id          | 1   | serial4      | [NULL]   | [NULL]    | true     | nextval('restaurants_id_seq'::regclass)    |
| name        | 2   | varchar(255) | [NULL]   | default   | false    | [NULL]                                     |
| type        | 3   | varchar(255) | [NULL]   | default   | false    | [NULL]                                     |


### `menus`

| Column Name   | #   | Data type | Identity | Collation | Not Null | Default                           |
|---------------|-----|-----------|----------|-----------|----------|-----------------------------------|
| id            | 1   | serial4   | [NULL]   | [NULL]    | true     | nextval('menus_id_seq'::regclass) |
| restaurant_id | 2   | int4      | [NULL]   | [NULL]    | false    | [NULL]                            |
| items         | 3   | _int4[]     | [NULL]   | [NULL]    | false    | [NULL]                            |


### `menu_items`

| Column Name | #   | Data type    | Identity | Collation | Not Null | Default                           |
|-------------|-----|--------------|----------|-----------|----------|-----------------------------------|
| id          | 1   | serial4      | [NULL]   | [NULL]    | true     | nextval('menu_items_id_seq'::regclass) |
| name        | 2   | varchar(255) | [NULL]   | default   | false    | [NULL]                            |
| price       | 3   | numeric(10, 2)  | [NULL]   | [NULL]    | false    | [NULL]                            |


[^1]: [RSO-Team2 Repositories](https://github.com/orgs/RSO-team2/repositories)