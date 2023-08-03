# Function for creating a new user is one does not already exist
#
# Author:   Sierra Bonilla
# Date:     31-07-2023

import mysql.connector
import json
from connect_to_db import connect_to_mysql, get_creds
from user_exists import check_user_account_exists

def create_user_if_not_exists(user_details, hostname='spiceworks', database='osticket_test'):
    """
    Creates a user if one does not already exist in the database.

    :param
        user_details (dict): A dictionary containing user details pertaining to osticket db.
        hostname (str, optional): The hostname of the database. Default is 'spiceworks'.
        database_name (str, optional): The name of the database. Default is 'osticket_test'.
       
    :return
        tuple: A tuple containing two elements:
            - The first element is a bool, True if the user was created, False if the user already existed.
            - The second element is an int representing the user_id 

    :raises
        mysql.connector.Error: If an error occurs will connecting to the database or performing query.
    """
    try:
        # Set email/name/phone variables
        email = user_details["email"]
        name = user_details["name"]
        phone = user_details["phone"]

        # Get user credentials 
        username, password = get_creds('db_creds.txt')

        # Check if user account already exists, if user exists return false and the user_id
        exists = check_user_account_exists(email, username, password, hostname=hostname,database=database)
        if exists[0]:
            return (False, exists[1])
        
        else:
            # Connect to the MySQL database
            connection = connect_to_mysql(hostname, username, password, database)
            
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
            query_insert_user = "INSERT INTO ost_user (id, name, org_id, created, updated, default_email_id) VALUES (%s, %s, 0, NOW(), NOW(), %s)"
            cursor.execute(query_insert_user, (user_id, name, user_id))

            # Insert into ost_form_entry 
            query_insert_form_entry = "INSERT INTO `ost_form_entry` SET `form_id` = 1, `sort` = 1, `created` = NOW(), `object_type` = 'U', `object_id` = %s, `updated` = NOW()"
            cursor.execute(query_insert_form_entry, (user_id,))

            # Get query insert entry id
            form_entry_id = cursor.lastrowid 

            # Insert into ost_form_entry_values
            query_insert_form_entry_values = "INSERT INTO `ost_form_entry_values` SET `field_id` = 3, `entry_id` = %s"
            cursor.execute(query_insert_form_entry_values, (form_entry_id,))

            # Insert or update phone number
            query_insert_phone = "INSERT INTO ost_user__cdata (user_id, phone) VALUES (%s, %s);"
            cursor.execute(query_insert_phone, (user_id, phone))

            # Create correct syntax for content
            content = f' {email}\n{email}'

            # Replace into ost__search
            query_replace_search = "REPLACE INTO ost__search SET object_type='U', object_id=%s, content= %s, title=%s"
            cursor.execute(query_replace_search, (user_id, content, name))

            # Commit the changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return (True, user_id)
        
    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error

if __name__ == '__main__':

    user_details_file_path = 'user_details.txt'

    with open(user_details_file_path, 'r') as file:
        user_details = json.load(file)

    if create_user_if_not_exists(user_details)[0]:
        print('User {} was created'.format(user_details["email"]))
    else:
        print('User {} already exists'.format(user_details["email"]))