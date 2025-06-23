import os
import pandas as pd
from config import config
from parser import XMLParser
from helpers import cargar_base_datos_por_blocktype, safe_update_original, medir_tiempo
from ui_logger import logger


@medir_tiempo
def construir_excel_desde_xml():

    print(f"📥 Procesando: ")
    print(f"- IMM: {config.imm_file_path}")
    print(f"- IFS: {config.ifs_file_path}")

    index_blocktype = cargar_base_datos_por_blocktype(config.blocktype_json)
    parser = XMLParser(index_blocktype)

    imm_data = parser.parse_imm(config.imm_file_path)
    ifs_data = parser.parse_ifs(config.ifs_file_path)

    for row in imm_data:
        incoming = ifs_data.get(row.get("FullPath"), {"Name": "NO IFS-DATA", "ConAddrDecimal": None, "MonAddrDecimal": None, "ConType": None, "MonType": None})
        safe_update_original(row, incoming) if config.use_safe_update else row.update(incoming)

    df = pd.DataFrame(imm_data)
    columnas_filtradas = df.columns if config.export_all else [col for col in config.columns_to_export if col in df.columns]
    df = df[columnas_filtradas]

    os.makedirs(config.output_dir, exist_ok=True)
    df.to_excel(config.output_dir / config.output_filename, index=False)
    print(f"✅ Excel generado en: {config.output_dir / config.output_filename}")
