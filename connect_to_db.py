# Function for creating a connection to the mysql database
# This requires that the pc that you are connecting to the database, has been granted priveleges to remote connect
# e.g. GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root_password';
#
# Author:   Sierra Bonilla
# Date:     14-07-2023

import mysql.connector 
import ast

def connect_to_mysql(host, username, password, database):
    """
    Connects to a MySQL database.

    :param
        host (str): The hostname or IP address of the MySQL server
        username (str): The username to authenticate with the MySQL server
        password (str): The password to authenticate with the MySQL server
        database (str): The name of the database to connect to 

    :return
        mysql.connector.connection.MySQLConnection: The MySQL connection object 

    :raises
        mysql.connector.Error: If an error occurs with connecting to the database.    
    """
    try:

        # Create connection object
        connection = mysql.connector.connect(
            host = host, 
            user = username,
            password = password,
            database = database
        )

        return connection
    except mysql.connector.Error as error:

        raise error

def get_creds(text_file_path):
    """
    Reads credential text file and returns username and password, if text file contains creds.
    text file should be a dictionary like:
        {'username':'password'}

    :param
        text_file_path (str): The file path to a text file with credentials to MySQL database

    :return
        username, password (tuple): Username and Password to use to connect to MySQL database

    :raises
        Error: If an error occurs when opening the file or reading credentials.    
    """
    try:
        with open(text_file_path, 'r') as file:
            db_creds = file.read()
        
        creds = ast.literal_eval(db_creds)

        if creds:
            username, password = next(iter(creds.items()))
            return username, password
        else:
            print('No credentials found in the file or not in dictionary form. Check format of dictionary.')
    except: 
        print('There is a problem with the text file with credentials.')

if __name__ == '__main__':

    username, password = get_creds('db_creds.txt')

    host = 'spiceworks'
    database = 'osticket_test'
    connection = connect_to_mysql(host, username, password, database)
    connection.close()

    