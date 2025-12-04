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

        bg1 = Image.open("assets/background.jpg")
        bg1 = bg1.resize((900, 650))
        self.bg1_img = ImageTk.PhotoImage(bg1)

        bg2 = Image.open("assets/background_2.png")
        bg2 = bg2.resize((900, 650))
        self.bg2_img = ImageTk.PhotoImage(bg2)

        self.queue = QueueLaundry()
        self.counter = 1
        self.selected_item = None

        self.slide_container = tk.Frame(self.root, width=900, height=650)
        self.slide_container.place(x=0, y=0)

        self.slide1 = tk.Frame(self.slide_container, width=900, height=650)
        self.slide1.place(x=0, y=0)

        self.bg1_label = tk.Label(self.slide1, image=self.bg1_img)
        self.bg1_label.place(x=0, y=0)

        self.slide2 = tk.Frame(self.slide_container, width=900, height=650)
        self.bg2_label = tk.Label(self.slide2, image=self.bg2_img)
        self.bg2_label.place(x=0, y=0)

        self.build_slide1()
        self.build_slide2()

        self.show_slide(self.slide1)

    def show_slide(self, slide):
        self.slide1.place_forget()
        self.slide2.place_forget()
        slide.place(x=0, y=0)

    def build_slide1(self):
        tk.Label(
            self.slide1,
            text="LAUNDRYGO - QUEUE SYSTEM",
            font=("Segoe UI", 22, "bold"),
            bg=self.slide1["bg"],
            fg="#000"
        ).place(x=240, y=20)

        form_frame = tk.Frame(self.slide1, bg="#ffffff", bd=2, relief="ridge")
        form_frame.place(x=50, y=80, width=800, height=240)

        tk.Label(form_frame, text="Nama Pelanggan:", font=("Segoe UI", 11), bg="white").place(x=30, y=20)
        self.entry_name = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        self.entry_name.place(x=180, y=20)

        tk.Label(form_frame, text="Berat (kg):", font=("Segoe UI", 11), bg="white").place(x=30, y=70)
        self.entry_weight = tk.Entry(form_frame, font=("Segoe UI", 11), width=10)
        self.entry_weight.place(x=180, y=70)

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

        self.member_var = tk.BooleanVar()
        tk.Checkbutton(
            form_frame,
            text="Member (Diskon 10%)",
            variable=self.member_var,
            bg="white",
            font=("Segoe UI", 11)
        ).place(x=180, y=160)

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

        self.btn_update = tk.Button(
            form_frame,
            text="Update Data",
            font=("Segoe UI", 11, "bold"),
            bg="#FFA500",
            fg="white",
            padx=10,
            pady=5,
            command=self.update_selected
        )
        self.btn_update.place(x=450, y=170)

        tk.Button(
            self.slide1,
            text="Lihat Antrian →",
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=10,
            pady=8,
            command=lambda: self.show_slide(self.slide2)
        ).place(x=360, y=350)

    def build_slide2(self):
        tk.Label(
            self.slide2,
            text="DAFTAR ANTRIAN LAUNDRY",
            font=("Segoe UI", 22, "bold"),
            bg=self.slide2["bg"],
            fg="#000"
        ).place(x=260, y=20)

        self.table_frame = tk.Frame(self.slide2, bg="white", bd=2, relief="ridge")
        self.table_frame.place(x=50, y=80, width=800, height=450)

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

        self.table = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Nama", "Layanan", "Berat", "HargaKg", "HargaAwal", "HargaAkhir"),
            show="headings"
        )

        self.table.heading("ID", text="Antrian")
        self.table.heading("Nama", text="Nama")
        self.table.heading("Layanan", text="Layanan")
        self.table.heading("Berat", text="Berat (kg)")
        self.table.heading("HargaKg", text="Harga / kg")
        self.table.heading("HargaAwal", text="Harga Awal")
        self.table.heading("HargaAkhir", text="Harga Akhir")

        self.table.column("ID", width=80, anchor="center")
        self.table.column("Nama", width=150)
        self.table.column("Layanan", width=110)
        self.table.column("Berat", width=80, anchor="center")
        self.table.column("HargaKg", width=100, anchor="e")
        self.table.column("HargaAwal", width=120, anchor="e")
        self.table.column("HargaAkhir", width=120, anchor="e")

        self.table.pack(fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", self.load_selected)

        tk.Button(
            self.slide2,
            text="← Kembali",
            font=("Segoe UI", 12, "bold"),
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=8,
            command=lambda: self.show_slide(self.slide1)
        ).place(x=70, y=550)

        tk.Button(
            self.slide2,
            text="Selesaikan Antrian (Dequeue)",
            font=("Segoe UI", 12, "bold"),
            bg="#d9534f",
            fg="white",
            padx=10,
            pady=8,
            command=self.finish_laundry
        ).place(x=600, y=550)

    # 🔥 VALIDASI NAMA → hanya huruf & spasi
    def validate_name(self, name):
        return name.replace(" ", "").isalpha()

    def add_queue(self):
        name = self.entry_name.get()
        weight = self.entry_weight.get()
        service = self.service_var.get()
        is_member = self.member_var.get()

        # 🛑 VALIDASI NAMA
        if not self.validate_name(name):
            messagebox.showerror("Error", "Nama hanya boleh berisi huruf dan spasi!")
            return

        if name == "" or weight == "":
            messagebox.showerror("Error", "Semua data harus diisi!")
            return

        try:
            weight = float(weight)
        except:
            messagebox.showerror("Error", "Berat harus berupa angka!")
            return

        if service == "Cuci":
            price_per_kg = 5000
        elif service == "Cuci + Setrika":
            price_per_kg = 8000
        else:
            price_per_kg = 4000

        harga_awal = weight * price_per_kg
        harga_akhir = harga_awal * 0.9 if is_member else harga_awal

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

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for item in self.queue.queue:
            self.table.insert(
                "",
                "end",
                values=(
                    item.id_pelanggan,
                    item.nama,
                    item.layanan,
                    item.berat,
                    f"Rp{item.harga_per_kg:,}",
                    f"Rp{item.harga_awal:,.0f}",
                    f"Rp{item.harga_akhir:,.0f}"
                )
            )

    def load_selected(self, event):
        selected = self.table.focus()
        if not selected:
            return

        values = self.table.item(selected, "values")
        if not values:
            return

        antrian_id = int(values[0])

        for item in self.queue.queue:
            if item.id_pelanggan == antrian_id:
                self.selected_item = item
                break

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, item.nama)

        self.entry_weight.delete(0, tk.END)
        self.entry_weight.insert(0, item.berat)

        self.service_var.set(item.layanan)
        self.member_var.set(False)

        self.show_slide(self.slide1)

    def update_selected(self):
        if not self.selected_item:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        name = self.entry_name.get()
        weight = self.entry_weight.get()
        service = self.service_var.get()
        is_member = self.member_var.get()

        # 🛑 VALIDASI NAMA
        if not self.validate_name(name):
            messagebox.showerror("Error", "Nama hanya boleh berisi huruf dan spasi!")
            return

        if name == "" or weight == "":
            messagebox.showerror("Error", "Semua data harus diisi!")
            return

        try:
            weight = float(weight)
        except:
            messagebox.showerror("Error", "Berat harus berupa angka!")
            return

        if service == "Cuci":
            price_per_kg = 5000
        elif service == "Cuci + Setrika":
            price_per_kg = 8000
        else:
            price_per_kg = 4000

        harga_awal = weight * price_per_kg
        harga_akhir = harga_awal * 0.9 if is_member else harga_awal

        self.selected_item.nama = name
        self.selected_item.berat = weight
        self.selected_item.layanan = service
        self.selected_item.harga_per_kg = price_per_kg
        self.selected_item.harga_awal = harga_awal
        self.selected_item.harga_akhir = harga_akhir
        self.selected_item.total = harga_akhir

        self.update_table()
        self.selected_item = None

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")

        self.entry_name.delete(0, tk.END)
        self.entry_weight.delete(0, tk.END)
        self.member_var.set(False)

    def finish_laundry(self):
        removed = self.queue.dequeue()

        if removed:
            messagebox.showinfo("Sukses", f"Laundry pelanggan '{removed.nama}' selesai!")

            new_id = 1
            for item in self.queue.queue:
                item.id_pelanggan = new_id
                new_id += 1

            self.counter = new_id

        else:
            messagebox.showwarning("Kosong", "Tidak ada antrian!")

        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = LaundryApp(root)
    root.mainloop()
