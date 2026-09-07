import os
import time
import csv
import serial
import serial.tools.list_ports
import pandas as pd

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
BAUDIOS = 115200          # Debe coincidir con Serial.begin(115200) de Sensor.ino
N_MUESTRAS = 20           # Muestras por ventana (2 segundos a 100ms por muestra)
ARCHIVO = 'datos/datos.csv'

# Asegurar la existencia de la carpeta datos/
os.makedirs('datos', exist_ok=True)

# 1. Detección automática del puerto COM del Arduino
puertos = list(serial.tools.list_ports.comports())
if not puertos:
    raise RuntimeError("No se detectaron puertos COM/Serial disponibles. Verifica la conexión de tu Arduino.")
PUERTO = puertos[0].device
print(f"[+] Puerto COM detectado automáticamente: {PUERTO}")

# 2. Averiguar en qué número de ventana te quedaste la vez pasada
archivo_existe = os.path.exists(ARCHIVO) and os.path.getsize(ARCHIVO) > 0
ventana = 0

if archivo_existe:
    try:
        df = pd.read_csv(ARCHIVO)
        if 'ventana' in df.columns and not df.empty:
            ventana = int(df['ventana'].max()) + 1
            print(f"[+] Reanudando capturas desde la ventana número: {ventana}")
    except Exception as e:
        print(f"[!] No se pudo leer la última ventana de {ARCHIVO}: {e}")
        ventana = 0

# 3. Solicitar datos de la captura al usuario
etiqueta = input("Etiqueta de esta pieza (bajo, medio, alto): ").strip().lower()
n_ventanas = int(input("¿Cuántas ventanas vas a capturar?: "))

# 4. Conexión Serial con Arduino
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)  # El Arduino se reinicia al abrir el puerto

# 5. Apertura del archivo en modo 'a' (append) para no borrar lo capturado antes
archivo = open(ARCHIVO, 'a', newline='', encoding='utf-8')
escritor = csv.writer(archivo)

# Escribir la fila de encabezados si el archivo está vacío
if not archivo_existe:
    escritor.writerow(['ventana', 't', 'valor', 'etiqueta'])
    archivo.flush()

# 6. Bucle principal de adquisición
try:
    for i in range(n_ventanas):
        input(f"\nVentana {ventana} ({etiqueta}). Enter y pasa la pieza...")
        ser.reset_input_buffer()  # Tira lo que se acumuló mientras esperabas
        
        t = 0
        while t < N_MUESTRAS:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                try:
                    # Dado que Sensor.ino envía "peso,estadoSensor" (ej. "0.272,1"),
                    # tomamos el primer valor correspondiente al peso
                    partes = linea.split(',')
                    valor = float(partes[0])
                    
                    # Escribir la fila exacta: ventana, t, valor, etiqueta
                    escritor.writerow([ventana, t, valor, etiqueta])
                    archivo.flush()
                    
                    t += 1
                    print(f"  -> Muestra {t}/{N_MUESTRAS} | Valor: {valor:.3f} kg", end='\r')
                except ValueError:
                    # Ignorar encabezados o textos impresos por error
                    continue

        print(f"\n  ✓ {N_MUESTRAS} muestras guardadas en ventana {ventana}")
        ventana += 1

finally:
    archivo.close()
    ser.close()
    print(f"\nListo. Datos guardados en {ARCHIVO}")