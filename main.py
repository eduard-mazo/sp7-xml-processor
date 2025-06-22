from excel_builder import construir_excel_desde_xml


def ejecutar_proceso():
    try:
        construir_excel_desde_xml()
        return True
    except Exception as e:
        print(f"[ERROR]: {e}")
        return False


if __name__ == "__main__":
    ejecutar_proceso()
