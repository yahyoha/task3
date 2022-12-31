import re
import csv
from datetime import datetime

from pyspark import rdd
from pyspark.sql.types import StructType, StringType

type_schema = StructType() \
  .add("Type", StringType(), True) \
  .add("CostResourceTag", StringType(), True)

resource_schema = StructType() \
  .add("CostResourceID", StringType(), True) \
  .add("CostResourceTag", StringType(), True)


def load_mapping_file(spark, file_location, schema) -> rdd :
    return \
        spark.read \
        .option("header", "true") \
        .option("delimiter", "\t") \
        .option("multiLine", "true") \
        .option("ignoreTrailingWhiteSpace", "true") \
        .schema(schema)\
        .csv(file_location) \
        .rdd
