import re
from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, array, split, array_join, array_union, concat, to_date, explode
from pyspark.sql.types import StructType, StringType, ArrayType, DecimalType
import pandas as pd
import cloudbillingtool.helper as helper

hetzner_schema = StructType() \
  .add("Type",StringType(), True) \
  .add("Product",StringType(), True) \
  .add("Description",StringType(), True) \
  .add("StartDate",StringType(), True) \
  .add("EndDate",StringType(), True) \
  .add("Quantity",StringType(), True) \
  .add("UnitPrice", StringType(), True) \
  .add("Price", StringType(), True) \
  .add("HetznerCostResourceID", StringType(), True)


def load_files(spark, hetzner_data, work_folder ) -> rdd :
    resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    return\
        spark.read\
        .options(format='csv', escape="\"", header=False)\
        .schema(hetzner_schema)\
        .csv(hetzner_data)\
        .rdd\
        .map(lambda row: {
            "Type": row.Type,
            "Price": row.Price,
            "Product": row.Product,
            "Description": row.Description,
            "StartDate": row.StartDate,
            "EndDate": row.EndDate,
            "Quantity": row.Quantity,
            "UnitPrice": row.UnitPrice,
            "CostResourceID":  helper.extract_costresourceid(row.Description),
            "CostResourceTag": helper.merge_tags_from_dt(
                                    resource_mapping_df,
                                    type_mapping_df,
                                    helper.extract_costresourceid(row.Description),
                                    row.Type
                                )
        })


def load_files_with_mapping(spark, hetzner_data, mapping_files_path):
    hetzner_df: DataFrame = \
        load_files(spark, hetzner_data, mapping_files_path)\
        .toDF()\
        .alias("hetzner_df") \

    joined_with_tags = hetzner_df \
        .select(lit("hetzner").alias("provider"),
                col("hetzner_df.Type"),
                col("hetzner_df.Product").alias("ProductName"),
                col("hetzner_df.Price").cast("float").alias("Costs"),
                col("hetzner_df.UnitPrice").cast("float").alias("UnitPrice"),
                col("hetzner_df.Quantity").cast("float").alias("Quantity"),
                to_date(col("hetzner_df.StartDate"), "yyyy-MM-dd").alias("Date"),
                col("hetzner_df.CostResourceID").alias("CostResourceID"),
                explode("hetzner_df.CostResourceTag").alias("CostResourceTag"))

    return joined_with_tags
