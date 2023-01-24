import sqlite3
import json
from models import Species

def get_all_species(query_params):
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
            z.id,
            z.name 
        FROM Species z
        {sort_by}
        """


        db_cursor.execute(sql_to_execute)

        # Initialize an empty list to hold all snake representations
        species = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an owner instance from the current row
            specie = Species(row['id'], row['name'])

        

    # Add the dictionary representation of the animal to the list
            species.append(specie.__dict__)

    return species

def get_single_species(id):
    # Open a connection to the database
    with sqlite3.connect("./snake.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            z.id,
            z.name 
        FROM Species z
        WHERE z.id = ?
        """, ( id, ))


        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

       
        
        specie = Species(data['id'], data['name'])
        
        return specie.__dict__
