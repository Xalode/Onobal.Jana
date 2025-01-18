import psycopg

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "jana"
DB_USER = "yourusername"
DB_PASSWORD = "your_password"
DB_PORT="5432"

# SQL statement to create a table
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS cardholder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def findcardholder(badgeID,reader):
    print("Find BadgeID #",   badgeID )


    result = {
        "code": 20,
        "relay": 0,
        "timeout":0
      }

    try:
    # Connect to the PostgreSQL database
        with psycopg.connect(
            f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
        ) as conn:
        
        # Open a cursor to perform database operations
            with conn.cursor() as cur:
            # Execute the SQL command
                # cur.execute(CREATE_TABLE_QUERY)
                # print("Table created (if it did not already exist).")

                query = f"SELECT public.access_validation({badgeID}, {reader});"
                cur.execute(query)

                records = cur.fetchone()

                for record in records:
                    result = {"code": record[0],"relay":record[1], "timeout":record[2]}

                

        return result
    except Exception as e:
        print("An error occurred:", e)
        result = {"code": 20,"relay":0, "timeout":0}
        return "error"



