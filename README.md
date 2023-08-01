# 00-SpiceWorks-Migration
Spiceworks 7.5.00107 database to OsTicket v1.18 migration

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
- Update the MySQL database credentials (as seen in example_creds.txt)
- Modify the **`hostname`** and **`database_name`** parameters in the function calls to match your osTicket database configuration 
- If your osTicket instance has custom fields, adjust the **`ticket_details`** dictionary in the **`create_ticket`** function to include the appropriate custom fields and their corresponding values (removing the system and department fields - our custom fields)
- Save columns **`id`** and **`value`** from **`ost_list_items`** table as a dictionary {id:value}

### To-Do tomorrow: 
1. create proper Read-Me
2. fill in create_ticket 
3. test create_ticket 

 To-Do Wednesday:
 1. create post_replies 
 2. test post_replies

 To-Do Thursday:
 1. create integration script that runs export from spiceworks and import to osticket 

