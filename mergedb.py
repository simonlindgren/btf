import sqlite3
import os

# Get connections to the databases
db_a = sqlite3.connect('livetweets.db')
db_b = sqlite3.connect('histtweets.db')

# Get the contents of a table
b_cursor = db_b.cursor()
b_cursor.execute('SELECT * FROM tweets')
output = b_cursor.fetchall()   # Returns the results as a list.

# Insert those contents into another table.
a_cursor = db_a.cursor()
for row in output:
    try:
        a_cursor.execute('INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?)', row)
    except sqlite3.IntegrityError: # skip duplicate tweet ids
        pass

# Cleanup
db_a.commit()
a_cursor.close()
b_cursor.close()

# Rename the merged db, and delete the other
os.rename('livetweets.db', 'tweets.db')
os.remove('histtweets.db')

print("Databases merged = tweets.db")