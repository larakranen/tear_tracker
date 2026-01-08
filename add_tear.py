import sqlite3
from datetime import datetime

# 1. Connect to the database
connection = sqlite3.connect('tears.db')
cursor = connection.cursor()

# 2. Collect Data (Interactive)
print("--- Log a new cry ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
duration = int(input("Duration (minutes): "))
location = input("Location: ")
category = input("Category (Work/Sad/Happy/etc): ")
intensity = int(input("Intensity (1-10): "))
was_alone_input = input("Were you alone? (yes/no): ").lower()
was_alone = 1 if was_alone_input == 'yes' else 0 # SQLite stores Booleans as 1 (True) or 0 (False)
people = input("People that saw me cry (if any): ")
notes = input("Notes: ")

# 3. The SQL Command (9 Columns total, but we skip 'id')
# We need 8 placeholders (?) to match the 8 variables we provide
sql_insert = '''
INSERT INTO crying_logs (
    timestamp, duration_minutes, location, category, 
    intensity, was_alone, people_involved, notes
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''

# 4. Execute
cursor.execute(sql_insert, (
    timestamp, duration, location, category, 
    intensity, was_alone, people, notes
))

# 5. Save and Close
connection.commit()
connection.close()

print("\nSaved to database! Open DB Browser to view it.")