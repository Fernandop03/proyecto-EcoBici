import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# --- Configuración estética profesional ---
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 12


def cargar_datos():
    """
    Carga los resultados de los análisis leyendo los archivos part-
    dentro de las carpetas creadas por Spark en 'resultados'.
    Espera encontrar carpetas llamadas 'rutas.csv', 'horas.csv', y 'eficiencia.csv'.
    """
    datos = {}
    directorio_resultados = "resultados"
    print(f"=== Cargando datos para visualización desde '{directorio_resultados}' ===")

    nombres_carpetas_spark = ['rutas.csv', 'horas.csv', 'eficiencia.csv']
    nombres_claves_datos = ['rutas', 'horas', 'eficiencia']

    for nombre_carpeta_spark, nombre_clave in zip(nombres_carpetas_spark, nombres_claves_datos):
        ruta_carpeta_spark = os.path.join(directorio_resultados, nombre_carpeta_spark)
        print(f" - Buscando datos para '{nombre_clave}' en la carpeta '{ruta_carpeta_spark}'")

        if os.path.isdir(ruta_carpeta_spark):
            archivos_part = glob.glob(os.path.join(ruta_carpeta_spark, 'part-*.csv'))

            if archivos_part:
                print(f" - Encontrados {len(archivos_part)} archivo(s) 'part-' para '{nombre_clave}'. Leyendo...")
                try:
                    lista_dfs_part = [pd.read_csv(archivo_part) for archivo_part in archivos_part]
                    datos[nombre_clave] = pd.concat(lista_dfs_part, ignore_index=True)
                    print(f" - Datos para '{nombre_clave}' cargados correctamente.")

                except Exception as e:
                    print(f"ERROR al leer archivo(s) 'part-' para '{nombre_clave}': {str(e)}")
                    datos[nombre_clave] = pd.DataFrame()
            else:
                print(f" - No se encontraron archivos 'part-' dentro de '{ruta_carpeta_spark}'. Datos no disponibles.")
                datos[nombre_clave] = pd.DataFrame()
        else:
            print(f" - Carpeta de resultados '{ruta_carpeta_spark}' no encontrada para '{nombre_clave}'. Datos no disponibles.")
            datos[nombre_clave] = pd.DataFrame()

    print("=== Carga de datos completada ===")
    return datos

def generar_visualizaciones(datos):
    """
    Genera visualizaciones a partir de los datos de análisis cargados,
    vinculándolas al valor de negocio.
    """
    directorio_visualizaciones = "visualizaciones"
    os.makedirs(directorio_visualizaciones, exist_ok=True)
    print(f"\n=== Generando visualizaciones de valor de negocio en '{directorio_visualizaciones}' ===")

    # --- 1. Gráfico de Top N Tipos de Viaje (Rutas Simuladas) ---
    # Valor de Negocio: Muestra los perfiles de viaje (duración/distancia) más comunes,
    # ayudando a entender qué tipo de desplazamientos dominan el uso del servicio.
    if 'rutas' in datos and not datos['rutas'].empty and 'ruta_simulada' in datos['rutas'].columns and 'total_viajes' in datos['rutas'].columns:
        plt.figure()
        top_n = 15
        rutas_top = datos['rutas'].head(top_n).sort_values('total_viajes', ascending=True).reset_index(drop=True)

        ax = sns.barplot(x='total_viajes', y='ruta_simulada', data=rutas_top, palette='viridis')

        for index, row in rutas_top.iterrows():
            ax.text(row['total_viajes'], index, f" {row['total_viajes']:,}", color='black', va='center')

        plt.title(f'Impacto en el Negocio: Top {top_n} Tipos de Viaje Más Frecuentes', pad=20) # Título con valor de negocio
        plt.xlabel('Número Total de Viajes')
        plt.ylabel('Tipo de Viaje (Duración ~Hrs / Distancia ~Km)') # Etiqueta más descriptiva
        plt.tight_layout()
        ruta_salida = os.path.join(directorio_visualizaciones, 'impacto_tipos_viaje.png') # Nombre de archivo descriptivo
        plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        plt.close()
        print(f" - '{os.path.basename(ruta_salida)}' generado (Impacto en tipos de viaje)")

    else:
        print(" - Datos de rutas (tipos de viaje) no disponibles o incompletos. Omitiendo visualización.")


    # --- 2. Gráfico de Uso por Rango Horario ---
    # Valor de Negocio: Visualiza la demanda a lo largo del día, esencial para la planificación
    # de recursos, rebalanceo y operaciones diarias.
    if 'horas' in datos and not datos['horas'].empty and 'rango_hora' in datos['horas'].columns and 'viajes' in datos['horas'].columns:
        plt.figure()
        orden_horas = ["Noche (20-5)", "Mañana (6-9)", "Mediodía (10-14)", "Tarde (15-19)"]
        datos['horas']['rango_hora'] = pd.Categorical(datos['horas']['rango_hora'], categories=orden_horas, ordered=True)
        datos_horas_ordenado = datos['horas'].sort_values('rango_hora').reset_index(drop=True)

        ax = sns.barplot(x='rango_hora', y='viajes', data=datos_horas_ordenado, palette='viridis')

        for index, row in datos_horas_ordenado.iterrows():
             ax.text(index, row['viajes'], f" {row['viajes']:,}", ha='center', va='bottom')

        plt.title('Impacto en el Negocio: Demanda de Viajes por Rango Horario', pad=20) # Título con valor de negocio
        plt.xlabel('Rango Horario del Día')
        plt.ylabel('Número Total de Viajes')
        plt.tight_layout()
        ruta_salida = os.path.join(directorio_visualizaciones, 'impacto_demanda_horaria.png') # Nombre de archivo descriptivo
        plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        plt.close()
        print(f" - '{os.path.basename(ruta_salida)}' generado (Impacto en demanda horaria)")
    else:
         print(" - Datos de horarios no disponibles o incompletos. Omitiendo visualización de horario.")


    # --- 3. Gráfico de Top N Bicicletas Más Eficientes ---
    # Valor de Negocio: Ayuda a identificar las bicicletas con mejor/peor rendimiento
    # para optimizar el mantenimiento y la gestión de la flota.
    if 'eficiencia' in datos and not datos['eficiencia'].empty and 'bici' in datos['eficiencia'].columns and 'eficiencia_km_min' in datos['eficiencia'].columns:
        plt.figure()
        top_n = 15
        eficiencia_top = datos['eficiencia'].sort_values('eficiencia_km_min', ascending=False).head(top_n).reset_index(drop=True)

        ax = sns.barplot(x='eficiencia_km_min', y='bici', data=eficiencia_top, palette='viridis')

        for index, row in eficiencia_top.iterrows():
             ax.text(row['eficiencia_km_min'], index, f" {row['eficiencia_km_min']:.2f}", color='black', va='center')


        plt.title(f'Impacto en el Negocio: Top {top_n} Bicicletas Más Eficientes (km/min)', pad=20) # Título con valor de negocio
        plt.xlabel('Eficiencia (km por minuto)')
        plt.ylabel('ID de Bicicleta')
        plt.tight_layout()
        ruta_salida = os.path.join(directorio_visualizaciones, 'impacto_eficiencia_bicis.png') # Nombre de archivo descriptivo
        plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        plt.close()
        print(f" - '{os.path.basename(ruta_salida)}' generado (Impacto en eficiencia de bicis)")
    else:
        print(" - Datos de eficiencia no disponibles o incompletos. Omitiendo visualización de eficiencia.")

    print("\n=== Generación de visualizaciones completada ===")


def main():
    """
    Función principal que orquesta el proceso completo de visualización.
    """
    os.makedirs("resultados", exist_ok=True)
    os.makedirs("visualizaciones", exist_ok=True)

    datos = cargar_datos()

    generar_visualizaciones(datos)

if __name__ == "__main__":
    main()