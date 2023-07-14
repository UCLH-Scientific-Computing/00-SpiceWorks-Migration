# Function for checking if user exists
import mysql.connector
from connect_to_db import connect_to_mysql

def check_user_account_exists(email, username, password, database):
    """
    Check if a user with a specific email exists in the 'ost_user_email' table.

    :param
        email (str): The email address to check.
        username (str): The username to authenticate with the MySQL server
        password (str): The password to authenticate with the MySQL server
        database (str): The name of the database to connect to 

    :return
        bool: True if a user with given email exists, False otherwise.

    :raises
        mysql.connector.Error: If an error occurs will connecting to the database or performing query.
    """
    try:

        # Connect to the MySQL database
        connection = connect_to_mysql('spiceworks', username, password, database)

        # Create a cursor object to execute query 
        cursor = connection.cursor()

        # Prepare the SQL query 
        query = 'SELECT * FROM ost_user_email WHERE address = %s'

        # Execute the SQL Query 
        cursor.execute(query, (email, ))

        # Fetch results
        result = cursor.fetchone()

        # Check if a user with the given email exists
        exists = result is not None

        # close cursor and connection
        cursor.close()
        connection.close()

        return exists
    except mysql.connector.Error as error:

        raise error
    
if __name__ == '__main__':

    email = 'random.person@nhs.net'
    username = 'migrator'
    password = 'nicetry'
    database = 'osticket_test'

    result = check_user_account_exists(email, username, password, database)

    if result:
        print('User with email: ' + email + ' exists already! WOW')
    else:
        print('User with email: ' + email + ' does not already exist! Please create a new user.')
