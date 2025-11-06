import functools
import sqlite3
from time import time


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


def retry_on_failure(retries=3, delay=2):
    """
    Parameterized decorator that retries the decorated function if it raises an exception.

    Args:
        retries (int): The maximum number of times to retry the function.
        delay (int): The number of seconds to wait between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            # Loop for the specified number of retry attempts
            for attempt in range(1, retries + 1):
                try:
                    # Attempt to execute the function
                    print(f"[{func.__name__}] Attempt {attempt} of {retries}...")
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    # If this is the last attempt, don't delay
                    if attempt == retries:
                        print(f"[{func.__name__}] Max retries reached. Giving up.")
                        # Re-raise the exception to be caught by the outer decorator (with_db_connection)
                        raise last_exception
                    
                    print(f"[{func.__name__}] Transient failure: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            
            # This line is technically unreachable due to the 'raise' above, but good practice
            # to handle potential control flow issues.
            # raise last_exception if last_exception else Exception("Unknown error during retry process.")

        return wrapper
    
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT 5;")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)