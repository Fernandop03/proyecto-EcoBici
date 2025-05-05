# api.py
from fastapi import FastAPI
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import uvicorn
import os
os.environ['HADOOP_HOME'] = "C:\\hadoop"  # Asegúrate de tener esto instalado
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'

app = FastAPI()
@app.on_event("startup")
def startup_event():
    global spark
    spark = SparkSession.builder \
        .appName("EcoBiciAPI") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "1g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
    
    global df
    df = spark.read.csv("viajes_individuales.csv", header=True, inferSchema=True)

@app.on_event("shutdown")
def shutdown_event():
    spark.stop()
# Iniciar sesión de Spark
spark = SparkSession.builder \
    .appName("EcoBiciAPI") \
    .getOrCreate()

# Cargar el dataset
df = spark.read.csv("viajes_individuales.csv", header=True, inferSchema=True)

@app.get("/")
def root():
    return {"message": "API de movilidad urbana con Spark"}

@app.get("/viajes-mas-largos")
def viajes_mas_largos():
    top_viajes = df.orderBy(col("mins_viaje").desc()).limit(10)
    results = top_viajes.toPandas().to_dict(orient="records")
    return results

