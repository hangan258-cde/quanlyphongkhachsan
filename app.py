import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Khách Sạn")
        self.root.geometry("1100x800")

        # -------------------------------------------------------------
        # 1. CÂU LỆNH KHỞI TẠO VÀ TẢI HÌNH ẢNH VT.JPG TRANG CHỦ
        # -------------------------------------------------------------
        self.image_filename = "VT.jpg"
        
        # Ảnh banner lớn cho trang chủ (1050x180 px)
        self.home_banner_photo = self.load_room_image(self.image_filename, size=(1050, 180))
        
        # Ảnh nhỏ cho khung chi tiết phòng (250x160 px)
        self.room_photo = self.load_room_image(self.image_filename, size=(250, 160))

        # Khởi tạo dữ liệu danh sách phòng mẫu
        self.rooms = {
            "101": {"type": "Standard", "price": 500000, "status": "Trống", "guest": "", "phone": "", "checkin": ""},
            "102": {"type": "Standard", "price": 500000, "status": "Trống", "guest": "", "phone": "", "checkin": ""},
            "201": {"type": "Superior", "price": 750000, "status": "Trống", "guest": "", "phone": "", "checkin": ""},
            "202": {"type": "Superior", "price": 750000, "status": "Đang ở", "guest": "Nguyễn Văn A", "phone": "0901234567", "checkin": "2026-09-28 08:00"},
            "301": {"type": "Deluxe", "price": 1000000, "status": "Trống", "guest": "", "phone": "", "checkin": ""},
            "302": {"type": "VIP Suite", "price": 1800000, "status": "Trống", "guest": "", "phone": "", "checkin": ""}
        }

        self.setup_ui()

    # -------------------------------------------------------------
    # 2. CÂU LỆNH HÀM XỬ LÝ TẢI VÀ TỐI ƯU KÍCH THƯỚC ẢNH VT.JPG
    # -------------------------------------------------------------
    def load_room_image(self, image_path, size=(250, 160)):
        """Tải ảnh VT.jpg và resize theo kích thước mong muốn"""
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Lỗi khi mở file ảnh {image_path}: {e}")
                return None
        else:
            print(f"Cảnh báo: Không tìm thấy file '{image_path}' trong thư mục chạy code.")
            return None

    def setup_ui(self):
        # Thanh tiêu đề chính
        header_frame = tk.Frame(self.root, bg="#2C3E50", height=50)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame, 
            text="HỆ THỐNG QUẢN LÝ KHÁCH SẠN", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#2C3E50"
        )
        header_label.pack(pady=10)

        # -------------------------------------------------------------
        # 3. CÂU LỆNH HIỂN THỊ BANNER ẢNH VT.JPG TRÊN ĐẦU TRANG CHỦ
        # -------------------------------------------------------------
        if self.home_banner_photo:
            banner_label = tk.Label(self.root, image=self.home_banner_photo, bg="#2C3E50")
            banner_label.pack(fill=tk.X, padx=10, pady=(10, 0))
        else:
            banner_label = tk.Label(
                self.root, 
                text="[ TRANG CHỦ KHÁCH SẠN - FILE VT.JPG CHƯA ĐƯỢC TẢI ]", 
                font=("Arial", 12, "bold"), 
                bg="#34495E", 
                fg="white", 
                height=4
            )
            banner_label.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Các Tab giao diện chính
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Sơ đồ phòng
        tab_map = ttk.Frame(notebook)
        notebook.add(tab_map, text=" Sơ Đồ Phòng ")
        self.setup_room_map_tab(tab_map)

        # Tab 2: Quản lý Check-in / Check-out
        tab_checkin = ttk.Frame(notebook)
        notebook.add(tab_checkin, text=" Quản Lý Check-in / Check-out ")
        self.setup_checkin_tab(tab_checkin)

    def setup_room_map_tab(self, parent):
        main_frame = tk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cột bên trái: Các nút chọn phòng
        rooms_frame = tk.LabelFrame(main_frame, text="Danh Sách Phòng", font=("Arial", 12, "bold"), padx=10, pady=10)
        rooms_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.room_buttons = {}
        row, col = 0, 0
        for room_id, info in self.rooms.items():
            btn_color = "#2ECC71" if info["status"] == "Trống" else "#E74C3C"
            btn_text = f"Phòng {room_id}\n({info['type']})\n{info['status']}"

            btn = tk.Button(
                rooms_frame, text=btn_text, font=("Arial", 11, "bold"),
                bg=btn_color, fg="white", width=15, height=3,
                command=lambda r=room_id: self.show_room_details(r)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            self.room_buttons[room_id] = btn

            col += 1
            if col > 2:
                col = 0
                row += 1

        # Cột bên phải: Xem thông tin chi tiết & Ảnh minh họa
        details_frame = tk.LabelFrame(main_frame, text="Thông Tin Chi Tiết", font=("Arial", 12, "bold"), padx=15, pady=15)
        details_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # Khung hiển thị ảnh minh họaVT.jpg
        self.lbl_image = tk.Label(details_frame, text="[Ảnh Phòng]", bg="#BDC3C7", width=30, height=8)
        self.lbl_image.pack(pady=(0, 15))
        if self.room_photo:
            self.lbl_image.config(image=self.room_photo, text="", width=250, height=160)

        self.lbl_detail_room = tk.Label(details_frame, text="Chọn phòng để xem chi tiết", font=("Arial", 12, "bold"))
        self.lbl_detail_room.pack(anchor="w", pady=5)

        self.lbl_detail_type = tk.Label(details_frame, text="Loại phòng: -", font=("Arial", 11))
        self.lbl_detail_type.pack(anchor="w", pady=2)

        self.lbl_detail_price = tk.Label(details_frame, text="Giá: -", font=("Arial", 11))
        self.lbl_detail_price.pack(anchor="w", pady=2)

        self.lbl_detail_status = tk.Label(details_frame, text="Trạng thái: -", font=("Arial", 11))
        self.lbl_detail_status.pack(anchor="w", pady=2)

        self.lbl_detail_guest = tk.Label(details_frame, text="Khách hàng: -", font=("Arial", 11))
        self.lbl_detail_guest.pack(anchor="w", pady=2)

        self.lbl_detail_phone = tk.Label(details_frame, text="Số điện thoại: -", font=("Arial", 11))
        self.lbl_detail_phone.pack(anchor="w", pady=2)

    def show_room_details(self, room_id):
        info = self.rooms[room_id]
        self.lbl_detail_room.config(text=f"Phòng: {room_id}")
        self.lbl_detail_type.config(text=f"Loại phòng: {info['type']}")
        self.lbl_detail_price.config(text=f"Giá: {info['price']:,} VNĐ/đêm")
        self.lbl_detail_status.config(text=f"Trạng thái: {info['status']}")
        self.lbl_detail_guest.config(text=f"Khách hàng: {info['guest'] if info['guest'] else 'N/A'}")
        self.lbl_detail_phone.config(text=f"Số điện thoại: {info['phone'] if info['phone'] else 'N/A'}")

    def setup_checkin_tab(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        form_frame = tk.LabelFrame(frame, text="Thao Tác Nhận / Trả Phòng", font=("Arial", 12, "bold"), padx=15, pady=15)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(form_frame, text="Chọn Phòng:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.cb_rooms = ttk.Combobox(form_frame, values=list(self.rooms.keys()), font=("Arial", 11), state="readonly")
        self.cb_rooms.grid(row=0, column=1, sticky="ew", pady=5)
        if self.rooms:
            self.cb_rooms.current(0)

        tk.Label(form_frame, text="Tên Khách Hàng:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_guest = tk.Entry(form_frame, font=("Arial", 11))
        self.entry_guest.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Số Điện Thoại:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_phone = tk.Entry(form_frame, font=("Arial", 11))
        self.entry_phone.grid(row=2, column=1, sticky="ew", pady=5)

        btn_checkin = tk.Button(form_frame, text="Check-in (Nhận Phòng)", bg="#2ECC71", fg="white", font=("Arial", 11, "bold"), command=self.handle_checkin)
        btn_checkin.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 5))

        btn_checkout = tk.Button(form_frame, text="Check-out (Trả Phòng)", bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), command=self.handle_checkout)
        btn_checkout.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        form_frame.columnconfigure(1, weight=1)

        # Hiển thị ảnh mẫu VT.jpg bên phải tab Check-in
        img_preview_frame = tk.LabelFrame(frame, text="Hình Ảnh Minh Họa (VT.jpg)", font=("Arial", 12, "bold"), padx=15, pady=15)
        img_preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        lbl_tab2_img = tk.Label(img_preview_frame, text="[VT.jpg]", bg="#BDC3C7")
        lbl_tab2_img.pack(fill=tk.BOTH, expand=True)
        if self.room_photo:
            lbl_tab2_img.config(image=self.room_photo, text="")

    def handle_checkin(self):
        room_id = self.cb_rooms.get()
        guest = self.entry_guest.get().strip()
        phone = self.entry_phone.get().strip()

        if not room_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return

        if self.rooms[room_id]["status"] == "Đang ở":
            messagebox.showerror("Lỗi", f"Phòng {room_id} hiện đang có khách ở!")
            return

        if not guest or not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin khách hàng!")
            return

        self.rooms[room_id]["status"] = "Đang ở"
        self.rooms[room_id]["guest"] = guest
        self.rooms[room_id]["phone"] = phone

        self.room_buttons[room_id].config(bg="#E74C3C", text=f"Phòng {room_id}\n({self.rooms[room_id]['type']})\nĐang ở")
        self.show_room_details(room_id)

        self.entry_guest.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

        messagebox.showinfo("Thành công", f"Đã check-in thành công cho phòng {room_id}!")

    def handle_checkout(self):
        room_id = self.cb_rooms.get()

        if not room_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return

        if self.rooms[room_id]["status"] == "Trống":
            messagebox.showerror("Lỗi", f"Phòng {room_id} hiện đang trống!")
            return

        guest_name = self.rooms[room_id]["guest"]
        self.rooms[room_id]["status"] = "Trống"
        self.rooms[room_id]["guest"] = ""
        self.rooms[room_id]["phone"] = ""

        self.room_buttons[room_id].config(bg="#2ECC71", text=f"Phòng {room_id}\n({self.rooms[room_id]['type']})\nTrống")
        self.show_room_details(room_id)

        messagebox.showinfo("Thành công", f"Đã trả phòng {room_id} (Khách hàng: {guest_name}) thành công!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
