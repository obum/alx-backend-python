import time
import sqlite3 
import functools


query_cache = {}

def cache_query(func):
    """
    Decorator that caches the result of a database query based on the 
    SQL query string provided in the 'query' keyword argument.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        
        # 1. Determine the cache key
        # We need the SQL query string, which is assumed to be in kwargs['query'].
        # Use .get() for safety, defaulting to None if the key isn't found.
        cache_key = kwargs.get('query') 
        
        if cache_key is None:
            print("[Cache] Error: Query key not found. Executing function without caching.")
            return func(conn, *args, **kwargs)

        # 2. Check the cache
        if cache_key in query_cache:
            print(f"[Cache Hit] Retrieving result for query: {cache_key[:30]}...")
            return query_cache[cache_key]
        
        # 3. Cache Miss: Execute the original function
        print(f"[Cache Miss] Executing query: {cache_key[:30]}...")
        result = func(conn, *args, **kwargs)
        
        # 4. Store the result in the cache
        query_cache[cache_key] = result
        return result

    return wrapper


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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM user_data")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM user_data")