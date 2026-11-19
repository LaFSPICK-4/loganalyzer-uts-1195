"""Modul analyzer: pencarian, filtering, pengelompokan, rekap, dan deduplikasi."""

from loganalyzer import BATAS_BRUTE_FORCE


def filter_berdasarkan_severity(data, severity):
    """Ambil log dengan severity tertentu.

    Parameter: data (list of dict), severity (str).
    Return: list of dict.
    """
    return [log for log in data if log["severity"] == severity.upper()]


def cari_berdasarkan_ip(data, ip):
    """Cari semua log dari satu alamat IP.

    Parameter: data (list of dict), ip (str).
    Return: list of dict (bisa kosong).
    """
    return [log for log in data if log["ip"] == ip]


def rekap_per_event(data):
    """Hitung jumlah kejadian per jenis event.

    Parameter: data (list of dict).
    Return: dict {event: jumlah}.
    """
    rekap = {}
    for log in data:
        rekap[log["event"]] = rekap.get(log["event"], 0) + 1
    return rekap


def kelompokkan_per_ip(data):
    """Kelompokkan log berdasarkan IP.

    Parameter: data (list of dict).
    Return: dict {ip: list of log}.
    """
    kelompok = {}
    for log in data:
        kelompok.setdefault(log["ip"], []).append(log)
    return kelompok


def ip_unik(data):
    """Ambil daftar IP tanpa duplikat (pakai set).

    Parameter: data (list of dict).
    Return: list IP terurut.
    """
    return sorted({log["ip"] for log in data})


def deteksi_brute_force(data, batas=BATAS_BRUTE_FORCE):
    """Deteksi IP dengan LOGIN_FAILED sebanyak batas atau lebih.

    Parameter: data (list of dict), batas (int) minimal gagal login.
    Return: dict {ip: jumlah_gagal} diurutkan dari terbanyak.
    Edge case: data kosong -> dict kosong.
    """
    gagal = {}
    for log in data:
        if log["event"] == "LOGIN_FAILED":
            gagal[log["ip"]] = gagal.get(log["ip"], 0) + 1
    mencurigakan = {ip: n for ip, n in gagal.items() if n >= batas}
    return dict(sorted(mencurigakan.items(), key=lambda item: item[1], reverse=True))


def ringkasan(data):
    """Buat ringkasan keseluruhan untuk disimpan ke JSON.

    Parameter: data (list of dict).
    Return: dict berisi total, rekap event, IP unik, dan IP brute force.
    """
    return {
        "total_log": len(data),
        "rekap_event": rekap_per_event(data),
        "jumlah_ip_unik": len(ip_unik(data)),
        "ip_brute_force": deteksi_brute_force(data),
        "log_severity_high": len(filter_berdasarkan_severity(data, "HIGH")),
    }
