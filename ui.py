import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import json
from config import config
from main import ejecutar_proceso
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from tinydb import TinyDB
from ui_logger import ui_logger

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Procesador XML SP7")
        self.geometry("1000x650")

        self.imm_path = ctk.StringVar(value=str(config.imm_file_path))
        self.ifs_path = ctk.StringVar(value=str(config.ifs_file_path))

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self._crear_tab_selector()
        self._crear_tab_constantes()

        ui_logger.set_callback(self.log)  # Redirige los logs a esta GUI

    def _crear_tab_selector(self):
        tab = self.notebook.add("Selector de Archivos")

        frame_superior = ctk.CTkFrame(tab)
        frame_superior.pack(padx=10, pady=10, fill="x")

        # IMM
        ctk.CTkLabel(frame_superior, text="📁").grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_superior, text="Ruta IMM:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ctk.CTkEntry(frame_superior, textvariable=self.imm_path, width=600).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(frame_superior, text="...", width=30, command=self.select_imm).grid(row=0, column=3, padx=5)

        # IFS
        ctk.CTkLabel(frame_superior, text="📁").grid(row=1, column=0, padx=5)
        ctk.CTkLabel(frame_superior, text="Ruta IFS:").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ctk.CTkEntry(frame_superior, textvariable=self.ifs_path, width=600).grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkButton(frame_superior, text="...", width=30, command=self.select_ifs).grid(row=1, column=3, padx=5)

        # Procesar
        ctk.CTkButton(tab, text="Ejecutar Procesamiento", command=self.run_main, fg_color="green").pack(pady=10)

        # Log de eventos enriquecido
        log_frame = ctk.CTkFrame(tab)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, height=10, bg="#1a1a1a", fg="white", insertbackground="white")
        self.log_text.pack(fill="both", expand=True)
        self._configurar_tags_log()

    def _configurar_tags_log(self):
        self.log_text.tag_config("normal", foreground="white")
        self.log_text.tag_config("warning", foreground="yellow")
        self.log_text.tag_config("danger", foreground="red")

    def _crear_tab_constantes(self):
        tab = self.notebook.add("Constantes")

        self.btn_guardar = ctk.CTkButton(tab, text="Guardar Cambios (JSON crudo)", command=self.guardar_constantes)
        self.btn_guardar.pack(pady=10)

        self.constantes_viewer = ctk.CTkTextbox(tab)
        self.constantes_viewer.pack(expand=True, fill="both", padx=10, pady=10)

        self.mostrar_constantes()

    def log(self, mensaje, nivel="normal"):
        try:
            if "\n" not in mensaje:
                mensaje += "\n"
            self.log_text.insert("end", mensaje, nivel)
            self.log_text.see("end")
        except Exception as e:
            print(f"Log error: {e}")

    def select_imm(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if path:
            self.imm_path.set(path)
            self.log(f"IMM seleccionado: {path}", "normal")

    def select_ifs(self):
        path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if path:
            self.ifs_path.set(path)
            self.log(f"IFS seleccionado: {path}", "normal")

    def run_main(self):
        try:
            config.update(config.negocio, self.imm_path.get(), self.ifs_path.get())
            self.log("Procesamiento iniciado...", "normal")
            ok = ejecutar_proceso()
            if ok:
                self.log("✅ Procesamiento completado correctamente.", "normal")
            else:
                self.log("❌ Hubo un error durante el procesamiento.", "danger")
        except Exception as e:
            self.log(f"❌ Error: {e}", "danger")

    def mostrar_constantes(self):
        self.constantes_viewer.delete("1.0", "end")
        try:
            db = TinyDB("config_db.json")
            data = db.all()[0] if db.all() else {}
            pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
            self.constantes_viewer.insert("1.0", pretty_json)
        except Exception as e:
            self.constantes_viewer.insert("1.0", f"Error al cargar constantes: {e}")

    def guardar_constantes(self):
        try:
            texto = self.constantes_viewer.get("1.0", "end").strip()
            datos = json.loads(texto)
            db = TinyDB("config_db.json")
            db.truncate()
            db.insert(datos)
            self.log("✔️ Constantes guardadas correctamente.", "normal")
        except Exception as e:
            self.log(f"❌ Error al guardar constantes: {e}", "danger")


if __name__ == "__main__":
    app = App()
    app.mainloop()
