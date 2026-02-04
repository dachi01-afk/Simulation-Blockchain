# Dokumentasi: Simulation-Blockchain

Dokumentasi ini menjelaskan arsitektur, API, cara menjalankan, dan panduan kontribusi untuk project Simulation-Blockchain — sebuah simulasi jaringan blockchain terdistribusi sederhana yang dibangun dengan Python & Flask.

## Ringkasan
Projek ini mensimulasikan jaringan blockchain terdistribusi dengan fitur utama: pembuatan blok (Block), Proof-of-Work sederhana, antrian transaksi, dan sinkronisasi node (replace chain) melalui bootstrap nodes. UI web sederhana tersedia di folder `templates`/`static` untuk visualisasi.

- Repository: `dachi01-afk/Simulation-Blockchain`
- Deskripsi: Simple distributed blockchain network using Python & Flask
- Bahasa utama: Python (inti aplikasi), JavaScript/HTML/CSS di frontend

## Struktur proyek (file & direktori penting)
- `run.py` — Entrypoint aplikasi. Menjalankan Flask app; menerima argumen port (contoh: `python run.py 5001`).
- `config.py` — Konfigurasi global (mis. `DIFFICULTY`, `BOOTSTRAP_NODES`). Lihat [config.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/config.py).
- `requirements.txt` — Daftar dependensi.
- `app/` — Kode aplikasi utama:
  - `app/routes.py` — Semua route API dan halaman web (lihat: [app/routes.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/app/routes.py)).
  - `app/blockchain/`:
    - `blockchain.py` — Logika blockchain: chain, pending_transactions, mining, jaringan dan konsensus (replace_chain).
    - `block.py` — Model Block dan `calculate_hash()` (SHA-256).
    - `consensus.py` — ProofOfWork sederhana.
    - `utils.py` — Fungsi utilitas (`serialize_block`).
  - `app/network/` — Implementasi node/peer (mis. `node.py`).
- `templates/` dan `static/` — Front-end sederhana untuk dashboard, melihat chain, transaksi, dan nodes.

## Konfigurasi penting
- DIFFICULTY: tingkat kesulitan PoW (didefinisikan di `config.py`). Semakin besar nilai, semakin lama menambang.
- BOOTSTRAP_NODES: daftar alamat node bootstrap yang digunakan untuk auto-register dan menemukan peer.

Periksa `config.py` untuk nilai default: [config.py](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/config.py)

## Cara instal & jalankan
1. Clone repository:
```bash
git clone https://github.com/dachi01-afk/Simulation-Blockchain.git
cd Simulation-Blockchain
```
2. (Opsional) Buat virtual environment dan aktifkan:
```bash
ewline 
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
Setiap node akan mencoba mendaftar ke `BOOTSTRAP_NODES` yang didefinisikan di `config.py` dan sinkronisasi chain secara otomatis.

## API (endpoints)
Berikut endpoint yang tersedia (lihat implementasi di `app/routes.py`):

- GET /api/chain
  - Deskripsi: Mengambil seluruh chain.
  - Response: JSON array berisi blok (index, transactions, timestamp, previous_hash, nonce, hash).
  - Contoh: `curl "http://localhost:5000/api/chain"`

- POST /api/transactions
  - Deskripsi: Menambahkan transaksi ke antrian pending.
  - Body: JSON transaksi (contoh: `{"sender":"Alice", "recipient":"Bob", "amount":10}`)
  - Contoh: 
```bash
curl -X POST "http://localhost:5000/api/transactions" 
  -H "Content-Type: application/json" 
  -d '{"sender":"Alice","recipient":"Bob","amount":10}'
```

- GET /api/mine
  - Deskripsi: Memicu proses mining untuk membuat blok baru dari pending transactions.
  - Response: data blok yang baru ditambang atau pesan kesalahan jika tidak ada transaksi.
  - Contoh: `curl -X GET "http://localhost:5000/api/mine"`

- GET /api/validate
  - Deskripsi: Mengecek apakah chain lokal valid menurut aturan is_chain_valid().
  - Contoh: `curl "http://localhost:5000/api/validate"`

- POST /api/register-node
  - Deskripsi: Mendaftarkan node baru ke node ini. Node baru akan menerima daftar peers.
  - Body: `{ "address": "http://localhost:5001" }`
  - Contoh: 
```bash
curl -X POST "http://localhost:5000/api/register-node" 
  -H "Content-Type: application/json" 
  -d '{"address":"http://localhost:5001"}'
```

- POST /api/receive-block
  - Deskripsi: Endpoint untuk menerima blok baru yang dibroadcast oleh peer. Server akan memeriksa `previous_hash` dan mengganti chain jika perlu.
  - Body: objek blok yang diserialisasi. Implementasi ada di `app/routes.py`.

## Halaman web (pages)
- GET / — Dashboard (templates/dashboard.html)
- GET /chain-page — Tampilan chain
- GET /transaction-page — Tambah transaksi
- GET /mine-page — Halaman mining
- GET /nodes — Kelola nodes

## Contoh alur menjalankan beberapa node (praktis)
1. Terminal A: `python run.py 5000`
2. Terminal B: `python run.py 5001`
3. Di node A, daftarkan node B:
```bash
curl -X POST "http://localhost:5000/api/register-node" -H "Content-Type: application/json" -d '{"address":"http://localhost:5001"}'
```
4. Tambahkan transaksi di node B dan mine, kemudian cek node A untuk sinkronisasi otomatis via `replace_chain()` dan broadcast blok.

## Desain & implementasi singkat
- Block model (`app/blockchain/block.py`) menggunakan SHA-256 terhadap JSON terurut dari field block.
- ProofOfWork (`app/blockchain/consensus.py`) melakukan increment nonce sampai hash memenuhi prefix '0' * DIFFICULTY.
- Blockchain (`app/blockchain/blockchain.py`) mengelola chain, pending transactions, mining, broadcast blok, pendaftaran node, dan replace_chain() untuk konsensus chain terpanjang.
- Node networking: node mendaftarkan dirinya ke bootstrap nodes (lihat `Config.BOOTSTRAP_NODES`) dan saling membroadcast node/blocks (lihat `app/network/node.py`).

## Hal yang bisa ditingkatkan / kontribusi
- Menambahkan validasi struktur transaksi dan autentikasi (signature).
- Menyimpan chain ke database untuk persistensi (fungsi `save_chain_to_db()` placeholder).
- Menambahkan test otomatis dan CI.
- Memperbaiki error handling & logging, retry pada jaringan, dan keamanan.

## Lisensi
Project ini dilisensikan di bawah MIT License. Lihat file [LICENSE](https://github.com/dachi01-afk/Simulation-Blockchain/blob/main/LICENSE).