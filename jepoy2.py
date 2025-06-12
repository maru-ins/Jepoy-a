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

    # Ambil halaman utama dan form search
    print("[~] Mengambil form dari halaman utama...")
    resp = requests.get("https://zefoy.com", headers=headers)
    if resp.status_code != 200:
        print("[x] Gagal mengakses Zefoy.com (status code != 200)")
        return

    soup = BeautifulSoup(resp.text, 'html.parser')
    form = soup.find('form', action=True)
    if not form:
        print("[x] Gagal menemukan form. Pastikan CAPTCHA sudah diisi dan cookie benar.")
        return

    endpoint = 'https://zefoy.com/' + form['action']
    search_field = form.find('input', {'type': 'search'})['name']
    print(f"[✓] Endpoint: {endpoint}")
    print(f"[✓] Search field name: {search_field}\n")

    # Input data video
    link = input("[>] Masukkan link TikTok: ").strip()
    try:
        count = int(input("[>] Berapa kali ingin dijalankan?: ").strip())
    except ValueError:
        print("[x] Input jumlah tidak valid.")
        return

    for i in range(1, count + 1):
        print(f"\n[#] Percobaan ke-{i}/{count}: Searching video...")
        # Step 1: Search untuk dapat hidden fields
        data_search = {search_field: link}
        r1 = requests.post(endpoint, headers=headers, data=data_search)
        if r1.status_code != 200:
            print("[x] Gagal POST search, status code:", r1.status_code)
            break

        soup1 = BeautifulSoup(r1.text, 'html.parser')
        hidden_inputs = soup1.find_all('input', {'type': 'hidden'})
        payload = {inp['name']: inp['value'] for inp in hidden_inputs}
        if not payload:
            print("[x] Gagal mengambil hidden inputs.")
            break

        print(f"[~] Found hidden fields: {list(payload.keys())}")

        # Step 2: Submit boost request
        print("[#] Mengirim request boost...")
        r2 = requests.post(endpoint, headers=headers, data=payload)
        text = r2.text

        # Deteksi delay atau success
        if 'Please wait' in text:
            # parse wait time
            m = re.search(r'Please wait (\d+) minute', text)
            s = re.search(r'(\d+) seconds', text)
            wait = 300
            if m and s:
                wait = int(m.group(1)) * 60 + int(s.group(1))
            print(f"[!] Harus menunggu {wait} detik sebelum submit berikutnya...")
            time.sleep(wait)
            continue
        elif 'Next Submit: READY' in text or r2.status_code == 200:
            print(f"[✓] Boost ke-{i} berhasil!")
        else:
            print("[!] Respons tak terduga, periksa manual output:")
            print(text)

        # Delay kecil antar percobaan
        time.sleep(5)

    print("\n[✓] Semua percobaan selesai.")


if __name__ == '__main__':
    main()
