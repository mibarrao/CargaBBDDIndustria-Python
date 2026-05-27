# -*- coding: utf-8 -*-
from operator import mul
import pandas as pd
from sqlalchemy import create_engine, text
import urllib
import pyodbc
import openpyxl
#import unicodedata
#import requests


# --- CONFIGURACION ---
# Asegurate de que la ruta sea accesible 
ruta_excel = r'C:\Users\mibarra\Downloads\Tasa de interés promedio otorgado por cada C.C.A.F. a sus afiliadas(os) pensionadas(os)__.xlsx'
#ruta_excel =  r'C:\Users\mibarra\Downloads\Montos en créditos de consumo otorgados por el sistema C.C.A.F. a afiliadas(os) pensionadas(os).xlsx'
servidor = r'LH-GESTIONDOS2'
base_datos = 'ESTUDIOSCOMERCIALES'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servidor};DATABASE={base_datos};Trusted_Connection=yes'

params_quoted = urllib.parse.quote_plus(conn_str)

# 2. Cadena codificada para SQLAlchemy
# params_quoted = urllib.parse.quote_plus(
#     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#     f'SERVER={servidor};'
#     f'DATABASE={base_datos};'
#     f'Trusted_Connection=yes'

# )
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params_quoted}', fast_executemany = True )


with engine.connect() as connection:
    print(f"Conexion exitosa")

conexion = pyodbc.connect(conn_str) 
conexion.timeout = 300 
cursor = conexion.cursor()


query_log_success = """
INSERT INTO dbo.Log_IDG 
(NOMBRE_SP, USUARIO, FECHA_EJECUCION
, ESTADO, FECHA_PROCESO, MENSAJE, CANTIDAD_REGISTROS)
VALUES 
(?, ORIGINAL_LOGIN(), GETDATE(), ?, CAST(GETDATE() AS DATE), ?, ?)
"""
# --- LECTURA FILAS | COLUMNAS ---

print("Inicio de carga..")
cursor.execute(query_log_success, ('BI_Tasas', 'PROCESADO', 'Inicio Carga Excel', '0'))
conexion.commit()

try:
    
    xls = pd.ExcelFile(ruta_excel) # CARGA EL ARCHIVO EXCEL PARA OBTENER INFORMACION DE LAS HOJAS
    nombreHoja = xls.sheet_names[0] # OBTIENE EL NOMBRE DE LA PRIMERA HOJA

    excel_file= pd.read_excel(ruta_excel,sheet_name=nombreHoja) #LEE ARCHIVO DE MANERA RAPIDA
    excel_file = excel_file.astype(str).replace(['nan', 'NaT', 'NaN', 'nat'], None) # CONVIERTE nombreHoja TODO A STRING PARA EVITAR PROBLEMAS DE TIPO DE DATO EN LA CARGA


    cantidadFilas = len(excel_file.index)
    cantidadColumnas = len (excel_file.columns)
    
    
    print(f"total de filas: {cantidadFilas} y son {cantidadColumnas} " )

    # --- PROCESO CARGA A BASE DE DATOS ---

    try:      

        print(f"\nProcesando carga ")

        nuevas_columnas = [f"F{i+1}" for i in range(len(excel_file.columns))]
        excel_file.columns = nuevas_columnas

        with engine.begin() as con:
            con.execute(text("DROP TABLE IF EXISTS TMP_TASA;"))
            

        excel_file.to_sql(
            name="TMP_TASA_PRUEBA"
            , con=engine
            , if_exists='replace'
            , index=False
            )
        
              
        print(f"carga exitosa.")
        cursor.execute(query_log_success, ('BI_Tasas', 'PROCESADO', 'Ejecución Correcta TMP_TASA', {cantidadFilas}))
        conexion.commit()

        # --- EJECUCION PROCEDURE ---

        # print(f"\nEjecutando procedimiento almacenado...")
        cursor.execute(query_log_success, ('BI_Tasas', 'PROCESANDO', 'Inicio exec Etl_BaseIndustria_TasaCredito', '0'))
        conexion.commit()

        spName = 'dbo.Etl_BaseIndustria_TasaCredito'
        with engine.begin() as con:

            con.execute(text(f"EXEC {spName}"))

        #     print(f"procedimiento almacenado ejecutado exitosamente.")
        cursor.execute(query_log_success, ('BI_Tasas', 'PROCESADO', 'Ejecución Correcta Etl_BaseIndustria_TasaCredito', {cantidadFilas}))
        conexion.commit()

        
    except Exception as e:
        print(f"Error al procesar la carga: {e}")
        cursor.execute(query_log_success, ('BI_Tasas', 'REVISAR', {e}, 0))
        conexion.commit()        


except Exception as e:
    print(f"Error critico al procesar: {e}")
    cursor.execute(query_log_success, ('BI_Tasas', 'REVISAR', {e}, 0))
    conexion.commit()
    
finally:
    print("\nProceso finalizado.")