import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageDv")

        self.image_list = []
        self.common_width_cm = tk.DoubleVar(value=0)
        self.common_height_cm = tk.DoubleVar(value=0)

        self.carta_width_cm = 21.59
        self.carta_height_cm = 27.94
        self.thumbnail_images = {}

        self.setup_ui()

    def setup_ui(self):
        # Configurar el estilo
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", background="#000000", foreground="BLACK", padding=(5, 5), font=('Helvetica', 10))
        style.configure("TButton.BlackText", foreground="black")  # Nuevo estilo para texto negro
        style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))

        # Marco principal
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.grid(row=0, column=0)

        # Etiquetas y campos de entrada para las dimensiones comunes
        width_label = ttk.Label(main_frame, text="Ancho común (cm):")
        width_label.grid(row=0, column=0, padx=5, pady=5)

        width_entry = ttk.Entry(main_frame, textvariable=self.common_width_cm)
        width_entry.grid(row=0, column=1, padx=5, pady=5)

        height_label = ttk.Label(main_frame, text="Altura común (cm):")
        height_label.grid(row=1, column=0, padx=5, pady=5)

        height_entry = ttk.Entry(main_frame, textvariable=self.common_height_cm)
        height_entry.grid(row=1, column=1, padx=5, pady=5)

        # Lienzo para previsualización de la hoja tamaño carta y las imágenes
        self.canvas = tk.Canvas(self.root, width=300, height=400, bg="white")
        self.canvas.grid(row=0, column=1, rowspan=8, pady=10)

        # Barra de herramientas
        toolbar = ttk.Frame(self.root, style="TFrame")
        insert_button = ttk.Button(toolbar, text="Insertar", command=self.insert_image, style="TButton")
        clear_button = ttk.Button(toolbar, text="Limpiar", command=self.clear_canvas, style="TButton")
        export_button = ttk.Button(toolbar, text="Exportar a PDF", command=self.export_to_pdf, style="TButton")

        insert_button.grid(row=0, column=0, padx=5, pady=5)
        clear_button.grid(row=0, column=1, padx=5, pady=5)
        export_button.grid(row=0, column=2, padx=5, pady=5)

        toolbar.grid(row=8, column=0, columnspan=2, pady=10)


    def clear_canvas(self):
        # Limpiar el lienzo
        self.canvas.delete("all")

        # Limpiar la memoria de imágenes
        self.image_list = []
        self.thumbnail_images = {}



        
    def insert_image(self):
        if self.common_width_cm.get() == 0 or self.common_height_cm.get() == 0:
            messagebox.showerror("Error", "Por favor, defina las dimensiones comunes antes de insertar imágenes.")
            return

        # Abrir el explorador de archivos y obtener la ruta de las imágenes
        file_paths = filedialog.askopenfilenames(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])

        for file_path in file_paths:
            # Cargar la imagen
            image = Image.open(file_path)

            # Guardar la imagen en la lista junto con las dimensiones comunes
            self.image_list.append((image, self.common_width_cm.get(), self.common_height_cm.get()))

        # Actualizar la previsualización
        self.update_preview()

    def update_preview(self):
        # Limpiar el lienzo
        self.canvas.delete("all")

        # Dibujar la hoja tamaño carta
        carta_width_px = int(self.carta_width_cm * 100 / 2.54)  # Ajustar el tamaño de la hoja
        carta_height_px = int(self.carta_height_cm * 100 / 2.54)  # Ajustar el tamaño de la hoja
        self.canvas.create_rectangle(0, 0, carta_width_px, carta_height_px, outline="black")

        # Dibujar las imágenes en el lienzo con un espacio de 0.2 cm entre ellas
        x_offset, y_offset = 0, 0

        for image, width_cm, height_cm in self.image_list:
            # Convertir tamaños de cm a píxeles
            target_size_px = (int(width_cm * 100 / 2.54), int(height_cm * 100 / 2.54))  # Ajustar el tamaño de las imágenes
            resized_image = image.resize(target_size_px)

            # Calcular el factor de escala para que las imágenes entren en el lienzo
            scale_factor = min(1, 300 / (x_offset + target_size_px[0]))

            # Escalar la imagen para que quepa en el lienzo
            scaled_size = (int(target_size_px[0] * scale_factor), int(target_size_px[1] * scale_factor))
            scaled_image = resized_image.resize(scaled_size)

            # Dibujar la imagen en el lienzo
            photo_image = ImageTk.PhotoImage(scaled_image)
            self.thumbnail_images[(x_offset, y_offset)] = photo_image
            self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo_image)

            x_offset += scaled_size[0] + int(0.2 * 100 / 2.54)  # Ajustar el espacio entre las imágenes

            # Si la siguiente imagen no cabe en la misma fila, pasar a la siguiente fila
            if x_offset + scaled_size[0] > 300:
                x_offset = 0
                y_offset += scaled_size[1] + int(0.2 * 100 / 2.54)  # Ajustar el espacio entre las filas


    def export_to_pdf(self):
        if not self.image_list:
            messagebox.showerror("Error", "No hay imágenes para exportar.")
            return

        # Lógica para organizar y exportar las imágenes a PDF
        # Puedes usar bibliotecas como reportlab para crear el PDF

        # Ejemplo de cómo podrías guardar todas las imágenes en un solo PDF
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])

        if pdf_path:
            # Añadir márgenes a la hoja tamaño carta
            carta_width_px = int(self.carta_width_cm * 300 / 2.54)
            carta_height_px = int(self.carta_height_cm * 300 / 2.54)
            margin = int(1 * 300 / 2.54)
            pdf_width = carta_width_px - 2 * margin
            pdf_height = carta_height_px - 2 * margin

            # Crear un nuevo PDF con márgenes
            pdf = Image.new('RGB', (carta_width_px, carta_height_px), (255, 255, 255))
            pdf.paste(Image.new('RGB', (pdf_width, pdf_height), (255, 255, 255)), (margin, margin))

            x_offset, y_offset = margin, margin

            for image, width_cm, height_cm in self.image_list:
                # Convertir tamaños de cm a píxeles
                target_size_px = (int(width_cm * 300 / 2.54), int(height_cm * 300 / 2.54))
                resized_image = image.resize(target_size_px)

                pdf.paste(resized_image, (x_offset, y_offset))
                x_offset += resized_image.size[0] + int(0.4 * 300 / 2.54)

                # Si la siguiente imagen no cabe en la misma fila, pasar a la siguiente fila
                if x_offset + resized_image.size[0] > pdf_width + margin:
                    x_offset = margin
                    y_offset += resized_image.size[1] + int(0.4 * 300 / 2.54)

            pdf.save(pdf_path)
            messagebox.showinfo("Éxito", f"PDF guardado en {pdf_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()