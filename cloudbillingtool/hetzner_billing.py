import re
from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, array, split, array_join, array_union, concat, to_date, explode
from pyspark.sql.types import StructType, StringType, ArrayType, DecimalType
import pandas as pd

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


def extract_costresourceid(desc):
    if desc and len(desc) > 0:
        return re.search(r'#[0-9]+', desc).group() if re.search(r'#[0-9]+', desc) else ""
    else:
        return""


def fix_date_format_for_hetzner(billing_date_hetzner):
    if not billing_date_hetzner:
        return ""
    year, day, month = billing_date_hetzner.split('-')
    return f"{month}-{day}-{year}"


def flatten(l):
    return [item for sublist in l for item in sublist]


def find_tags_in_df(df, field, pattern):
    matching_rows = df.loc[df[field].str.contains(pattern, case=False)]['CostResourceTag']
    return flatten(list( map( lambda x: x.split(","), matching_rows.tolist())))


def merge_tags_from_dt(resource_mapping_df, type_mapping_df, rowDescription, rowType):
    return  (list(set(find_tags_in_df(resource_mapping_df, "CostResourceID",
                              extract_costresourceid(rowDescription)) +
              find_tags_in_df(type_mapping_df, "Type", rowType)))) + ['']


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
            "StartDate": fix_date_format_for_hetzner(row.StartDate),
            "EndDate": fix_date_format_for_hetzner(row.EndDate),
            "Quantity": row.Quantity,
            "UnitPrice": row.UnitPrice,
            "CostResourceID":  extract_costresourceid(row.Description),
            "CostResourceTag": merge_tags_from_dt( resource_mapping_df,type_mapping_df,row.Description, row.Type )
        })


def load_with_mapping(spark, hetzner_data, mapping_files_path):
    hetzner_df: DataFrame = \
        load_files(spark, hetzner_data, mapping_files_path)\
        .toDF()\
        .alias("hetzner_df") \

    joined_with_tags = hetzner_df \
        .select(lit("hetzner").alias("provider"),
                col("hetzner_df.Type"),
                col("hetzner_df.Product").alias("ProductName"),
                col("hetzner_df.Price").cast(DecimalType(12, 2)).alias("Price"),
                to_date(col("hetzner_df.StartDate"), "MM-dd-yyyy").alias("Date"),
                col("hetzner_df.CostResourceID").alias("CostResourceID"),
                explode("hetzner_df.CostResourceTag").alias("CostResourceTag"))

    return joined_with_tags
