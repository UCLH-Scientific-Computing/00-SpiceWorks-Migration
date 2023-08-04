# Function for creating a new ticket
#
# Author:   Sierra Bonilla
# Date:     31-07-2023

import mysql.connector
import json
from datetime import datetime 
from re import sub
from connect_to_db import connect_to_mysql, get_creds
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
        # ------------------------------ PREPARE SQL INPUT VARIABLES ------------------------------ 

        # Prepare user_id from osTicket db
        user_id = ticket_details["created_by"]

        # Prepare user email from osTicket db
        user_email = ticket_details["created_by_email"]

        # Prepare staff_id from osTicket db
        staff_id = ticket_details["assigned_to"]

        # Prepare staff_id username from osTicket db
        staff_username = ticket_details["assigned_to_username"]

        # Prepare ticket_number in correct format
        ticket_number_str = str(ticket_details["id"]).zfill(6)

        # Prepare search title 
        search_title = ticket_number_str + ' ' + ticket_details["summary"]

        # Prepare ticket body recipients
        ticket_recipients = '{\"to\":{\"' + str(user_id) + '\":\"<' + user_email + '>\"}}'

        # Prepare created_at in correct format
        created_at = datetime.strptime(ticket_details["created_at"], '%Y-%m-%d %H:%M:%S')

        # Prepare created_at in correct format
        if ticket_details["closed_at"] is None:
            closed_at = "NOW()"
        else:
            closed_at = "'{}'".format(datetime.strptime(ticket_details['closed_at'], '%Y-%m-%d %H:%M:%S')) 

        # Prepare ticket body to remove any UNICODE (NEED TO REMOVE UNICODE)
        ticket_body = r"{0}".format(ticket_details['description'])

        # Prepare spe form_entry_values value (CUSTOM FIELD: SYSTEM -> CHANGE/REMOVE)
        spe_value = '{\"' + str(ticket_details["spe_id"]) + '\":\"' + ticket_details["spe"] + '\"}'

        # Prepare dep form_entry_values value (CUSTOM FIELD: DEPARTMENT -> CHANGE/REMOVE)
        dep_value = '{\"' + str(ticket_details["department_id"]) + '\":\"' + ticket_details["department"] + '\"}'

        # Prepare search content (CUSTOM FIELD: SPE + DEPARTMENT -> CHANGE/REMOVE)
        search_content = ticket_details["summary"] + ' yes ' + ticket_details["spe"] + ' ' + ticket_details["department"]

        # Prepare your imported help topic id (CUSTOM FIELD: HELP TOPIC ID -> CHANGE)
        help_topic_id = 18

        # -------------------------------------- CONNECT TO DATABASE -------------------------------------- 

        # Get user credentials 
        username, password = get_creds()        

        # Connect to the MySQL database; Change spiceworks to host server
        connection = connect_to_mysql(hostname, username, password, database_name)

        # if this ticket already exists, skip
        ticket_exists_result = ticket_exists(connection, ticket_number_str)
        if ticket_exists_result[0]:
            # Close the connection 
            connection.close()

            return (False, ticket_exists_result[1])
        
        # ----------------------------------------- CREATE TICKET ----------------------------------------- 
        else:

            # Create a cursor object to execute the queries
            cursor = connection.cursor()

            # Insert into ost_ticket
            query_ticket_intiate = """INSERT INTO ost_ticket
            (created, lastupdate, number, user_id, dept_id, sla_id, topic_id, staff_id, ip_address, source, updated)
            VALUES (%s, NOW(), %s, %s, '1', '1', %s, %s, '8.8.8.8', 'Other', NOW())"""
            cursor.execute(query_ticket_intiate, (created_at, ticket_number_str, user_id, help_topic_id, staff_id))

            # Get ticket_id used for all later transactions
            ticket_id = cursor.lastrowid

            # Insert into ost_thread
            query_thread_initiate = "INSERT INTO `ost_thread` SET `id` = %s, `object_id` = %s, `object_type` = 'T', `created` = NOW()"
            cursor.execute(query_thread_initiate, (ticket_id, ticket_id))

            # Insert into ost_form_entry 
            query_form_entry_initiate = """INSERT INTO `ost_form_entry` SET `form_id` = 2, `sort` = 0, `created` = NOW(), 
            `extra` = '{\"disable\":[]}', `object_type` = 'T', `object_id` = %s, `updated` = NOW()"""
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

            # Insert into ost_form_entry_values (CUSTOM FIELD: IMPORTED -> CHANGE/REMOVE) 
            query_form_entry_import = "INSERT INTO `ost_form_entry_values` SET `field_id` = 36, `entry_id` = %s, `value` = '{\"yes\":\"yes\"}'"
            cursor.execute(query_form_entry_import, (form_entry_id, ))

            # Insert into ost_ticket__cdata (CUSTOM FIELD: IMPORTED -> CHANGE/REMOVE) 
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
            query_thread_event = """INSERT INTO `ost_thread_event` SET `thread_type` = 'T', `staff_id` = %s, 
            `team_id` = 0, `dept_id` = 1, `topic_id` = %s, `timestamp` = NOW(), `uid_type` = 'S', `uid` = %s, 
            `username` = %s, `event_id` = 1, `thread_id` = %s"""
            cursor.execute(query_thread_event, (staff_id, help_topic_id, staff_id, staff_username, ticket_id))

            # Update ost_ticket (ticket status -> 1 = open)
            query_ticket_status = "UPDATE `ost_ticket` SET `status_id` = '1', `updated` = NOW() WHERE `ost_ticket`.`ticket_id` = %s LIMIT 1"
            cursor.execute(query_ticket_status, (ticket_id, ))

            # Replace into ost__search 
            query_replace_search = "REPLACE INTO ost__search SET object_type='T', object_id=%s, content=%s, title=%s"
            cursor.execute(query_replace_search, (ticket_id, search_content, search_title))

            # Insert into ost_thread_entry (ticket body)
            query_ticket_body = """INSERT INTO `ost_thread_entry` SET `created` = NOW(), `type` = 'M', `thread_id` = %s, 
            `format` = 'html', `user_id` = %s, `poster` = %s, `source` = 'Other', `flags` = 577, 
            `recipients` = %s, `ip_address` = '8.8.8.8', 
            `body` = %s, `updated` = NOW()"""
            cursor.execute(query_ticket_body, (ticket_id, user_id, user_email, ticket_recipients, ticket_body))

            # Get thread ID 
            thread_entry_id = cursor.lastrowid 

            # Replace into ost__search (thready entry)
            query_search_thread = "REPLACE INTO ost__search SET object_type='H', object_id=%s, content=%s, title=%s"
            cursor.execute(query_search_thread, (thread_entry_id, ticket_body, ticket_details["summary"]))

            # ------------------------------------------ CLOSE TICKET ------------------------------------------ 

            # Update ost_ticket (ticket status -> 3 = closed) 
            query_close_ticket = """UPDATE `ost_ticket` SET `lastupdate` = NOW(), `closed` = {}, `status_id` = 3, 
            `updated` = NOW() WHERE `ost_ticket`.`ticket_id` = %s LIMIT 1""".format(closed_at)
            cursor.execute(query_close_ticket, (ticket_id, ))
            
            # Insert into ost_thread_referral 
            query_thread_referral = "INSERT INTO `ost_thread_referral` SET `thread_id` = %s, `object_id` = 3, `object_type` = 'S', `created` = NOW()"
            cursor.execute(query_thread_referral, (ticket_id, ))

            # Update ost_thread_event set to annulled 
            query_thread_annulled = """UPDATE `ost_thread_event` SET `annulled` = 1 WHERE `ost_thread_event`.`thread_id` = %s 
            AND `ost_thread_event`.`event_id` = 2"""
            cursor.execute(query_thread_annulled, (ticket_id, ))

            # Insert into ost_thread_event
            query_final_thread_event = """INSERT INTO `ost_thread_event` SET `thread_type` = 'T', `staff_id` = %s, `dept_id` = 1, 
            `topic_id` = %s, `timestamp` = NOW(), `uid_type` = 'S', `uid` = %s, `username` = %s, `event_id` = 2, `team_id` = 0,
            `data` = '{\"status\":[3,\"Closed\"]}', `thread_id` = %s"""
            cursor.execute(query_final_thread_event, (staff_id, help_topic_id, staff_id, staff_username, ticket_id))

            # ----------------------------------------- CLOSE CONNECTION -----------------------------------------

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

    test_ticket_file_path = r'dictionaries\ticket_details.txt'

    with open(test_ticket_file_path, 'r') as file:
        ticket_details = json.load(file)

    user_details_file_path = r'dictionaries\user_details.txt'

    with open(user_details_file_path, 'r') as file:
        user_details = json.load(file)

    result = create_ticket(ticket_details)

    if result[0]:
        print('\nTicket was created & closed! \n \U0001f984 Ticket ID: {}\n \U0001f984 Ticket Number: {}\n'.format(result[1], ticket_details["id"]))
    else:
        print('\nTicket already exists! \n \U0001f984 Ticket Number: {}\n'.format(ticket_details["id"]))
