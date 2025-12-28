import sqlite3

# Connect to database (it will create database.db if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create tasks table to store phrase → image data
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT,
    phrase TEXT UNIQUE,
    image_url TEXT
);
""")

print("✅ Database and tasks table created successfully!")

conn.commit()
conn.close()
