# 00-SpiceWorks-Migration
Spiceworks 7.5.00107 to OsTicket v1.18 database migration 🦆

The migration process involves transferring ticket data, including ticket details, comments, and user information, from the Spiceworks database to the osTicket database - noatably, we ignored attachments. To achieve this, import functions have been created in python based on the analysis of osTicket's SQL logs. There are other ways to migrate - including using the API to create tickets.

## Getting Started 

### Prerequisites 

Before running the project, make sure you have the following packages installed: 
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/): Python MySQL connector to interact with MySQL databases.
- [json](https://docs.python.org/3/library/json.html): Python JSON module for handling JSON data.

You can install the required packages using pip:

`pip install mysql-connector-python`

### Installing 

## Usage

### Functions

### Customization

Before running, make sure to customize the following items for your own OsTicket configuration: 
- Update MySQL database credentials in example_creds.txt and rename file db_creds.txt (note: this requires that the pc that you are connecting to the database has been granted priveleges to remote connect e.g. `GRANT ALL PRIVILEGES ON *.* TO 'migrator_username'@'%' IDENTIFIED BY 'password';`)
- Modify the **`hostname`** and **`database_name`** parameters in the function calls to match your osTicket database configuration 
- In **`create_ticket`** function on first insert into ost_ticket, change value 18 to preferred imported help topic found in **`ost_help_topic table`** (**CHANGE 18 -> YOUR IMPORTED HELP TOPIC ID**)
- **REMOVE LAST 4 FIELDS IN** **`ticket_details`** **DICT AND INSERT STATEMENTS IN** **`create_ticket`** **WITH CHANGE/REMOVE OR FUNCTION WILL NOT WORK**
- If your osTicket instance has custom fields, adjust the **`ticket_details`** dictionary in the **`create_ticket`** function to include the appropriate custom fields and their corresponding values and you'll need to add your own SQL insert calls
- Save columns **`id`** and **`value`** from **`ost_list_items`** table as a dictionary {id:value}

### To-Do: 
<del>1. finish in create_ticket </del>

<del>2. test create_ticket </del>

 To-Do Thursday:
 1. create import bot staff user to post all replies/comments 
 2. create post_replies 

 To-Do Friday:
 1. test post_replies

 To-Do Next Week:
 1. create integration script that runs export from spiceworks and import to osticket 
 2. finish proper Read-Me

