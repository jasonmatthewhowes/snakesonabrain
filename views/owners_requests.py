import sqlite3
import json
from models import Owner

def get_all_owners(query_params):
    # Open a connection to the database
    with sqlite3.connect("./snake.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""

        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

        # Write the SQL query to get the information you want
        sql_to_execute = f"""
        SELECT
            o.id,
            o.first_name,
            o.last_name,
            o.email
            
        FROM Owners o
        {sort_by}
        """


        db_cursor.execute(sql_to_execute)

        # Initialize an empty list to hold all owner representations
        owners = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an owner instance from the current row
            owner = Owner(row['id'], row['first_name'], row['last_name'], row['email'])

        

    # Add the dictionary representation of the animal to the list
            owners.append(owner.__dict__)

    return owners

def get_single_owner(id):
    # Open a connection to the database
    with sqlite3.connect("./snake.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.first_name,
            o.last_name,
            o.email
            
        FROM Owners o
        WHERE o.id = ?
        """, ( id, ))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        owner = Owner(data['id'], data['first_name'], data['last_name'], data['email'])
        return owner.__dict__
