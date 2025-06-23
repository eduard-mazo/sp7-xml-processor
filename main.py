from excel_builder import construir_excel_desde_xml
from ui_logger import ui_logger


def ejecutar_proceso():
    try:
        construir_excel_desde_xml()
        return True
    except Exception as e:
        ui_logger.log(f"[ERROR]: {e}")
        return False


if __name__ == "__main__":
    ejecutar_proceso()
