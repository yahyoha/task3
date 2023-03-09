import pandas as pd
import csv
from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, to_date, explode
from . import helper


def load_files(spark, aws_data, work_folder ) -> rdd :
    resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    # Format AWS data to loosely match Hetzner / Azure data    
    with open(aws_data) as file:
        reader = csv.reader(file)
        data = list(reader)

    services = data[0]

    data.pop(0)
    data.pop(0)
    print(data[0][0])
    formatted_aws_data = []
    for row in data:
        date = row[0]
        for i, cell in enumerate(row):
            if i == 0:
                continue
            formatted_aws_data.append({
                'Date': date,
                'Product': services[i],
                'Costs': cell
            }
            )

    return\
        spark.read\
        .options(format='json', escape="\"", header=True)\
        .json(formatted_aws_data)\
        .withColumn("effectivePrice",col("effectivePrice").cast("decimal(12,8)")) \
        .withColumn("quantity", col("quantity").cast("decimal(12,8)"))\
        .withColumn("costInBillingCurrency", col("costInBillingCurrency").cast("decimal(12,8)"))\
        .withColumn("unitPrice", col("unitPrice").cast("decimal(12,8)")) \
        .rdd \
        .map(lambda row: {
            "Provider": "aws",
            "Type":  "",  # Missing 
            "Costs": row.Costs,
            "UnitPrice": "", # Missing
            "Quantity": "", # Missing
            "Product": row.Product,
            "Date": row.Date,
            "CostResourceID": "",
            "CostResourceTag": "",
            "ProductTag": ""
      })


def load_files_with_mapping(spark, aws_data, metadata_folder):
    hetzner_df: DataFrame = \
        load_files(spark, aws_data, metadata_folder+"/mappingfiles")\
        .toDF()\
        .alias("azure_df") \

    joined_with_tags = hetzner_df \
        .select(lit("azure").alias("Provider"),
                col("azure_df.Type"),
                col("azure_df.Product").alias("ProductName"),
                col("azure_df.Costs").cast("float").alias("Costs"),
                col("azure_df.UnitPrice").cast("float").alias("UnitPrice"),
                col("azure_df.Quantity").cast("float").alias("Quantity"),
                to_date(col("azure_df.Date"), "MM/dd/yyyy").alias("Date"),
                col("azure_df.CostResourceID").alias("CostResourceID"),
                col("azure_df.CostResourceTag").alias("CostResourceTag"),
                col("azure_df.ProductTag").alias("ProductTag"))

    return joined_with_tags
