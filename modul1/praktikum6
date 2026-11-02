import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_logika_fuzzy_tugas2"

)
# ==========================================================
# 2. FUNGSI KEANGGOTAAN
# ==========================================================
def fungsi_remaja_naik(x):
    """
    Fungsi keanggotaan remaja bagian naik.
    Domain: 10 <= x <= 13
    Persamaan: μ(x) = (x - 10) / 3
    """
    return (x - 10) / 3

def fungsi_remaja_turun(x):
    """
    Fungsi keanggotaan remaja bagian turun.
    Domain: 16 < x <= 19
    Persamaan: μ(x) = (19 - x) / 3
    """
    return (19 - x) / 3

# ==========================================================
# 3. DAFTAR FUNGSI (DICTIONARY)
# ==========================================================
fungsi = {
    "Di luar interval": lambda x: 0,
    "mu(x) = (x - 10) / 3": fungsi_remaja_naik,
    "mu(x) = 1": lambda x: 1,
    "mu(x) = (19 - x) / 3": fungsi_remaja_turun
}

# ==========================================================
# 4. FUNGSI FUZZIFIKASI
# ==========================================================
def fuzzifikasi_usia(x):
    cursor = db.cursor()

    query = """
        SELECT DISTINCT kondisi_x, rumus_perhitungan
        FROM domain_remaja
    """

    cursor.execute(query)
    aturan_database = cursor.fetchall()
    cursor.close()

    if x < 10 or x > 19:
        kondisi = "x < 10 atau x > 19"
        penemuan = "0 – 10 → 0" if x < 10 else "x > 19 → 0"
    elif x <= 13:
        kondisi = "10 <= x <= 13"
        penemuan = "10 – 13 → μ(x) = (x - 10) / 3"
    elif x <= 16:
        kondisi = "13 < x <= 16"
        penemuan = "13 – 16 → μ(x) = 1"
    else:
        kondisi = "16 < x <= 19"
        penemuan = "16 – 19 → μ(x) = (19 - x) / 3"

    aturan = dict(aturan_database)
    nama_fungsi = aturan.get(kondisi)

if nama_fungsi is None:        raise ValueError(f"Aturan '{kondisi}' tidak ditemukan di tabel domain_remaja.")

    if nama_fungsi in fungsi:
        fungsi_y = fungsi[nama_fungsi]
        return fungsi_y(x), penemuan

    raise ValueError(f"Rumus '{nama_fungsi}' belum didukung di
Python.")

# ==========================================================
# 5. EXECUTION MAIN PROGRAM
# ==========================================================
try:
    # Input Usia
    usia = float(input("Masukan:\n"))

    # Proses Fuzzifikasi
    nilai_keanggotaan, penemuan = fuzzifikasi_usia(usia)

    # Menampilkan Hasil
    print(f"\nPenemuan basis data:\n{penemuan}")
    print(f"\nHasil:\nμ({usia:g}) = {nilai_keanggotaan:g}")

finally:
    # Menutup Koneksi Database
    db.close()
