import ollama
import json
import sqlite3

db = sqlite3.connect("db/miel.db")
cursor = db.cursor()

def add_task(task, deadline=None):
    cursor.execute(
        """INSERT INTO  tasks(task, deadline)
        VALUES (?, ?)
        """,
        (task, deadline)
    )

    db.commit()

    return f"Tugas '{task}' berhasil disimpan."

user_input = input("Kamu: ")

response = ollama.chat(
    model="qwen2.5:3b",
messages = [
    {
        "role": "system",
        "content": """
Kamu adalah parser perintah untuk AI assistant.

Tugasmu adalah mengubah kalimat pengguna menjadi JSON.

ATURAN SANGAT PENTING:
1. Jangan pernah mengarang nama tugas.
2. Kata deadline, hari, nama hari, tanggal, atau waktu BUKAN nama tugas.
3. Jika pengguna tidak menyebut nama tugas, task harus null.
4. Deadline harus dipisahkan dari nama tugas.
5. Jika deadline tidak disebutkan, deadline harus null.
6. Jangan memasukkan deadline ke dalam task.
7. Hanya gunakan informasi yang benar-benar disebutkan pengguna.

Action yang tersedia:
- add_task
- get_tasks
- complete_task
- delete_task
- chat

Contoh:

Input:
aku ada tugas deadline hari selasa

Output:
{
    "action": "add_task",
    "task": null,
    "deadline": "hari selasa"
}

Input:
aku ada tugas data mining deadline hari selasa

Output:
{
    "action": "add_task",
    "task": "data mining",
    "deadline": "hari selasa"
}

Jawab HANYA JSON.
"""
    },
    {
        "role": "user",
        "content": user_input
    }
]
)

text = response["message"]["content"]

data = json.loads(text)

print("Action:", data["action"])
print("Task:", data["task"])
print("Deadline:", data["deadline"])

#menentukan aksi
if data["action"] == "add_task":
    if data["task"] is None:
        print("MIEL: Tugasnya apa?")
    else:
        print("MIEL",
              add_task(
                  data["task"],
                  data["deadline"]
                  )
              )
elif data["action"] == "get_tasks":
    print("MIEL: Saya akan mengambil daftar tugas.")

elif data["action"] == "complete_task":
    print("MIEL: Saya akan menyelesaikan daftar tugas.")

elif data["action"] == "delete_tasks":
    print("MIEL: Saya akan menghapus daftar tugas.")

else:
    print("MIEL: Saya akan ngobrol dengan kamu.")