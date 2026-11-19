"""Modul exporter: menyimpan hasil analisis ke file JSON dan CSV."""

import csv
import json
import os


def simpan_json(data, path):
    """Simpan dict/list ke file JSON.

    Parameter: data (dict atau list), path (str).
    Return: path file yang ditulis.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


def simpan_csv(data, path):
    """Simpan list of dict ke file CSV.

    Parameter: data (list of dict), path (str).
    Return: path file yang ditulis.
    Raise: ValueError jika data kosong (tidak ada header yang bisa dibuat).
    """
    if not data:
        raise ValueError("Tidak ada data untuk disimpan ke CSV.")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        penulis = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        penulis.writeheader()
        penulis.writerows(data)
    return path
