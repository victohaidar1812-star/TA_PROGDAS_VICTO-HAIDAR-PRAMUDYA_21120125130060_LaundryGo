import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from laundry_item import LaundryItem
from queue_laundry import QueueLaundry


class LaundryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LaundryGo")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # ==== LOAD BACKGROUND ====
        bg = Image.open("assets/background.jpg")
        bg = bg.resize((900, 650))
        self.bg_img = ImageTk.PhotoImage(bg)

        self.bg_label = tk.Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0)

        # Queue
        self.queue = QueueLaundry()
        self.counter = 1

        # ===== TITLE =====
        self.title_label = tk.Label(
            self.root,
            text="LAUNDRYGO - QUEUE SYSTEM",
            font=("Segoe UI", 22, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        self.title_label.place(x=240, y=20)

        # ===== INPUT FORM =====
        form_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="ridge")
        form_frame.place(x=50, y=80, width=800, height=240)

        # Nama
        tk.Label(form_frame, text="Nama Pelanggan:", font=("Segoe UI", 11), bg="white").place(x=30, y=20)
        self.entry_name = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        self.entry_name.place(x=180, y=20)

        # Berat laundry
        tk.Label(form_frame, text="Berat (kg):", font=("Segoe UI", 11), bg="white").place(x=30, y=70)
        self.entry_weight = tk.Entry(form_frame, font=("Segoe UI", 11), width=10)
        self.entry_weight.place(x=180, y=70)

        # Pilihan layanan
        tk.Label(form_frame, text="Jenis Layanan:", font=("Segoe UI", 11), bg="white").place(x=30, y=120)
        self.service_var = tk.StringVar()
        self.combo_service = ttk.Combobox(
            form_frame,
            textvariable=self.service_var,
            values=["Cuci", "Cuci + Setrika", "Setrika"],
            state="readonly",
            font=("Segoe UI", 11),
            width=25
        )
        self.combo_service.place(x=180, y=120)
        self.combo_service.current(0)

        # Member Check
        self.member_var = tk.BooleanVar()
        tk.Checkbutton(
            form_frame,
            text="Member (Diskon 10%)",
            variable=self.member_var,
            bg="white",
            font=("Segoe UI", 11)
        ).place(x=180, y=160)

        # Tombol Submit
        self.btn_add = tk.Button(
            form_frame,
            text="Tambah ke Antrian",
            font=("Segoe UI", 11, "bold"),
            bg="#0078FF",
            fg="white",
            padx=10,
            pady=5,
            command=self.add_queue
        )
        self.btn_add.place(x=600, y=170)

        # ===== TABEL =====
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 12, "bold"),
                        background="#0078FF",
                        foreground="white",
                        padding=8)

        style.configure("Treeview",
                        font=("Segoe UI", 11),
                        rowheight=30,
                        background="white",
                        fieldbackground="white")

        style.map("Treeview",
                  background=[("selected", "#4da3ff")])

        self.table_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.table_frame.place(x=50, y=340, width=800, height=260)

        self.table = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Nama", "Layanan", "Berat", "HargaKg", "HargaAwal", "HargaAkhir"),
            show="headings"
        )

        self.table.heading("ID", text="ID")
        self.table.heading("Nama", text="Nama")
        self.table.heading("Layanan", text="Layanan")
        self.table.heading("Berat", text="Berat (kg)")
        self.table.heading("HargaKg", text="Harga / kg")
        self.table.heading("HargaAwal", text="Harga Awal")
        self.table.heading("HargaAkhir", text="Harga Akhir")

        self.table.column("ID", width=60, anchor="center")
        self.table.column("Nama", width=150)
        self.table.column("Layanan", width=110)  # <<< DIPERKECIL LAGI
        self.table.column("Berat", width=80, anchor="center")
        self.table.column("HargaKg", width=100, anchor="e")
        self.table.column("HargaAwal", width=120, anchor="e")
        self.table.column("HargaAkhir", width=120, anchor="e")

        self.table.pack(fill="both", expand=True)

        # Tombol Laundry Selesai
        self.btn_done = tk.Button(
            self.root,
            text="Laundry Selesai (Hapus Antrian)",
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=10,
            pady=8,
            command=self.finish_laundry
        )
        self.btn_done.place(x=300, y=605)

    # ========== FUNGSI TAMBAH ANTRIAN ==========
    def add_queue(self):
        name = self.entry_name.get()
        weight = self.entry_weight.get()
        service = self.service_var.get()
        is_member = self.member_var.get()

        if name == "" or weight == "":
            messagebox.showerror("Error", "Semua data harus diisi!")
            return

        try:
            weight = float(weight)
        except:
            messagebox.showerror("Error", "Berat harus berupa angka!")
            return

        # Harga per kg
        if service == "Cuci":
            price_per_kg = 5000
        elif service == "Cuci + Setrika":
            price_per_kg = 8000
        else:
            price_per_kg = 4000

        harga_awal = weight * price_per_kg

        # Diskon Member
        if is_member:
            harga_akhir = harga_awal * 0.9
        else:
            harga_akhir = harga_awal

        # Buat item
        item = LaundryItem(
            id_pelanggan=self.counter,
            nama=name,
            layanan=service,
            berat=weight,
            total=harga_akhir
        )

        item.harga_per_kg = price_per_kg
        item.harga_awal = harga_awal
        item.harga_akhir = harga_akhir

        self.queue.enqueue(item)
        self.counter += 1

        self.update_table()

        self.entry_name.delete(0, tk.END)
        self.entry_weight.delete(0, tk.END)
        self.member_var.set(False)

    # ========== FUNGSI UPDATE TABEL ==========
    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for item in self.queue.queue:
            self.table.insert("",
                              "end",
                              values=(
                                  item.id_pelanggan,
                                  item.nama,
                                  item.layanan,
                                  item.berat,
                                  f"Rp{item.harga_per_kg:,}",
                                  f"Rp{item.harga_awal:,.0f}",
                                  f"Rp{item.harga_akhir:,.0f}"
                              ))

    # ========== FUNGSI HAPUS ANTRIAN ==========
    def finish_laundry(self):
        removed = self.queue.dequeue()
        if removed:
            messagebox.showinfo("Sukses",
                                f"Laundry pelanggan '{removed.nama}' selesai!")
        else:
            messagebox.showwarning("Kosong", "Tidak ada antrian!")

        self.update_table()


# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = LaundryApp(root)
    root.mainloop()
