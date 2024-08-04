import mysql.connector
import psycopg2

# Connect to MySQL
def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host="172.21.154.71",
            user="root",
            password="ueWmopVhTLOlI6S6HsH5NY3x",
            database="sales"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Connect to PostgreSQL
def connect_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="sales",
            user="postgres",
            password="vk05uDz7SZIAYaCgQc11P5RX",
            host="172.21.241.107"
        )
        return conn
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None

# Find out the last rowid from PostgreSQL data warehouse
def get_last_rowid():
    conn = connect_postgresql()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(rowid) FROM sales_data;")
            last_rowid = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return last_rowid if last_rowid is not None else 0
        except psycopg2.Error as err:
            print(f"Error: {err}")
            return 0
    return 0

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
def get_latest_records(rowid):
    conn = connect_mysql()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM sales_data WHERE rowid > %s;"
            cursor.execute(query, (rowid,))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
    return []

# Insert the additional records from MySQL into PostgreSQL data warehouse.
def insert_records(records):
    conn = connect_postgresql()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.executemany(insert_query, records)
            conn.commit()
            cursor.close()
            conn.close()
        except psycopg2.Error as err:
            print(f"Error: {err}")

# Main program
if __name__ == "__main__":
    last_row_id = get_last_rowid()
    print("Last row id on production data warehouse = ", last_row_id)

    new_records = get_latest_records(last_row_id)
    print("New rows on staging data warehouse = ", len(new_records))

    if new_records:
        insert_records(new_records)
        print("New rows inserted into production data warehouse = ", len(new_records))
    else:
        print("No new rows to insert.")
