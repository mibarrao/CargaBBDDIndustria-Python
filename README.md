# 📊 ETL Ingesta y Consolidación de Presupuesto / Budget Ingestion & Consolidation ETL

🇪🇸 **[ESPAÑOL]**

Este proyecto es un pipeline **ETL (Extracción, Transformación y Carga)** híbrido diseñado para centralizar presupuestos financieros y métricas operacionales distribuidas en múltiples archivos independientes de Excel (cada uno con una única hoja de datos). El sistema normaliza estructuras heterogéneas localmente mediante Python y, tras una ingesta manual guiada en SQL Server, consolida la información en una matriz relacional para análisis avanzado.

### 🚀 Arquitectura y Flujo de Datos
1. **Extracción (Python/Pandas):** Lectura dinámica de múltiples archivos de Excel de una sola hoja, procesando layouts complejos que contienen tablas apiladas o bloques contiguos con caracteres especiales (ej. `%`).
2. **Transformación:** Mapeo seguro de columnas por posición para evitar errores de índices, limpieza profunda de filas de totales/encabezados internos, estandarización de tipos de datos numéricos y exportación a un formato plano unificado (CSV) para mitigar restricciones corporativas de red o permisos directos sobre la base de datos.
3. **Carga (SQL Server):** Creación de tablas intermedias con llaves primarias autoincrementales (`ID IDENTITY`) e ingesta manual/guiada (vía Import Wizard o Bulk Load) de los archivos planos normalizados para asegurar la integridad y el orden de los registros en el entorno de destino.
4. **Consolidación (T-SQL):** Ejecución de un motor de reglas basado en **Cursores Dinámicos** y **Unpivot**. El proceso transforma meses de columnas a filas, calcula indicadores compuestos (Padre-Hijo) y segmenta automáticamente entre Pensionados (P) y Trabajadores (T).

### 🛠️ Tecnologías Utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Openpyxl](https://img.shields.io/badge/openpyxl-107C41?style=for-the-badge&logo=microsoft-excel&logoColor=white)

* **Lenguaje:** Python 3.12
* **Librerías:** `pandas`, `openpyxl`
* **Base de Datos:** SQL Server (Azure / On-premise)
* **Conceptos:** SQL Dinámico, Unpivot, Cursores, ETL híbrido de archivos planos independientes.

---

🇬🇧 **[ENGLISH]**

This project is a hybrid **ETL (Extract, Transform, Load)** pipeline designed to centralize financial budgets and operational metrics distributed across multiple independent Excel files (each containing a single sheet). The system normalizes heterogeneous data structures locally using Python and, following a guided manual ingestion into SQL Server, consolidates the information into a relational matrix for advanced analysis.

### 🚀 Architecture & Data Flow
1. **Extraction (Python/Pandas):** Dynamic reading of multiple single-sheet Excel files, handling complex layouts containing stacked tables or contiguous blocks with special characters (e.g., `%`).
2. **Transformation:** Secure column mapping by position to prevent index errors, deep cleaning of internal header/total rows, standardization of numeric data types, and local flat-file exportation (CSV) to bypass corporate network or database permission constraints.
3. **Loading (SQL Server):** Creation of intermediate staging tables with auto-incremental primary keys (`ID IDENTITY`) and manual/guided ingestion (via Import Wizard or Bulk Load) of normalized records to ensure data integrity and order.
4. **Consolidation (T-SQL):** Execution of a rules engine based on **Dynamic Cursors** and **Unpivot**. The process transforms months from columns to rows, calculates composite indicators (Parent-Child), and automatically segments between Pensioners (P) and Workers (T).

### 🛠️ Tech Stack & Tools

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Openpyxl](https://img.shields.io/badge/openpyxl-107C41?style=for-the-badge&logo=microsoft-excel&logoColor=white)

* **Language:** Python 3.12
* **Libraries:** `pandas`, `openpyxl`
* **Database:** SQL Server (Azure / On-premise)
* **Concepts:** Dynamic SQL, Unpivot, Cursors, Hybrid Flat-file ETL.

---

### 📂 Archivos del Proyecto / Project Files

* `BaseIndustrias_CantidadAfiliados.py`,`BaseIndustrias_MontosCreditosConsumo.py`,`BaseIndustrias_tasas.py`,`BaseIndustrias_TotalCreditosConsumo.py`: Script de Python para la lectura iterativa de archivos, limpieza posicional y consolidación local / *Python script for iterative file reading, positional cleansing, and local consolidation*.
* `Etl_BaseIndustria_CantidadAfiliado.sql`, `Etl_BaseIndustria_MontosCreditoConsumo`,`Etl_BaseIndustria_TasaCredito.sql`, `Etl_BaseIndustria_TotalCreditoConsumo`: Procedimiento almacenado de consolidación y unpivot ejecutado tras la ingesta manual / *Consolidation and unpivot stored procedure executed after manual ingestion*.
