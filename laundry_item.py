class LaundryItem:
    def __init__(self, id_pelanggan, nama, layanan, berat, total):
        # Data utama
        self.id_pelanggan = id_pelanggan
        self.nama = nama
        self.layanan = layanan
        self.berat = berat
        self.total = total

        # Akan diisi dari main.py setelah dibuat
        self.harga_per_kg = 0
        self.harga_awal = 0
        self.harga_akhir = total

    def __str__(self):
        return (f"ID {self.id_pelanggan} - {self.nama} | "
                f"{self.layanan} | {self.berat} kg | Total Rp{self.harga_akhir:,.0f}")
