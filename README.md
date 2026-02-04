# Dokumentasi — Simulation-Blockchain

Sebuah simulasi jaringan blockchain terdistribusi sederhana dibangun dengan Python & Flask. Dokumentasi ini menjelaskan arsitektur, API, cara menjalankan, konfigurasi, serta panduan kontribusi dan pengembangan.

---

## Ringkasan singkat
- Nama repo: `dachi01-afk/Simulation-Blockchain`  
- Deskripsi: Simple distributed blockchain network using Python & Flask  
- Bahasa utama: Python (inti aplikasi). Frontend menggunakan JavaScript / HTML / CSS.

Aplikasi ini mengimplementasikan:
- Model Block sederhana (index, transactions, timestamp, previous_hash, nonce, hash).
- Proof-of-Work (PoW) untuk menambang blok.
- Antrian transaksi (pending transactions).
- Mekanisme jaringan dasar: pendaftaran node (register), broadcast blok, dan konsensus berdasarkan chain terpanjang (replace_chain).
- Halaman web sederhana (templates/static) untuk visualisasi dan operasi manual.

---

## Struktur proyek (ringkasan)
- `run.py` — Entrypoint; jalankan Flask app, menerima argumen port (contoh: `python run.py 5001`).
- `config.py` — Konfigurasi global (mis. `DIFFICULTY`, `BOOTSTRAP_NODES`). Lihat [config.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/config.py).
- `requirements.txt` — Dependensi Python.
- `LICENSE` — Lisensi MIT.

- `app/`
  - `__init__.py`
  - `routes.py` — Semua route API & halaman web (lihat: [app/routes.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/app/routes.py)).
  - `blockchain/`
    - `blockchain.py` — Logika blockchain: chain, pending_transactions, mining, jaringan dan konsensus (replace_chain).
    - `block.py` — Model Block dan `calculate_hash()`.
    - `consensus.py` — ProofOfWork sederhana.
    - `utils.py` — Fungsi utilitas (`serialize_block`).
  - `network/`
    - `node.py` — Logika pendaftaran node, broadcast, dsb.
- `templates/` dan `static/` — Frontend (dashboard, halaman chain/transactions/mine/nodes).

---

## Konfigurasi penting
- DIFFICULTY (integer) — tingkat kesulitan PoW; semakin besar nilai, semakin lama proses mining.
- BOOTSTRAP_NODES (list) — daftar alamat node bootstrap yang akan dihubungi saat node mulai untuk menemukan peers.

Periksa `config.py` untuk menyesuaikan nilai: [config.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/config.py)

---

## Instalasi & menjalankan
Prasyarat:
- Python 3.8+
- pip
- (opsional) virtual environment

Langkah:
1. Clone repo:
   ```bash
   git clone https://github.com/dachi01-afk/Simulation-Blockchain.git
   cd Simulation-Blockchain
   ```

2. (Opsional) Buat virtualenv dan aktifkan:
   ```bash
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows (PowerShell)
   venv\Scripts\Activate.ps1
   # Windows (cmd)
   venv\Scripts\activate
   ```

3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

4. Menjalankan node:
   - Node default pada port 5000:
     ```bash
     python run.py 5000
     ```
   - Menjalankan node lain pada port 5001, 5002, dll:
     ```bash
     python run.py 5001
     python run.py 5002
     ```

Setiap node akan mencoba mendaftar ke `BOOTSTRAP_NODES` (lihat `config.py`) dan melakukan sinkronisasi chain secara otomatis.

---

## API — Endpoint utama
Implementasi endpoint ada di `app/routes.py` — lihat file untuk detail: [app/routes.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/app/routes.py)

Ringkasan endpoint:

- GET /api/chain  
  Ambil seluruh chain lokal (array blok ter-serialize).  
  Contoh:
  ```bash
  curl "http://localhost:5000/api/chain"
  ```

- POST /api/transactions  
  Tambah transaksi ke antrian pending. Body: JSON transaksi (contoh umum):
  ```json
  { "sender": "Alice", "recipient": "Bob", "amount": 10 }
  ```
  Contoh:
  ```bash
  curl -X POST "http://localhost:5000/api/transactions" \
    -H "Content-Type: application/json" \
    -d '{"sender":"Alice","recipient":"Bob","amount":10}'
  ```

- GET /api/mine  
  Memicu proses mining (membuat blok dari pending transactions). Jika tidak ada transaksi, akan mengembalikan pesan error.
  ```bash
  curl -X GET "http://localhost:5000/api/mine"
  ```

- GET /api/validate  
  Mengecek apakah chain lokal valid menurut `is_chain_valid()`.
  ```bash
  curl "http://localhost:5000/api/validate"
  ```

- POST /api/register-node  
  Mendaftarkan node baru. Body:
  ```json
  { "address": "http://localhost:5001" }
  ```
  Contoh:
  ```bash
  curl -X POST "http://localhost:5000/api/register-node" \
    -H "Content-Type: application/json" \
    -d '{"address":"http://localhost:5001"}'
  ```

  Catatan:
  - Node tidak akan mendaftarkan dirinya sendiri.
  - Saat menerima node baru, server mengirim daftar peers yang sudah ada ke node baru agar terhubung dua arah.
  - Node akan menyebarkan node baru ke peers lainnya.

- POST /api/receive-block  
  Endpoint untuk menerima blok yang di-broadcast oleh peer. Jika `previous_hash` tidak cocok, node akan memanggil `replace_chain()` untuk sinkronisasi.

---

## Halaman Web (UI)
Route halaman:
- GET / — Dashboard
- GET /chain-page — Tampilan chain
- GET /transaction-page — Tambah transaksi
- GET /mine-page — Halaman mining
- GET /nodes — Kelola nodes

Folder `templates/` dan `static/` berisi asset & halaman yang digunakan.

---

## Alur contoh menjalankan beberapa node (praktis)
1. Terminal A:
   ```bash
   python run.py 5000
   ```
2. Terminal B:
   ```bash
   python run.py 5001
   ```
3. Daftarkan node B ke A:
   ```bash
   curl -X POST "http://localhost:5000/api/register-node" \
     -H "Content-Type: application/json" \
     -d '{"address":"http://localhost:5001"}'
   ```
4. Tambah transaksi di salah satu node, lalu panggil `/api/mine`. Node yang menambang akan men-broadcast blok baru; peers akan memeriksa dan melakukan `replace_chain()` jika diperlukan.

---

## Desain & implementasi singkat (teknis)
- Block:
  - `app/blockchain/block.py` — Block memiliki fields: `index`, `transactions`, `timestamp`, `previous_hash`, `nonce`, `hash`.
  - `calculate_hash()` menggunakan SHA-256 dari JSON terurut dari field block.

- ProofOfWork:
  - `app/blockchain/consensus.py` — Loop increment `nonce` sampai `hash` memenuhi kondisi prefix `'0' * DIFFICULTY`.

- Blockchain core:
  - `app/blockchain/blockchain.py` — Mengelola chain, pending transactions, mining, broadcast, pendaftaran node, dan konsensus via `replace_chain()`.

- Networking:
  - `app/network/node.py` — Pengelolaan daftar nodes (peers), broadcasting blok/registrasi.
  - Node mencoba auto-register ke `BOOTSTRAP_NODES` dan menerima peer list dari bootstrap.

- Persistensi:
  - Saat ini, penyimpanan chain bersifat in-memory. Ada placeholder `save_chain_to_db()` untuk pengembangan persistensi.

---

## Troubleshooting singkat
- Jika node gagal terhubung ke bootstrap, periksa alamat/port di `BOOTSTRAP_NODES` dan pastikan node bootstrap berjalan.
- Jika mining terlalu lama, kurangi `DIFFICULTY` di `config.py` untuk pengujian.
- Pastikan port yang dipakai tidak diblokir oleh firewall.

---

## Area yang bisa ditingkatkan / ide kontribusi
- Validasi payload API dan signature transaksi untuk keamanan.
- Penyimpanan chain ke database (persistensi).
- Unit tests & CI untuk integrasi/end-to-end.
- Logging & error handling yang lebih baik pada komunikasi antar-node.
- UI interaktif untuk manajemen multi-node.
- Optimisasi mekanisme broadcast (mis. message queue).

---

## Panduan kontribusi singkat
1. Fork repo.
2. Buat branch fitur: `git checkout -b feature/your-feature`
3. Implementasi & tambahkan test bila relevan.
4. Commit & push: `git commit -m "Deskripsi perubahan"` lalu `git push origin feature/your-feature`
5. Buka Pull Request dengan deskripsi perubahan dan alasan.

Sertakan test dan dokumentasi untuk perubahan fungsional yang signifikan.

---

## Lisensi
Project dilisensikan di bawah MIT License. Lihat file `LICENSE` di root repository: [LICENSE](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/LICENSE).

---

Jika Anda mau, saya dapat:
- Menambahkan README.md ringkas yang merujuk ke dokumentasi ini.
- Menyediakan contoh skrip Python yang menggunakan `requests` untuk berinteraksi dengan API (contoh multi-node bootstrap + mining).
- Membuat checklist issue untuk perbaikan (tests, persistensi, security).
