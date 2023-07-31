# General functions

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

# Create a User

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

# Create a ticket

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

# Posting an Internal Note