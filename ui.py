import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from config import config

# Crear directorios si no existen
for directory in [config.xml_dir, config.json_dir, config.output_dir]:
    directory.mkdir(parents=True, exist_ok=True)


def actualizar_config(imm_path, ifs_path, negocio):
    config.update(negocio, imm_path, ifs_path)


class XMLSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SP7 Selector de Archivos")
        self.root.geometry("750x400")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Pestaña de selección
        self.frame_selector = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_selector, text="Seleccionar Archivos")

        self.imm_path = tk.StringVar()
        self.ifs_path = tk.StringVar()
        self.negocio_name = tk.StringVar()

        ttk.Label(self.frame_selector, text="Archivo IMM:").pack(pady=5)
        ttk.Entry(self.frame_selector, textvariable=self.imm_path, width=90).pack()
        ttk.Button(self.frame_selector, text="Seleccionar IMM", command=self.select_imm).pack(pady=5)

        ttk.Label(self.frame_selector, text="Archivo IFS:").pack(pady=5)
        ttk.Entry(self.frame_selector, textvariable=self.ifs_path, width=90).pack()
        ttk.Button(self.frame_selector, text="Seleccionar IFS", command=self.select_ifs).pack(pady=5)

        ttk.Button(self.frame_selector, text="Confirmar y continuar", command=self.confirm_selection).pack(pady=20)

        # Pestaña de constantes
        self.frame_constantes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_constantes, text="Constantes")

        self.constantes_text = tk.Text(self.frame_constantes, wrap="word")
        self.constantes_text.pack(fill="both", expand=True)
        self.mostrar_constantes()

    def select_imm(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")], title="Selecciona el archivo IMM")
        if path:
            self.imm_path.set(path)
            self.extract_negocio_name(path)

    def select_ifs(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")], title="Selecciona el archivo IFS")
        if path:
            self.ifs_path.set(path)

    def extract_negocio_name(self, filepath):
        filename = Path(filepath).name
        if filename.startswith("IMM_") and filename.endswith(".xml"):
            self.negocio_name.set(filename[4:-4])

    def confirm_selection(self):
        imm = self.imm_path.get()
        ifs = self.ifs_path.get()
        negocio = self.negocio_name.get()

        if not imm or not ifs:
            messagebox.showerror("Error", "Debes seleccionar ambos archivos.")
            return

        actualizar_config(imm, ifs, negocio)

        print("Archivo IMM:", imm)
        print("Archivo IFS:", ifs)
        print("Negocio:", negocio)

        from main import ejecutar_proceso

        messagebox.showinfo("Listo", "Archivos seleccionados correctamente. Ejecutando procesamiento...")

        resultado = ejecutar_proceso()

        if resultado:
            messagebox.showinfo("Éxito", "Procesamiento completado correctamente.")
        else:
            messagebox.showerror("Fallo", "Hubo un error durante el procesamiento. Consulta la consola para más detalles.")

    def mostrar_constantes(self):
        self.constantes_text.delete("1.0", tk.END)
        atributos = [
            ("valid_tags", config.valid_tags),
            ("invalid_tags", config.invalid_tags),
            ("valid_attrs", config.valid_attrs),
            ("invalid_elements", config.invalid_elements),
            ("terminal_tag_map", config.terminal_tag_map),
            ("columns_to_export", config.columns_to_export),
            ("imm_filename", config.imm_filename),
            ("ifs_filename", config.ifs_filename),
        ]
        for nombre, valor in atributos:
            if isinstance(valor, dict) or isinstance(valor, set) or isinstance(valor, list):
                self.constantes_text.insert(tk.END, f"{nombre}: {len(valor)} elementos\n")
            else:
                self.constantes_text.insert(tk.END, f"{nombre}: {valor}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = XMLSelectorApp(root)
    root.mainloop()
