from create_tables import make_tables
from populate_tables import populate_tables

if __name__  == "__main__":
    conn, cursor = make_tables()
    populate_tables(conn, cursor)

    conn.commit()
    cursor.close()
    conn.close()