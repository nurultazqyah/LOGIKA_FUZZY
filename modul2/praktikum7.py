
import numpy as np
import matplotlib.pyplot as plt

# =====================================
# 1. FUNGSI KEANGGOTAAN
# =====================================

def trapmf(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)

    if a == b:
        y[x <= b] = 1
    else:
        idx = (x > a) & (x < b)
        y[idx] = (x[idx] - a) / (b - a)

    y[(x >= b) & (x <= c)] = 1

    if c == d:
        y[x >= c] = 1
    else:
        idx = (x > c) & (x < d)
        y[idx] = (d - x[idx]) / (d - c)

    return np.clip(y, 0, 1)


def trimf(x, a, b, c):
    return trapmf(x, a, b, b, c)


# =====================================
# 2. KELAS FUZZY INFERENCE SYSTEM
# =====================================

class FuzzyInferenceSystem:

    def __init__(self):
        self.inputs = {}
        self.output = None
        self.rules = []
        self.last_rules = []
        self.last_aggregation = None

    # Menambahkan variabel input
    def add_input_variable(self, name, universe, mf_dict):
        self.inputs[name] = {
            "universe": universe,
            "mf": mf_dict
        }

    # Menambahkan variabel output
    def set_output_variable(self, name, universe, mf_dict):
        self.output = {
            "name": name,
            "universe": universe,
            "mf": mf_dict
        }

    # Menambahkan aturan fuzzy
    def add_rule(self, rule_tuple):
        self.rules.append(rule_tuple)

    # Menghitung hasil fuzzy
    def compute(self, input_values_dict):

        # A. FUZZIFIKASI
        fuzzifikasi = {}

        for name, value in input_values_dict.items():

            data = self.inputs[name]
            fuzzifikasi[name] = {}

            for label, mf in data["mf"].items():

                fuzzifikasi[name][label] = np.interp(
                    value,
                    data["universe"],
                    mf
                )

        # B. EVALUASI DAN AGREGASI
        u = self.output["universe"]
        agregasi = np.zeros_like(u)
        aturan_aktif = []

        for i, rule in enumerate(self.rules, start=1):

            var1, mf1, var2, mf2, hasil = rule

            nilai1 = fuzzifikasi[var1][mf1]
            nilai2 = fuzzifikasi[var2][mf2]

            # Firing strength menggunakan MIN
            alpha = min(nilai1, nilai2)

            if alpha > 0:

                aturan_aktif.append(
                    (i, mf1, mf2, hasil, alpha)
                )

                # Implikasi Clipping MIN
                kurva = np.minimum(
                    alpha,
                    self.output["mf"][hasil]
                )

                # Agregasi MAX
                agregasi = np.maximum(
                    agregasi, kurva
                )

        # C. DEFUZZIFIKASI CENTROID
        pembilang = np.sum(u * agregasi)
        penyebut = np.sum(agregasi)

        if penyebut == 0:
            crisp_output = 0
        else:
            crisp_output = pembilang / penyebut

        self.last_rules = aturan_aktif
        self.last_aggregation = agregasi

        # Mengembalikan nilai crisp output
        return crisp_output


# =====================================
# 3. MEMBUAT VARIABEL INPUT
# =====================================

fis = FuzzyInferenceSystem()

# Pendapatan usaha (juta rupiah)
u_pendapatan = np.linspace(0, 50, 501)

fis.add_input_variable(
    "Pendapatan",
    u_pendapatan,
    {
        "Rendah": trapmf(
            u_pendapatan, 0, 0, 5, 15
        ),
        "Sedang": trapmf(
            u_pendapatan, 5, 15, 25, 35
        ),
        "Tinggi": trapmf(
            u_pendapatan, 25, 35, 50, 50
        )
    }
)

# Beban pinjaman (persen)
u_beban = np.linspace(0, 100, 501)

fis.add_input_variable(
    "Beban",
    u_beban,
    {
        "Ringan": trapmf(
            u_beban, 0, 0, 20, 40
        ),
        "Sedang": trapmf(
            u_beban, 20, 40, 60, 80
        ),
        "Berat": trapmf(
            u_beban, 60, 80, 100, 100
        )
    }
)


# =====================================
# 4. MEMBUAT VARIABEL OUTPUT
# =====================================

u_kelayakan = np.linspace(0, 100, 1001)

fis.set_output_variable(
    "Kelayakan",
    u_kelayakan,
    {
        "Tidak Layak": trapmf(
            u_kelayakan, 0, 0, 25, 50
        ),
        "Dipertimbangkan": trimf(
            u_kelayakan, 25, 50, 75
        ),
        "Layak": trapmf(
            u_kelayakan, 50, 75, 100, 100
        )
    }
)


# =====================================
# 5. MEMBUAT 9 ATURAN FUZZY
# =====================================

aturan = [

    ("Pendapatan", "Rendah",
     "Beban", "Ringan", "Dipertimbangkan"),

    ("Pendapatan", "Rendah",
     "Beban", "Sedang", "Tidak Layak"),

    ("Pendapatan", "Rendah",
     "Beban", "Berat", "Tidak Layak"),

    ("Pendapatan", "Sedang",
     "Beban", "Ringan", "Layak"),

    ("Pendapatan", "Sedang",
     "Beban", "Sedang", "Dipertimbangkan"),

    ("Pendapatan", "Sedang",
     "Beban", "Berat", "Tidak Layak"),

    ("Pendapatan", "Tinggi",
     "Beban", "Ringan", "Layak"),

    ("Pendapatan", "Tinggi",
     "Beban", "Sedang", "Layak"),

    ("Pendapatan", "Tinggi",
     "Beban", "Berat", "Dipertimbangkan")
]

for rule in aturan:
    fis.add_rule(rule)


# =====================================
# 6. PENGUJIAN 3 KASUS
# =====================================

kasus = [
    ("Kasus 1", 3, 70),
    ("Kasus 2", 12, 35),
    ("Kasus 3", 24, 15)
]

print("SISTEM PENDUKUNG KEPUTUSAN")
print("KELAYAKAN PINJAMAN KREDIT USAHA")

hasil_semua = []

for nama, pendapatan, beban in kasus:

    print("\n================================")
    print(nama)
    print("Pendapatan:", pendapatan, "juta")
    print("Beban Pinjaman:", beban, "%")

    input_data = {
        "Pendapatan": pendapatan,
        "Beban": beban
    }

    # Memanggil fungsi compute
    hasil = fis.compute(input_data)

    # Menampilkan aturan aktif
    print("\nATURAN YANG AKTIF:")

    for no, p, b, output, alpha in fis.last_rules:

        print(
            f"R{no}: {p} AND {b} "
            f"THEN {output}"
        )

        print(
            f"Firing Strength = {alpha:.2f}"
        )

    # Menampilkan nilai output
    print("\nHASIL DEFUZZIFIKASI:")
    print(f"Nilai Kelayakan = {hasil:.2f}")

    if hasil < 40:
        keputusan = "TIDAK LAYAK"
    elif hasil <= 60:
        keputusan = "DIPERTIMBANGKAN"
    else:
        keputusan = "LAYAK"

    print("Keputusan:", keputusan)

    hasil_semua.append(
        (nama, pendapatan, beban, hasil, keputusan)
    )

    # Menampilkan grafik
    plt.figure(figsize=(8, 4))

    plt.plot(
        u_kelayakan,
        fis.last_aggregation,
        label="Hasil Agregasi"
    )

    plt.axvline(
        hasil,
        linestyle="--",
        label=f"Centroid = {hasil:.2f}"
    )

    plt.title("Grafik " + nama)
    plt.xlabel("Nilai Kelayakan Pinjaman")
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.savefig(
        nama.replace(" ", "_") + ".png",
        dpi=300
    )

    plt.show()


# =====================================
# 7. RINGKASAN HASIL
# =====================================

print("\n================================")
print("RINGKASAN HASIL PENGUJIAN")

for nama, p, b, hasil, keputusan in hasil_semua:

    print(
        f"{nama}: Pendapatan={p} juta, "
        f"Beban={b}%, Output={hasil:.2f}, "
        f"Keputusan={keputusan}"
    )   
