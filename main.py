"""LOGGUARD - program utama (command line).

Cara jalan:
    python main.py                      (pakai data/log_keamanan.csv)
    python main.py data/log_rusak.csv   (pakai file lain)
"""

import sys

from loganalyzer import analyzer, exporter, loader, ui

FILE_DEFAULT = "data/log_keamanan.csv"


def muat_data(path):
    """Baca file log dan tampilkan peringatan jika ada baris rusak.

    Parameter: path (str).
    Return: list of dict, atau None jika gagal dibaca.
    """
    try:
        data, error = loader.baca_log_csv(path)
    except FileNotFoundError:
        print(f"Error: file '{path}' tidak ditemukan.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except PermissionError:
        print(f"Error: tidak punya izin membaca '{path}'.")
        return None
    for pesan in error:
        print("Peringatan:", pesan)
    print(f"Berhasil memuat {len(data)} baris log dari '{path}'.")
    return data


def tampilkan_rekap(data):
    """Cetak rekap jumlah per event."""
    rekap = analyzer.rekap_per_event(data)
    print("\nRekap event:")
    for event, jumlah in rekap.items():
        print(f"  {event:<14}: {jumlah}")


def tampilkan_brute_force(data):
    """Cetak IP yang terdeteksi brute force."""
    hasil = analyzer.deteksi_brute_force(data)
    if not hasil:
        print("Tidak ada IP yang terdeteksi brute force.")
        return
    print("\nIP terdeteksi brute force:")
    for ip, jumlah in hasil.items():
        print(f"  {ip:<15}: {jumlah} kali gagal login")


def simpan_hasil(data):
    """Simpan ringkasan (JSON) dan log HIGH (CSV) ke folder output."""
    if not data:
        print("Tidak ada data untuk disimpan.")
        return
    log_high = analyzer.filter_berdasarkan_severity(data, "HIGH")
    try:
        exporter.simpan_json(analyzer.ringkasan(data), "output/ringkasan.json")
        print("Tersimpan: output/ringkasan.json")
        if log_high:
            exporter.simpan_csv(log_high, "output/log_high.csv")
            print("Tersimpan: output/log_high.csv")
        else:
            print("Tidak ada log HIGH, log_high.csv tidak dibuat.")
    except OSError as e:
        print("Error menulis file:", e)


def jalankan_menu(data):
    """Loop menu utama sampai pengguna memilih keluar."""
    while True:
        ui.tampilkan_menu()
        pilihan = ui.minta_pilihan(6)
        if pilihan == 0:
            print("Sampai jumpa.")
            break
        elif pilihan == 1:
            tampilkan_rekap(data)
        elif pilihan == 2:
            sev = ui.minta_teks("Severity (LOW/MEDIUM/HIGH): ").upper()
            if sev not in {"LOW", "MEDIUM", "HIGH"}:
                print("Severity tidak valid.")
            else:
                ui.cetak_log(analyzer.filter_berdasarkan_severity(data, sev))
        elif pilihan == 3:
            ip = ui.minta_teks("Masukkan IP: ")
            ui.cetak_log(analyzer.cari_berdasarkan_ip(data, ip))
        elif pilihan == 4:
            tampilkan_brute_force(data)
        elif pilihan == 5:
            print("IP unik:", ", ".join(analyzer.ip_unik(data)) or "-")
        elif pilihan == 6:
            simpan_hasil(data)


def main():
    """Titik masuk program."""
    path = sys.argv[1] if len(sys.argv) > 1 else FILE_DEFAULT
    data = muat_data(path)
    if data is None:
        sys.exit(1)
    if not data:
        print("Peringatan: tidak ada data valid, hasil analisis akan kosong.")
    try:
        jalankan_menu(data)
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")


if __name__ == "__main__":
    main()
