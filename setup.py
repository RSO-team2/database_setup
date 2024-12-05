from create_tables import make_tables
from populate_tables import populate_tables

if __name__  == "__main__":
    conn, cursor = make_tables() # Make blank tables
    populate_tables(cursor) # Populate tables with AI generated data

    conn.commit() # Commit changes
    cursor.close() # Close cursor
    conn.close() # Close connection