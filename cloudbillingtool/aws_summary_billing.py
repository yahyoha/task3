import pandas as pd
import csv
from pyspark import rdd, Row
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


def transform_columns_to_rows(row):
    rows = []
    for idx, col_name in enumerate(row.__fields__):
        if idx == 0: # skip first column
            continue
        value = getattr(row, col_name)
        rows.append(Row(Product=col_name.rstrip("($)"), Costs=value, Date=row[0]))
    return rows


def load_files(spark, aws_data, work_folder ) -> rdd :

    #Not defined (required)
    #resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    #type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    return \
        spark.read\
        .options(format='csv', escape="\"", header=True,  inferSchema=True) \
        .csv(aws_data) \
        .alias("aws_df") \
        .rdd \
        .flatMap(transform_columns_to_rows) \
        .map(lambda row: {
            "Provider": "aws",
            "Type":  "",  # Missing
            "Costs": row.Costs if row.Costs is not None else 0.0,
            "UnitPrice": "", # Missing
            "Quantity": 1, # Missing
            "Product": row.Product,
            "Date": row.Date,
            "CostResourceID": "",
            "CostResourceTag": [""],
            "ProductTag": [""]
        }) \
        .filter(lambda row: row['Product'] != 'Total costs')

    # Mapping not yet defined

def load_files_with_mapping(spark, aws_data, metadata_folder):

    aws_df: DataFrame = \
        load_files(spark, aws_data, metadata_folder+"/mappingfiles")\
        .toDF()\
        .alias("aws_df") \

    aws_df_with_types = aws_df \
        .select(lit("aws").alias("Provider"),
                col("aws_df.Type"),
                col("aws_df.Product").alias("ProductName"),
                col("aws_df.Costs").cast("float").alias("Costs"),
                col("aws_df.UnitPrice").cast("float").alias("UnitPrice"),
                col("aws_df.Quantity").cast("float").alias("Quantity"),
                to_date(col("aws_df.Date"), "yyyy-MM-dd").alias("Date"),
                col("aws_df.CostResourceID").alias("CostResourceID"),
                col("aws_df.CostResourceTag").alias("CostResourceTag"),
                col("aws_df.ProductTag").alias("ProductTag"))

    return aws_df_with_types
