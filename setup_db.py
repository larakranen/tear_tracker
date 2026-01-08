import sqlite3

# 1. Connect to the database (This creates 'tears.db' if it doesn't exist yet)
connection = sqlite3.connect('tears.db')

# 2. Create a cursor object to execute SQL commands
cursor = connection.cursor()

# 3. Define the SQL command to create the table
sql_command = '''
CREATE TABLE IF NOT EXISTS crying_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    duration_minutes INTEGER,
    location TEXT,
    category TEXT,
    intensity INTEGER,
    was_alone BOOLEAN,
    people_involved TEXT,
    is_period BOOLEAN,
    notes TEXT
)
'''

# 4. Execute the command
cursor.execute(sql_command)

# 5. Commit (save) the changes and close the connection
connection.commit()
connection.close()

print("Database and table created successfully!")