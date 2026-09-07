import os
import re
import sys
import time
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt

# Detectar sistema operativo para lectura no bloqueante del teclado
if os.name == 'nt':
    import msvcrt
else:
    import select

## 1. CONFIGURACIÓN DE RUTAS Y CARPETAS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_CODIGO = os.path.join(BASE_DIR, 'codigo')
DIR_DATOS = os.path.join(BASE_DIR, 'datos')
DIR_FIGURAS = os.path.join(BASE_DIR, 'figuras')

for folder in [DIR_CODIGO, DIR_DATOS, DIR_FIGURAS]:
    os.makedirs(folder, exist_ok=True)


# 2. CONEXIÓN SERIAL CON ARDUINO

def conectar_arduino(puerto=None, baudrate=115200):
    """Detecta automáticamente el puerto de Arduino y conecta a 115200 baudios."""
    if puerto is None:
        puertos = list(serial.tools.list_ports.comports())
        if not puertos:
            raise RuntimeError("No se detectaron puertos COM/Serial disponibles. Verifica la conexión.")
        puerto = puertos[0].device
        print(f"[+] Puerto COM detectado automáticamente: {puerto}")
    
    return serial.Serial(puerto, baudrate, timeout=1)

# ==========================================
# 3. LÓGICA DE CLASIFICACIÓN Y AUTO-INCREMENTO
# ==========================================
def clasificar_peso(peso):
    """Clasifica el peso (kg) en las categorías requeridas."""
    if peso < 0.5:
        return "Bajo"
    elif 0.51 <= peso <= 1.0:
        return "Medio"
    elif peso >= 1.1:
        return "Alto"
    else:
        return "Transición (0.50 - 0.51 kg)"

def obtener_siguiente_nombre_figura(directorio):
    """Busca la secuencia existente de senalX.png en 'figuras/' e incrementa +1 el contador."""
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

def tecla_q_presionada():
    """Detecta la tecla 'Q' de forma no bloqueante en Windows y Linux/Mac."""
    if os.name == 'nt':
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode('utf-8', errors='ignore')
            return tecla.upper() == 'Q'
    else:
        if sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
            tecla = sys.stdin.readline().strip()
            return tecla.upper() == 'Q'
    return False

# ==========================================
# 4. BUCLE PRINCIPAL DE LECTURA Y GRAFICACIÓN
# ==========================================
def main():
    valores_peso = []
    estados_sensor = []
    categorias_conteo = {"Bajo": 0, "Medio": 0, "Alto": 0, "Otros": 0}
    
    try:
        arduino = conectar_arduino(baudrate=115200)
        print("\n=== CAPTURA DE DATOS DESDE ARDUINO (HX711 + SENSOR DIGITAL) ===")
        print("Presiona la tecla 'Q' y ENTER (o presiona Ctrl+C) para finalizar la captura.\n")
        
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    try:
                        # Separar los valores numéricos CSV: "PESO,ESTADO" (Ej: "0.245,1")
                        partes = linea.split(',')
                        if len(partes) == 2:
                            peso = float(partes[0])
                            estado_sensor = int(partes[1])
                            
                            cat = clasificar_peso(peso)
                            valores_peso.append(peso)
                            estados_sensor.append(estado_sensor)
                            
                            if cat in categorias_conteo:
                                categorias_conteo[cat] += 1
                            else:
                                categorias_conteo["Otros"] += 1
                                
                            print(f"Muestra #{len(valores_peso):03d} | Peso: {peso:.3f} kg | Sensor: {estado_sensor} | Cat: {cat}")
                    
                    except ValueError:
                        # Ignora líneas con datos corruptos o de inicio
                        pass

            if tecla_q_presionada():
                print("\n[!] Tecla 'Q' detectada. Deteniendo la captura...")
                break

    except KeyboardInterrupt:
        print("\n[!] Captura detenida manualmente (Ctrl + C).")
    except Exception as e:
        print(f"Error en la comunicación serial: {e}")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("[+] Puerto serial cerrado correctamente.")

    # Generación de reporte y gráfica
    if valores_peso:
        print(f"\nResumen de la corrida: Total lecturas = {len(valores_peso)}")
        print(f"  - Bajo (<0.5 kg):    {categorias_conteo['Bajo']}")
        print(f"  - Medio (0.51-1.0 kg): {categorias_conteo['Medio']}")
        print(f"  - Alto (>=1.1 kg):   {categorias_conteo['Alto']}")

        # Crear Gráfica con dos subplots (Peso y Estado del Sensor)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
        
        # Subplot 1: Peso
        ax1.plot(valores_peso, color='#2b5c8f', linewidth=1.8, marker='o', markersize=3, label='Peso Celda de Carga (kg)')
        ax1.axhline(y=0.5, color='#e74c3c', linestyle='--', linewidth=1.2, label='Umbral Bajo (<0.5 kg)')
        ax1.axhline(y=1.0, color='#f39c12', linestyle='--', linewidth=1.2, label='Umbral Medio (1.0 kg)')
        ax1.axhline(y=1.1, color='#2ecc71', linestyle='--', linewidth=1.2, label='Umbral Alto (>=1.1 kg)')
        ax1.set_title('Señal de Peso y Sensor Digital en Tiempo Real', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Peso Registrado (kg)', fontsize=10)
        ax1.grid(True, linestyle=':', alpha=0.6)
        ax1.legend(loc='upper right')

        # Subplot 2: Estado del Sensor Digital (0 o 1)
        ax2.step(range(len(estados_sensor)), estados_sensor, color='#8e44ad', where='post', linewidth=1.5, label='Estado Sensor Digital')
        ax2.set_xlabel('Número de Muestra', fontsize=10)
        ax2.set_ylabel('Estado (0/1)', fontsize=10)
        ax2.set_yticks([0, 1])
        ax2.grid(True, linestyle=':', alpha=0.6)
        ax2.legend(loc='upper right')

        plt.tight_layout()

        # Guardado autoincremental
        ruta_guardado = obtener_siguiente_nombre_figura(DIR_FIGURAS)
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
        print(f"\n[+] Gráfica guardada exitosamente en: {ruta_guardado}")
        
        plt.show()
    else:
        print("[!] No se recolectaron datos durante la corrida.")

if __name__ == '__main__':
    main()