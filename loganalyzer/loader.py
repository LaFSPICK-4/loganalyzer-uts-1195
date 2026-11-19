"""Modul loader: membaca dan memvalidasi data log dari file CSV."""

import csv

from loganalyzer import EVENT_VALID, SEVERITY_VALID

KOLOM_WAJIB = ["timestamp", "ip", "username", "event", "severity"]


def validasi_baris(baris):
    """Cek satu baris log.

    Parameter: baris (dict) hasil csv.DictReader.
    Return: tuple (valid, pesan). pesan berisi alasan jika tidak valid.
    """
    for kolom in KOLOM_WAJIB:
        nilai = baris.get(kolom)
        if nilai is None or nilai.strip() == "":
            return False, f"kolom '{kolom}' kosong"
    if baris["event"].strip().upper() not in EVENT_VALID:
        return False, f"event '{baris['event']}' tidak dikenal"
    if baris["severity"].strip().upper() not in SEVERITY_VALID:
        return False, f"severity '{baris['severity']}' tidak valid"
    return True, ""


def baca_log_csv(path):
    """Baca file CSV log keamanan.

    Parameter: path (str) lokasi file CSV.
    Return: tuple (data, error) -> data list of dict yang valid,
            error list of str berisi baris yang dilewati.
    Raise: FileNotFoundError, ValueError (header salah).
    """
    data = []
    error = []
    with open(path, newline="", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        if pembaca.fieldnames is None or set(KOLOM_WAJIB) - set(pembaca.fieldnames):
            raise ValueError("Header CSV tidak sesuai. Harus: " + ",".join(KOLOM_WAJIB))
        for nomor, baris in enumerate(pembaca, start=2):
            valid, pesan = validasi_baris(baris)
            if valid:
                data.append({
                    "timestamp": baris["timestamp"].strip(),
                    "ip": baris["ip"].strip(),
                    "username": baris["username"].strip(),
                    "event": baris["event"].strip().upper(),
                    "severity": baris["severity"].strip().upper(),
                })
            else:
                error.append(f"Baris {nomor} dilewati: {pesan}")
    return data, error
