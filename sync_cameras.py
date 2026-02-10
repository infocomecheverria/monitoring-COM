import pandas as pd
import json
import os

# CONFIGURACIÓN
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRBiQ_Z-lLUTmHFgrzKgDFRub2sAwiLfqNtyuDNq7pcYSFtU0kUwy94qOHOMdvSYfO8D6VnDcs_h0VC/pub?gid=1790267431&single=true&output=csv"
# Ruta interna del contenedor según tu docker-compose
OUTPUT_FILE = "/data/camaras.json" 

def sync():
    try:
        print("Descargando datos desde Google Sheets...")
        df = pd.read_csv(SHEET_CSV_URL, nrows=1668)
        
        # Limpiamos espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()
        print(f"Columnas detectadas en el CSV: {list(df.columns)}")

        # Buscamos las columnas de forma flexible por si cambian de nombre
        col_ip = [c for c in df.columns if 'IPS' in c.upper() or 'IP' in c.upper()][0]
        col_nombre = [c for c in df.columns if 'NOMBRE CON ID' in c.upper()][0]
        col_mikrotik = [c for c in df.columns if 'MIKROTIK' in c.upper()][0]

        print(f"Usando columna de IP: {col_ip}")

        targets_list = []
        for _, row in df.iterrows():
            ip = str(row[col_ip]).strip()
            
            # Filtro: Si la IP está vacía, es 'nan' o no tiene puntos, la saltamos
            if not ip or ip.lower() == 'nan' or '.' not in ip:
                continue

            nombre = str(row[col_nombre]).strip()
            mikrotik = str(row[col_mikrotik]).strip()

            targets_list.append({
                "targets": [ip],
                "labels": {
                    "nombre": nombre if nombre.lower() != 'nan' else f"Camara {ip}",
                    "mikrotik": mikrotik if mikrotik.lower() != 'nan' else "Sin Nodo",
                }
            })

        # Creamos la carpeta /data si no existe (dentro del contenedor)
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(targets_list, f, indent=4, ensure_ascii=False)
            
        print(f"¡Éxito! Se procesaron {len(targets_list)} cámaras correctamente.")

    except Exception as e:
        print(f"ERROR DURANTE LA EJECUCIÓN: {e}")

if __name__ == "__main__":
    sync()
