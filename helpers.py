import json
from collections import defaultdict


def cargar_base_datos_por_blocktype(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    index = defaultdict(list)
    for group_name, blocks in data.items():
        for block in blocks:
            block_type = block.get("BlockType")
            if block_type:
                index[block_type].append({"group": group_name, **block})
    return index


def buscar_por_blocktype(blocktype_valor, index):
    return index.get(blocktype_valor, [])


def safe_update_original(base: dict, incoming: dict, suffix="_ifs"):
    for key, value in incoming.items():
        if key in base:
            new_key = f"{key}{suffix}"
            while new_key in base:
                new_key += "_1"
            base[new_key] = value
        else:
            base[key] = value


def medir_tiempo(func):
    import time

    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        print(f"⏱️ Tiempo de ejecución: {time.time() - inicio:.2f} segundos")
        return resultado
    return wrapper
