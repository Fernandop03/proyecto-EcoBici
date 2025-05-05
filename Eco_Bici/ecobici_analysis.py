from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import datetime


# --- Configuración de Spark ---
spark = SparkSession.builder \
    .appName("Analisis EcoBici CMX Final") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.legacy.timeParsePolicy", "LEGACY") \
    .getOrCreate() # Corregido: .getOrCreate() en nueva línea sin '\'


# --- 1. Carga y limpieza de datos ---
def cargar_datos(ruta_csv):

    print("=== Cargando y procesando datos ===")
    try:
        # Cargar datos
        df = spark.read.csv(ruta_csv, header=True, inferSchema=True)

        # Validar columnas necesarias (añadido para robustez)
        columnas_necesarias = ["fecha_referencia", "bici", "mins_viaje", "distancia_approx"]
        for col_name in columnas_necesarias:
            if col_name not in df.columns:
                raise ValueError(f"Columna '{col_name}' no encontrada en el dataset.")

        # Limpieza avanzada con manejo de errores
        df = df.withColumn("fecha_hora",
                         to_timestamp(col("fecha_referencia"), "dd/MM/yyyy")) \
               .withColumn("hora", hour(col("fecha_hora"))) \
               .withColumn("dia_semana", date_format(col("fecha_hora"), "EEEE")) \
               .withColumn("es_fin_semana",
                         when(col("dia_semana").isin(["Saturday", "Sunday"]), True).otherwise(False))

        # Validación de datos
        print("\n=== Resumen de Calidad de Datos ===")
        print(f"Registros totales: {df.count():,}")
        for columna in df.columns:
            nulos = df.filter(col(columna).isNull()).count()
            print(f"Valores nulos en {columna}: {nulos} ({nulos/df.count():.2%})")

        return df
    except Exception as e:
        print(f"\nERROR en carga de datos: {str(e)}")
        return None


# --- 2. Análisis de datos con valor de negocio ---
def analizar_datos(df):

    if df is None:
        return None

    resultados = {}

    print("\n=== Realizando análisis de valor de negocio ===")

    try:

        print("1. Análisis de Patrones de Uso por Tipo de Viaje (Rutas Simuladas)...")
        df = df.withColumn("ruta_simulada",
                          concat(
                              lit("Duracion_~"),
                              (col("mins_viaje") / 60).cast("int"), # Duración aproximada en horas
                              lit("hrs_Dist_~"),
                              (col("distancia_approx") / 1000).cast("int"), # Distancia aproximada en km
                              lit("km")
                          ))

        resultados['rutas'] = df.groupBy("ruta_simulada") \
            .agg(count("*").alias("total_viajes"),
                 avg("mins_viaje").alias("tiempo_promedio"),
                 avg("distancia_approx").alias("distancia_promedio")) \
            .orderBy(col("total_viajes").desc())

        print("2. Análisis de Gestión de la Demanda por Horario...")
        df = df.withColumn("rango_hora",
                      when(col("hora").between(6, 9), "Mañana (6-9)")
                      .when(col("hora").between(10, 14), "Mediodía (10-14)")
                      .when(col("hora").between(15, 19), "Tarde (15-19)")
                      .otherwise("Noche (20-5)"))

        resultados['horas'] = df.groupBy("rango_hora") \
            .agg(count("*").alias("viajes"),
                 avg("mins_viaje").alias("duracion_promedio"),
                 sum("distancia_approx").alias("distancia_total")) \
            .orderBy("viajes", ascending=False)

        print("3. Análisis de Rendimiento y Eficiencia de la Flota...")
        resultados['eficiencia'] = df.groupBy("bici") \
            .agg(count("*").alias("viajes"),
                 sum("distancia_approx").alias("distancia_total"),
                 sum("mins_viaje").alias("minutos_totales")) \
            .withColumn("eficiencia_km_min",
                        when(col("minutos_totales") > 0, col("distancia_total")/col("minutos_totales"))
                        .otherwise(0)) \
            .orderBy(col("eficiencia_km_min").desc())

        return resultados
    except Exception as e:
        print(f"\nERROR durante el análisis: {str(e)}")
        return None


# --- 3. Guardado de resultados en CSV ---
def guardar_resultados(resultados):
    if resultados is None:
        print("\nNo hay resultados para guardar.")
        return

    print("\n=== Guardando resultados para Visualización ===")
    directorio_resultados = "resultados"
    os.makedirs(directorio_resultados, exist_ok=True)

    # Nombres esperados para las carpetas de salida de Spark
    nombres_salida_spark = {
        'rutas': 'rutas.csv', # Spark creará una carpeta llamada rutas.csv
        'horas': 'horas.csv', # Spark creará una carpeta llamada horas.csv
        'eficiencia': 'eficiencia.csv' # Spark creará una carpeta llamada eficiencia.csv
    }


    for nombre_clave, df in resultados.items():
         if nombre_clave in nombres_salida_spark:
            nombre_carpeta_spark = nombres_salida_spark[nombre_clave]
            ruta_carpeta_spark = os.path.join(directorio_resultados, nombre_carpeta_spark)
            print(f" - Intentando guardar '{nombre_clave}' como carpeta '{ruta_carpeta_spark}'")
            try:
                # Coalesce(1) para escribir en un solo archivo part- dentro de la carpeta
                df.coalesce(1).write.csv(ruta_carpeta_spark, header=True, mode="overwrite")
                print(f" - '{nombre_clave}' guardado correctamente como carpeta '{nombre_carpeta_spark}'.")
            except Exception as e:
                print(f"\nERROR al guardar '{nombre_clave}' en '{ruta_carpeta_spark}': {str(e)}")
                print("Esto puede deberse a problemas de permisos o configuraci\u00F3n de HADOOP_HOME/winutils en Windows.")
         else:
             print(f" - Nombre de clave '{nombre_clave}' no reconocido para guardar.")


# --- Función principal ---
def main():
    """
    Función principal que orquesta el proceso completo de análisis.
    """
    ruta_datos = "viajes_individuales.csv" # Asegúrate de que este sea el nombre correcto

    try:
        # Cargar datos
        df = cargar_datos(ruta_datos)

        # Mostrar información básica (si la carga fue exitosa)
        if df is not None:
            print("\n=== Muestra de datos procesados ===")
            columnas_a_mostrar = ["bici", "mins_viaje", "distancia_approx", "fecha_hora", "hora", "dia_semana"]
            columnas_existentes = [col_name for col_name in columnas_a_mostrar if col_name in df.columns]
            if columnas_existentes:
                df.select(*columnas_existentes).show(5)
            else:
                print("No hay columnas seleccionadas para mostrar.")

            print("\n=== Ideas de Valor de Negocio (Basadas en el Análisis) ===")
            print("- Con este análisis, un gerente puede:")
            print("  - Identificar las bicicletas m\u00E1s usadas y eficientes para optimizar mantenimiento y gesti\u00F3n de flota.")
            print("  - Entender los patrones de uso por horario para planificar operaciones y rebalanceo de bicicletas.")
            print("  - Tener una idea de los tipos de viajes m\u00E1s comunes (por duraci\u00F3n/distancia) para entender mejor a los usuarios.")
            print("  - Monitorear el rendimiento general del sistema.")


            # Realizar análisis
            resultados = analizar_datos(df)

            # Mostrar resúmenes (si el análisis fue exitoso)
            if resultados is not None:
                print("\n=== Resúmenes de análisis detallado ===") # Cambiado el título

                if 'rutas' in resultados and resultados['rutas'] is not None:
                     print("\nTop 5 Tipos de Viaje (Rutas Simuladas) más frecuentes:")
                     resultados['rutas'].show(5, truncate=False)

                if 'horas' in resultados and resultados['horas'] is not None:
                    print("\nUso de Bicicletas por Rango Horario:")
                    resultados['horas'].show(truncate=False)

                if 'eficiencia' in resultados and resultados['eficiencia'] is not None:
                    print("\nTop 5 Bicicletas más eficientes (km/min):")
                    resultados['eficiencia'].show(5, truncate=False)

                # Guardar resultados
                guardar_resultados(resultados)
            else:
                print("\nAnálisis fallido. No se generaron resultados.")

        else:
            print("\nCarga de datos fallida. No se pudo realizar el análisis.")

    except Exception as e:
        print(f"\nERROR inesperado durante la ejecución principal: {str(e)}")
    finally:
        # Detener la sesión de Spark al finalizar (incluso si hubo errores)
        if 'spark' in globals() and spark is not None:
            spark.stop()
            print("\n=== Sesión de Spark detenida ===")
        print("\n=== Proceso de análisis finalizado ===")


if __name__ == "__main__":
    main()