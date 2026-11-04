import os
import time
import csv
import serial
import serial.tools.list_ports
import pandas as pd

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
BAUDIOS = 115200          # Velocidad sincronizada con Arduino
N_MUESTRAS = 200          # <-- 200 muestras a 100Hz = 2 segundos exactos
ARCHIVO = 'datos/datos.csv'

# Asegurar la existencia de la carpeta 'datos'
os.makedirs('datos', exist_ok=True)

# 1. Detección automática del puerto COM
puertos = list(serial.tools.list_ports.comports())
if not puertos:
    raise RuntimeError("No se detectaron puertos COM. Verifica la conexión.")
PUERTO = puertos[0].device
print(f"[+] Puerto COM detectado: {PUERTO}")

# 2. Averiguar última ventana capturada
archivo_existe = os.path.exists(ARCHIVO) and os.path.getsize(ARCHIVO) > 0
ventana = 0

if archivo_existe:
    try:
        df = pd.read_csv(ARCHIVO)
        if 'ventana' in df.columns and not df.empty:
            ventana = int(df['ventana'].max()) + 1
            print(f"[+] Reanudando en ventana número: {ventana}")
    except Exception:
        ventana = 0

# 3. Solicitar datos de etiqueta y cantidad de ventanas
etiqueta = input("Etiqueta de esta pieza (ej. madera, metal, plastico): ").strip().lower()
n_ventanas = int(input("¿Cuántas ventanas vas a capturar?: "))

# 4. Conexión Serial
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2) # Espera a que Arduino se reinicie

archivo = open(ARCHIVO, 'a', newline='', encoding='utf-8')
escritor = csv.writer(archivo)

# Escribir encabezados si el archivo es nuevo
if not archivo_existe:
    escritor.writerow(['ventana', 't', 'valor', 'etiqueta'])
    archivo.flush()

# 5. Captura a máxima velocidad (Uso de RAM)
try:
    for i in range(n_ventanas):
        input(f"\nVentana {ventana} ({etiqueta}). Enter y pasa la pieza...")
        ser.reset_input_buffer()
        
        datos_en_ram = []  # Almacena temporalmente para no frenar la lectura
        t = 0
        
        tiempo_inicio = time.time()
        
        while t < N_MUESTRAS:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                try:
                    # Arduino envía el formato: "0.450,0"
                    partes = linea.split(',')
                    valor = float(partes[0]) 
                    
                    # Estructura estricta: ventana, t, valor, etiqueta
                    datos_en_ram.append([ventana, t, valor, etiqueta])
                    t += 1
                except ValueError:
                    continue

        tiempo_fin = time.time()
        
        # Guardado en disco de una sola vez
        escritor.writerows(datos_en_ram)
        archivo.flush()
        
        tiempo_total = tiempo_fin - tiempo_inicio
        print(f"  ✓ {N_MUESTRAS} muestras capturadas en {tiempo_total:.2f} segundos")
        
        ventana += 1

finally:
    archivo.close()
    ser.close()
    print(f"\nListo. Datos guardados en {ARCHIVO}")