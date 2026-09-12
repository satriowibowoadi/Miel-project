import sqlite3

db = sqlite3.connect("db/miel.db")
cursor = db.cursor()

def save_memory(key, value):
    cursor.execute(
        """
        INSERT INTO memories (key, value)
        VALUES (?, ?)
        """,
        (key, value)
    )

    db.commit()

def get_memory(key):
    cursor.execute(
        """
        SELECT value
        FROM memories
        WHERE key = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (key,)
    )

    memory = cursor.fetchone()

    if not memory:
        return None

    return memory[0]

save_memory("nama", "Rio")

print("Memory tersimpan!")

nama = get_memory("nama")

print("Nama dari memory:", nama)

db.close()