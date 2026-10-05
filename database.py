import sqlite3
import os


DATABASE_PATH = "data/food_donation.db"


def get_connection():
    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            role TEXT NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Food donations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            food_name TEXT NOT NULL,
            description TEXT,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            expiry_time TEXT NOT NULL,
            pickup_address TEXT NOT NULL,
            status TEXT DEFAULT 'Available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (donor_id)
            REFERENCES users(id)
        )
    """)

    # Donation requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (donation_id)
            REFERENCES donations(id),

            FOREIGN KEY (receiver_id)
            REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()
