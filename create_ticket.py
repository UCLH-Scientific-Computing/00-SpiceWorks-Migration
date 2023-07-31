# Function for creating a new ticket
#
# Author:   Sierra Bonilla
# Date:     31-07-2023

import mysql.connector
import json
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
        result = cursor.fetchone()[0]

        # Close the cursor and the connection 
        cursor.close()
        connection.close()

        return result>0
    
    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error

def create_ticket(ticket_details, hostname='spiceworks', database_name='osticket_test'):
    """
    Creates a new ticket in the specified database.

    :param
        ticket_details (dict): A dictionary containing ticket details.
        hostname (str, optional): The hostname of the database. Default is 'spiceworks'.
        database_name (str, optional): The name of the database. Default is 'osticket_test'.

    :return
        tuple: A tuple containing two elements:
            - The first element is a bool, True if the user was created, False if the user already existed.
            - The second element is an int representing the ticket_id 

    :raises
        mysql.connector.Error: If an error occurs while executing the query.
    """
    try:
        # Get user credentials 
        username, password = get_creds('db_creds.txt')

        # Prepare ticket_number for correct format
        ticket_number_str = str(ticket_details["id"]).zfill(6)

         # Connect to the MySQL database; Change spiceworks to host server
        connection = connect_to_mysql(hostname, username, password, database_name)

        # if this ticket already exists, skip
        if ticket_exists(connection, ticket_number_str):
            return (False, None)
        
        # else create the ticket
        else:
            # Create a cursor object to execute the queries
            cursor = connection.cursor()

            # Insert into ost_ticket

            # Insert into ost_thread

            # Insert into ost_form_entry 

            # Insert into ost_form_entry_values (subject)

            # Insert into ost_ticket__cdata (subject)

            # Insert into ost_form_entry_values (priority)

            # Insert into ost_ticket__cdata (priority)

            # Insert into ost_form_entry_values (imported)

            # Insert into ost_ticket__cdata (imported)

            # Insert into ost_form_entry_values (custom field: system)

            # Insert into ost_ticket__cdata (custom field: system)

            # Insert into ost_form_entry_values (custom field: hospital)

            # Insert into ost_ticket__cdata (custom field: hospital)

            # Insert into ost_thread_event 

            # Update ost_ticket (ticket status -> 2 = closed)

            # Replace into ost__search 

            # Insert into ost_thread_entry (ticket body)

            # Replace into ost__search (thready entry)

            # Replace into ost__search (ticket c__data include system + hospital)

            # Update ost_thread_entry (flag)

            # Update ost_ticket (staff_id)

            # Insert into ost_thread_event

            # 

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return (True, 0)

    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error

if __name__ == '__main__':

    test_ticket_file_path = 'test_ticket.txt'

    with open(test_ticket_file_path, 'r') as file:
        ticket_details = json.load(file)

    result = create_ticket(ticket_details)

    if result[0]:
        print('Ticket {} was created'.format(ticket_details["id"]))
    else:
        print('Ticket {} already exists'.format(ticket_details["id"]))
