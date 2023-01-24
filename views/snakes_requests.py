import sqlite3
import json
from models import Snake

def get_all_snakes(query_params):
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
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
            
        FROM Snakes s
        {sort_by}
        """


        db_cursor.execute(sql_to_execute)

        # Initialize an empty list to hold all snake representations
        snakes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an owner instance from the current row
            snake = Snake(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])

        

    # Add the dictionary representation of the animal to the list
            snakes.append(snake.__dict__)

    return snakes

def get_single_snake(id):
    # Open a connection to the database
    with sqlite3.connect("./snake.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
            
        FROM Snakes s
        WHERE s.id = ?
        """, ( id, ))


        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

       
        
        snake = Snake(data['id'], data['name'], data['owner_id'], data['species_id'], data['gender'], data['color'])
        
        return snake.__dict__
