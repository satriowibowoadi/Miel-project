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

    if user_input.lower() in ["exit", "quit", "keluar"]:
        print("MIEL:Baik, Sampai jumpa!")
        break

    #========================
    #AI PARSER
    #========================

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": """
Kamu adalah parser perintah untuk AI assistant.

Tugasmu adalah mengubah kalimat pengguna menjadi JSON.

Tugasmu adalah mengubah kalimat pengguna menjadi JSON.

ATURAN UTAMA:

1. Tugas utama kamu adalah memahami maksud pengguna dan mengubahnya menjadi JSON yang sesuai.

2. Jangan pernah mengarang informasi yang tidak diberikan pengguna.

3. Jangan pernah mengarang nama tugas.

4. Jangan pernah mengarang deadline.

5. Pisahkan nama tugas dan deadline dengan benar.

6. Kata "tugas", "PR", "pekerjaan", atau "assignment" tidak otomatis menjadi nama tugas. Tentukan dari konteks kalimat.

7. Jika pengguna mengatakan memiliki atau ingin menambahkan tugas baru, gunakan action "add_task".

8. Jika pengguna hanya menyebut kata "tugas" tetapi tidak bermaksud menambahkan tugas, jangan gunakan "add_task".

9. Jika pengguna meminta melihat, mengecek, menampilkan, atau mengetahui daftar tugasnya, gunakan action "get_tasks".

10. Jika pengguna mengatakan suatu tugas sudah selesai, gunakan action "complete_task".

11. Jika pengguna meminta menghapus, membatalkan, atau membuang suatu tugas, gunakan action "delete_task".

12. Jika pengguna hanya menyapa, bertanya, bercanda, memberikan informasi umum, atau mengobrol tanpa meminta tindakan terhadap tugas, gunakan action "chat".

13. Jika pengguna tidak menyebut nama tugas dengan jelas, nilai "task" harus null.

14. Jika pengguna tidak menyebut deadline, nilai "deadline" harus null.

15. Jangan memasukkan deadline ke dalam nama tugas.

16. Jangan memasukkan kata "deadline", "besok", "lusa", nama hari, tanggal, atau waktu ke dalam nama tugas jika kata tersebut berfungsi sebagai informasi waktu.

17. Pahami variasi bahasa sehari-hari, bahasa informal, singkatan, dan susunan kalimat yang berbeda. Jangan hanya mencocokkan kalimat dengan contoh.

18. Pahami maksud kalimat berdasarkan keseluruhan konteks, bukan berdasarkan satu kata saja.

19. "Besok", "lusa", "hari Senin", "hari Jumat", "tanggal 20", "jam 10", dan informasi waktu lainnya dapat menjadi deadline jika digunakan sebagai batas waktu tugas.

20. Jika pengguna mengatakan "aku punya tugas matematika", pahami bahwa pengguna memiliki tugas bernama "matematika".

21. Jika pengguna mengatakan "aku ada tugas matematika deadline besok", maka task adalah "matematika" dan deadline adalah "besok".

22. Jika pengguna mengatakan "tolong tambahkan tugas matematika", maka gunakan action "add_task".

23. Jika pengguna mengatakan "tugas matematika sudah selesai", maka gunakan action "complete_task" dengan task "matematika".

24. Jika pengguna mengatakan "hapus tugas matematika", maka gunakan action "delete_task" dengan task "matematika".

25. Jika pengguna mengatakan "tugas saya apa saja?", "aku punya tugas apa?", atau "coba cek tugas", gunakan action "get_tasks".

26. Jika pengguna mengatakan sesuatu yang ambigu dan informasi yang diperlukan tidak tersedia, jangan menebak. Gunakan null pada bagian informasi yang tidak diketahui.

27. Selalu pertahankan informasi yang diberikan pengguna tanpa mengubah makna.

28. Jangan menambahkan kata-kata yang tidak diperlukan ke dalam nilai task.

29. Nama tugas dapat terdiri dari satu atau beberapa kata.

30. Nama tugas dapat berupa nama mata kuliah, proyek, pekerjaan, laporan, praktikum, atau aktivitas lainnya.

31. Jika pengguna menyebut beberapa informasi dalam satu kalimat, pisahkan setiap informasi ke field yang sesuai.

32. Jika pengguna meminta tindakan terhadap tugas, prioritaskan action tugas daripada "chat".

33. Jika pengguna hanya membicarakan tugas tanpa meminta tindakan dan tanpa menyatakan ingin menambahkan, melihat, menyelesaikan, atau menghapus tugas, gunakan action "chat".

34. Output harus selalu berupa JSON yang valid.

35. Jangan memberikan penjelasan, markdown, atau teks tambahan di luar JSON.


Action yang tersedia:
- add_task
- get_tasks
- complete_task
- delete_task
-chat

CONTOH:

Input:
halo MIEL

Output:
{
    "action": "chat",
    "task": null,
    "deadline": null
}

Input:
aku ada tugas matematika

Output:
{
    "action": "add_task",
    "task": "matematika",
    "deadline": null
}

Input:
besok ada tugas basis data

Output:
{
    "action": "add_task",
    "task": "basis data",
    "deadline": "besok"
}

Input:
aku punya tugas pemrograman web yang harus dikumpulkan Jumat

Output:
{
    "action": "add_task",
    "task": "pemrograman web",
    "deadline": "Jumat"
}

Input:
tolong masukin tugas data mining deadline Senin

Output:
{
    "action": "add_task",
    "task": "data mining",
    "deadline": "Senin"
}

Input:
aku ada tugas laporan praktikum

Output:
{
    "action": "add_task",
    "task": "laporan praktikum",
    "deadline": null
}

Input:
tugas saya apa aja?

Output:
{
    "action": "get_tasks",
    "task": null,
    "deadline": null
}

Input:
coba cek tugas yang belum selesai

Output:
{
    "action": "get_tasks",
    "task": null,
    "deadline": null
}

Input:
aku punya tugas apa?

Output:
{
    "action": "get_tasks",
    "task": null,
    "deadline": null
}

Input:
matematika sudah selesai

Output:
{
    "action": "complete_task",
    "task": "matematika",
    "deadline": null
}

Input:
tugas matematika udah kelar

Output:
{
    "action": "complete_task",
    "task": "matematika",
    "deadline": null
}

Input:
hapus tugas matematika

Output:
{
    "action": "delete_task",
    "task": "matematika",
    "deadline": null
}

Input:
buang tugas data mining

Output:
{
    "action": "delete_task",
    "task": "data mining",
    "deadline": null
}

Input:
hari ini capek banget

Output:
{
    "action": "chat",
    "task": null,
    "deadline": null
}

Input:
kamu bisa bantu aku?

Output:
{
    "action": "chat",
    "task": null,
    "deadline": null
}

Jawab HANYA JSON dengan format berikut:

{
"action": "nama_action",
"task": "nama_tugas",
"deadline": "deadline atau null"
}
"""

            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    #========================
    #BACA HASIL AI
    #========================

    import json

    text = response["message"]["content"].strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {
            "action": "chat",
            "task": None,
            "deadline": None
        }

    # =========================
    # MENENTUKAN AKSI
    # =========================

    if data["action"]=="add_task":

        if data["task"] is None:
            print("MIEL: Tugasnya apa?")
        else:
            print(
                "MIEL: ",
                add_task(
                    data["task"],
                    data["deadline"]
                )
            )

    elif data["action"] == "get_tasks":
        print("MIEL:", get_tasks())

    elif data["action"] == "complete_task":

        if data["task"] is None:
            print("MIEL: Tugas mana yang sudah selesai?")
        else:
            print(
                "MIEL:",
                complete_task(data["task"])
            )

    elif data["action"] == "delete_task":

        if data["task"] is None:
            print("MIEL: Tugas mana yang mau dihapus?")
        else:
            print(
                "MIEL:",
                delete_task(data["task"])
            )

    else:

        #========================
        #CHAT BIASA
        #========================

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": """Kamu adalah MIEL, asisten AI pribadi saya.
                    
                    Gunakan bahasa indonesia yang santai, ramah, dan hangat.
                    Jawab dengan natural, singkat, dan jelas.
                    """

                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        print("MIEL:", response["message"]["content"])