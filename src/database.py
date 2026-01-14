import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', 5432),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
    
    def get_connection(self):
        """Create and return a database connection"""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

    def get_unprocessed_records(self):
        """Fetch all unprocessed records from the database"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT record_id_bank, transaction_date, currency_date, account, 
                       description, amount, currency
                FROM unprocessed_records
                """
                cursor.execute(query)
                records = cursor.fetchall()
                return [dict(record) for record in records]
        except Exception as e:
            print(f"Error fetching unprocessed records: {e}")
            return []
        finally:
            conn.close()

    def create_processed_records_table(self):
        """Create the processed_records table if it doesn't exist"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS processed_records (
                    record_id_bank VARCHAR(255) PRIMARY KEY,
                    transaction_date DATE,
                    currency_date DATE,
                    account VARCHAR(255),
                    description TEXT,
                    amount DECIMAL,
                    currency VARCHAR(10),
                    category VARCHAR(255),
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating processed_records table: {e}")
            return False
        finally:
            conn.close()

    def insert_processed_record(self, record, category):
        """Insert a processed record into the processed_records table and remove it from unprocessed_records"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO processed_records (
                    record_id_bank, transaction_date, currency_date, account,
                    description, amount, currency, category
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    record['record_id_bank'],
                    record['transaction_date'],
                    record['currency_date'],
                    record['account'],
                    record['description'],
                    record['amount'],
                    record['currency'],
                    category
                ))
                conn.commit()
                
                # Delete the record from unprocessed_records table
                delete_query = "DELETE FROM unprocessed_records WHERE record_id_bank = %s"
                cursor.execute(delete_query, (record['record_id_bank'],))
                conn.commit()
                
                return True
        except Exception as e:
            print(f"Error inserting processed record: {e}")
            return False
        finally:
            conn.close()