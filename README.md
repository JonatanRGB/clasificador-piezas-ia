# Clasificador de piezas - Material

Proyecto del curso Inteligencia Artificial.

- Alumno: Jonatan Rios Ramos
- Código: 219400751
- Dominio: Clasificación automática de piezas por peso utilizando una celda de carga con módulo de amplificación HX711 y un microcontrolador Arduino.

El proyecto recolecta mediciones de peso en masa de distintas piezas para categorizarlas en tres rangos de clasificación: **Bajo**, **Medio** y **Alto**.

## Descripción

sistema que lee señales mediante peso, las cuales clasifican las señales del sensor en tres diferentes de categorias, las cuales son Alto (para alto peso), mediano y bajo, y esto nos ayuda a poder calcular el peso del contenido de los elementos que deseamos pesar para la tabla.

## Semana 2

en la clase de la semana se empezo a trabajar el funcionamiento de los sensores seleccionados, en mi caso aplique el funcionamiento de una celda de carga la cual mediante la comunicación intermedia de arduino pude conectarme a la celda, la cual gracias a un modulo Hx711 lograria obtener esas señales y clasificarlas segun su peso, para posteriormente graficarlas.

## Semana 3
en la semana tres nos encargamos de observar como los datos que recopilamos la semana 2 nos seran utiles para poder emplearlos para crear la estructura de como es que estos iran a partir de ahora, es decir, de como los datos se iran generando progresivamente con las corridas.
Nota:se hizo la correcion de datos corruptos debido a un error de sobre escritura.

## Semana 4
En esta semana limpié los datos. Primero quité las lecturas que eran imposibles (por ejemplo 8 kg), que fueron 17. Después le apliqué a cada ventana un filtro de promedio de 3 muestras para quitar el ruido sin borrar el pico del golpe. También le resté a cada ventana su línea base para que todas empezaran en 0, y al final normalicé todo entre 0 y 1 con los mismos valores para todas las ventanas. Así no se pierde la diferencia de peso entre los materiales. Los datos limpios quedaron en `datos/datos_limpios.csv`.

## Semana 5
En esta semana saqué las características de cada ventana, o sea, unos cuantos números que resumen la señal en lugar de usar las 200 muestras. Me quedé con la media, la desviación, el máximo, el rango, la meseta (el peso cuando ya se estabilizó) y el sobrepaso (cuánto se pasa el golpe del peso final). Quité el mínimo, la energía y la duración porque salían casi iguales en los tres materiales. La que mejor separa es la meseta, porque es prácticamente el peso.