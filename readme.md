# USB-Ducky: Emulasi USB Rubber Ducky dengan USB Biasa

## Deskripsi
**usb-ducky** adalah proyek untuk menjadikan USB flash drive biasa sebagai alat emulasi USB Rubber Ducky menggunakan fitur autorun. Proyek ini memungkinkan eksekusi skrip otomatis (payload) untuk keperluan pentesting etis atau edukasi keamanan siber. Cocok untuk simulasi serangan sederhana tanpa hardware khusus.

**Peringatan:** Gunakan hanya untuk tujuan edukasi atau pentesting dengan izin. Penyalahgunaan dapat melanggar hukum.

## Fitur
- Mengubah USB biasa menjadi alat pentesting dengan autorun.
- Mendukung payload berbasis Batch (.bat) atau PowerShell.
- Kompatibel dengan Windows (autorun harus aktif).
- Mudah dimodifikasi untuk berbagai skenario.
- Tidak memerlukan hardware Rubber Ducky.

## Persyaratan
- USB flash drive (disarankan 4GB+).
- Komputer Windows untuk setup.
- Software autorun (misal: USB Autorun Creator) atau buat manual `autorun.inf`.
- Pengetahuan dasar scripting (Batch/PowerShell).

**Catatan:** Autorun sering dinonaktifkan di Windows modern. Pastikan target mengizinkan autorun atau gunakan social engineering.

## Cara Setup
1. **Format USB:**
   - Colok USB, format ke FAT32 (File Explorer > Klik kanan USB > Format > FAT32).

2. **Download Repo:**
   ```bash
   git clone https://github.com/PsychoH4x0r/usb-ducky.git
   cd usb-ducky
