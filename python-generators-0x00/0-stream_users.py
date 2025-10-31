import seed

def stream_users(connection, table_name='user_data'):
    """
    Generator that fetches users from the database one at a time.
    """
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    
    for user in cursor:
        yield user
    
    cursor.close()

if __name__ == "__main__":
    connection = seed.connect_db()
    seed.connect_to_prodev(connection)
    

    for user_record in stream_users(connection, 'user_data'):
        print(user_record)