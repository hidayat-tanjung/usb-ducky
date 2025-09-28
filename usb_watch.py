import os
import time
import subprocess

# Path USB yang mau dicek (ganti sesuai drive USB lo)
usb_drive = "E:\\"

while True:
    if os.path.exists(usb_drive):
        print("USB terdeteksi! Menjalankan script...")
        subprocess.run(["python", "duck.py"])  # Ganti dengan script lo
        break
    time.sleep(5)  # Cek setiap 5 detik
