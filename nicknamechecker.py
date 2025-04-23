import requests
import time
import tkinter as tk
from tkinter import messagebox
import os

token_file = "tokens.txt"
input_file = "usernameslist.txt"
output_file = "emptyusernames.txt"

if os.path.exists(output_file):
    os.remove(output_file)

def check_usernames():
    with open(token_file, "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]

    with open(input_file, "r", encoding="utf-8") as f:
        usernames = [line.strip() for line in f if line.strip()]

    token_index = 0  # İlk token ile başla
    while usernames and token_index < len(tokens):
        token = tokens[token_index]
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        for i in range(min(3, len(usernames))):
            username = usernames[i]
            payload = {
                "username": username
            }

            response = requests.post("https://discord.com/api/v9/users/@me/relationships", json=payload, headers=headers)

            if response.status_code == 400:
                if "Unknown User" in response.text:
                    print(f"[BOŞ] {username}")
                    with open(output_file, "a", encoding="utf-8") as out:
                        out.write(username + "\n")
                else:
                    print(f"[DOLU] {username} - HATA: {response.text}")
            elif response.status_code == 204 or "Already friends" in response.text:
                print(f"[DOLU] {username}")
            else:
                print(f"[??] {username} - DURUM: {response.status_code}, CEVAP: {response.text}")

            time.sleep(4)

        usernames = usernames[3:]

        token_index += 1

        if token_index == len(tokens):
            break

    print("Tüm işlemler tamamlandı.")

def on_start():
    print("İşlem başlatıldı...")
    check_usernames()
    messagebox.showinfo("Bilgi", "Tüm işlemler tamamlandı. Program kapanıyor.")
    window.quit()  # Programı kapat

window = tk.Tk()
window.title("Discord Kullanıcı Adı Kontrol Aracı")
window.geometry("400x250")

label1 = tk.Label(window, text="Discord Token'larını (virgül ile ayırarak) girin:")
label1.pack(pady=10)

start_button = tk.Button(window, text="Başlat", command=on_start)
start_button.pack(pady=20)

window.mainloop()
