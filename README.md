# LOGGUARD - Analisis Log Keamanan (CLI)

UTS Pemrograman Dasar (TK091) - Universitas Amikom Yogyakarta, TA 2026/2027.

## Deskripsi
Aplikasi command line berbasis Python untuk menganalisis log keamanan server dari file CSV. Aplikasi mencari IP mencurigakan (brute force), memfilter log berdasarkan severity, merekap jenis kejadian, lalu menyimpan hasilnya ke JSON dan CSV.

Target pengguna: admin jaringan atau mahasiswa yang ingin cek log dengan cepat.

## Persyaratan
- Python 3.8 atau lebih baru
- Hanya standard library (csv, json, os, sys). Tidak perlu install apa pun.

## Cara menjalankan
```
cd logguard
python main.py
```
Pakai file lain:
```
python main.py data/log_rusak.csv
```

## Struktur folder
```
logguard/
  main.py                  program utama dan menu
  loganalyzer/             package buatan sendiri
    __init__.py            konstanta (event valid, batas brute force)
    loader.py              baca dan validasi CSV
    analyzer.py            filter, cari, kelompok, rekap, deteksi
    exporter.py            simpan ke JSON dan CSV
    ui.py                  menu dan input pengguna
  data/
    log_keamanan.csv       contoh input normal (20 baris)
    log_rusak.csv          input dengan 3 baris rusak
    log_kosong.csv         edge case: hanya header
  output/                  hasil: ringkasan.json, log_high.csv
  hasil_uji/               hasil output tiap skenario uji
```

## Format input (CSV)
Header wajib: `timestamp,ip,username,event,severity`

Nilai event: LOGIN_FAILED, LOGIN_SUCCESS, PORT_SCAN, SQL_INJECTION, FILE_ACCESS.
Nilai severity: LOW, MEDIUM, HIGH.

## Format output
- `output/ringkasan.json`: total log, rekap event, jumlah IP unik, IP brute force.
- `output/log_high.csv`: semua log dengan severity HIGH.

## Fitur utama
1. Rekap jumlah kejadian per jenis event.
2. Filter log berdasarkan severity dan cari log berdasarkan IP.
3. Deteksi brute force (IP dengan 3 kali atau lebih LOGIN_FAILED).
4. Daftar IP unik (set).
5. Simpan hasil ke JSON dan CSV.

## Alur dependensi antar modul
```
main.py
  -> loganalyzer.loader     (baca CSV, validasi)
  -> loganalyzer.analyzer   (olah data)
  -> loganalyzer.exporter   (tulis file)
  -> loganalyzer.ui         (menu dan input)
loader dan analyzer memakai konstanta dari loganalyzer/__init__.py
```

## Penanganan error
- File tidak ditemukan: pesan error, program berhenti dengan rapi.
- Header CSV salah: pesan error.
- Baris rusak (kolom kosong, event atau severity tidak valid): dilewati dan dilaporkan.
- Input menu bukan angka atau di luar rentang: diminta ulang.
- Data kosong: program tetap jalan, hasil kosong, tidak crash.
- Ctrl+C atau Ctrl+D: keluar dengan pesan sopan.

## Debugging
Skenario bug yang ditemukan dan diperbaiki: saat data kosong, menu simpan menulis ringkasan.json kosong tetapi log_high.csv gagal dengan ValueError, sehingga hasil tidak konsisten. Perbaikan: fungsi `simpan_hasil` di main.py sekarang mengecek data kosong lebih dulu, dan hanya membuat CSV jika ada log HIGH.

## Referensi dan bantuan AI
- Dokumentasi Python: modul csv dan json (docs.python.org).
- Bantuan AI: Claude (Anthropic) dipakai untuk membantu membuat kerangka kode, data contoh, dan draft dokumentasi. Kode sudah dijalankan dan diuji, dan saya memahami isinya.
