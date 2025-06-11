import requests
import time
import re
from bs4 import BeautifulSoup

# Step 1: Minta user input manual
print("[!] Silakan buka https://zefoy.com di browser dan selesaikan CAPTCHA.")
cookie = input("[>] Masukkan PHPSESSID: ").strip()

headers = {
    "User-Agent": "Mozilla/5.0 (Android 15; Mobile; rv:141.0) Gecko/141.0 Firefox/141.0",
    "Cookie": f"PHPSESSID={cookie}",
}

# Step 2: Ambil nama field dinamis dari form input
print("[~] Mengakses halaman utama Zefoy...")
res = requests.get("https://zefoy.com", headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
form = soup.find("form")

if not form or not form.get("action"):
    print("[x] Gagal mengambil form dari halaman, pastikan CAPTCHA sudah selesai dan cookie valid.")
    exit()

endpoint = "https://zefoy.com/" + form.get("action")
input_field = form.find("input")

if not input_field or not input_field.get("name"):
    print("[x] Gagal menemukan input field, mungkin CAPTCHA belum selesai atau format berubah.")
    exit()

field_name = input_field.get("name")
print(f"[✓] Endpoint: {endpoint}\n[✓] Nama Field: {field_name}\n")

# Step 3: Input fitur dan link
print("Pilih fitur yang ingin digunakan:")
print("1. View\n2. Like")
fitur = input("[>] Masukkan angka fitur: ").strip()
link = input("[>] Masukkan link TikTok: ").strip()
jumlah = int(input("[>] Berapa kali ingin dijalankan?: ").strip())

# Step 4: Jalankan loop sesuai jumlah
for i in range(jumlah):
    print(f"\n[#] Percobaan ke-{i+1}...")
    payload = {
        field_name: link
    }

    r = requests.post(endpoint, headers=headers, data=payload)
    
    if "Too many requests" in r.text or "Please wait" in r.text:
        print("[!] Kena delay, menunggu 5 menit...")
        for s in range(300, 0, -1):
            print(f"    Tunggu {s} detik...", end="\r")
            time.sleep(1)
        continue
    
    if "Session expired" in r.text or "Invalid" in r.text:
        print("[x] Session tidak valid. Coba ulangi CAPTCHA dan ambil PHPSESSID baru.")
        break

    print("[✓] Berhasil mengirim request!")
    time.sleep(5)  # Delay antar request biar aman

print("\n[✓] Selesai!")
