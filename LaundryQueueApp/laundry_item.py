class LaundryItem:
    def __init__(self, id_pelanggan, nama, layanan, berat, total):
        self.id_pelanggan = id_pelanggan
        self.nama = nama
        self.layanan = layanan
        self.berat = berat
        self.total = total

    def __str__(self):
        return f"{self.id_pelanggan} - {self.nama} - {self.layanan} - {self.berat}kg - Rp{self.total}"
