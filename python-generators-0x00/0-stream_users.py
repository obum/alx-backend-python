from itertools import islice
import mysql.connector
import seed

DB_CONFIG = seed.DB_CONFIG
DB_CONFIG['database'] = 'ALX_prodev'



def stream_users():
    """
    Generator that fetches users from the database one at a time.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    print("Connection to Mysql database server established successfully.")
    print()
    print()
    table_name='user_data'
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    
    for user in cursor:
        yield user
    
    cursor.close()

if __name__ == "__main__":

    print(f"Database Configuration: {DB_CONFIG}")

    for user in islice(stream_users(), 6):
        print(user)

    