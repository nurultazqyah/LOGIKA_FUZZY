# SISTEM PENDUKUNG KEPUTUSAN
# KELAYAKAN PINJAMAN KREDIT USAHA
# Metode Logika Fuzzy
# 1. Derajat keanggotaan input pendapatan usaha
pendapatan = {
    "Rendah": 0.2,
    "Sedang": 0.8,
    "Tinggi": 0.0
}
# 2. Derajat keanggotaan input beban pinjaman
beban = {
    "Ringan": 0.0,
    "Sedang": 0.5,
    "Berat": 0.5
}
# 3. Basis aturan fuzzy (9 aturan)
aturan = [
    ("Rendah", "Ringan", "Dipertimbangkan"),
    ("Rendah", "Sedang", "Tidak Layak"),
    ("Rendah", "Berat", "Tidak Layak"),

    ("Sedang", "Ringan", "Layak"),
    ("Sedang", "Sedang", "Dipertimbangkan"),
    ("Sedang", "Berat", "Tidak Layak"),

    ("Tinggi", "Ringan", "Layak"),
    ("Tinggi", "Sedang", "Layak"),
    ("Tinggi", "Berat", "Dipertimbangkan")
]
# 4. Evaluasi aturan fuzzy
print("SISTEM PENDUKUNG KEPUTUSAN KELAYAKAN PINJAMAN")
print("=" * 55)
hasil_aturan = []
agregasi = {
    "Tidak Layak": 0,
    "Dipertimbangkan": 0,
    "Layak": 0
}
for i, (p, b, output) in enumerate(aturan, start=1):
    # Menghitung firing strength menggunakan MIN
    alpha = min(pendapatan[p], beban[b])
    if alpha > 0:
        hasil_aturan.append((i, p, b, output, alpha))
        # Agregasi menggunakan MAX
        agregasi[output] = max(agregasi[output], alpha)
# 5. Menampilkan aturan yang aktif
print("\nDAFTAR ATURAN YANG AKTIF")
for no, p, b, output, alpha in hasil_aturan:
    print(f"Aturan {no}: Pendapatan {p} AND Beban {b}")
    print(f"          THEN {output}")
    print(f"          Firing Strength = {alpha:.2f}\n")
# 6. Menampilkan hasil agregasi
print("=" * 55)
print("HASIL AGREGASI")
for kategori, nilai in agregasi.items():
    print(f"{kategori}: {nilai:.2f}")
# 7. Menentukan hasil keputusan berdasarkan nilai terbesar
hasil = max(agregasi, key=agregasi.get)
print("\nHASIL KEPUTUSAN:")
print("Kelayakan Pinjaman:", hasil)
