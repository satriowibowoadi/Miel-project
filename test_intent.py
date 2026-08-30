import ollama
import json

user_input = input("Kamu: ")

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "system",
            "content": """
Kamu adalah sistem untuk memahami perintah pengguna.

Tentukan action:
- add_task
- get_tasks
- complete_task
- delete_task
- chat

Jika action adalah add_task, ambil nama tugas dan deadline jika ada.

Jawab HANYA dalam format JSON seperti ini:

{
    "action": "add_task",
    "task": "nama tugas",
    "deadline": "deadline atau null"
}

Jika bukan add_task, gunakan:

{
    "action": "nama_action",
    "task": null,
    "deadline": null
}
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