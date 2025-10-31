import csv
import uuid
import mysql.connector

# DATABASE connection details - replace with your actual credentials
DB_CONFIG  = {
    "host": "localhost",
    "user": "root",
    "password": "Stevengerad8!",
}

# NEW_DB_NAME = "ALX_prodev"
# CREATE_DB_QUERY = f"CREATE DATABASE {NEW_DB_NAME}"


def connect_db():
    """
        Connect to the database using credentials from DB_CONFIG\n
        Returns a tuple of (connection, cursor) if successful, else returns (None, None)
    """
    connection = None  # Initialize connection to None

    print(f"Attempting to connect to database server'{DB_CONFIG.get('database')}'...")

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection to Mysql database server established successfully.")
        print()
        print()
        return connection
    
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_database(connection, db_name=''):
    """
         creates a database if it does not exist\n
         Input: connection - a mysql.connector connection object\n
         returns: database name if created successfully, else None
    """
    cursor = connection.cursor()
    CREATE_DB_QUERY = f"CREATE DATABASE {db_name}"
    try:
        cursor.execute(CREATE_DB_QUERY)
        print(f"Database '{db_name}' created successfully.")
        return db_name
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        return None
    finally:
        cursor.close()

def connect_to_a_dbv(connection, db_name=''):
    """
        connect to a database\n
        return cursor if successful , else None   
    """ 
    try:
        connection.database = db_name   # Set the database for the connection
        print(f"Successfully connected to database '{db_name}'.")
        print()
        print()
        return True
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{db_name}': {err}")
        return False

def connect_to_prodev(connection):
    """
        connect to the alx_prodev database\n
        return cursor if successful , else None   
    """ 
    db_name='ALX_prodev'
    try:
        connection.database = db_name   # Set the database for the connection
        print(f"Successfully connected to database '{db_name}'.")
        print()
        print()
        return True
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{db_name}': {err}")
        return False


def create_table(connection):
    """
        creates a table in the connected database\n
        Input: connection - a mysql.connector connection object\n
        returns: True if created successfully, else False
    """
    cursor = connection.cursor()
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        age DECIMAL NOT NULL
    );
    """
    try:
        cursor.execute(CREATE_TABLE_QUERY)
        print("Table 'user_data' created successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        return False
    finally:
        cursor.close()  


def insert_data(connection, data):
    """
    Inserts data into the 'user_data' table only if a user with the given email 
    does not already exist.

    Args:
        connection (mysql.connector.connection.MySQLConnection): Active database connection.
        data (dict): A dictionary containing user data: 
                     {'name': str, 'email': str, 'age': int}
    """


    user_id = str(uuid.uuid4())
    
    # 1. Query to check if the user already exists based on the unique email
    check_query = "SELECT user_id FROM user_data WHERE email = %s"
    
    # 2. SQL query for insertion
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    cursor = connection.cursor()

    try:

        # Check if user with the given email already exists
        cursor.execute(check_query, (data['email'],))
        result = cursor.fetchone()
        
        if result:
            print(f"User with email {data['email']} already exists. Skipping insertion.")
            return False
        
        # Insert new user data
                # Prepare data tuple for insertion
        insert_values = (
            user_id,
            data['name'],
            data['email'],
            data['age']
        )
        cursor.execute(insert_query, insert_values)
        connection.commit()
        print(f"Data inserted successfully for user {data['name']}.")
        return True
    
    except mysql.connector.Error as e:
        print(f"ERROR: Could not insert {data['email']}. Reason: {e}")
        connection.rollback() # Rollback changes in case of an error
    
    finally:
        cursor.close()


def read_data_from_csv(filepath):
    """
    Reads user data from a CSV file and converts it into a list of dictionaries.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, or an empty list if the file fails to read.
    """
    data_list = []
    try:
        # Using 'with' ensures the file is closed automatically
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            # DictReader uses the first row as keys (headers)
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure 'age' is converted from string (CSV default) to integer
                try:
                    row['age'] = int(row['age'])
                    data_list.append(row)
                except ValueError:
                    print(f"Skipping row due to invalid age value: {row}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at path: {filepath}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return []

    return data_list




if __name__ == '__main__':

    # Call the function to get the connection and cursor
    connection = connect_db()
    connect_to_prodev(connection)

    # connect_to_a_dbv(connection, 'PCL_Operations')
    create_table(connection)

    
    data_list = read_data_from_csv(filepath=r"C:\Users\Emmanuel\ALX_PRODEV\user_data.csv")
    if data_list:
            print(f"Found {len(data_list)} records to process. Starting insertion loop...")
            
            # 3. Loop through the list and call the insert function for each record
            for user_data in data_list:
                insert_data(connection, user_data)
    else:
        print("No valid data found in CSV file. Nothing to insert.")

