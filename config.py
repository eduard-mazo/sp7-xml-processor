from datetime import datetime

# === Paths & Config ===
NEGOCIO_NAME = "GAS"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

XML_DIR = "resources/XML"
JSON_DIR = "resources/JSON"
OUTPUT_DIR = "resources/XLSX"
IMM_FILENAME = f"IMM_{NEGOCIO_NAME}.xml"
IFS_FILENAME = "IFS_COMPLETE.xml"
HIERARCHY_JSON = "hierarchy.json"
BLOCKTYPE_JSON = "block_types_all.json"
OUTPUT_FILENAME = f"MUI_{NEGOCIO_NAME}_{TIMESTAMP}.xlsx"

USE_SAFE_UPDATE = True
EXPORT_ALL = False

# === Columns to Export ===
COLUMNS_TO_EXPORT = [
    "AreaOfResponsibilityId", "FullPath", "JERARQUIA", "Name_ifs", "PointType",
    "ElementName", "Element", "ElementText", "ElementType",
    "B1_tag", "B1_name", "B1", "B2_tag", "B2_name", "B2", "B3_tag", "B3_name", "B3",
    "ConAddrDecimal", "MonAddrDecimal", "ConType", "MonType"
]

# === Tag and Attribute Rules ===
VALID_TAGS = {
    "GASstation", "GeographicalRegion", "PressureLevel", "GasTank", "Terminal",
    "Substation", "GasJunction", "ConnectivityNode", "GasValve", "GasCompressor",
    "GasEvacValve", "B1Block", "GasPipe", "BasePressure", "B2Block", "Bay",
    "Discrete", "DiscreteValue", "Analog", "AnalogValue", "B3Block", "Parent",
    "SubGeographicalRegion", "Link_ConductingEquipmentHasTPStatusMeasurement",
    "Breaker", "ControlCenterDataAccessRight", "VoltageLevel", "LineVoltageLevel",
    "PowerTransformer", "AnalogInfo", "AnalogLimit", "DiscreteInfo"
}

VALID_ATTRS = {
    "ElementName", "SignInvSE", "NoElType", "ElementText", "Name", "B2Number",
    "AreaOfResponsibilityId", "UnitOfMeasure", "ElementNameString",
    "BlockType", "B3Number", "MeasurementType", "ElementType"
}

INVALID_TAGS = {"Terminal"}
INVALID_ELEMENTS = {"Bl Spec", "Topo Sta", "MvNomina",
                    "MvLim01L", "MvLim01U", "MvLim02L", "MvLim02U"}

TERMINAL_TAG_MAP = {
    "DiscreteValue": "Status",
    "AnalogValue": "MvMoment",
    "DiscreteInfo": "AlStat",
    "AnalogInfo": "MvNomina",
    "AnalogLimit": "MvLim01L",  # Nota: solo una clave será efectiva
}
