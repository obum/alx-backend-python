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

def transactional(func):
    """
    Decorator that wraps a database operation in a transaction.
    It commits changes if the function succeeds or rolls back changes if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # The 'conn' object is guaranteed to be the first positional argument
        # because the @with_db_connection decorator handles inserting it.
        try:
            # 1. Execute the decorated function (which performs the DB operation)
            result = func(conn, *args, **kwargs)
            
            # 2. If no error, commit the changes to make them permanent
            conn.commit()
            print("Transaction committed successfully.")
            return result
            
        except Exception as e:
            # 3. If any error occurs, rollback the changes
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            # Reraise the exception so the outer decorator (@with_db_connection) 
            # or the calling code knows about the failure.
            raise
            
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE user_data SET email = ? WHERE user_id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id='c0d6860d-9d08-455c-ab79-6e415a4279b3', new_email='Crawford_Cartwright@hotmail.com')