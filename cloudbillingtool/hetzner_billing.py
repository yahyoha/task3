import re
import csv
from datetime import datetime

from pyspark.shell import spark
from pyspark.sql.types import StructType, StringType


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


def load_files(files_location):
    return\
        spark.read\
        .options(format='csv', escape="\"", header=False)\
        .schema(hetzner_schema)\
        .csv(files_location)
