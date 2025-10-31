
import seed
import mysql.connector

DB_CONFIG = seed.DB_CONFIG
DB_CONFIG['database'] = 'ALX_prodev'


def stream_user_ages():
    """
    Generator that streams only the ages of users from the database one at a time.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    print("Connection to Mysql database server established successfully.")
    print()
    print()
    # table_name='user_data'
    cursor = connection.cursor()
    query = f"SELECT age FROM user_data"
    cursor.execute(query)
    
    for (age,) in cursor:
        yield age


    
    cursor.close()


def calculate_average_age():
    """
    Calculate the average age of users in the database.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users:  {average_age}")



if __name__ == "__main__":
    calculate_average_age()