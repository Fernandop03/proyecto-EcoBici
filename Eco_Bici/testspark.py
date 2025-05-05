from pyspark.sql import SparkSession
import os
os.environ['HADOOP_HOME'] = "C:\\hadoop"  # Asegúrate de tener esto instalado
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'

spark = SparkSession.builder \
    .appName("Test") \
    .getOrCreate()

df = spark.range(100)
df.show()