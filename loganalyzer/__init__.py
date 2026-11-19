"""Package loganalyzer: analisis log keamanan sederhana (CLI)."""

EVENT_VALID = {"LOGIN_FAILED", "LOGIN_SUCCESS", "PORT_SCAN", "SQL_INJECTION", "FILE_ACCESS"}
SEVERITY_VALID = {"LOW", "MEDIUM", "HIGH"}
BATAS_BRUTE_FORCE = 3
