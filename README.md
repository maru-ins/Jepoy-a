![Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Python_logo_1990s.svg/1280px-Python_logo_1990s.svg.png)

# JepoyOtomatis
By mpa


# 🎯 Zefoy Auto View / Like Sender (Termux Edition)

Script Python sederhana untuk memanfaatkan fitur **Views** atau **Likes** TikTok dari [Zefoy.com](https://zefoy.com), dengan captcha input manual dan bypass limit 5 menit.  
✅ Cocok dijalankan langsung di **Termux + Android Browser**.

---

## 🔧 Fitur

- Manual input captcha di awal
- Pilih fitur (views atau likes)
- Input link TikTok langsung dari user
- Loop otomatis sesuai jumlah yang diinginkan
- Bypass limit antar pengiriman
- Tidak perlu login TikTok

---

## 🧪 Prasyarat

- Android dengan Termux
- Browser (untuk isi captcha Zefoy)
- Aplikasi [HTTP Canary](https://play.google.com/store/apps/details?id=com.guoshi.httpcanary) (untuk ambil endpoint, cookies, dll)
- Alternatif Http Canary > [FireFox Nightly + extension Dev App](https://play.google.com/store/apps/details?id=org.mozilla.fenix)

---

## 📦 Instalasi di Termux

```bash
pkg update && pkg upgrade -y
pkg install python -y
pip install requests beautifulsoup4

atau

> pip install -r requirements.txt
> python GAS.py

```

Kieu alur na : 
1. Isi captcha di browser (manual).
2. Copy cookies dari browser andalan canary/firefox
3. Pilih fitur (views atau likes).
4. Masukkan link TikTok.
5. Tentukan berapa kali ingin dijalankan.
6. Dagoan deh🔥


#☕ Supprot
Bila kamu merasa script ini membantu, jangan lupa kasih ⭐ di repo ini!
