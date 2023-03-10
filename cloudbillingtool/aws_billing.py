import pandas as pd
import csv
from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, to_date, explode
from . import helper


# EXAMPLE
# INPUT
#"Service","EC2-Instances($)","EC2-Other($)","Tax($)","EC2-ELB($)","Support (Developer)($)","VPC($)","CloudWatch($)","Greengrass($)","S3($)","IoT($)","IoT Device Management($)","Lambda($)","Glue($)","Cognito($)","DynamoDB($)","SNS($)","Key Management Service($)","CloudShell($)","Service Catalog($)","Total costs($)"
#"Service total","1771.6043260751","1240.6996371889","757.57","346.9232428487","290","231.528","89.9016232584","9.54","6.2471532432","0.8051679","0.0045279","0.0000836146","0","0","0","0","0","0","0","4744.8237620289"
#"2022-03-01","3.4704","4.4454342454","53.33","","29","","0","0.36","0.0007563993","0.00251856","0.0000108","0.0000001891","0","0","0","0","","","","90.6091201938"

## OUTPUT
## Provider: AWS
## Type: EC2-Instances($)
## Costs:



def load_files(spark, aws_data, work_folder ) -> rdd :
    resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    return\
        spark.read\
        .options(format='csv', escape="\"", header=True) \
        .csv(aws_data) \
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

    # joined_with_tags = hetzner_df \
    #     .select(lit("azure").alias("Provider"),
    #             col("azure_df.Type"),
    #             col("azure_df.Product").alias("ProductName"),
    #             col("azure_df.Costs").cast("float").alias("Costs"),
    #             col("azure_df.UnitPrice").cast("float").alias("UnitPrice"),
    #             col("azure_df.Quantity").cast("float").alias("Quantity"),
    #             to_date(col("azure_df.Date"), "MM/dd/yyyy").alias("Date"),
    #             col("azure_df.CostResourceID").alias("CostResourceID"),
    #             col("azure_df.CostResourceTag").alias("CostResourceTag"),
    #             col("azure_df.ProductTag").alias("ProductTag"))
    #
    # return joined_with_tags
