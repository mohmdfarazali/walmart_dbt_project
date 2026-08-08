#!/usr/bin/env python3
"""
Script to load CSV data into Ghost PostgreSQL database using COPY command
"""

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get connection string from environment
connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

if not connection_string:
    raise ValueError("POSTGRES_CONNECTION_STRING not found in .env file")

# Define the mapping of CSV files to database tables
csv_to_table_mapping = {
    "walmart_dataset/data/customers.csv": "raw.customers",
    "walmart_dataset/data/employees.csv": "raw.employees",
    "walmart_dataset/data/products.csv": "raw.products",
    "walmart_dataset/data/stores.csv": "raw.stores",
    "walmart_dataset/data/orders.csv": "raw.orders",
    "walmart_dataset/data/order_items.csv": "raw.order_items",
}

def load_csv_to_table(connection, csv_file, table_name):
    """Load a CSV file into a table using COPY command"""
    try:
        with connection.cursor() as cursor:
            with open(csv_file, "r") as f:
                cursor.copy_expert(
                    sql.SQL("COPY {} FROM STDIN WITH (FORMAT csv, HEADER true)").format(
                        sql.Identifier(*table_name.split("."))
                    ),
                    f
                )
            connection.commit()
            print(f"✓ Successfully loaded {csv_file} into {table_name}")
    except Exception as e:
        connection.rollback()
        print(f"✗ Error loading {csv_file}: {e}")
        raise

def main():
    """Main function to load all CSV files"""
    try:
        # Connect to the database
        connection = psycopg2.connect(connection_string)
        print("✓ Connected to Ghost PostgreSQL database")
        
        # Load each CSV file
        for csv_file, table_name in csv_to_table_mapping.items():
            if os.path.exists(csv_file):
                load_csv_to_table(connection, csv_file, table_name)
            else:
                print(f"✗ File not found: {csv_file}")
        
        connection.close()
        print("\n✓ All CSV files loaded successfully!")
        
    except Exception as e:
        print(f"✗ Connection error: {e}")
        raise

if __name__ == "__main__":
    main()
