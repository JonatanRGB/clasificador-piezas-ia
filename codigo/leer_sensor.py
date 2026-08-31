import os
import re
import sys
import time
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS Y CARPETAS
# ==========================================
# Subir un nivel desde la carpeta 'codigo' para situarse en 'clasificador-piezas-ia'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_CODIGO = os.path.join(BASE_DIR, 'codigo')
DIR_DATOS = os.path.join(BASE_DIR, 'datos')
DIR_FIGURAS = os.path.join(BASE_DIR, 'figuras')

# Asegurar la existencia de las carpetas principales
for folder in [DIR_CODIGO, DIR_DATOS, DIR_FIGURAS]:
    os.makedirs(folder, exist_ok=True)

# ==========================================
# 2. CONEXIÓN SERIAL CON ARDUINO
# ==========================================
def conectar_arduino(puerto=None, baudrate=9600):
    """Detecta automáticamente el puerto de Arduino si no se especifica."""
    if puerto is None:
        puertos = list(serial.tools.list_ports.comports())
        if not puertos:
            raise RuntimeError("No se detectaron puertos COM/Serial disponibles. Verifica la conexión del Arduino.")
        puerto = puertos[0].device
        print(f"[+] Puerto COM detectado automáticamente: {puerto}")
    
    return serial.Serial(puerto, baudrate, timeout=1)

# ==========================================
# 3. LÓGICA DE CLASIFICACIÓN Y AUTO-INCREMENTO
# ==========================================
def clasificar_peso(peso):
    """
    Clasifica el peso recibido (en kg) según las 3 categorías requeridas:
    - Bajo:  < 0.5 kg
    - Medio: 0.51 - 1.0 kg
    - Alto:  >= 1.1 kg
    """
    if peso < 0.5:
        return "Bajo"
    elif 0.51 <= peso <= 1.0:
        return "Medio"
    elif peso >= 1.1:
        return "Alto"
    else:
        return "Transición (0.50 - 0.51 kg)"

def obtener_siguiente_nombre_figura(directorio):
    """
    Busca la secuencia existente de senalX.png en 'figuras/' y incrementa +1 el contador.
    """
    patron = re.compile(r"^senal(\d+)\.png$", re.IGNORECASE)
    max_num = 0
    
    if os.path.exists(directorio):
        for archivo in os.listdir(directorio):
            coincidencia = patron.match(archivo)
            if coincidencia:
                num = int(coincidencia.group(1))
                if num > max_num:
                    max_num = num
                    
    siguiente_num = max_num + 1
    return os.path.join(directorio, f"senal{siguiente_num}.png")

# ==========================================
# 4. BUCLE PRINCIPAL DE LECTURA Y GRAFICACIÓN
# ==========================================
def main():
    valores = []
    categorias_conteo = {"Bajo": 0, "Medio": 0, "Alto": 0, "Otros": 0}
    
    try:
        arduino = conectar_arduino()
        print("\n=== CAPTURA DE DATOS DESDE ARDUINO (HX711 / CELDA DE CARGA) ===")
        print("El Arduino iniciará la comunicación por el puerto serie.")
        print("Presiona la tecla 'Q' y ENTER en cualquier momento para finalizar la corrida.\n")
        
        # En sistemas Unix / Linux / Mac vs Windows:
        import select
        
        while True:
            # Leer datos de la celda de carga vía Arduino
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    try:
                        peso = float(linea)
                        cat = clasificar_peso(peso)
                        valores.append(peso)
                        
                        if cat in categorias_conteo:
                            categorias_conteo[cat] += 1
                        else:
                            categorias_conteo["Otros"] += 1
                            
                        print(f"Muestra #{len(valores):03d} | Peso: {peso:.3f} kg | Categoría: {cat}")
                    except ValueError:
                        # Para ignorar encabezados o textos impresos por la librería HX711 en Arduino
                        pass

            # Detectar tecla 'Q' para terminar
            if sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
                tecla = sys.stdin.readline().strip()
                if tecla.upper() == 'Q':
                    print("\n[!] Tecla 'Q' detectada. Deteniendo la captura...")
                    break

    except Exception as e:
        print(f"Error en la comunicación serial: {e}")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("[+] Puerto serial cerrado correctamente.")

    # Generación de reporte y gráfica si hay lecturas
    if valores:
        print(f"\nResumen de la corrida: Total lecturas = {len(valores)}")
        print(f"  - Bajo (<0.5 kg):    {categorias_conteo['Bajo']}")
        print(f"  - Medio (0.51-1.0 kg): {categorias_conteo['Medio']}")
        print(f"  - Alto (>=1.1 kg):   {categorias_conteo['Alto']}")

        # Crear Gráfica de la Señal
        plt.figure(figsize=(10, 5))
        plt.plot(valores, color='#2b5c8f', linewidth=1.8, marker='o', markersize=4, label='Lectura Celda de Carga (kg)')
        
        # Líneas de umbral de clasificación
        plt.axhline(y=0.5, color='#e74c3c', linestyle='--', linewidth=1.2, label='Umbral Bajo (<0.5 kg)')
        plt.axhline(y=1.0, color='#f39c12', linestyle='--', linewidth=1.2, label='Umbral Medio (1.0 kg)')
        plt.axhline(y=1.1, color='#2ecc71', linestyle='--', linewidth=1.2, label='Umbral Alto (>=1.1 kg)')
        
        plt.title('Señal de Peso en Tiempo Real - Celda de Carga HX711', fontsize=12, fontweight='bold')
        plt.xlabel('Número de Muestra / Tiempo', fontsize=10)
        plt.ylabel('Peso Registrado (kg)', fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper right')
        
        # Guardado autoincremental en carpeta figuras/
        ruta_guardado = obtener_siguiente_nombre_figura(DIR_FIGURAS)
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
        print(f"\n[+] Gráfica guardada exitosamente en: {ruta_guardado}")
        
        plt.show()
    else:
        print("[!] No se recolectaron datos durante la corrida.")

if __name__ == '__main__':
    main()