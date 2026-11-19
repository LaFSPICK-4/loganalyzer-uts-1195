"""Modul ui: tampilan menu dan input pengguna (defensive programming)."""

MENU = """
=== LOGGUARD - Analisis Log Keamanan ===
1. Ringkasan rekap event
2. Filter berdasarkan severity
3. Cari log berdasarkan IP
4. Deteksi brute force
5. Daftar IP unik
6. Simpan hasil ke file (JSON dan CSV)
0. Keluar
"""


def tampilkan_menu():
    """Cetak menu utama. Tidak ada return."""
    print(MENU)


def minta_pilihan(batas_atas):
    """Minta angka menu dari pengguna sampai valid.

    Parameter: batas_atas (int) nomor menu terbesar.
    Return: int pilihan 0..batas_atas.
    """
    while True:
        teks = input("Pilih menu: ").strip()
        try:
            pilihan = int(teks)
        except ValueError:
            print("Input harus angka. Coba lagi.")
            continue
        if 0 <= pilihan <= batas_atas:
            return pilihan
        print(f"Pilihan harus 0 sampai {batas_atas}.")


def minta_teks(pesan):
    """Minta teks tidak kosong dari pengguna.

    Parameter: pesan (str) teks prompt.
    Return: str hasil input yang sudah di-strip.
    """
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("Input tidak boleh kosong.")


def cetak_log(daftar):
    """Cetak daftar log dalam bentuk baris rapi.

    Parameter: daftar (list of dict).
    """
    if not daftar:
        print("Data tidak ditemukan.")
        return
    for no, log in enumerate(daftar, start=1):
        print(f"{no:>2}. {log['timestamp']} | {log['ip']:<14} | {log['username']:<8} | "
              f"{log['event']:<14} | {log['severity']}")
