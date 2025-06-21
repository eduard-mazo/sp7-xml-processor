import os
import pandas as pd
from config import *
from parser import parse_imm_xml, parse_ifs_xml
from helpers import cargar_base_datos_por_blocktype, safe_update_original, medir_tiempo


@medir_tiempo
def construir_excel_desde_xml():
    imm_path = os.path.join(XML_DIR, IMM_FILENAME)
    ifs_path = os.path.join(XML_DIR, IFS_FILENAME)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    print(f"📥 Procesando:\n - IMM: {imm_path}\n - IFS: {ifs_path}")

    index_blocktype = cargar_base_datos_por_blocktype(
        os.path.join(JSON_DIR, BLOCKTYPE_JSON))
    imm_data = parse_imm_xml(imm_path, index_blocktype)
    ifs_data = parse_ifs_xml(ifs_path)

    for row in imm_data:
        incoming = ifs_data.get(
            row.get("FullPath"),
            {"Name": "NO IFS-DATA", "ConAddrDecimal": None,
                "MonAddrDecimal": None, "ConType": None, "MonType": None}
        )
        safe_update_original(
            row, incoming) if USE_SAFE_UPDATE else row.update(incoming)

    df = pd.DataFrame(imm_data)
    columnas_filtradas = df.columns if EXPORT_ALL else [
        col for col in COLUMNS_TO_EXPORT if col in df.columns]
    df = df[columnas_filtradas]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"✅ Excel generado en: {output_path}")
