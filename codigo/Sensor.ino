#include "HX711.h"

// Pines HX711 (Celda de carga)
const int DOUT_PIN = A1;
const int CLK_PIN = A0;

// Pin para el sensor digital
const int PIN_SENSOR_DIGITAL = 2; 

HX711 balanza;

void setup() {
  Serial.begin(115200);

  pinMode(PIN_SENSOR_DIGITAL, INPUT);

  balanza.begin(DOUT_PIN, CLK_PIN);
  balanza.set_scale(106658.72);
  balanza.tare(20);
}

void loop() {
  if (balanza.is_ready()) {
    float peso = balanza.get_units(1);
    int estadoSensor = digitalRead(PIN_SENSOR_DIGITAL);

    // Solo valores numéricos: "0.245,1"
    Serial.print(peso, 3);
    Serial.print(",");
    Serial.println(estadoSensor);
  }
}