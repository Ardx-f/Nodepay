import requests
from loguru import logger
import json
import os

# Konfigurasi endpoint
DASHBOARD_URL = "https://app.nodepay.ai/dashboard"  # URL dashboard pengguna

# Nama file untuk menyimpan cookies
COOKIES_FILE = "cookies.json"

def save_cookies(cookies):
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f)
    logger.info("Cookies berhasil disimpan.")

def load_cookies():
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    return None

def get_dashboard_info(cookies):
    try:
        response = requests.get(DASHBOARD_URL, cookies=cookies, timeout=15)
        response.raise_for_status()
        logger.info("Data dashboard berhasil diambil.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error saat mengambil data dashboard: {e}")
        return None

def main():
    os.system('clear')

    # Coba memuat cookies dari file
    cookies = load_cookies()
    if cookies:
        logger.info("Cookies berhasil dimuat dari file.")
    else:
        # Jika tidak ada cookies, minta input dari pengguna
        cookies_input = input("Masukkan cookies dalam format JSON: ")
        try:
            cookies = json.loads(cookies_input)  # Mengubah string JSON menjadi dict
            save_cookies(cookies)  # Simpan cookies untuk penggunaan selanjutnya
        except json.JSONDecodeError:
            logger.error("Format cookies tidak valid. Pastikan dalam format JSON.")
            exit(1)

    # Menggunakan cookies untuk mendapatkan informasi dashboard
    dashboard_info = get_dashboard_info(cookies)
    if dashboard_info:
        logger.info(f"Informasi dashboard: {dashboard_info}")

if __name__ == "__main__":
    main()
