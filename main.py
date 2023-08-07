# Main script for running all export and import scripts
#
# Author:   Sierra Bonilla
# Date:     07-08-2023

from get_ticket import get_ticket
from get_user import get_user
from get_comments import get_comments
from create_ticket_helper_fns import check_key_in_json_file, get_rid_of_all_fun
from create_user import create_user_if_not_exists
from create_ticket import create_ticket
from create_comment import create_comment
from get_spiceworks import get_spiceworks

import json
import random

def process_tickets(batch_size=100, save_filename='remaining_tickets.txt'):
    """
    
    """
    try:
        with open(save_filename, 'r') as file:
            remaining_tickets = json.load(file)

        # -------------------------------- DEFINE GLOBAL VARIABLES --------------------------------- 

        hostname = 'spiceworks'
        database = 'osticket-clone'

        staff_id_file = r'dictionaries\staff_email_to_id.txt'
        staff_username_file = r'dictionaries\staff_email_to_un.txt'
        spe_file = r'dictionaries\sw_spe_to_os_spe.txt'
        spe_id_file = r'dictionaries\sw_spe_to_os_spe_id.txt'
        dep_file = r'dictionaries\sw_dep_to_os_dep.txt'
        dep_id_file = r'dictionaries\sw_dep_to_os_dep_id.txt'

        import_bot_id = 11
        import_bot_username = "irobot"
        import_bot_name = "Import Bot"

        while remaining_tickets:
            batch = remaining_tickets[:batch_size]
            for ticket_id in batch:

                # ------------------ GET TICKET/USER/COMMENT DETAILS FOR SINGLE TICKET ------------------ 

                sw_ticket_details = get_ticket(ticket_id)
                sw_user_details = get_user(sw_ticket_details['created_by'])
                sw_comment_details = get_comments(ticket_id)

                # ------------------------------- CREATE USER IN OSTICKET -------------------------------

                os_user_result = create_user_if_not_exists(sw_user_details, hostname=hostname, database=database)
                if os_user_result[0]:
                    print('User was created!')
                    print('\U0001F47D User email: {}\n\U0001F47D User ID: {}\n'.format(sw_user_details["email"], os_user_result[1]))
                else:
                    print('User already exists! \n\U0001F480 User email: {}'.format(sw_user_details["email"]))
                    print('\U0001F480 User ID: {}\n'.format(os_user_result[1]))

                # ------------------------------ CREATE TICKET IN OSTICKET ------------------------------

                os_ticket_details = {}
                os_ticket_details["id"] = sw_ticket_details["id"]
                os_ticket_details["summary"] = get_rid_of_all_fun(sw_ticket_details["summary"])
                os_ticket_details["description"] = get_rid_of_all_fun(sw_ticket_details["description"])
                os_ticket_details["created_at"] = sw_ticket_details["created_at"]
                os_ticket_details["closed_at"] = sw_ticket_details["closed_at"]
                os_ticket_details["created_by"] = os_user_result[1]
                os_ticket_details["created_by_email"] = sw_user_details["email"]

                assigned_to_results = check_key_in_json_file(sw_ticket_details["assigned_to"], staff_id_file)
                if assigned_to_results[0]:
                    os_ticket_details["assigned_to"] = assigned_to_results[1]
                    os_ticket_details["assigned_to_username"] = check_key_in_json_file(sw_ticket_details["assigned_to"], staff_username_file)[1]
                else:
                    os_ticket_details["assigned_to"] = import_bot_id
                    os_ticket_details["assigned_to_username"] = import_bot_username 

                spe_results = check_key_in_json_file(sw_ticket_details["spe"], spe_file)
                if spe_results[0]:
                    os_ticket_details["spe"] = spe_results[1]
                    os_ticket_details["spe_id"] = check_key_in_json_file(sw_ticket_details["spe"], spe_id_file)[1]
                else:
                    os_ticket_details["spe"] = "IMPORTED"
                    os_ticket_details["spe_id"] = 46

                dept_results = check_key_in_json_file(sw_ticket_details["department"], dep_file)
                system_is_dept = check_key_in_json_file(sw_ticket_details["spe"], dep_file)
                if dept_results[0]:
                    os_ticket_details["department"] = dept_results[1]
                    os_ticket_details["department_id"] = check_key_in_json_file(sw_ticket_details["department"], dep_id_file)[1]
                elif system_is_dept[0]:
                    os_ticket_details["department"] = system_is_dept[1]
                    os_ticket_details["department_id"] = check_key_in_json_file(sw_ticket_details["spe"], dep_id_file)[1]
                else:
                    os_ticket_details["department"] = "IMPORTED"
                    os_ticket_details["department_id"] = 34
                
                os_ticket_result = create_ticket(os_ticket_details, hostname=hostname, database_name=database)
                if os_ticket_result[0]:
                    print('\nTicket was created & closed!')
                    print('\U0001f984 Ticket ID: {}\n\U0001f984 Ticket Number: {}\n'.format(os_ticket_result[1], os_ticket_details["id"]))
                else:
                    print('\nTicket already exists! \n\U0001f47B Ticket Number: {}'.format(os_ticket_details["id"]))
                    print('\U0001f47B Ticket ID: {}\n'.format(os_ticket_result[1]))
                
                os_ticket_id = os_ticket_result[1]

                # ------------------------------ CREATE COMMENT IN OSTICKET ------------------------------

                if os_ticket_result[0]:
                    os_comment_details = {}
                    os_comment_details["ticket_id"] = os_ticket_id
                    os_comment_details["body_html"] = get_rid_of_all_fun(sw_comment_details["body"])
                    os_comment_details["staff_name"] =  import_bot_name
                    os_comment_details["title"] = "All Replies/Comments"
                    os_comment_details["staff_id"] = 11

                    os_comment_result = create_comment(os_comment_details, hostname=hostname, database_name=database)
                    if os_comment_result[0]:
                        print('\nComment was created!')
                        print('\U0001f984 Ticket ID: {}\n\U0001f984 Thread ID: {}\n'.format(os_comment_details["ticket_id"], os_comment_result[1]))
                    else:
                        print('\nUnable to make comment! \n:( Ticket Number: {}\n'.format(os_comment_details["ticket_id"]))
                else:
                    print('\nTicket already exists - not making comment! \n:( Ticket Number: {}\n'.format(os_ticket_id))

            # Remove processed tickets from the list
            remaining_tickets = remaining_tickets[batch_size:]

            # Save remaining tickets to file
            with open(save_filename, 'w') as file:
                json.dump(remaining_tickets, file)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':

    # ------------------------------ SELECT ALL SPICEWORKS TICKETS ------------------------------ 

    con = get_spiceworks()
    cursor = con.cursor()
    query = 'SELECT id FROM tickets'
    result = cursor.execute(query)
    all_ticket_ids = [row[0] for row in result.fetchall()]
    con.close()

    print(sorted(random.sample(all_ticket_ids, 15)))
    save_filepath = 'all_tickets.txt'
    with open(save_filepath, 'w') as file:
        json.dump(all_ticket_ids, file)