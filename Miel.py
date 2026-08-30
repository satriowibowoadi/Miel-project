from asyncio import Task

import ollama
import sqlite3
import os

# =========================
# DATABASE MIEL
# =========================

os.makedirs("db", exist_ok=True)

db = sqlite3.connect("db/miel.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    deadline TEXT,
    status TEXT DEFAULT 'belum selesai'
)
""")

db.commit()


# =========================
# MENAMPILKAN TUGAS
# =========================

def get_tasks():
    cursor.execute("""
        SELECT id, task, deadline, status
        FROM tasks
        WHERE status = 'belum selesai'
    """)

    tasks = cursor.fetchall()

    if not tasks:
        return "Saat ini tidak ada tugas yang belum selesai."

    result = "Tugas yang belum selesai:\n"

    for task in tasks:
        result += f"- {task[1]}"

        if task[2]:
            result += f" (deadline: {task[2]})"

        result += "\n"

    return result

def add_task(task, deadline=None):
    cursor.execute(
        """
        INSERT INTO tasks (task, deadline)
        VALUES (?, ?)
        """,
        (task, deadline)
    )

    db.commit()

    return f"Tugas '{task}' berhasil disimpan."

def complete_task(task_name):
    cursor.execute(
        """UPDATE tasks
        SET status = 'selesai'
        WHERE task = ?
        """,
        (task_name,)
    )

    db.commit()

    return f"Tugas '{task_name}'sudah di tandai sebagai selesai."

def delete_task(task_name):
    cursor.execute(
        """DELETE FROM tasks
        WHERE task = ?
        """,
        (task_name,)
    )

    db.commit()

    return f"Tugas '{task_name}'berhasil di hapus."
# =========================
# MIEL
# =========================

print("MIEL: Halo, saya MIEL. Ada yang bisa saya bantu?")

while True:

    user_input = input("Kamu: ")

    if user_input.lower().startswith("tambah tugas"):
        task_input = user_input[12:].strip()

        if "deadline" in task_input.lower():
            task_name, deadline = task_input.split("deadline", 1)

            task_name = task_name.strip()
            deadline = deadline.strip()

            print("MIEL:", add_task(task_name, deadline))

        else:
            print("MIEL:", add_task(task_input))

        continue
    if user_input.lower().startswith("selesai"):
        task_name = user_input[7:].strip()

        if task_name:
            print("MIEL:", complete_task(task_name))
        else:
            print("MIEL: Tugas mana yang sudah selesai?")

            continue

    if user_input.lower() in ["keluar", "exit", "quit"]:
        print("MIEL: Baik, sampai jumpa.")
        break

    if user_input.lower().startswith("hapus tugas"):
        task_name = user_input[11:].strip() 

        if task_name:
            print("MIEL: ",delete_task(task_name))
        else:
            print("MIEL: Tugas mana yang mau dihapus")

            continue

    if "tugas" in user_input.lower():
        print("MIEL:", get_tasks())
        continue

    # AI MIEL
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": """
Kamu adalah MIEL, asisten AI pribadi saya.

Gunakan bahasa Indonesia.
Jawab dengan natural, singkat, dan jelas.
Jangan memberikan informasi yang tidak relevan.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("MIEL:", response["message"]["content"])