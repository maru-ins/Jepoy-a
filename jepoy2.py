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

    res = requests.get("https://zefoy.com", headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.find('form', action=True)
    if not form:
        print("[x] Form tidak ditemukan. Pastikan captcha selesai dan cookie valid.")
        return

    endpoint = 'https://zefoy.com/' + form['action']
    input_field = form.find('input', {'type': 'search'})
    if not input_field:
        print("[x] Field pencarian tidak ditemukan.")
        return

    field_name = input_field.get('name')
    link = input("[>] Masukkan link TikTok: ").strip()
    try:
        jumlah = int(input("[>] Berapa kali ingin dijalankan?: ").strip())
    except ValueError:
        print("[x] Jumlah tidak valid.")
        return

    for i in range(jumlah):
        print(f"\n[#] Percobaan ke-{i+1}/{jumlah}")
        data_search = {field_name: link}
        r1 = requests.post(endpoint, headers=headers, data=data_search)

        soup1 = BeautifulSoup(r1.text, 'html.parser')
        boost_form = soup1.find('form', action=form['action'])
        if not boost_form:
            print("[!] Tidak menemukan form pengiriman. Mungkin sedang delay.")
            if 'Please wait' in r1.text:
                delay_match = re.search(r'(\d+)\s*seconds', r1.text)
                wait_time = int(delay_match.group(1)) if delay_match else 300
                print(f"[~] Menunggu {wait_time} detik...")
                time.sleep(wait_time)
                continue
            continue

        hidden_inputs = boost_form.find_all('input', {'type': 'hidden'})
        payload = {inp['name']: inp['value'] for inp in hidden_inputs if inp.get('name') and inp.get('value')}

        if not payload:
            print("[x] Tidak menemukan data tersembunyi untuk dikirim.")
            continue

        r2 = requests.post(endpoint, headers=headers, data=payload)
        if 'Please wait' in r2.text or 'views-countdown' in r2.text:
            print("[!] Terkena limit. Menunggu...")
            delay = 300
            match = re.search(r'(\d+)\s*seconds', r2.text)
            if match:
                delay = int(match.group(1))
            print(f"[~] Delay: {delay} detik")
            time.sleep(delay)
        else:
            print(f"[✓] Boost ke-{i+1} berhasil!")

        time.sleep(5)

    print("\n[✓] Semua percobaan selesai.")


if __name__ == '__main__':
    main()
