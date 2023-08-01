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
        bool: True if ticket exists, False if the ticket doesn't exist.

    :raises
        mysql.connector.Error: If an error occurs while executing the query.
    """
    try:
        # create a cursor object to execute select query
        cursor = connection.cursor()
        
        # Select from ost_ticket
        select_query = "SELECT * FROM ost_ticket WHERE number=%s"
        cursor.execute(select_query, (ticket_number_str, ))

        # Fetch the result 
        result = cursor.fetchone()

        # Close the cursor
        cursor.close()

        return (result is not None)
    
    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error
