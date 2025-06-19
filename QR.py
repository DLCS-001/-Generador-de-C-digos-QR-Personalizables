import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk
import os

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Códigos QR con Logo y Colores")
        self.root.geometry("600x750")

        self.qr_image = None
        self.photo_image = None
        self.logo_path = None
        self.fill_color = "black"
        self.back_color = "white"

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Texto / URL:").grid(row=0, column=0, sticky=tk.W)
        self.text_input = ttk.Entry(main_frame, width=50)
        self.text_input.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(main_frame, text="Tamaño del QR:").grid(row=2, column=0, sticky=tk.W)
        self.size_var = tk.StringVar(value="10")
        ttk.Entry(main_frame, textvariable=self.size_var, width=10).grid(row=2, column=1)

        ttk.Label(main_frame, text="Borde:").grid(row=3, column=0, sticky=tk.W)
        self.border_var = tk.StringVar(value="1")
        ttk.Entry(main_frame, textvariable=self.border_var, width=10).grid(row=3, column=1)

        ttk.Label(main_frame, text="Color del QR:").grid(row=4, column=0, sticky=tk.W)
        ttk.Button(main_frame, text="Elegir color", command=self.choose_fill_color).grid(row=4, column=1)

        ttk.Label(main_frame, text="Color de fondo:").grid(row=5, column=0, sticky=tk.W)
        ttk.Button(main_frame, text="Elegir color", command=self.choose_back_color).grid(row=5, column=1)

        ttk.Button(main_frame, text="Elegir logo", command=self.select_logo).grid(row=6, column=0, columnspan=2, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Generar QR", command=self.generate_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guardar QR", command=self.save_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_all).pack(side=tk.LEFT, padx=5)

        self.qr_display = ttk.Label(main_frame)
        self.qr_display.grid(row=8, column=0, columnspan=2, pady=10)

    def choose_fill_color(self):
        color = colorchooser.askcolor(title="Elegir color del QR")[1]
        if color:
            self.fill_color = color

    def choose_back_color(self):
        color = colorchooser.askcolor(title="Elegir color de fondo")[1]
        if color:
            self.back_color = color

    def select_logo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if path:
            self.logo_path = path

    def generate_qr(self):
        text = self.text_input.get().strip()
        if not text:
            messagebox.showerror("Error", "Ingrese un texto.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=int(self.size_var.get()),
                border=int(self.border_var.get()),
            )
            qr.add_data(text)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert("RGB")

            if self.logo_path:
                logo = Image.open(self.logo_path)
                qr_width, qr_height = qr_img.size

                # Redimensionar logo al 20% del QR
                logo_size = int(qr_width * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

            self.qr_image = qr_img
            self.photo_image = ImageTk.PhotoImage(qr_img)
            self.qr_display.configure(image=self.photo_image)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el QR: {str(e)}")

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Genere un código QR primero.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
        if path:
            self.qr_image.save(path)
            messagebox.showinfo("Éxito", "QR guardado correctamente.")

    def clear_all(self):
        self.text_input.delete(0, tk.END)
        self.size_var.set("10")
        self.border_var.set("1")
        self.qr_display.configure(image='')
        self.qr_image = None
        self.photo_image = None
        self.logo_path = None
        self.fill_color = "black"
        self.back_color = "white"

def main():
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
