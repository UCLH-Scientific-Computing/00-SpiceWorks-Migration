# <span style ="color:blue">**General Functions**</span>

## Get credentials to database

### Inputs

- **`text_file_path`** (str): The file path to a text file with credentials to MySQL database in dict format

### Outputs

- **`tuple`**: A tuple containing two elements:
    - username (str): Username to connect to MySQL database
    - password (str): Password to connect to MySQL database

## Get connection object to database

### Inputs

- **`host`** (str): The hostname or IP address of the MySQL server
- **`username`** (str): The username to authenticate with the MySQL server
- **`password`** (str): The password to authenticate with the MySQL server
- **`database`**  (str): The name of the database to connect to 

### Outputs

- **`mysql.connector.connection.MySQLConnection`**: The MySQL connection object 


# <span style="color:blue">**Create a User**</span>

## Check if user exists already

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

## Create a user, if user doesn't exist

### Inputs

- **`email`** (str): The email address to check.
- **`name`** (str): The name of the user (if exists, otherwise '').
- **`phone`** (str): The phone number of user (if exists, otherwise '').

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the user was created, False if the user already existed.
    - The second element is an int representing the user_id 

# <span style="color:blue">**Create a Ticket**</span>

## Find System/Hospital Name (custom field)

### Inputs

- **`text_file_path`** (str): The file path to a text file with **`ost_list_items`** table items in dict format
- **`name`** (str) : A system or hospital name to search the dict for

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the system/hospital name exists, False if not.
    - The second element is an int representing the id for the system/hospital

## Check if a ticket exists

### Inputs

- **`connection`** (mysql.connector.Connection): A connection object to the MySQL database.
- **`ticket_number_str`** (str): The ticket number in the format of '001234'.

### Outputs

- **`bool`**: True if ticket exists, False if the ticket doesn't exist.

## Create a ticket

### Inputs

- **`ticket_details`** (dict): Dictionary of {str: str} of ticket info.
- **`database`**  (str): The name of the database to connect to 

### Outputs

- **`tuple`**: A tuple containing two elements:
    - The first element is a bool, True if the ticket was created, False if the ticket number already existed.
    - The second element is an int representing the ticket_id 

# <span style="color:blue">**Posting an Internal Note**</span>





# <span style ="color:blue">**Import from Spiceworks**</span>

## Get info about ticket sender `getSender`

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`) *OR* **`user`** the user ID (`ticket.reported_by_id`) **Which one do we want?**

### Outputs

- email (from `users.email`)
- name (from (`users.first_name` + `users_last.name`)) **This field is only filled out for "real" users (ProUser type) - what do we want to do with email-only users (EndUser type)?**
- phone number (from `users.office_phone` or `users.cell_phone`) **This field is almost always empty in SW - do we actually want it?**

## Get ticket content `getTicket`

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`)

### Outputs

- ticket id (from `tickets.id`) note: this is also one of the inputs! Returned for validation
- summary (from `tickets.summary`)
- description (from `tickets.description`) this is **not** currently HTML-ified in any way
- Time ticket of last
    - Created (from `tickets.created_at`)
    - Closed (from `tickets.closed_at`)
- Created by, but by the email of that user (from `users.email where users.id = tickets.created_by`)
- Assigned to, but by the email of that user (from `users.email where users.id = tickets.assigned_to`)
- c_spe (from `tickets.c_spe`)
- c_department (from `tickets.c_department`)

## Get all ticket comments into one big HTML string

### Inputs

- **`swconn`** a connection to SpiceWorks
- **`ticket`** the ticket ID (`tickets.id`)

### Outputs

- comment chunk built from `comments` in the following format

        <h3>created_at time created_by person 1 email:</h3> <p>content of body..</p> <hr>
        <h3>created_at time created_by person 2 email:</h3> <p>content of body..</p> <hr>
        <p>Find the attachments to this ticket: C:\\Program Files (x86)\\Spiceworks\\data\\uploads\\Ticket\\ticket_id<br /></p>'

  content extracted from
    - person email: `users.email where users.id = comments.created_by`
    - timestamp: `comments.created_at`
    - body: `comments.body` **May need a bit of HTML transform (e.g. `<br>` lines)**
    - attachments: `C:\\Program Files (x86)\\Spiceworks\\data\\uploads\\Ticket\\`*`ticket_id`*`\\`_`attachment_name`_
  collated from `comments where comments.ticket_id = tickets.id`