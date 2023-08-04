# Helper Functions for creating a new ticket
#
# Author:   Sierra Bonilla
# Date:     01-08-2023

import mysql.connector
import json
from datetime import datetime 
from connect_to_db import connect_to_mysql, get_creds
from create_user import create_user_if_not_exists

def ticket_exists(connection, ticket_number_str):
    """
    Checks if ticket with the specified ticket number exists.

    :param
        connection (mysql.connector.Connection): A connection object to the MySQL database.
        ticket_number_str (str): The ticket number in the format of '001234'.
        
    :return
         tuple: A tuple containing two elements:
            - The first element is a bool, True if the ticket exists, False otherwise.
            - The second element is the ticket_id if the ticket exists, or None if it doesn't.

    :raises
        mysql.connector.Error: If an error occurs while executing the query.
    """
    try:
        # create a cursor object to execute select query
        cursor = connection.cursor()
        
        # Select from ost_ticket
        select_query = "SELECT ticket_id FROM ost_ticket WHERE number=%s"
        cursor.execute(select_query, (ticket_number_str, ))

        # Fetch the result 
        result = cursor.fetchone()

        if result is not None:
            # Close the cursor
            cursor.close()
            return True, result[0]
        else:
            # Close the cursor
            cursor.close()
            return False, None
    
    except mysql.connector.Error as error:

        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error
    
def check_key_in_json_file(key, file_path):
    """
    Checks if a key is present in a JSON-like text file and if so, returns the value at that key.

    :param
        key (str): The key to check in the JSON data.
        file_path (str): The path to the JSON-like text file.

    :return
        tuple: A tuple containing two elements:
            - The first element is a bool, True if the key is present, False otherwise.
            - The second element is the value associated with the key, or None if the key is not present.

    :raises
        FileNoteFoundError: If the specified file does not exist. 
    """
    try: 
        with open(file_path, 'r') as file:
            data = file.read()
            json_data = json.loads(data)
            if key in json_data:
                return True, json_data[key]
            else:
                return False, None 
    except json.JSONDecodeError as error:
        raise error

