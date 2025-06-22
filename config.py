# config.py
from pathlib import Path
from datetime import datetime
from tinydb import TinyDB

CONFIG_DB_PATH = Path("config_db.json")


class AppConfig:
    def __init__(self):
        # Rutas base (no cambian)
        self.xml_dir = Path("resources/XML")
        self.json_dir = Path("resources/JSON")
        self.output_dir = Path("resources/XLSX")

        # Base de datos
        self.db = TinyDB(CONFIG_DB_PATH)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Carga dinámica del JSON
        self._load_config()

    def _load_config(self):
        if self.db:
            data = self.db.all()
            if data:
                config_dict = data[0]
                for key, value in config_dict.items():
                    # Convert sets back from lists
                    if key in {"valid_tags", "invalid_tags", "invalid_elements", "valid_attrs"} and isinstance(value, list):
                        value = set(value)
                    setattr(self, key, value)
            else:
                self._set_default_config()
                self._persist_config()
        else:
            self._set_default_config()

    def _set_default_config(self):
        # Valores por defecto mínimos
        self.negocio = "GAS"
        self.imm_filename = "IMM_GAS.xml"
        self.ifs_filename = "IFS_COMPLETE.xml"
        self.use_safe_update = True
        self.export_all = False

        self.columns_to_export = []

        self.valid_tags = {}

        self.invalid_tags = {}

        self.invalid_elements = {}

        self.valid_attrs = {}

        self.terminal_tag_map = {}

    def _persist_config(self):
        self.db.truncate()

        # Prepara datos serializables (convierte sets a listas)
        config_data = {}
        for key, value in self.__dict__.items():
            if key in {"db", "xml_dir", "json_dir", "output_dir"}:
                continue
            if isinstance(value, Path):
                config_data[key] = str(value)
            elif isinstance(value, set):
                config_data[key] = list(value)
            else:
                config_data[key] = value

        self.db.insert(config_data)

    def update(self, negocio, imm_path, ifs_path):
        self.negocio = negocio
        self.imm_filename = Path(imm_path).name
        self.ifs_filename = Path(ifs_path).name
        self.imm_file_path = Path(imm_path)
        self.ifs_file_path = Path(ifs_path)
        self.output_filename = f"MUI_{negocio}_{self.timestamp}.xlsx"
        self._persist_config()


config = AppConfig()
