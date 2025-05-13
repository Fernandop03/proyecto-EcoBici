# Práctica Spark: Análisis de Movilidad Urbana con EcoBici en CDM
**Universidad Nacional Autónoma de México**

**Facultad de Estudios Superiores Acatlán**

**Licenciatura en Matemáticas Aplicadas y Computación**

**Programación Paralela y Concurrente**

Prof. José Gustavo Fuentes Cabrera

04/05/2025

**Alumno:** Ramírez Gómez Fernando Axel

**No. C.** 422066442

![image](https://github.com/user-attachments/assets/ec7c69d1-1d5a-4280-8eb0-5149a3cca6c0)


# Descripción general

Este repositorio contiene el código y los resultados del proyecto de la Práctica 2 de la materia Programación Paralela y Concurrente, enfocada en el análisis de datos de movilidad urbana en la Ciudad de México utilizando Apache Spark.

![image](https://github.com/user-attachments/assets/78c17592-80a4-434e-8236-46233e0d2c5b)

## 🎯 Objetivo

Aplicar los conceptos de programación distribuida con Apache Spark (RDDs, DataFrames, transformaciones y acciones) para extraer información significativa de un dataset real, mejorando la eficiencia del análisis de datos a gran escala y facilitando la visualización de patrones clave.

## 🧠 Introducción

El sistema EcoBici ofrece una oportunidad única para estudiar el comportamiento de la movilidad urbana. En este proyecto se analiza un conjunto de datos con miles de registros de viajes, aplicando técnicas de procesamiento distribuido con Spark y visualización local con Pandas y Matplotlib.

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


## 📁 Estructura del Proyecto

```graphql
Eco_Bici/                                # Directorio raíz del proyecto
│
├── Eco_Bici/                            # Carpeta principal con el código fuente
│   ├── api.py                           # Funciones de conexión o simulación de API de Ecobici
│   ├── data-2025-04-18.csv              # Conjunto de datos principal para el análisis
│   ├── ecobici_analysis.py              # Módulo de análisis estadístico y procesamiento de datos
│   ├── ecobici_visualization.py         # Módulo para generar gráficas y visualizaciones
│   ├── resultados_bicis_mas_usadas.csv  # Resultados del análisis de uso por bicicleta
│   ├── resultados_categorias_duracion.csv  # Clasificación por duración de los viajes
│   ├── resultados_uso_diario.csv        # Uso agregado por día
│   ├── resultados_uso_mensual.csv       # Uso agregado por mes
│   ├── testspark.py                     # Prueba de integración con PySpark
│   ├── viajes_individuales.csv          # Detalle de viajes individuales para análisis granular
│
│   ├── resultados/                      # Resultados procesados automáticamente (formato Spark)
│   │   ├── eficiencia.csv/              # Datos de eficiencia por bicicleta
│   │   ├── horas.csv/                   # Frecuencia de viajes por hora
│   │   ├── rutas.csv/                   # Información sobre las rutas más frecuentes
│
│   ├── visualizaciones/                 # Visualizaciones generadas automáticamente
│   │   ├── impacto_demanda_horaria.png
│   │   ├── impacto_eficiencia_bicis.png
│   │   ├── impacto_tipos_viaje.png
```

## ⚙️ ¿Cómo se ejecuta?

1.  Instala las dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

2.  Ejecuta el análisis con Spark:

    ```bash
    python ecobici_analysis.py
    ```

3.  Genera las visualizaciones:

    ```bash
    python ecobici_visualization.py
    ```

## 📊 Metodología Aplicada

### 🔹 Análisis de Datos (Spark)
* Limpieza de datos desde `viajes_individuales.csv`.
* Transformaciones y generación de variables como hora, día, tipo de viaje.
* Agregaciones por duración, eficiencia, demanda por hora y rendimiento de bicicletas.

### 🔹 Visualización (Pandas + Matplotlib/Seaborn)
* Carga de resultados agregados.
* Generación de gráficos:
    * Demanda horaria.
    * Bicicletas más utilizadas.
    * Rutas más frecuentes.

## 📈 Principales Hallazgos

* **Patrones de uso:** Los viajes más comunes son breves y frecuentes en horarios laborales.
* **Demanda por hora:** La mayor actividad se registra entre las 8-9 am y 6-7 pm.
* **Rendimiento de flota:** Se identificaron bicicletas con alta y baja eficiencia para mantenimiento o sustitución.

## 🧠 Relación con los Paradigmas de Programación

* **Distribución:** Apache Spark permite dividir el procesamiento del dataset en tareas paralelas.
* **Transformación Funcional:** Uso de operaciones inmutables en RDDs y DataFrames.
* **Visualización Secuencial:** Herramientas como Pandas y Matplotlib se usan eficientemente en etapas posteriores del pipeline.

## Análisis de Resultados y Valor de Negocio

El análisis de los resultados proporciona información valiosa para la gestión del sistema EcoBici:

* **Patrones de Uso por Tipo de Viaje**: Identificación de las combinaciones de duración y distancia más populares, ayudando a entender el comportamiento del usuario.
* **Demanda Horaria**: Identificación de los períodos del día con mayor y menor actividad, permitiendo optimizar la programación de rebalanceo, mantenimiento y personal.
* **Rendimiento de la Flota**: Identificación de las bicicletas con mayor uso o eficiencia, útil para priorizar mantenimiento preventivo e investigar unidades con bajo rendimiento.

Estos insights permiten tomar decisiones informadas para optimizar la operación y mejorar la experiencia del usuario.


## ✅ Conclusión

Este proyecto demostró la eficacia de usar Apache Spark como motor de análisis distribuido para grandes volúmenes de datos reales. La combinación con herramientas de visualización locales brinda una solución escalable, interpretativa y eficiente para resolver problemas urbanos.

## 🤖 Uso Ético de Herramientas de IA

Durante el desarrollo del proyecto se utilizaron herramientas de IA (Gemini, ChatGPT) de forma ética y documentada para:

* Comprender conceptos de Spark.
* Optimizar código.
* Redactar documentación técnica.

## 📚 Referencias

* Agencia Digital de Innovación Pública. (2023). Datos de bicicletas (Ecobici). Portal de Datos Abiertos CDMX.
* Google. (2025). Gemini [Modelo de lenguaje grande].

Se uso para:
- Estructuración y revisión técnica del código.
- Mejora de redacción en la documentación.
- Generación de ideas para el diseño del sistema.
