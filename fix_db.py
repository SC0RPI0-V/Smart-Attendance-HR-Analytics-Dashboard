import sqlite3

db_path = "instance/hr.db"  # adjust if your DB is elsewhere

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;
""")

conn.commit()
conn.close()

print("✔ is_active column added successfully")
