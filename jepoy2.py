import requests
import time
import re
from bs4 import BeautifulSoup

def main():
    print("[!] Silakan buka https://zefoy.com di browser dan selesaikan CAPTCHA.")
    phpsessid = input("[>] Masukkan PHPSESSID: ").strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 15; Mobile; rv:141.0) Gecko/141.0 Firefox/141.0",
        "Cookie": f"PHPSESSID={phpsessid}"
    }

    # 1) Ambil form Search
    res = requests.get("https://zefoy.com", headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    search_form = soup.find('form', action=True)
    endpoint = 'https://zefoy.com/' + search_form['action']
    search_field = search_form.find('input', {'type': 'search'})['name']

    # Input user
    link = input("[>] Masukkan link TikTok: ").strip()
    total_runs = int(input("[>] Berapa kali ingin dijalankan?: ").strip())

    for attempt in range(1, total_runs + 1):
        print(f"\n[#] Percobaan ke-{attempt}/{total_runs}")

        # 2) POST Search → dapat form kedua
        r_search = requests.post(endpoint, headers=headers, data={search_field: link})
        soup2 = BeautifulSoup(r_search.text, 'html.parser')
        send_form = soup2.find('form', action=search_form['action'])
        if not send_form:
            wait_el = soup2.find(class_='views-countdown')
            if wait_el:
                m, s = re.findall(r'(\d+)\s*minute.*?(\d+)\s*seconds', wait_el.text)[0]
                delay = int(m)*60 + int(s)
                print(f"[!] Harus menunggu {delay} detik...")
                time.sleep(delay)
                continue
            print("[x] Gagal menemukan form kirim views.")
            continue

        # 3) Ambil hidden inputs → payload
        hidden = {inp['name']: inp['value']
                  for inp in send_form.find_all('input', {'type': 'hidden'})}
        if not hidden:
            print("[x] Hidden inputs tidak ditemukan.")
            continue

        # 4) POST boost
        r_send = requests.post(endpoint, headers=headers, data=hidden)
        if 'views-countdown' in r_send.text:
            wait_el = BeautifulSoup(r_send.text, 'html.parser').find(class_='views-countdown')
            m, s = re.findall(r'(\d+)\s*minute.*?(\d+)\s*seconds', wait_el.text)[0]
            delay = int(m)*60 + int(s)
            print(f"[!] Delay lagi: {delay} detik.")
            time.sleep(delay)
        else:
            print(f"[✓] Boost ke-{attempt} berhasil!")

        time.sleep(5)

    print("\n[✓] Semua percobaan selesai.")

if __name__ == '__main__':
    main()
