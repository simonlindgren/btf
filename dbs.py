import sqlite3

# Create first database and table (run once)

conn = sqlite3.connect("livetweets.db")
c = conn.cursor()
c.execute("""CREATE TABLE tweets (
id TEXT,
created_at TEXT,
author TEXT,
author_location TEXT,
author_followers INT,
author_friends INT,
hashtags TEXT,
tweet TEXT,
in_reply_to TEXT,
lang TEXT,
method TEXT,
UNIQUE(id))
""")
conn.close()

print("First database created.")

# Create second database and table (run once)

conn = sqlite3.connect("histtweets.db")
c = conn.cursor()
c.execute("""CREATE TABLE tweets (
id TEXT,
created_at TEXT,
author TEXT,
author_location TEXT,
author_followers INT,
author_friends INT,
hashtags TEXT,
tweet TEXT,
in_reply_to TEXT,
lang TEXT,
method TEXT,
UNIQUE(id))
""")
conn.close()

print("Second database created.")
