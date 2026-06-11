# Finance BI

Aplikasi analisis keuangan sederhana menggunakan Flask dan Docker.

## Fitur
- Dashboard
- Wallet
- Analisis Pengeluaran
- Laporan Keuangan
- Export PDF
- Dark Mode & Light Mode

## Menjalankan Aplikasi

### Python

pip install -r requirements.txt
python app.py

### Docker

docker build -t analisis-python .

docker run -d -p 5000:5000 analisis-python

Akses:
http://localhost:5000
