# Function for checking if user exists
#
# Author:   Sierra Bonilla
# Date:     14-07-2023

import mysql.connector
from connect_to_db import connect_to_mysql, get_creds

def check_user_account_exists(email, username, password, hostname='spiceworks', database='osticket_test'):
    """
    Check if a user with a specific email exists in the 'ost_user_email' table.

    :param
        email (str): The email address to check.
        username (str): The username to authenticate with the MySQL server
        password (str): The password to authenticate with the MySQL server
        hostname (str, optional): The hostname of the database. Default is 'spiceworks'.
        database_name (str, optional): The name of the database. Default is 'osticket_test'.

    :return
        tuple: A tuple containing two elements:
            - The first element is a bool, True if the user exists, False otherwise.
            - The second element is an int representing the user_id if the user exists,
              or None if the user does not exist.results tuple(bool, int): True if a user with given email exists along with user_id, False otherwise.

    :raises
        mysql.connector.Error: If an error occurs will connecting to the database or performing query.
    """
    try:

        # Connect to the MySQL database
        connection = connect_to_mysql(hostname, username, password, database)

        # Create a cursor object to execute query 
        cursor = connection.cursor()

        # Prepare the SQL query 
        query = "SELECT user_id FROM ost_user_email WHERE address = %s"

        # Execute the SQL Query 
        cursor.execute(query, (email, ))

        # Fetch results
        result = cursor.fetchone()

        # close cursor and connection
        cursor.close()
        connection.close()

        return (True, result[0]) if result else (False, None)
    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        raise error
    
if __name__ == '__main__':

    username, password = get_creds('db_creds.txt')

    email = 'random.person@nhs.net'
    database = 'osticket_test'

    result = check_user_account_exists(email, username, password, database=database)

    if result[0]:
        print('🦆 - 🦆 - 🦆 - 🦆 - 🦆 - 🦆 - 🦆 - 🦆 - 🦆 - 🦆')
        print('User with email: ' + email + ' exists already! WOW')
    else:
        print('User with email: ' + email + ' does not already exist! Please create a new user.')
