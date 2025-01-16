import sqlite3
import os

def init_database():
    """Initialize the SQLite database and create the sensor_data table"""
    db_path = "sensor_data.db"
    
    # Check if database already exists
    if os.path.exists(db_path):
        print(f"Database already exists at {db_path}")
        return
    
    # Create new database and table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for sensor data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        x REAL NOT NULL,
        y REAL NOT NULL,
        z REAL NOT NULL,
        rotation_x REAL NOT NULL,
        rotation_y REAL NOT NULL,
        rotation_z REAL NOT NULL
    )
    """)
    
    # Create index on timestamp for faster queries
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_timestamp 
    ON sensor_data(timestamp)
    """)
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_database()
