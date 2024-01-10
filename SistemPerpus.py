import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

registered_members = []
registered_member_ids = []

class BoxAddBook(simpledialog.Dialog):
    def __init__(self, parent, master):
        self.master = master 
        super().__init__(parent)
        
    def body(self, master):
        tk.Label(master, text="Judul Buku:").grid(row=0, sticky="e")
        tk.Label(master, text="Pengarang:").grid(row=1, sticky="e")
        tk.Label(master, text="ISBN:").grid(row=2, sticky="e")
        tk.Label(master, text="Jumlah Halaman:").grid(row=3, sticky="e")

        self.title_entry = tk.Entry(master)
        self.author_entry = tk.Entry(master)
        self.isbn_entry = tk.Entry(master)
        self.pages_entry = tk.Entry(master)

        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=1, column=1)
        self.isbn_entry.grid(row=2, column=1)
        self.pages_entry.grid(row=3, column=1)

    def validate(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        pages = self.pages_entry.get()

        if not (title and author and isbn and pages):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
            return False

        return True

    def apply(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        pages = self.pages_entry.get()

        if not (title and author and pages and isbn):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
            return
        global book_info
        
        book_info = {"title": title, "author": author, "pages": pages, "isbn": isbn, "status": "Tersedia"}
        print(book_info)
        messagebox.showinfo("Info", "Buku berhasil ditambahkan!")
        return book_info
        
class BoxRegistration(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Nama:").grid(row=0)
        tk.Label(master, text="Username:").grid(row=1)
        tk.Label(master, text="Password:").grid(row=2)
        tk.Label(master, text="Pelajar (Y/N):").grid(row=3)
        tk.Label(master, text="Alamat:").grid(row=4)
        tk.Label(master, text="No Telepon:").grid(row=5)

        self.name_entry = tk.Entry(master)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")
        self.pelajar_var = tk.StringVar(value="N")
        self.pelajar_entry = ttk.Combobox(master, textvariable=self.pelajar_var, values=["Y", "N"])
        self.alamat_entry = tk.Entry(master)
        self.telp_entry = tk.Entry(master)

        self.name_entry.grid(row=0, column=1)
        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        self.pelajar_entry.grid(row=3, column=1)
        self.alamat_entry.grid(row=4, column=1)
        self.telp_entry.grid(row=5, column=1)

    def validate(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        pelajar = self.pelajar_var.get()
        alamat = self.alamat_entry.get()
        telp = self.telp_entry.get()

        if not (name and username and password and pelajar and alamat and telp):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
            return False

        return True

    def apply(self):
        if not self.validate():
            return
        
        member_id = self.generate_member_id()

        self.result = (
            member_id,
            self.name_entry.get(),
            self.username_entry.get(),
            self.password_entry.get(),
            self.pelajar_var.get(),
            self.alamat_entry.get(),
            self.telp_entry.get()
        )

    def generate_member_id(self):
        member_id = len(registered_member_ids) + 1
        registered_member_ids.append(member_id)
        return member_id
        
class LibrarySystem:
    def __init__(self, root, registered_members):
        self.root = root
        self.root.title("Sistem Perpustakaan")
        self.root.geometry("600x400")

        self.is_admin = False
        self.logged_in_user = None
        self.books = [] 
        self.members = registered_members
        self.current_member_name = None

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Login sebagai:").grid(row=0, column=0, padx=10, pady=10)

        tk.Button(self.login_frame, text="Admin", command=self.admin_login).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.login_frame, text="Member", command=self.member_login).grid(row=1, column=1, padx=10, pady=10)

    def admin_login(self):
        username = simpledialog.askstring("Login Admin", "Masukkan username admin:")
        password = simpledialog.askstring("Login Admin", "Masukkan password admin:")
        
        if username == "admin" and password == "admin123":
            self.is_admin = True
            self.create_admin_dashboard()
        else:
            messagebox.showwarning("Peringatan", "Login admin gagal. Coba lagi.")

    def member_login(self):
        option = messagebox.askquestion("Login Member", "Apakah Anda sudah memiliki akun?")
        
        if option == 'yes':
            username = simpledialog.askstring("Login Member", "Masukkan username member:")
            password = simpledialog.askstring("Login Member", "Masukkan password member:")
            
            for member in self.members:
                if member['username'] == username and member['password'] == password:
                    self.is_admin = False
                    self.logged_in_user = member
                    self.current_member_name = member['username']
                    self.create_member_dashboard()
                    return
            messagebox.showwarning("Peringatan", "Login member gagal. Coba lagi.")
        else:
            registration_dialog = BoxRegistration(self.root)
            result = registration_dialog.result

            if result:
                member_id, name, new_username, new_password, is_student_str, address, telp = result

                if not (member_id and name and new_username and new_password and is_student_str and address and telp):
                    messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
                    return

                is_student = is_student_str.upper() == 'Y'

                new_member = {"id": member_id, "name": name, "username": new_username, "password": new_password, "address": address, "is_student": is_student, "no_telepon": telp}
                self.members.append(new_member)

                username = new_username
                password = new_password

                self.is_admin = False
                self.logged_in_user = new_member
                self.current_member_name = new_member['name'] 
                self.create_member_dashboard()
    
    def show_registered_members(self):
        if self.is_admin:
            member_info = ""
            for i, member in enumerate(self.members, 1):
                member_info += f"Member {i}:\n"
                member_info += f"  ID: {member['id']}\n"
                member_info += f"  Nama: {member['name']}\n"
                member_info += f"  Alamat: {member['address']}\n"
                member_info += f"  Status: {'Pelajar' if member['is_student'] else 'Bekerja'}\n"
                member_info += f"  No Telepon: {member['no_telepon']}\n"
            
            if member_info:
                messagebox.showinfo("Daftar Member Terdaftar", member_info)
            else:
                messagebox.showinfo("Daftar Member Terdaftar", "Belum ada member terdaftar.")
        else:
            messagebox.showwarning("Peringatan", "Anda bukan admin. Hak akses terbatas.")
        
    def create_admin_dashboard(self):
        self.login_frame.destroy()

        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack(pady=20)

        tk.Label(self.admin_frame, text="Admin Dashboard").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Tambah Buku", command=self.add_book).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Hapus Buku", command=self.remove_book).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Update Status Buku", command=self.update_book_status).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Lihat Daftar Member", command=self.show_registered_members).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Lihat Daftar Buku", command=self.show_books).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Logout", command=self.logout_admin).grid(row=7, column=0, padx=10, pady=10)
        
    def add_book(self):
        add_book_dialog = BoxAddBook(self.root, self)
        self.books.append(book_info)

    def remove_book(self):
        title = simpledialog.askstring("Hapus Buku", "Masukkan judul buku yang akan dihapus:")
        for book in self.books:
            if book["title"] == title:
                self.books.remove(book)
                messagebox.showinfo("Info", f"Buku '{title}' berhasil dihapus!")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak ditemukan!")

    def update_book_status(self):
        title = simpledialog.askstring("Update Status Buku", "Masukkan judul buku:")
        
        # Menambahkan combo box untuk memilih status
        status_options = ["Tersedia", "Tidak Tersedia"]
        status = self.create_status_combobox("Pilih Status", status_options)
        
        if status is None:
            return  # Batal jika pengguna membatalkan

        for book in self.books:
            if book["title"] == title:
                book["status"] = status
                messagebox.showinfo("Info", f"Status buku '{title}' berhasil diupdate menjadi {status}.")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak ditemukan!")

    def create_status_combobox(self, title, options):
        # Membuat jendela pop-up dengan kombinasi kotak entri dan combo box
        status_dialog = tk.Toplevel(self.root)
        status_dialog.title(title)

        status_var = tk.StringVar(value=options[0])

        tk.Label(status_dialog, text="Status:").grid(row=0, column=0, padx=10, pady=10)
        
        status_combobox = ttk.Combobox(status_dialog, textvariable=status_var, values=options)
        status_combobox.grid(row=0, column=1, padx=10, pady=10)
        
        ok_button = tk.Button(status_dialog, text="OK", command=status_dialog.destroy)
        ok_button.grid(row=1, column=0, columnspan=2, pady=10)

        status_dialog.focus_set()
        status_dialog.grab_set()

        self.root.wait_window(status_dialog)

        return status_var.get()

    def create_member_dashboard(self):
        self.login_frame.destroy()

        self.member_frame = tk.Frame(self.root)
        self.member_frame.pack(pady=20)

        if self.logged_in_user:
            tk.Label(self.member_frame, text=f"Halo {self.logged_in_user['name']}").grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.member_frame, text="Member Dashboard").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Pinjam Buku", command=self.borrow_book).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Kembalikan Buku", command=self.return_book).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Lihat Daftar Buku", command=self.show_books).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Logout", command=self.logout_member).grid(row=4, column=0, padx=10, pady=10)
        
    def show_books(self):
        books_info = ""
        for i, book in enumerate(self.books, 1):
            books_info += f"Buku {i}:\n"
            books_info += f"Judul: {book['title']}\n"
            books_info += f"Pengarang: {book['author']}\n"
            books_info += f"ISBN: {book['isbn']}\n"
            books_info += f"Halaman: {book['pages']}\n"
            books_info += f"Status: {book['status']}\n"

        if books_info:
            messagebox.showinfo("Daftar Buku", books_info)
        else:
            messagebox.showinfo("Daftar Buku", "Belum ada buku yang ditambahkan.")

    def borrow_book(self):
        title = simpledialog.askstring("Pinjam Buku", "Masukkan judul buku yang akan dipinjam:")
        for book in self.books:
            if book["title"] == title and book["status"] == "Tersedia":
                book["status"] = "Dipinjam"
                book["borrower"] = self.current_member_name
                messagebox.showinfo("Info", f"Buku '{title}' berhasil dipinjam oleh {self.current_member_name}!")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak tersedia atau tidak ditemukan!")

    def return_book(self):
        if not self.logged_in_user:
            messagebox.showwarning("Peringatan", "Anda belum login. Silakan login terlebih dahulu.")
            return

        title = simpledialog.askstring("Kembalikan Buku", "Masukkan judul buku yang akan dikembalikan:")
        for book in self.books:
            if (
                book["title"] == title
                and book["status"] == "Dipinjam"
                and book["borrower"] == self.logged_in_user["name"]
            ):
                book["status"] = "Tersedia"
                book["borrower"] = None
                messagebox.showinfo(
                    "Info",
                    f"Buku '{title}' berhasil dikembalikan oleh {self.logged_in_user['name']}. Status buku diubah menjadi Tersedia.",
                )
                return
        messagebox.showwarning(
            "Peringatan",
            f"Buku '{title}' tidak dapat dikembalikan dikarenakan bukan anda yang meminjam",
        )
        
    def logout_admin(self):
        self.admin_frame.destroy()
        self.is_admin = False
        self.create_login_screen()

    def logout_member(self):
        self.member_frame.destroy()
        self.logged_in_user = None
        self.create_login_screen()

if __name__ == "__main__":
    registered_members = []

    root = tk.Tk()
    app = LibrarySystem(root, registered_members)
    root.mainloop()