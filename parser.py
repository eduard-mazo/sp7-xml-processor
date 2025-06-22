import os
import xml.etree.ElementTree as ET
from config import config
from helpers import buscar_por_blocktype


class XMLParser:
    def __init__(self, index_blocktype=None):
        self.btdb = index_blocktype
        self.ifs_data = {}
        self.imm_data = []

    def parse_ifs(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        self.ifs_data = {
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
        return self.ifs_data

    def parse_imm(self, path, incluir_tags=None, excluir_tags=None, verbose=False):
        tree = ET.parse(path)
        root = tree.getroot()
        self.imm_data = []

        for parent in root.findall(".//Parent"):
            jerarquia = [{"Parent": {"Path": parent.attrib.get("Path", "")}}]
            walker = XMLWalker(btdb=self.btdb, incluir_tags=incluir_tags, excluir_tags=excluir_tags, verbose=verbose)
            walker.recorrer(parent, jerarquia, {"name": [], "tag": []})
            self.imm_data.extend(walker.resultados)

        return self.imm_data


class XMLWalker:
    def __init__(self, btdb, incluir_tags=None, excluir_tags=None, verbose=False):
        self.btdb = btdb
        self.resultados = []
        self.incluir_tags = incluir_tags or []
        self.excluir_tags = excluir_tags or []
        self.verbose = verbose

    def log(self, mensaje):
        if self.verbose:
            print(f"[XMLWalker] {mensaje}")

    def validar_nodo(self, nodo):
        obligatorio = ("ODBName", "Name", "aliasName", "ElementName", "Path")
        for attr in obligatorio:
            valor = nodo.attrib.get(attr)
            if attr == "Path":
                if valor is not None:  # Acepta incluso si es ""
                    return True
            elif valor and valor.strip():  # Solo acepta si no está vacío ni son espacios
                return True
        return False

    def recorrer(self, nodo, jerarquia=None, paths=None):
        try:
            tag = nodo.tag

            if tag in config.invalid_tags:
                self.log(f"🚫 Etiqueta inválida: {tag}")
                return

            if self.excluir_tags and tag in self.excluir_tags:
                self.log(f"⛔ Excluido por filtro: {tag}")
                return

            if self.incluir_tags and tag not in self.incluir_tags:
                self.log(f"🔍 No incluido por filtro: {tag}")
                return

            if not self.validar_nodo(nodo):
                self.log(f"⚠️ Nodo sin atributos requeridos: {tag}")
                return

            jerarquia = jerarquia or []
            paths = paths or {"name": [], "tag": []}

            nombre_visible = next((nodo.attrib.get(attr) for attr in ("ODBName", "Name", "aliasName", "ElementName", "Path") if nodo.attrib.get(attr)), None)

            if nombre_visible in config.invalid_elements:
                for hijo in nodo:
                    self.recorrer(hijo, jerarquia[:], paths.copy())
                return

            if nombre_visible:
                paths = {"name": paths["name"] + [nombre_visible.strip()], "tag": paths["tag"] + [tag]}

            nueva_jerarquia = jerarquia[:] + [{tag: dict(nodo.attrib)}]

            if len(nodo):  # Tiene hijos
                for hijo in nodo:
                    self.recorrer(hijo, nueva_jerarquia, paths)
            else:
                fila = extraer_datos_fila(nodo, nueva_jerarquia, self.btdb)
                fila["PointType"] = config.terminal_tag_map.get(tag, "")
                fila["Element"] = fila.get("Discrete_Name", fila.get("Analog_Name", ""))
                fila["FullPath"] = "/".join(paths["name"])
                fila["JERARQUIA"] = (
                    f"{fila.get('B1_tag')}-{fila.get('B1_name')}-{fila.get('B1')}:"
                    f"{fila.get('B2_tag')}-{fila.get('B2_name')}-{fila.get('B2')}:"
                    f"{fila.get('B3_tag')}-{fila.get('B3_name')}-{fila.get('B3')}"
                )
                self.resultados.append(fila)
                self.log(f"✔️ Nodo final procesado: {fila['FullPath']}")

        except Exception as e:
            self.log(f"❌ Error procesando nodo <{nodo.tag}>: {e}")


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
                if k in config.valid_attrs:
                    key = k if k not in fila else f"{tag}_{k}"
                    fila[key] = v

    for k, v in nodo.attrib.items():
        if k in config.valid_attrs:
            fila[k] = v

    for level in sorted(niveles):
        fila[f"{level.upper()}"] = niveles[level]["BlockType"]
        fila[f"{level.upper()}_tag"] = niveles[level]["Tag"]
        fila[f"{level.upper()}_name"] = niveles[level]["Name"]

    return fila
