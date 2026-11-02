import numpy as np
import matplotlib.pyplot as plt
 
def trimf(x, a, b, c):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x >= a) & (x <= b)
        y[m] = (x[m] - a) / (b - a)
    if c > b:
        m = (x >= b) & (x <= c)
        y[m] = np.maximum(y[m], (c - x[m]) / (c - b))
    y[x == b] = 1
    return np.clip(y, 0, 1)
 
def trapmf(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x >= a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    else:
        y[x >= a] = 1
    m = (x >= b) & (x <= c)
    y[m] = 1
    if d > c:
        m = (x > c) & (x <= d)
        y[m] = (d - x[m]) / (d - c)
    return np.clip(y, 0, 1)
 
# Himpunan fuzzy input (satuan juta rupiah)
penghasilan = {
    "Rendah": lambda x: trapmf(x, 0, 0, 3, 6),
    "Sedang": lambda x: trimf(x, 3, 7.5, 12),
    "Tinggi": lambda x: trapmf(x, 9, 12, 15, 15)
}
pinjaman = {
    "Rendah": lambda x: trapmf(x, 0, 0, 5, 15),
    "Sedang": lambda x: trimf(x, 10, 25, 40),
    "Tinggi": lambda x: trapmf(x, 30, 40, 50, 50)
}
kelayakan = {
    "Tidak Layak": lambda z: trapmf(z, 0, 0, 20, 45),
    "Dipertimbangkan": lambda z: trimf(z, 25, 50, 75),
    "Layak": lambda z: trapmf(z, 55, 80, 100, 100)
}
 
aturan = [
    ("Rendah", "Rendah", "Dipertimbangkan"),
    ("Rendah", "Sedang", "Tidak Layak"),
    ("Rendah", "Tinggi", "Tidak Layak"),
    ("Sedang", "Rendah", "Layak"),
    ("Sedang", "Sedang", "Dipertimbangkan"),
    ("Sedang", "Tinggi", "Tidak Layak"),
    ("Tinggi", "Rendah", "Layak"),
    ("Tinggi", "Sedang", "Layak"),
    ("Tinggi", "Tinggi", "Dipertimbangkan")
]
 
z = np.linspace(0, 100, 1001)
 
def evaluasi_fuzzy(nilai_penghasilan, nilai_pinjaman):
    if not (0 <= nilai_penghasilan <= 15):
        raise ValueError("Penghasilan harus 0 sampai 15 juta rupiah.")
    if not (0 <= nilai_pinjaman <= 50):
        raise ValueError("Pinjaman harus 0 sampai 50 juta rupiah.")
 
    mu_penghasilan = {
        nama: float(fungsi(np.array([nilai_penghasilan]))[0])
        for nama, fungsi in penghasilan.items()
    }
    mu_pinjaman = {
        nama: float(fungsi(np.array([nilai_pinjaman]))[0])
        for nama, fungsi in pinjaman.items()
    }
 
    agregasi = np.zeros_like(z)
    for label_penghasilan, label_pinjaman, label_output in aturan:
        alpha = min(mu_penghasilan[label_penghasilan],
                    mu_pinjaman[label_pinjaman])
        output_terpotong = np.minimum(
            alpha, kelayakan[label_output](z)
        )
        agregasi = np.maximum(agregasi, output_terpotong)
 
    luas = np.trapz(agregasi, z)
    if luas == 0:
        return 0.0
    nilai_crisp = np.trapz(agregasi * z, z) / luas
    return float(nilai_crisp)
 
if __name__ == "__main__":
    print("SISTEM KELAYAKAN PINJAMAN KREDIT USAHA KECIL")
    p = float(input("Penghasilan usaha per bulan (juta Rp): "))
    q = float(input("Jumlah pinjaman (juta Rp): "))
    hasil = evaluasi_fuzzy(p, q)
    print(f"Skor kelayakan: {hasil:.2f}")
 
    if hasil < 40:
        keputusan = "Tidak Layak"
    elif hasil < 70:
        keputusan = "Dipertimbangkan"
    else:
        keputusan = "Layak"
    print("Kategori keputusan:", keputusan)
