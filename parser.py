import xml.etree.ElementTree as ET
import os
from config import VALID_TAGS, VALID_ATTRS, INVALID_TAGS, INVALID_ELEMENTS, TERMINAL_TAG_MAP
from helpers import buscar_por_blocktype


def recorrer_nodos(nodo, jerarquia, resultados, parent_path, btdb, full_path=None):
    tag = nodo.tag
    if tag in INVALID_TAGS:
        return

    full_path = full_path or []
    nombre_visible = next((nodo.attrib.get(attr) for attr in ("ODBName", "Name", "aliasName", "ElementName", "Path") if nodo.attrib.get(attr)), None)

    if nombre_visible in INVALID_ELEMENTS:
        for hijo in nodo:
            recorrer_nodos(hijo, jerarquia.copy(), resultados, parent_path, btdb, full_path.copy())
        return

    if nombre_visible:
        full_path = full_path.copy()
        full_path.append(nombre_visible.strip())

    ruta_actual = jerarquia.copy()
    ruta_actual.append({tag: dict(nodo.attrib)})

    if len(nodo):
        for hijo in nodo:
            recorrer_nodos(hijo, ruta_actual, resultados, parent_path, btdb, full_path)
    else:
        fila = extraer_datos_fila(nodo, jerarquia, btdb)
        fila["PointType"] = TERMINAL_TAG_MAP.get(tag, "")
        fila["Element"] = fila.get("Discrete_Name", fila.get("Analog_Name", ""))
        fila["FullPath"] = "/".join(full_path)
        fila["JERARQUIA"] = (
            f"{fila.get('B1_tag')}-{fila.get('B1_name')}-{fila.get('B1')}:{fila.get('B2_tag')}-{fila.get('B2_name')}-{fila.get('B2')}:{fila.get('B3_tag')}-{fila.get('B3_name')}-{fila.get('B3')}"
        )
        resultados.append(fila)


def extraer_datos_fila(nodo, jerarquia, dtdb):
    fila = {}
    niveles = {}

    for nivel in jerarquia:
        for tag, attrs in nivel.items():
            blocktype = attrs.get("BlockType")
            if blocktype:
                match = buscar_por_blocktype(blocktype, dtdb)
                if match:
                    level = match[0].get("group")
                    niveles.setdefault(level, {"BlockType": blocktype, "Tag": tag, "Name": attrs.get("Name")})
            for k, v in attrs.items():
                if k in VALID_ATTRS:
                    key = k if k not in fila else f"{tag}_{k}"
                    fila[key] = v

    for k, v in nodo.attrib.items():
        if k in VALID_ATTRS:
            fila[k] = v

    for level in sorted(niveles):
        fila[f"{level.upper()}"] = niveles[level]["BlockType"]
        fila[f"{level.upper()}_tag"] = niveles[level]["Tag"]
        fila[f"{level.upper()}_name"] = niveles[level]["Name"]

    return fila


def parse_imm_xml(path, index_blocktype):
    tree = ET.parse(path)
    root = tree.getroot()
    resultados = []

    for parent in root.findall(".//Parent"):
        jerarquia = [{"Parent": {"Path": parent.attrib.get("Path", "")}}]
        recorrer_nodos(parent, jerarquia, resultados, parent.attrib.get("Path", ""), index_blocktype)
    return resultados


def parse_ifs_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return {
        point.find("Link_IfsPointLinksToInfo").attrib.get("PathB", ""): {
            "ConAddrDecimal": point.attrib.get("ConAddrDecimal"),
            "MonAddrDecimal": point.attrib.get("MonAddrDecimal"),
            "ConType": point.attrib.get("ConType"),
            "MonType": point.attrib.get("MonType"),
            "Name": point.attrib.get("Name"),
        }
        for point in root.findall(".//IfsPoint")
        if point.find("Link_IfsPointLinksToInfo") is not None
    }
