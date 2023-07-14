# Function for creating a connection to the mysql database
# This requires that the pc that you are connecting to the database, has been granted priveleges to remote connect
# e.g. GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root_password';
import mysql.connector 

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
        mysql.connector.Error: If an error occurs will connecting to the database.    
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
    
if __name__ == '__main__':

    host = 'spiceworks'
    username = 'migrator'
    password = 'nicetry'
    database = 'osticket_test'

    connection = connect_to_mysql(host, username, password, database)

    connection.close()