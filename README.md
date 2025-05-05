**Universidad Nacional Autónoma de México**

**Facultad de Estudios Superiores Acatlán**

**Licenciatura en Matemáticas Aplicadas y Computación**

**Programación Paralela y Concurrente**

Prof. José Gustavo Fuentes Cabrera

04/05/2025

**Alumno:** Ramírez Gómez Fernando Axel

**No. C.** 422066442

![image](https://github.com/user-attachments/assets/ec7c69d1-1d5a-4280-8eb0-5149a3cca6c0)


# Práctica Spark: Análisis de Movilidad Urbana con EcoBici en CDMX

Este repositorio contiene el código y los resultados del proyecto de la Práctica 2 de la materia Programación Paralela y Concurrente, enfocada en el análisis de datos de movilidad urbana en la Ciudad de México utilizando Apache Spark.

![image](https://github.com/user-attachments/assets/78c17592-80a4-434e-8236-46233e0d2c5b)

## Descripción del Proyecto

El objetivo principal de este proyecto es aplicar los conceptos fundamentales de Apache Spark (RDDs, DataFrames, transformaciones y acciones) para analizar un dataset real de viajes realizados en el sistema de bicicletas compartidas EcoBici de la Ciudad de México. El análisis busca identificar patrones de uso, entender la demanda horaria y evaluar el rendimiento de la flota de bicicletas para contribuir a una mejor gestión del sistema de movilidad urbana.

## Dataset

El dataset utilizado consiste en registros individuales de viajes de EcoBici. Las columnas clave incluyen:

* `anio`: Año del viaje.
* `mes`: Mes del viaje.
* `fecha_referencia`: Fecha específica del viaje.
* `bici`: Identificador único de la bicicleta.
* `mins_viaje`: Duración del viaje en minutos.
* `hrs_viaje`: Duración del viaje en horas.
* `dias_viaje`: Duración del viaje en días.
* `distancia_approx`: Distancia aproximada recorrida.

Los datos provienen del Portal de Datos Abiertos de la CDMX.

## Metodología

El proyecto se dividió en dos fases principales:

1.  **Análisis de Datos con PySpark (`ecobici_analysis.py`)**:
    * Carga y limpieza del dataset desde un archivo CSV (`viajes_individuales.csv`).
    * Transformaciones para extraer la hora del día, día de la semana e identificar fines de semana.
    * Análisis de patrones de uso mediante "rutas simuladas" basadas en duración y distancia.
    * Análisis de la demanda por rangos horarios.
    * Análisis de rendimiento y eficiencia de la flota de bicicletas.
    * Guardado de los resultados agregados en formato CSV.

2.  **Visualización de Resultados con Pandas y Matplotlib/Seaborn (`ecobici_visualization.py`)**:
    * Carga de los resultados agregados desde los archivos CSV generados por Spark.
    * Generación de gráficos de barras para visualizar los principales hallazgos (tipos de viaje más frecuentes, demanda horaria, bicicletas más eficientes).
    * Guardado de las visualizaciones en formato PNG.

## Análisis de Resultados y Valor de Negocio

El análisis de los resultados proporciona información valiosa para la gestión del sistema EcoBici:

* **Patrones de Uso por Tipo de Viaje**: Identificación de las combinaciones de duración y distancia más populares, ayudando a entender el comportamiento del usuario.
* **Demanda Horaria**: Identificación de los períodos del día con mayor y menor actividad, permitiendo optimizar la programación de rebalanceo, mantenimiento y personal.
* **Rendimiento de la Flota**: Identificación de las bicicletas con mayor uso o eficiencia, útil para priorizar mantenimiento preventivo e investigar unidades con bajo rendimiento.

Estos insights permiten tomar decisiones informadas para optimizar la operación y mejorar la experiencia del usuario.

## Reflexión sobre la Distribución y Eficiencia

La combinación de Spark para el procesamiento distribuido de grandes datasets (carga, limpieza, transformaciones a nivel de fila, agregaciones y guardado de resultados) y herramientas locales como Pandas y Matplotlib para la visualización de resultados agregados (más pequeños que el dataset original) demostró ser eficiente para este proyecto.

## Conclusión

Este proyecto demostró la efectividad de Apache Spark para el análisis de grandes volúmenes de datos de movilidad urbana, generando insights aplicables a la optimización operativa de un sistema de bicicletas compartidas. La metodología combinando Spark con herramientas de visualización locales se mostró eficiente.

## Uso Ético y Documentado de IA

Durante el desarrollo de esta práctica, se utilizó Gemini, un modelo de lenguaje grande, como herramienta auxiliar para comprender conceptos, depurar errores, explicar fragmentos de código y generar fragmentos de código, siempre de forma ética y documentada.

## Referencias

* Agencia Digital de Innovación Pública. (2023, 25 de mayo). Datos de bicicletas (Ecobici) \[Conjunto de datos]. Portal de Datos Abiertos de la CDMX.
* Google. (2025, 3 Mayo). Gemini \[Large language model].
