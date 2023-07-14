# Function for creating a new user is one does not already exist
import mysql.connector
from connect_to_db import connect_to_mysql
from user_exists import check_user_account_exists

def create_user_if_not_exists(email, name = '', phone = ''):
    """
    Creates a user if one does not already exist in the database.

    :param
        email (str): The email address to check.
        name (str): The name of the user (if exists, otherwise '').
        phone (str): The phone number of user (if exists, otherwise '').
       
    :return
        bool: True if a user was created, False if user already exists

    :raises
        mysql.connector.Error: If an error occurs will connecting to the database or performing query.
    """
    try:
        # Check if user exists
        if check_user_account_exists(email, 'migrator', 'nicetry', 'osticket_test'):
            return False
        
        else:
            # Connect to the MySQL database
            connection = connect_to_mysql('spiceworks', 'migrator', 'London2023!', 'osticket_test')
            
            # Create a cursor object to execute the queries
            cursor = connection.cursor()
            
            # Insert user email
            query_insert_email = "INSERT INTO ost_user_email (address, user_id) VALUES (%s, 0)"
            cursor.execute(query_insert_email, (email,))

            # Get user id
            user_id = cursor.lastrowid

            # Fix user id value 
            query_fix_user_id = "UPDATE ost_user_email SET user_id = %s WHERE id = %s"
            cursor.execute(query_fix_user_id, (user_id, user_id))
             

            # Insert into ost_user
            query_insert_user = "INSERT INTO ost_user (name, org_id, created, updated, default_email_id) VALUES (%s, 0, NOW(), NOW(), %s)"
            cursor.execute(query_insert_user, (name, user_id))

            # Insert or update phone number
            query_insert_phone = "INSERT INTO ost_user__cdata (user_id, phone) VALUES (%s, %s);"
            cursor.execute(query_insert_phone, (user_id, phone))

            # Commit the changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return True
    except mysql.connector.Error as error:
        # Handle the error
        raise error

if __name__ == '__main__':

    email = 'random123@nhs.net'
    name = 'buddy'
    phone = '1234567890'

    if create_user_if_not_exists(email, name, phone):
        print('User {} was created'.format(email))
    else:
        print('User {} already exists'.format(email))