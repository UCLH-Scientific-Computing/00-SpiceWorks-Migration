# General functions

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

### Inputs

- **`ticket_details`** (dict): Dictionary of {str: str} of ticket info.
- **`database`**  (str): The name of the database to connect to 

# Posting an Internal Note

# Closing the ticket 