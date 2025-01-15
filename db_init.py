import sqlite3

def init_db(db_path="sensor_data.db"):
  """
  Create (if not exist) a SQLite table 'sensor_data' to store IMU raw readings.
  """
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  c.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp REAL,  -- Unix timestamp (e.g., time.time())
      ax REAL,         -- Acceleration in X-axis
      ay REAL,         -- Acceleration in Y-axis
      az REAL,         -- Acceleration in Z-axis
      gx REAL,         -- Gyroscope in X-axis
      gy REAL,         -- Gyroscope in Y-axis
      gz REAL          -- Gyroscope in Z-axis
    )
  """)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  # Initialize the database
  init_db("sensor_data.db")
