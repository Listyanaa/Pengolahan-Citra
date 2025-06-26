import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1250x700")
        self.root.configure(bg="#d9d9d9")
        self.original_image = None
        self.processed_image = None

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 10), background="#e0e0e0", foreground="#333333", padding=6, anchor="w")
        self.style.map("TButton", background=[('active', '#cccccc')])

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root, width=250, bg="#bfbfbf")
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        label_title = tk.Label(control_frame, text="🎨 Fitur Aplikasi", font=("Helvetica", 14, "bold"), bg="#bfbfbf", fg="#222")
        label_title.pack(pady=10)

        button_wajib = [
            ("📂", "Input Gambar", self.load_image, "Membuka file gambar dari komputer"),
            ("🖤", "Grayscale", self.to_grayscale, "Mengubah gambar menjadi hitam putih"),
            ("⬛", "Biner", self.to_binary, "Konversi citra ke biner dengan threshold"),
            ("☀️", "Brightness", self.set_brightness, "Atur tingkat kecerahan gambar"),
            ("❌", "Logika NOT", self.logic, "Negatifkan citra menggunakan operasi logika NOT"),
        ]

        for icon, label, func, tip in button_wajib:
            btn = ttk.Button(control_frame, text=f"{icon}   {label}", command=func)
            btn.pack(pady=2, fill='x')
            btn.bind("<Enter>", lambda e, t=tip: self.root.title(t))
            btn.bind("<Leave>", lambda e: self.root.title("Aplikasi Pengolahan Citra Digital"))

        ttk.Separator(control_frame, orient="horizontal").pack(fill='x', pady=8)

        button_optional = [
            ("📊", "Histogram", self.histogram, "Tampilkan histogram citra grayscale"),
            ("🔍", "Konvolusi", self.convolution_menu, "Menu filter konvolusi (sharpening, blur, edge)"),
            ("🔧", "Morfologi", self.morphology_menu, "Menu operasi morfologi (erosi, dilasi)"),
        ]

        for icon, label, func, tip in button_optional:
            btn = ttk.Button(control_frame, text=f"{icon}   {label}", command=func)
            btn.pack(pady=2, fill='x')
            btn.bind("<Enter>", lambda e, t=tip: self.root.title(t))
            btn.bind("<Leave>", lambda e: self.root.title("Aplikasi Pengolahan Citra Digital"))

        ttk.Separator(control_frame, orient="horizontal").pack(fill='x', pady=8)

        button_utility = [
            ("🔄", "Reset Gambar", self.reset_image, "Kembalikan ke gambar asli"),
            ("💾", "Simpan Hasil", self.save_image, "Simpan hasil pengolahan citra")
        ]

        for icon, label, func, tip in button_utility:
            btn = ttk.Button(control_frame, text=f"{icon}   {label}", command=func)
            btn.pack(pady=2, fill='x')
            btn.bind("<Enter>", lambda e, t=tip: self.root.title(t))
            btn.bind("<Leave>", lambda e: self.root.title("Aplikasi Pengolahan Citra Digital"))

        # Area tampilan gambar
        image_frame = tk.Frame(self.root, bg="#d9d9d9")
        image_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        canvas_frame = tk.Frame(image_frame, bg="#d9d9d9")
        canvas_frame.pack(fill="both", expand=True)

        original_frame = tk.Frame(canvas_frame, bg="#d9d9d9")
        original_frame.pack(side="left", padx=20)
        self.original_label = tk.Label(original_frame, text="🖼️ Gambar Asli", font=("Helvetica", 12, "bold"), bg="#d9d9d9")
        self.original_label.pack(pady=5)
        self.original_canvas = tk.Label(original_frame, bg="#cccccc", width=480, height=360)
        self.original_canvas.pack()

        result_frame = tk.Frame(canvas_frame, bg="#d9d9d9")
        result_frame.pack(side="left", padx=20)
        self.result_label = tk.Label(result_frame, text="🎯 Hasil Proses", font=("Helvetica", 12, "bold"), bg="#d9d9d9")
        self.result_label.pack(pady=5)
        self.result_canvas = tk.Label(result_frame, bg="#cccccc", width=480, height=360)
        self.result_canvas.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image, self.original_canvas)
            self.display_image(self.processed_image, self.result_canvas)

    def display_image(self, img, canvas):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((480, 360))
        img_tk = ImageTk.PhotoImage(img_pil)
        canvas.configure(image=img_tk)
        canvas.image = img_tk

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image, self.result_canvas)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Berhasil", "Gambar berhasil disimpan.")

    def to_grayscale(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def to_binary(self):
        if self.original_image is not None:
            def apply_threshold(thresh_value):
                gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
                self.processed_image = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
                self.display_image(self.processed_image, self.result_canvas)

            self.slider_window("Threshold Biner", 0, 255, 127, apply_threshold)

    def set_brightness(self):
        if self.original_image is not None:
            def apply_brightness(value):
                result = cv2.convertScaleAbs(self.original_image, alpha=1, beta=value)
                self.processed_image = result
                self.display_image(self.processed_image, self.result_canvas)

            self.slider_window("Pengaturan Brightness", -100, 100, 0, apply_brightness)

    def logic(self):
        if self.original_image is not None:
            self.processed_image = cv2.bitwise_not(self.original_image)
            self.display_image(self.processed_image, self.result_canvas)

    def histogram(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist_img = np.ones((300, 400, 3), dtype=np.uint8) * 255
            hist = hist / hist.max() * 300
            for x in range(256):
                cv2.line(hist_img, (x + 70, 300), (x + 70, 300 - int(hist[x])), (0, 0, 0), 1)
            self.processed_image = hist_img
            self.display_image(self.processed_image, self.result_canvas)

    def convolution_menu(self):
        if self.original_image is None:
            messagebox.showwarning("Peringatan", "Silakan muat gambar terlebih dahulu!")
            return

        menu_win = tk.Toplevel(self.root)
        menu_win.title("🔍 Menu Konvolusi")
        menu_win.geometry("300x200")
        menu_win.configure(bg="#f0f0f0")

        tk.Label(menu_win, text="Pilih Jenis Filter:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        ttk.Button(menu_win, text="✨ Sharpening", command=lambda: [self.sharpening(), menu_win.destroy()]).pack(pady=5, fill='x', padx=20)
        ttk.Button(menu_win, text="🌫️ Blur (Gaussian)", command=lambda: [self.blur_filter(), menu_win.destroy()]).pack(pady=5, fill='x', padx=20)
        ttk.Button(menu_win, text="📐 Edge Detection (Sobel)", command=lambda: [self.edge_detection(), menu_win.destroy()]).pack(pady=5, fill='x', padx=20)

    def sharpening(self):
        if self.original_image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            self.processed_image = cv2.filter2D(self.original_image, -1, kernel)
            self.display_image(self.processed_image, self.result_canvas)

    def blur_filter(self):
        if self.original_image is not None:
            self.processed_image = cv2.GaussianBlur(self.original_image, (15, 15), 0)
            self.display_image(self.processed_image, self.result_canvas)

    def edge_detection(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.sqrt(sobelx**2 + sobely**2)
            sobel = np.uint8(np.clip(sobel, 0, 255))
            self.processed_image = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def morphology_menu(self):
        if self.original_image is None:
            messagebox.showwarning("Peringatan", "Silakan muat gambar terlebih dahulu!")
            return

        menu_win = tk.Toplevel(self.root)
        menu_win.title("🔧 Menu Morfologi")
        menu_win.geometry("350x300")
        menu_win.configure(bg="#f0f0f0")

        tk.Label(menu_win, text="Pilih Operasi & Structural Element:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        # Frame untuk operasi
        op_frame = tk.Frame(menu_win, bg="#f0f0f0")
        op_frame.pack(pady=5)
        tk.Label(op_frame, text="Operasi:", font=("Helvetica", 10, "bold"), bg="#f0f0f0").pack()
        
        # Frame untuk SE
        se_frame = tk.Frame(menu_win, bg="#f0f0f0")
        se_frame.pack(pady=5)
        tk.Label(se_frame, text="Structural Element:", font=("Helvetica", 10, "bold"), bg="#f0f0f0").pack()

        # Tombol operasi
        ttk.Button(menu_win, text="🌾 Erosi + Rectangular SE", 
                  command=lambda: [self.erosion_rectangular(), menu_win.destroy()]).pack(pady=3, fill='x', padx=20)
        ttk.Button(menu_win, text="🌾 Erosi + Elliptical SE", 
                  command=lambda: [self.erosion_elliptical(), menu_win.destroy()]).pack(pady=3, fill='x', padx=20)
        ttk.Button(menu_win, text="🔍 Dilasi + Rectangular SE", 
                  command=lambda: [self.dilation_rectangular(), menu_win.destroy()]).pack(pady=3, fill='x', padx=20)
        ttk.Button(menu_win, text="🔍 Dilasi + Elliptical SE", 
                  command=lambda: [self.dilation_elliptical(), menu_win.destroy()]).pack(pady=3, fill='x', padx=20)

    def erosion_rectangular(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # SE Rectangular 5x5
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            eroded = cv2.erode(binary, kernel, iterations=1)
            self.processed_image = cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def erosion_elliptical(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # SE Elliptical 7x7
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            eroded = cv2.erode(binary, kernel, iterations=1)
            self.processed_image = cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def dilation_rectangular(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # SE Rectangular 5x5
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            dilated = cv2.dilate(binary, kernel, iterations=1)
            self.processed_image = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def dilation_elliptical(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # SE Elliptical 7x7
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            dilated = cv2.dilate(binary, kernel, iterations=1)
            self.processed_image = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image, self.result_canvas)

    def slider_window(self, title, from_, to_, init, callback):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("300x100")
        win.configure(bg="#eeeeee")
        slider = ttk.Scale(win, from_=from_, to=to_, orient="horizontal")
        slider.set(init)
        slider.pack(pady=10, padx=10, fill='x')

        def update(_): callback(int(slider.get()))
        slider.bind("<Motion>", update)

        ttk.Button(win, text="OK", command=win.destroy).pack(pady=5)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()