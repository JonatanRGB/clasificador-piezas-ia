// Bucle de control (semana 8)
// Manda el peso cada 20 ms (50 Hz) y obedece las ordenes de Python con 3 LEDs:
//   A = ligero  (~14 g) -> LED ROJO
//   B = mediano (~40 g) -> LED AMARILLO
//   C = pesado  (~55 g) -> LED AZUL
//   0 = reposo -> todo apagado
#include "HX711.h"

const int DOUT_PIN = A1;
const int CLK_PIN = A0;
const int LED_ROJO = 5;       // ligero
const int LED_AMARILLO = 6;   // mediano
const int LED_AZUL = 7;       // pesado

const unsigned long PERIODO_MS = 20;   // una lectura cada 20 ms = 50 Hz (HX711 en modo 80 SPS)

HX711 balanza;
unsigned long ultimaLectura = 0;

void apagarTodo() {
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_AZUL, LOW);
}

void setup() {
  Serial.begin(115200);
  balanza.begin(DOUT_PIN, CLK_PIN);
  balanza.set_scale(106658.72);   // factor de calibracion de Sensor.ino
  balanza.tare(20);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_AZUL, OUTPUT);
  apagarTodo();
}

void loop() {
  if (millis() - ultimaLectura >= PERIODO_MS && balanza.is_ready()) {
    ultimaLectura = millis();
    Serial.println(balanza.get_units(1), 4);   // solo el numero, en kg
  }

  if (Serial.available() > 0) {
    char orden = Serial.read();
    switch (orden) {
      case 'A': apagarTodo(); digitalWrite(LED_ROJO, HIGH);     break;
      case 'B': apagarTodo(); digitalWrite(LED_AMARILLO, HIGH); break;
      case 'C': apagarTodo(); digitalWrite(LED_AZUL, HIGH);     break;
      case '0': apagarTodo(); break;
    }
  }
  delay(1);
}
