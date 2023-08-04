# <span style ="color:blue">**General Functions**</span>

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


# <span style="color:blue">**Create a User**</span>

## Check if user exists already `check_user_account_exists`

All users are identified by email.

### Inputs

- **`email`** (str): The email address to check.
- **`username`** (str): The username to authenticate with the MySQL server
- **`password`** (str): The password to authenticate with the MySQL server
- **`database`**  (str): The name of the database to connect to 

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the user exists, False otherwise.
    - The second element is an int representing the user_id if the user exists,
        or None if the user does not exist.results tuple(bool, int): True if a user with given email exists along with user_id, False otherwise.

## Create a user, if user doesn't exist `create_user_if_not_exists`

### Inputs

- **`user_details`** (dict): A dictionary of {str:str and int} of user details in json format:
  - id (str): spiceworks id (int)
  - email (str): the user email to check/create (str)
  - name (str): the name of user (if exists, otherwise '') (str)
  - phone (str): the phone number of user (if exists, otherwise ''). (str)
  - body_html (str): body of comment with any html formatting as desired (str, with single ticks '')
- `**hostname**` (str, optional): The hostname of the database. Default is 'spiceworks'.
- `**database**` (str, optional): The name of the database. Default is 'osticket_test'.


### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the user was created, False if the user already existed.
    - The second element is an int representing the user_id 

# <span style="color:blue">**Create a Ticket**</span>

## Check if a ticket exists `ticket_exists`

### Inputs

- **`connection`** (mysql.connector.Connection): A connection object to the MySQL database.
- **`ticket_number_str`** (str): The ticket number in the format of '001234'.

### Outputs

- **`bool`**: True if ticket exists, False if the ticket doesn't exist.

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
  - spe (str): custom field value, see ost_list_items (str) (REMOVE/CHANGE)
  - spe_id (str): custom field id, see ost_list_items (str) (REMOVE/CHANGE)
  - department (str): custom field value, see ost_list_items (str) (REMOVE/CHANGE)
  - department_id (str): custom field id, see ost_list_items (str) (REMOVE/CHANGE)
- **`hostname`** (str, optional): The hostname of the database. Default is 'spiceworks'.
- **`database`** (str, optional): The name of the database. Default is 'osticket_test'.

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the ticket was created, False if the ticket number already existed.
    - The second element is an int representing the ticket_id 

# <span style="color:blue">**Posting an Internal Note**</span>

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



# <span style ="color:blue">**Import from Spiceworks**</span>

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

