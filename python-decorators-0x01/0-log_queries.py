import csv
from itertools import islice
import sqlite3
import uuid

# 1. Define the database file name /// from datetime import datetime
DB_FILE = 'test2.db'



def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    try:
        connection = sqlite3.connect(db_file)
        print("Database connection established successfully.")
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None, None
    
def execute_query(connection, cursor, query):
    """Execute a single query using the provided cursor."""
    try:
        cursor.execute(query)
        print("Query executed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while executing the query: {e}")
    finally:
        if cursor:
            cursor.close()
            if connection:
                connection.close()
            print("Database connection closed.")

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
    check_query = "SELECT user_id FROM user_data WHERE email = ?"
    
    # 2. SQL query for insertion
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (?, ?, ?, ?)
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
    
    except sqlite3.Error as e:  
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

def log_queries(func):
    def wrapper():   
        print(f"Executing function: {func.__name__}")
        result = func()
        for user in result:
            print(f"User ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[3]}")
        print(f"Function: {func.__name__} executed successfully.")
        return result
    return wrapper

def execute_insert():
    data_list = read_data_from_csv(filepath=r"C:\Users\Emmanuel\ALX_PRODEV\user_data.csv")
    if data_list:
            print(f"Found {len(data_list)} records to process. Starting insertion loop...")
            
            # 3. Loop through the list and call the insert function for each record
            for user_data in data_list:
                insert_data(conn, user_data)
    else:
        print("No valid data found in CSV file. Nothing to insert.")

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
    except sqlite3.Error as err:
        print(f"Failed creating table: {err}")
        return False
    finally:
        cursor.close()  

@log_queries
def fetch_all_users(query='SELECT * FROM user_data LIMIT 5'):
    """Fetch and print all users from the user_data table."""
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        # for user in islice(users, 5):
        #     print(user)
        return users
    except sqlite3.Error as e:  
        print(f"An error occurred while fetching data: {e}")
        return None

if __name__ == "__main__":
    conn, cur = create_connection(DB_FILE)
    if conn and cur:
        CREATE_TABLE_QUERY = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE,
                age DECIMAL NOT NULL
        );
        """
        # create_table(conn)
        # execute_insert()
        READ_TABLE_QUERY = """
        SELECT * FROM user_data LIMIT 5;
        """       

            
        fetch_all_users()
 

    
    