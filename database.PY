import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('occurrence_book.db')
cursor = conn.cursor()

# Create Users Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Create Incidents Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY,
        name TEXT,
        accused TEXT,
        victim TEXT,
        reported_by TEXT,
        location TEXT,
        date TEXT,
        message TEXT,
        status TEXT
    )
''')


# Commit changes and close connection
conn.commit()
conn.close()
