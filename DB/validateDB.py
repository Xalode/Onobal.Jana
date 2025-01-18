import psycopg

try:

    db = 'jana'
    # Connect to PostgreSQL
    connection = psycopg.connect(
        dbname="postgres",
        user="yourusername",
        password="your_password",
        host="localhost",
        port="5432"
    )
    connection.autocommit = True

    cursor = connection.cursor()
    #find Database 
    cur = connection.cursor()
    cur.execute("SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower(%s);", (db,))
    
  
 
    if (bool(cur.rowcount)):
     print("Exist")
    else :
     #Preparing query to create a database
     sql = ''' CREATE database  '''+db;
 
     # executing above query
     cursor.execute(sql)
     print("Database created successfully........")




except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()