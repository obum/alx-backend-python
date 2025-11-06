import sqlite3 
import functools



def with_db_connection(func):
    """ your code goes here"""  
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            connection = sqlite3.connect('test2.db')
            print("Database connection established successfully.")
            result = func(connection, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None
        
        finally:
            if connection:
                connection.close()
                print("Database connection closed.")
        
    return wrapper



@with_db_connection 
def get_user_by_id(conn, user_id): 
    """Fetch a user by ID from the user_data table."""
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (user_id,)) 
    return cursor.fetchone() 
    


#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id='c0d6860d-9d08-455c-ab79-6e415a4279b3')
print(user)