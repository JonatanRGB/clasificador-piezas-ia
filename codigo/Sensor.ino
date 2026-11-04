#include "HX711.h"

// Pines HX711 (Celda de carga)
const int DOUT_PIN = A1;
const int CLK_PIN = A0;

HX711 balanza;

// Variables para obligar al Arduino a enviar a 100 Hz
unsigned long tiempoAnterior = 0;
const unsigned long INTERVALO_MS = 10; // 10 milisegundos = 100 envíos por segundo
float ultimoPeso = 0.0;

void setup() {
  Serial.begin(115200); // Baudios altos para que la comunicación sea instantánea

  balanza.begin(DOUT_PIN, CLK_PIN);
  balanza.set_scale(106658.72); // Tu factor de escala original
  balanza.tare(20);
}

void loop() {
  // 1. Actualizar el peso solo cuando el chip físico tenga una nueva lectura
  // Al no haber "delay()", el Arduino pasa por aquí miles de veces por segundo sin trabarse.
  if (balanza.is_ready()) {
    ultimoPeso = balanza.get_units(1);
  }

  // 2. Disparar el dato a Python estrictamente cada 10 milisegundos
  unsigned long tiempoActual = millis();
  
  if (tiempoActual - tiempoAnterior >= INTERVALO_MS) {
    tiempoAnterior = tiempoActual; // Reiniciamos el cronómetro
    
    // Imprimimos el peso con 3 decimales seguido de una coma y un 0
    // El ",0" es para rellenar el lugar del sensor digital y que tu linea.split(',') 
    // en Python funcione perfectamente sin marcar error.
    Serial.print(ultimoPeso, 3);
    Serial.println(",0"); 
  }
}