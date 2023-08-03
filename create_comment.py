# Function for creating a comment on a ticket
#
# Author:   Sierra Bonilla
# Date:     03-08-2023

import mysql.connector
import re
import ast 
from connect_to_db import get_creds, connect_to_mysql

def create_comment(comment_details, hostname='spiceworks', database_name='osticket_test'):
    """
    Creates a comment on the specified ticket in the given database.

    :param
        comments_details (dict): A dictionary containing comment details pertaining to osticket db.
        hostname (str, optional): The hostname of the database. Default is 'spiceworks'.
        database_name (str, optional): The name of the database. Default is 'osticket_test'.

    :return
        tuple: A tuple containing two elements:
            - The first element is a bool, True if the comment was created.
            - The second element is an int representing the thread_entry_id 
                (can check if exists in ost_thread_entry table)

    :raises
        mysql.connector.Error: If an error occurs while executing the query.
    """
    try:
        # ----------------------------------- PREPARE SQL INPUT VARIABLES --------------------------------- 

        ticket_id = comment_details["ticket_id"]
        staff_id = comment_details["staff_id"]
        staff_name = comment_details["staff_name"]
        title = comment_details["title"]
        body_html = comment_details["body_html"]

        # Get raw string for ost_search
        body = re.sub(r'<[^>]*>', ' ', body_html).strip()
        
        # -------------------------------------- CONNECT TO DATABASE -------------------------------------- 

        # Get user credentials 
        username, password = get_creds('db_creds.txt')        

        # Connect to the MySQL database; Change spiceworks to host server
        connection = connect_to_mysql(hostname, username, password, database_name)

        # Create a cursor object to execute the queries
        cursor = connection.cursor()

        # ----------------------------------------- POST COMMENT ------------------------------------------ 

        # Insert into ost_thread_entry html_body
        query_html_comment = """INSERT INTO `ost_thread_entry` SET `created` = NOW(), `type` = 'N', 
        `thread_id` = %s, `title` = %s, `format` = 'html', `staff_id` = %s, 
        `poster` = %s, `flags` = 64, `ip_address` = '8.8.8.8', `body` = %s, `updated` = NOW()"""
        cursor.execute(query_html_comment, (ticket_id, title, staff_id, staff_name, body_html))

        # Get thread_entry_id 
        thread_entry_id = cursor.lastrowid 

        # Insert into ost_search body
        query_search_comment = """REPLACE INTO ost__search SET object_type='H', object_id=%s, 
        content=%s, title=%s"""
        cursor.execute(query_search_comment, (thread_entry_id, body, title))

        # --------------------------------------- CLOSE CONNECTION ----------------------------------------

        # Commit changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return (True, thread_entry_id)

    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error
    
if __name__ == '__main__':

    comment_details_file_path = 'comment_details.txt'

    with open(comment_details_file_path, 'r') as file:
        comment_data = file.read()
    
    pattern = r'\{[^}]*\}'
    match = re.search(pattern, comment_data)
    if match:
        dict_text = match.group()
        comment_details = eval(dict_text)
        result = create_comment(comment_details)
        if result[0]:
            print('\Comment was created! \n \U0001f984 Ticket ID: {}\n \U0001f984 Thread ID: {}\n'.format(comment_details["ticket_id"], result[1]))
        else:
            print('\nUnable to make comment! \n \U0001f984 Ticket ID: {}\n'.format(comment_details["ticket_id"]))
    else: 
        print('No dictionary-like data found in the file. ')

