import matplotlib.pyplot as plt
# =========================================
# 1. FUNGSI KEANGGOTAAN TRAPESIUM
# =========================================
def trapmf(x, a, b, c, d):
    if a == b:
        kiri = 1 if x >= b else 0
    else:
        kiri = max(0, min(1, (x-a)/(b-a)))
    if c == d:
        kanan = 1 if x <= c else 0
    else:
        kanan = max(0, min(1, (d-x)/(d-c)))
    return max(0, min(kiri, kanan))

# =========================================
# 2. FUZZIFIKASI INPUT
# =========================================
def fuzzifikasi(pendapatan, beban):
    # Pendapatan usaha (juta rupiah)
    rendah = trapmf(
        pendapatan, 0, 0, 10, 30
    )
    tinggi = trapmf(
        pendapatan, 20, 40, 50, 50
    )
    # Beban pinjaman (persen)
    ringan = trapmf(
        beban, 0, 0, 20, 60
    )
    berat = trapmf(
        beban, 40, 80, 100, 100
    )
    return rendah, tinggi, ringan, berat

# =========================================
# 3. EMPAT ATURAN INFERENSI
# =========================================
def evaluasi_aturan(pendapatan, beban):
    rendah, tinggi, ringan, berat = fuzzifikasi(
        pendapatan, beban
    )
    # Operator AND menggunakan MIN
    alpha1 = min(rendah, ringan)
    alpha2 = min(rendah, berat)
    alpha3 = min(tinggi, ringan)
    alpha4 = min(tinggi, berat)
    return [alpha1, alpha2, alpha3, alpha4]

# =========================================
# 4. METODE SUGENO ORDE 0
# =========================================
def sugeno(alpha):
    # Konstanta output setiap aturan
    z = [50, 20, 85, 50]
    pembilang = sum(
        a * nilai for a, nilai in zip(alpha, z)
    )
    penyebut = sum(alpha)
    if penyebut == 0:
        return 0
    return pembilang / penyebut

# =========================================
# 5. METODE TSUKAMOTO
# =========================================
def tsukamoto(alpha):
    a1, a2, a3, a4 = alpha
    # Nilai crisp setiap aturan
    z1 = 30 + 40 * a1       # Dipertimbangkan
    z2 = 40 * (1 - a2)      # Tidak Layak
    z3 = 60 + 40 * a3       # Layak
    z4 = 30 + 40 * a4       # Dipertimbangkan
    z = [z1, z2, z3, z4]
    pembilang = sum(
        a * nilai for a, nilai in zip(alpha, z)
    )
    penyebut = sum(alpha)
    if penyebut == 0:
        return 0
    return pembilang / penyebut

# =========================================
# 6. MENENTUKAN KEPUTUSAN
# =========================================
def keputusan(nilai):
    if nilai < 40:
        return "Tidak Layak"
    elif nilai < 70:
        return "Dipertimbangkan"
    else:
        return "Layak"

# =========================================
# 7. LIMA VARIASI PENGUJIAN
# =========================================
data_uji = [
    ("Kasus 1", 8, 85),
    ("Kasus 2", 15, 50),
    ("Kasus 3", 25, 35),
    ("Kasus 4", 35, 20),
    ("Kasus 5", 45, 75)
]
hasil_sugeno = []
hasil_tsukamoto = []
print("SISTEM PENDUKUNG KEPUTUSAN")
print("KELAYAKAN PINJAMAN KREDIT USAHA KECIL")
print("=" * 65)
for nama, pendapatan, beban in data_uji:
    alpha = evaluasi_aturan(
        pendapatan, beban
    )
    nilai_sugeno = sugeno(alpha)
    nilai_tsukamoto = tsukamoto(alpha)
    hasil_sugeno.append(nilai_sugeno)
    hasil_tsukamoto.append(nilai_tsukamoto)
    print("\n", nama)
    print("Pendapatan usaha :", pendapatan, "juta")
    print("Beban pinjaman   :", beban, "%")
    print("\nFIRING STRENGTH:")
    for i, a in enumerate(alpha, start=1):
        print(f"R{i} = {a:.2f}")
    print("\nHASIL SUGENO:")
    print(f"Nilai = {nilai_sugeno:.2f}")
    print("Keputusan =", keputusan(nilai_sugeno))
    print("\nHASIL TSUKAMOTO:")
    print(f"Nilai = {nilai_tsukamoto:.2f}")
    print("Keputusan =", keputusan(nilai_tsukamoto))

# =========================================
# 8. TABEL PERBANDINGAN
# =========================================
print("\n\nTABEL PERBANDINGAN HASIL")
print("=" * 85)
print(
    f"{'Kasus':10s} {'Sugeno':12s} "
    f"{'Tsukamoto':12s} {'Selisih':12s}"
)
for i in range(len(data_uji)):
    selisih = abs(
        hasil_sugeno[i] - hasil_tsukamoto[i]
    )
    print(
        f"{data_uji[i][0]:10s} "
        f"{hasil_sugeno[i]:10.2f} "
        f"{hasil_tsukamoto[i]:12.2f} "
        f"{selisih:10.2f}"
    )

# =========================================
# 9. GRAFIK PERBANDINGAN
# =========================================
nama_kasus = [d[0] for d in data_uji]
posisi = range(len(nama_kasus))
lebar = 0.35
plt.figure(figsize=(10, 5))
plt.bar(
    [p - lebar/2 for p in posisi],
    hasil_sugeno,
    lebar,
    label="Sugeno Orde 0"
)
plt.bar(
    [p + lebar/2 for p in posisi],
    hasil_tsukamoto,
    lebar,
    label="Tsukamoto"
)
plt.xticks(list(posisi), nama_kasus)
plt.xlabel("Variasi Pengujian")
plt.ylabel("Nilai Kelayakan Pinjaman")
plt.title("Perbandingan Sugeno dan Tsukamoto")
plt.ylim(0, 100)
plt.legend()
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(
    "grafik_perbandingan_sugeno_tsukamoto.png",
    dpi=300
)
plt.show()
