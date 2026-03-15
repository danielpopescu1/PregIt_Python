# Quick script used to test SQLite CRUD operations during development.
# Not used by the main application.


from db_handler import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# INSERT test
cursor.execute("""
INSERT INTO tasks (title, description, owner, status, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?)
""", ("Test Task", "Testing DB", "Alice", "CREATED", 123456, 123456))

conn.commit()

print("Inserted task")

# SELECT test
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()

print("All tasks:")
for row in rows:
    print(row)

# UPDATE test
cursor.execute("""
UPDATE tasks
SET status = ?
WHERE id = ?
""", ("IN_PROGRESS", 1))

conn.commit()

print("Updated task")

conn.close()
