# Function for creating a new ticket
#
# Author:   Sierra Bonilla
# Date:     31-07-2023

import mysql.connector
import json
from datetime import datetime 
from connect_to_db import connect_to_mysql, get_creds
from create_user import create_user_if_not_exists
from create_ticket_helper_fns import ticket_exists 

def create_ticket(ticket_details, hostname='spiceworks', database_name='osticket_test'):
    """
    Creates a new ticket in the specified database.

    :param
        ticket_details (dict): A dictionary containing ticket details pertaining to osticket db.
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
        # Prepare SQL input Variables

        # Prepare ticket_number in correct format
        ticket_number_str = str(ticket_details["id"]).zfill(6)

        # Prepare created_at in correct format
        created_at = datetime.strptime(ticket_details["created_at"], '%Y-%m-%d %H:%M:%S')

        # Prepare created_at in correct format
        closed_at = datetime.strptime(ticket_details["closed_at"], '%Y-%m-%d %H:%M:%S')

        # Prepare spe form_entry_values value
        spe_value = '{\"' + str(ticket_details["spe_id"]) + '\":\"' + ticket_details["spe"] + '\"}'

        # Prepare dep form_entry_values value
        dep_value = '{\"' + str(ticket_details["department_id"]) + '\":\"' + ticket_details["department"] + '\"}'

        # Get user credentials 
        username, password = get_creds('db_creds.txt')        

        # Connect to the MySQL database; Change spiceworks to host server
        connection = connect_to_mysql(hostname, username, password, database_name)

        # if this ticket already exists, skip
        if ticket_exists(connection, ticket_number_str):
            # Close the connection 
            connection.close()

            return (False, None)
        
        # else create the ticket
        else:
            
            # User_id in OsTicket Db
            user_id = ticket_details["created_by"]

            # Staff_id in OsTicket Db
            staff_id = ticket_details["assigned_to"]

            # Create a cursor object to execute the queries
            cursor = connection.cursor()

            # Insert into ost_ticket (CHANGE 18 -> YOUR IMPORTED HELP TOPIC)
            query_ticket_intiate = """INSERT INTO ost_ticket
            (created, lastupdate, number, user_id, dept_id, sla_id, topic_id, staff_id, ip_address, source, updated)
            VALUES (%s, NOW(), %s, %s, '1', '1', '18', %s, '8.8.8.8', 'Other', NOW())"""
            cursor.execute(query_ticket_intiate, (created_at, ticket_number_str, user_id, staff_id))

            # Get ticket_id used for all later transactions
            ticket_id = cursor.lastrowid

            # Insert into ost_thread
            query_thread_initiate = "INSERT INTO `ost_thread` SET `id` = %s, `object_id` = %s, `object_type` = 'T', `created` = NOW()"
            cursor.execute(query_thread_initiate, (ticket_id, ticket_id))

            # Insert into ost_form_entry 
            query_form_entry_initiate = "INSERT INTO `ost_form_entry` SET `form_id` = 2, `sort` = 0, `created` = NOW(), `extra` = '{\"disable\":[]}', `object_type` = 'T', `object_id` = %s, `updated` = NOW()"
            cursor.execute(query_form_entry_initiate, (ticket_id, ))

            # Get form_entry_id 
            form_entry_id = cursor.lastrowid 

            # Insert into ost_form_entry_values (subject)
            query_form_entry_values = "INSERT INTO `ost_form_entry_values` SET `field_id` = 20, `value` = %s, `entry_id` = %s"
            cursor.execute(query_form_entry_values, (ticket_details["summary"], form_entry_id))

            # Insert into ost_ticket__cdata (subject)
            query_cdata_subject = "INSERT INTO `ost_ticket__cdata` SET `subject`=%s, `ticket_id`= %s ON DUPLICATE KEY UPDATE `subject`=%s"
            cursor.execute(query_cdata_subject, (ticket_details["summary"], ticket_id, ticket_details["summary"]))

            # Insert into ost_form_entry_values (priority --> normal)
            query_form_entry_prio = "INSERT INTO `ost_form_entry_values` SET `field_id` = 22, `value_id` = '2', `entry_id` = %s"
            cursor.execute(query_form_entry_prio, (form_entry_id, ))

            # Insert into ost_ticket__cdata (priority)
            query_cdata_prio = "INSERT INTO `ost_ticket__cdata` SET `priority`=2, `ticket_id`= %s ON DUPLICATE KEY UPDATE `priority`=2"
            cursor.execute(query_cdata_prio, (ticket_id, ))

            # Insert into ost_form_entry_values (imported) (CUSTOM FIELD: SYSTEM -> CHANGE/REMOVE) 
            query_form_entry_import = "INSERT INTO `ost_form_entry_values` SET `field_id` = 36, `entry_id` = %s, `value` = '{\"yes\":\"yes\"}'"
            cursor.execute(query_form_entry_import, (form_entry_id, ))

            # Insert into ost_ticket__cdata (imported) (CUSTOM FIELD: SYSTEM -> CHANGE/REMOVE) 
            query_cdata_import = "INSERT INTO `ost_ticket__cdata` SET `imported`='yes', `ticket_id`= %s ON DUPLICATE KEY UPDATE `imported`='yes'"
            cursor.execute(query_cdata_import, (ticket_id, ))

            # Insert into ost_form_entry_values (CUSTOM FIELD: SYSTEM -> CHANGE/REMOVE) 
            query_form_entry_spe = "INSERT INTO `ost_form_entry_values` SET `field_id` = 37, `entry_id` = %s, `value` = %s"
            cursor.execute(query_form_entry_spe, (form_entry_id, spe_value))

            # Insert into ost_ticket__cdata (CUSTOM FIELD: SYSTEM -> CHANGE/REMOVE) 
            query_cdata_spe = "INSERT INTO `ost_ticket__cdata` SET `system`=%s, `ticket_id`= %s ON DUPLICATE KEY UPDATE `system`=%s"
            cursor.execute(query_cdata_spe, (ticket_details["spe_id"], ticket_id, ticket_details["spe_id"]))

            # Insert into ost_form_entry_values (CUSTOM FIELD: HOSPITAL -> CHANGE/REMOVE) 
            query_form_entry_dep = "INSERT INTO `ost_form_entry_values` SET `field_id` = 38, `entry_id` = %s, `value` = %s"
            cursor.execute(query_form_entry_dep, (form_entry_id, dep_value))

            # Insert into ost_ticket__cdata (CUSTOM FIELD: HOSPITAL -> CHANGE/REMOVE) 
            query_cdata_dep = "INSERT INTO `ost_ticket__cdata` SET `h_departments`=%s, `ticket_id`= %s ON DUPLICATE KEY UPDATE `h_departments`=%s"
            cursor.execute(query_cdata_dep, (ticket_details["department_id"], ticket_id, ticket_details["department_id"]))

            # Insert into ost_thread_event 

            # Update ost_ticket (ticket status -> 2 = closed, closed -> date)

            # Replace into ost__search 

            # Insert into ost_thread_entry (ticket body)

            # Replace into ost__search (thready entry)

            # Replace into ost__search (ticket c__data include system + hospital)

            # Update ost_thread_entry (flag)

            # Update ost_ticket (staff_id)

            # Insert into ost_thread_event

            # Commit changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return (True, ticket_id)

    except mysql.connector.Error as error:
        # Rollback transaction in case of error
        connection.rollback()

        # Handle the error
        raise error

if __name__ == '__main__':

    test_ticket_file_path = 'ticket_details.txt'

    with open(test_ticket_file_path, 'r') as file:
        ticket_details = json.load(file)

    user_details_file_path = 'user_details.txt'

    with open(user_details_file_path, 'r') as file:
        user_details = json.load(file)

    result = create_ticket(ticket_details)

    if result[0]:
        print('Ticket was created: {}'.format(result[1]))
    else:
        print('Ticket already exists: {}'.format(ticket_details["id"]))
