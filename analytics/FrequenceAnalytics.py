import boto3
import pandas as pd
import pyspark
from pyspark.sql import SparkSession


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


# s3 = boto3.resource('s3')
# frequence_data = []

# for bucket in s3.buckets.all():
#     print(bucket.name)
#     responses = s3.list_objects_v2(Bucket=bucket.name)
#     for response in responses:
#         csv_data = spark.read.csv('datacamp_ecommerce.csv',header=True,escape="\"")
#         frequence_data.append(csv_data.all())
#         csv_data.show()


