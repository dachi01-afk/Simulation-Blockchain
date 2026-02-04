# ⛓️ Simulation Blockchain

Simulation Blockchain adalah proyek simulasi **blockchain sederhana** menggunakan **Python dan Flask**.  
Proyek ini dibuat untuk membantu memahami konsep dasar blockchain seperti pembuatan blok, hash, dan hubungan antar blok dalam sebuah jaringan blockchain sederhana.

---

## 📌 Tujuan Projek

- Memahami konsep dasar blockchain
- Mensimulasikan proses pembentukan blok
- Menampilkan blockchain melalui antarmuka web
- Media pembelajaran blockchain untuk pemula

---

## 🧠 Gambaran Umum Sistem

Proyek ini bekerja dengan cara:
1. Flask dijalankan sebagai web server
2. Blockchain dibuat dan disimpan di backend (Python)
3. Data blockchain ditampilkan melalui browser
4. Setiap blok saling terhubung menggunakan hash
5. Blok baru dapat ditambahkan ke dalam chain

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Keterangan |
|---------|-----------|
| Python | Bahasa pemrograman utama |
| Flask | Framework backend / web server |
| HTML | Tampilan antarmuka |
| CSS | Styling UI |
| JavaScript | Interaksi client |
| Werkzeug | HTTP utilities (Flask) |

---

## 📂 Struktur Folder

Simulation-Blockchain/
├── app/
│ ├── static/ # File CSS dan JavaScript
│ ├── templates/ # File HTML
│ └── init.py # Inisialisasi aplikasi Flask
├── config.py # Konfigurasi aplikasi
├── run.py # File utama untuk menjalankan server
├── requirements.txt # Daftar dependency Python
├── README.md # Dokumentasi project


---

## ⚙️ Cara Instalasi & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/dachi01-afk/Simulation-Blockchain.git
2️⃣ Masuk ke Folder Project
cd Simulation-Blockchain
3️⃣ (Opsional) Buat Virtual Environment
python -m venv venv
Aktifkan virtual environment:

Windows:

venv\Scripts\activate
Linux / Mac:

source venv/bin/activate
4️⃣ Install Dependency
pip install -r requirements.txt
▶️ Cara Menjalankan Aplikasi
Jalankan perintah berikut:

python run.py
Jika berhasil, aplikasi akan berjalan di:

http://127.0.0.1:5000/
Buka alamat tersebut di browser.

🧱 Penjelasan Konsep Blockchain di Project Ini
Block
Setiap blok berisi data, timestamp, hash, dan previous hash

Hash
Digunakan sebagai identitas unik blok

Previous Hash
Menghubungkan satu blok dengan blok sebelumnya

Blockchain
Kumpulan blok yang saling terhubung dan tervalidasi

🌐 Antarmuka Web
Aplikasi menyediakan antarmuka web sederhana untuk:

Melihat daftar blok

Melihat hash tiap blok

Menambahkan blok baru

Memahami alur blockchain secara visual

📸 Screenshot (Opsional)
Tambahkan screenshot UI jika diperlukan:

docs/screenshot.png
🧑‍💻 Author
Jimi Firgo Dakhi
GitHub: https://github.com/dachi01-afk

📌 Catatan
Proyek ini bersifat simulasi dan bukan blockchain produksi.
Cocok untuk pembelajaran, tugas kuliah, dan eksperimen awal.

🚀 Pengembangan Selanjutnya
Simulasi multi-node

Proof of Work (PoW)

Proof of Stake (PoS)

Visualisasi grafik blockchain

Penyimpanan blockchain ke database
