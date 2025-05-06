import boto3
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import json


def gerar_grafico():
    dados_x = []
    dados_y = []
    with open('dados.json') as f:
        for line in f:
            item = json.loads(line)
            if(item['valueType'] == 'Hz'):
                dados_x.append(item['EventProcessedUtcTime'])
                dados_y.append(item['value'])
    
    plt.plot(dados_x, dados_y, color='blue', linewidth=1)
    plt.title("Gráfico Harmônicas")
    plt.xlabel("Variação de Tempo")
    plt.ylabel("Valor (%)")
    plt.axhline(1, color='green', linestyle='-', linewidth=2, label='Estado Excelente')
    plt.axhline(5, color='yellow', linestyle='-', linewidth=2, label='Estado Normal')
    plt.axhline(100, color='red', linestyle='-', linewidth=2, label='Estado Terrível')
    plt.axhline((sum(dados_y)/len(dados_y)), color='purple', linestyle='-', linewidth=2, label='Média')
    plt.legend()
    plt.show()

spark = SparkSession.builder \
    .appName("Frequence Spark") \
    .master("local[*]") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "10g") \
    .config("spark.hadoop.hadoop.security.authentication", "simple") \
    .getOrCreate()

df = spark.read.csv("analytics/frequence.csv", header=True, inferSchema=True)

df.printSchema()

df.show()

df.show(1, vertical=True)

df.select("frequency").describe().show()
gerar_grafico()


# s3 = boto3.resource('s3')
# frequence_data = []

# for bucket in s3.buckets.all():
#     print(bucket.name)
#     responses = s3.list_objects_v2(Bucket=bucket.name)
#     for response in responses:
#         csv_data = spark.read.csv('datacamp_ecommerce.csv',header=True,escape="\"")
#         frequence_data.append(csv_data.all())
#         csv_data.show()


