import mysql.connector
import seed

DB_CONFIG = seed.DB_CONFIG
DB_CONFIG['database'] = 'ALX_prodev'

def paginate_users(page_size: int, offset: int):
        """
        Simulates fetching a page of users from the 'user_data' database table 
        using LIMIT and OFFSET.
        """
        connection = None
        cursor = None
        
        try:
            connection = mysql.connector.connect(**DB_CONFIG)  # Connect to the database using stored configuration details.
            cursor = connection.cursor()                       # Create a cursor object to execute SQL commands.
            
            table_name = 'user_data'
            
            # The SQL query uses LIMIT (how many rows to fetch) and OFFSET (where to start).
            query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s"
            
            # Execute the query, safely passing page_size and offset as parameters.
            cursor.execute(query, (page_size, offset))
            
            users = cursor.fetchall()                          # Fetch all the results (the single page) returned by the query.
            
            return users                                       # Return the list of users for this page.
            
        finally:
            if cursor:
                cursor.close()                                 # Always close the cursor to free database resources.
            if connection:
                connection.close()                             # Always close the connection to prevent resource leaks.

def lazy_paginate(page_size: int) :
    """
    Generator function that fetches data page by page using a single loop,
    only requesting the next page when the current one is consumed.
    """
    
    # --- Setup ---
    offset = 0                                       # Start the position count (offset) at 0, meaning the very beginning of the table.
    
    # --- Single Loop ---
    while True:                                      # Start an infinite loop. We need this because we don't know how many pages exist.
        
        # --- Fetch Data ---
        users = paginate_users(page_size, offset)    # Ask the database for the next page of users, starting from our current position (offset).
        
        # --- End Condition ---
        if not users:                                # If the database sends back an empty list (no users)...
            break                                    # ...it means we've reached the end of the entire table, so we stop the infinite loop.
            
        # --- Produce Page ---
        yield users                                  # If we got users, immediately give this batch (page) of users back to the caller. The function pauses here.
        
        # --- Prepare for Next Page ---
        offset += page_size                          # Increase the starting position (offset) by the size of the page we just fetched, so the next request gets the subsequent page.
        
        # The loop restarts here, ready to fetch the next page when the caller asks for it.
if __name__ == "__main__":
    
    PAGE_SIZE = 50
    # TOTAL_RECORDS = 12  # Simulated total records for demonstration purposes.
    
    # print(f"Total Records (Simulated): {TOTAL_RECORDS}")
    print(f"Fetching in pages of size: {PAGE_SIZE}")
    print("-" * 30)
    
    # 1. Get the generator object
    paginated_data = lazy_paginate(PAGE_SIZE)
    
    # 2. Iterate through the generator
    page_count = 0
    
    # The 'for' loop triggers the generator one page at a time.
    for page in paginated_data:
        page_count += 1
        
        # When we enter this block, the generator has yielded one page (a list of users).
        print(f"\n✅ FETCHED PAGE {page_count} (Offset starts at: {(page_count - 1) * PAGE_SIZE}):")
        
        # Process the users in this specific page
        for user in page:
            print(f"  -> User ID:{ user[0]}, Name: {user[1]}, Age: {user[3]}")
            
    print("-" * 30)
    print(f"Pagination complete. Total pages fetched: {page_count}")
