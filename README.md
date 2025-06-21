# 🏗️ SCADA XML Processor & Excel Exporter

Este proyecto permite **procesar archivos XML jerárquicos SCADA** y generar automáticamente **informes en Excel** con rutas lógicas, atributos clave y estructuras jerárquicas. Se utiliza principalmente en entornos de **automatización industrial, redes de gas y eléctricas**, con soporte para múltiples niveles de elementos y estructuras personalizadas.

---

## ✨ Características

- 🧠 Procesamiento jerárquico de nodos XML (IMM).
- 🔗 Vinculación con puntos IFS (telemetría/telecontrol).
- 📁 Configuración flexible basada en JSON para jerarquía y tipos de bloques (`BlockType`).
- 🧾 Exportación a Excel filtrando solo columnas relevantes.
- ⚙️ Modularización clara: configuración, parsers, utilidades y generación de Excel.

---

## 🗂️ Estructura del Proyecto
```
.
├── config.py # Configuración general y constantes
├── excel_builder.py # Construcción del Excel final
├── helpers.py # Utilidades comunes
├── parser.py # Funciones para recorrer y procesar XML
├── main.py # Entrada principal del script
├── README.md
└── resources/
├── XML/ # Archivos IMM.xml e IFS_COMPLETE.xml
├── JSON/ # Archivos JSON de jerarquía y tipos de bloque
└── XLSX/ # Salida generada en Excel
```
---

## 🛠️ Requisitos

- Python 3.8 o superior
- Paquetes Python:

```bash
pip install pandas openpyxl
```
