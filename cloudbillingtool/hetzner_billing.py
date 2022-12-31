import re
import csv
from datetime import datetime

from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType
import cloudbillingtool.mapping_file as mapping_file

hetzner_schema = StructType() \
  .add("Type",StringType(),True) \
  .add("Product",StringType(),True) \
  .add("Description",StringType(),True) \
  .add("StartDate",StringType(),True) \
  .add("EndDate",StringType(),True) \
  .add("Quantity",StringType(),True) \
  .add("UnitPrice", StringType(), True) \
  .add("Price", StringType(), True) \
  .add("HetznerCostResourceID", StringType(), True)


def extract_tag(desc):
    return re.search(r'#[0-9]+', desc).group() if re.search(r'#[0-9]+', desc) else None


def fix_date_format_for_hetzner(billing_date_hetzner):
    if not billing_date_hetzner:
        return ""
    month, day, year = billing_date_hetzner.split('-')
    return f"{month}/{day}/{year}"


def load_files(spark, files_location) -> rdd :
    return\
        spark.read\
        .options(format='csv', escape="\"", header=False)\
        .schema(hetzner_schema)\
        .csv(files_location)\
        .rdd\
        .map(lambda row : {
            "Type": row.Type,
            "Product": row.Product,
            "Description": row.Description,
            "StartDate": fix_date_format_for_hetzner(row.StartDate),
            "EndDate": fix_date_format_for_hetzner(row.EndDate),
            "Quantity": row.Quantity,
            "UnitPrice": row.UnitPrice,
            "CostResourceID":  extract_tag(row.Description),
            "CostResourceTag": ""
        })


def load_with_mapping(spark, hetzner_data, mapping_files_path):
    hetzner_df: DataFrame = load_files(spark, hetzner_data).toDF();
    type_mapping_df :DataFrame = mapping_file\
        .load_mapping_file(spark, mapping_files_path+"/type_mapping.csv", mapping_file.type_schema ).toDF();

    resource_mapping_df :DataFrame = mapping_file\
        .load_mapping_file(spark, mapping_files_path+"/resource_mapping.csv", mapping_file.resource_schema ).toDF();

    type_mapping_df.show()
    resource_mapping_df.show()

    joined = hetzner_df\
        .join(type_mapping_df, hetzner_df["Type"] == type_mapping_df["Type"], "left") \
        .join(resource_mapping_df, hetzner_df["CostResourceID"] == resource_mapping_df["CostResourceID"], "left")

    return joined
