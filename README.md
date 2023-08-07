# 00-SpiceWorks-Migration
Spiceworks 7.5.00107 to OsTicket v1.18 database migration 🦆

This migration process involves transferring ticket data, including ticket details, comments, and user information, from the Spiceworks database to the osTicket database - notably, we ignored attachments. To achieve this, import functions have been created in python based on the analysis of osTicket's SQL logs. There are probably many other ways to automate migration, this is just one method. Using this method will require customizing the code written here, but hopefully this helps cut down some of the headache of spending hours scrolling through query logs...

## Getting Started 

### Prerequisites 

The migration functions use the following non-standard package: 
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/): Python MySQL connector to interact with MySQL databases.

### Installing 

You can install the required packages using pip:

`pip install mysql-connector-python`



## Usage

### Customization

This migration method requires a descent amount of customization of these scripts (your custom fields will obviously be different): 
- Update MySQL database credentials in example_creds.txt and rename file db_creds.txt (note: this requires that the pc that you are connecting to the database has been granted priveleges to remote connect e.g. `GRANT ALL PRIVILEGES ON *.* TO 'migrator_username'@'%' IDENTIFIED BY 'password';`)
- Modify the **`hostname`** and **`database_name`** parameters in **`process_tickets`** function global variables to match your osTicket database configuration 
- Create an Import Agent for creating tickets and posting replies and change these values in global variables **`process_tickets`**
- In **`create_ticket`** function on first insert into ost_ticket, change value 18 to preferred imported help topic found in **`ost_help_topic table`** (**CHANGE 18 -> YOUR IMPORTED HELP TOPIC ID**)
- **REMOVE LAST 4 FIELDS IN** **`ticket_details`** **DICT AND INSERT STATEMENTS IN** **`create_ticket`** **WITH CHANGE/REMOVE OR FUNCTION WILL NOT WORK**
- If your osTicket instance has custom fields, adjust the **`ticket_details`** dictionary in the **`create_ticket`** function to include the appropriate custom fields and their corresponding values and you'll need to add your own SQL insert calls
- Save columns **`id`** and **`value`** from **`ost_list_items`** table as a dictionary {id:value}

# <span style ="color:blue">**Spiceworks: Export**</span>

## Get info about ticket sender `get_user`

### Inputs

- **`user`** (int) the user ID (`ticket.reported_by_id`)

### Outputs

- **`dict`** of `{str : str}`
  A dictionary of user info derived from database fields:
  - id: the user id
  - email: the user email, from `users.email`
  - name: the user name, concatenating first_name and last_name from `users.first_name` + `users_last.name` (only populated for "staff" users)
  - phone: the user phone number, concatenating `users.office_phone` and `users.cell_phone` (rarely populated)   

If the user doesn't exist, returns an empty dict.

## Get ticket content `get_ticket`

### Inputs

- **`ticket`** (int) the ticket ID (`tickets.id`)

### Outputs

- **`dict`** of `{str : str}`
    A dictionary of user info derived from database fields:
    - id (from `tickets.id`)
    - summary (from `tickets.summary`)
    - description (from `tickets.description`) Note: no cleaning/HTML-ification performed here
    - created_at (from `tickets.created_at`)
    - closed_at (from `tickets.closed_at`)
    - created_by, but by the email of that user (from `users.email where users.id = tickets.created_by`)
    - assigned_to, but by the email of that user (from `users.email where users.id = tickets.assigned_to`)
    - spe (from `tickets.c_spe`)
    - department (from `tickets.c_department`)

If the input id did not yield a ticket, returns an empty dict.

## Get all ticket comments into one big HTML string `get_comments`

### Inputs

- **`ticket`** (int) the ticket ID (`tickets.id`)

### Outputs

- **`dict`** of `{str : str}`
  A dictionary of comment thread info derived from database fields:
  - id: the ticket id, from `comments.ticket_id`
  - body: an HTML string of all the comments collated together, constructed from various fields in the `comments` table (see `make_html_comment` for formatting info)

If the ticket has no comments, *OR* doesn't exist, body will be ''

## Connection helper and wrapper `get_spiceworks`

### Inputs

- **`location`** (str|None)
  The path to the Spiceworks SQLite database file; if None, it will look for it in a config text file `SWlocation.txt`

### Outputs

- **`sqlite3.Connection`** object

## HTML comment thread helper `make_html_comment`

### Inputs

- **`row`** : tuple(\<int\>, \<int\>, \<string\>, \<string\>, \<string\>, \<string\>|None)
  The row data as extracted inside get_comments, containing:
  - id: the comment id (not used currently)
  - ticket_id: the id of the ticket this comment is for
  - body: the text of the comment
  - created_at: the timestamp of comment submission
  - email: the email of the comment author
  - attachment: the name of an attached file, if any, or None.

 ### Outputs

- **`str`**
  An HTML string with each comment in reverse submission order, with an H3 header for the author email and timestamp, the (roughly HTML-ified) body text, and the name of the attachment, if any.
  Note that threading of comments into a single HTML block is done by `get_comments`

  Example: 

        <h3><code>example_person@email.com</code> on 2022-01-01 10:00:00</h3><p>content of body..</p><p>Attachment: <em>myfile.jpg</em></p>


# <span style ="color:blue">**OsTicket: General Functions**</span>

Within file `create_ticket_helpers_fns.py`

## Get credentials to database `get_creds`

### Inputs

- **`text_file_path`** (str): The file path to a text file with credentials to MySQL database in dict format

### Outputs

- **`tuple`**: A tuple containing two elements:
    - username (str): Username to connect to MySQL database
    - password (str): Password to connect to MySQL database

## Get connection object to database `connect_to_mysql`

### Inputs

- **`host`** (str): The hostname or IP address of the MySQL server
- **`username`** (str): The username to authenticate with the MySQL server
- **`password`** (str): The password to authenticate with the MySQL server
- **`database`**  (str): The name of the database to connect to 

### Outputs

- **`mysql.connector.connection.MySQLConnection`**: The MySQL connection object 

## Find value in dictionary `check_key_in_json_file`

### Inputs

- **`key`** (str): The key that needs to be checked within the JSON data
- **`file_path`** (str): The file path to the JSON-like text file

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, `True` if the provided key is found in the JSON data, `False` otherwise.
    - The second element is the value associated with the provided key if it's present, or `None` if the key is not found.

### Raises

- **`FileNotFoundError`** (str): This exception is raised if the specified file path does not lead to an existing file

## Get rid of emojis 😿 `get_rid_of_all_fun`

### Inputs

- **`expression`** (str): The input string from which non-ASCII characters need to be removed.

### Outputs

- A new string where non-ASCII characters have been removed, while punctuation is retained.


# <span style="color:blue">**OsTicket: Create a User**</span>

Within file `user_exists.py` & `create_user.py`

## Check if user exists  `check_user_account_exists`

All users are identified by email.

### Inputs

- **`email`** (str): The email address to check.
- **`username`** (str): The username to authenticate with the MySQL server
- **`password`** (str): The password to authenticate with the MySQL server
- **`hostname`** (str, optional): The hostname of the database. Default is 'spiceworks'.
- **`database`** (str, optional): The name of the database. Default is 'osticket_test'.

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the user exists, False otherwise.
    - The second element is an int representing the user_id if the user exists,
        or None if the user does not exist.results tuple(bool, int): True if a user with given email exists along with user_id, False otherwise.

### Raises

- **`mysql.connector.Error`** (str): If an error occurs with connecting to the database or performing query. 

## Create user, if user doesn't exist `create_user_if_not_exists`

### Inputs

- **`user_details`** (dict): A dictionary of {str:str/int} of user details in json format:
  - id (str): spiceworks id (int)
  - email (str): the user email to check/create (str)
  - name (str): the name of user (if exists, otherwise '') (str)
  - phone (str): the phone number of user (if exists, otherwise ''). (str)
- **`hostname`** (str, optional): The hostname of the database. Default is 'spiceworks'.
- **`database`** (str, optional): The name of the database. Default is 'osticket_test'.


### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the user was created, False if the user already existed.
    - The second element is an int representing the user_id 

### Raises

- **`mysql.connector.Error`** (str): If an error occurs with connecting to the database or performing query. 

# <span style="color:blue">**OsTicket: Create a Ticket**</span>

Within file `create_ticket_helper_fns` & `create_ticket.py`

## Check if a ticket exists `ticket_exists`

### Inputs

- **`connection`** (mysql.connector.Connection): A connection object to the MySQL database.
- **`ticket_number_str`** (str): The ticket number in the format of '001234'.

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the ticket exists, False otherwise.
    - The second element is an int representing the ticket_id if the ticket exists, or None if it doesn't. 

### Raises

- **`mysql.connector.Error`** (str): If an error occurs with connecting to the database or performing query. 

## Create a ticket `create_ticket`

### Inputs

- **`ticket_details`** (dict): A dictionary of {str:str and int} of ticket details in json format:
  - id (str): spiceworks id (int)
  - summary (str): summary/title/brief of ticket (str)
  - description (str): body of main ticket with html formatting if preferred (may need to use '' & a different read in format if reading from txt file - json doesn't like backslashes) (str)
  - created_at (str): date in `%Y-%m-%d %H:%M:%S` format (str)
  - closed_at (str):  date in `%Y-%m-%d %H:%M:%S` format (str)
  - created_by (str): osTicket user ID, see ost_user (int)
  - created_by_email (str): email of user (str)
  - assigned_to (str): osTicket staff ID, see ost_staff (int)
  - assigned_to_username (str): osTicket staff username, see ost_staff (str)
  - spe (str): custom field value, see ost_list_items (str) **(REMOVE/CHANGE)**
  - spe_id (str): custom field id, see ost_list_items (str) **(REMOVE/CHANGE)**
  - department (str): custom field value, see ost_list_items (str) **(REMOVE/CHANGE)**
  - department_id (str): custom field id, see ost_list_items (str) **(REMOVE/CHANGE)**
- **`hostname`** (str, optional): The hostname of the database. Default is 'spiceworks'.
- **`database`** (str, optional): The name of the database. Default is 'osticket_test'.

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the ticket was created, False if the ticket number already existed.
    - The second element is an int representing the ticket_id 

### Raises

- **`mysql.connector.Error`** (str): If an error occurs with connecting to the database or performing query. 

# <span style="color:blue">**OsTicket: Posting an Internal Note**</span>

## Create a Comment `create_comment`

### Inputs

- **`comment_details`** (dict): A dictionary of {str:str and int} of comment details:
  - ticket_id (str): osTicket ticket id (int)
  - staff_id (str): osTicket staff id (int)
  - staff_name (str): osTicket staff name (str)
  - title (str): preferred comment title (str)
  - body_html (str): body of comment with any html formatting as desired (str, with single ticks '')
- **`hostname`** (str, optional): The hostname of the database. Default is 'spiceworks'.
- **`ticket_number_str`** (str, optional): The name of the database. Default is 'osticket_test'.

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the comment was created.
    - The second element is an int representing the thread_entry_id 
                (can check if exists in ost_thread_entry table)

### Raises

- **`mysql.connector.Error`** (str): If an error occurs with connecting to the database or performing query. 



### Example Comment 
![Example Comment](imgs/ExampleComment.png)
 
 2. finish proper Documentation
    - Plan
    - Read Me 
    - Process_Ticket() documentation 

