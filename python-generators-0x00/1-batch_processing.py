import mysql.connector
import seed

DB_CONFIG = seed.DB_CONFIG
DB_CONFIG['database'] = 'ALX_prodev'


def stream_users_in_batches(batch_size:int):
    """
        Generator that fetches users from the database in batches.
        """
    """
    Arguments:
        batch_size (int): Number of users to fetch in each batch.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    print("Connection to Mysql database server established successfully.")

    cursor = connection.cursor()
    table_name = 'user_data'

    query = f"SELECT * FROM {table_name} LIMIT %s"

    cursor.execute(query, (batch_size,))

    while True:
        users = cursor.fetchmany(batch_size)
        if not users:
            break
        yield users
    cursor.close()  

# def batch_processing(batch_size):
#     """
#         processes each batch to filter users over the age of 25`
#     """

#     connection = mysql.connector.connect(**DB_CONFIG)
#     print("Connection to Mysql database server established successfully.")

#     cursor = connection.cursor()
#     table_name = 'user_data'

#     query = f"SELECT * FROM {table_name} WHERE age > 25 LIMIT %s"

#     cursor.execute(query)

#     while True:
#         users = cursor.fetchmany(batch_size)
#         if not users:
#             break
#         yield users
#     cursor.close()  







# if __name__ == "__main__":
#     batch_size = 5
#     for user_batch in stream_users_in_batches(batch_size):
#         print(f"Fetched batch of {len(user_batch)} users:")
#         for user in user_batch:
#             print(user)
#         print()


def batch_processing(batch_size: int) :
    """
    Processes each batch yielded by stream_users_in_batches to filter users 
    over the age of 25.
    """
    
    # 1. Get the generator object
    batch_generator = stream_users_in_batches(batch_size)
    
    # 2. Iterate through each batch yielded by the fetching generator
    for user_batch in batch_generator:
        
        # 3. Filter the current batch using a list comprehension.
        #    - user[3] is the Decimal object containing the age.
        #    - int(user[3]) safely converts the Decimal to an integer for comparison.
        filtered_batch = [
            user for user in user_batch 
            if int(user[3]) > 25
        ]
        
        # 4. Yield the resulting filtered batch
        yield filtered_batch

# --- Example Execution ---

if __name__ == "__main__":
    batch_size = 3
    print("--- Starting Filtered Batch Processing ---")
    
    # This loop consumes the filtered batches from batch_processing
    for filtered_batch in batch_processing(batch_size):
        
        print(f"\n✅ Fetched and Filtered batch of {len(filtered_batch)} users:")
        
        # This loop processes the individual users in the filtered batch
        for user in filtered_batch:
            # We access the age as an integer for cleaner display
            age = int(user[3]) 
            print(f"-> ID: {user[0]} | Name: {user[1]} | Age: {age}")
            
    print("\n--- Processing Complete ---")