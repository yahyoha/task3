import unittest
import sys
import os

import pandas as pd
from pyspark.sql.functions import col, concat_ws
from pyspark.sql import SparkSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloudbillingtool import azure_billing
from cloudbillingtool import hetzner_billing
from cloudbillingtool import helper

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


# class TestHetznerBilling(unittest.TestCase):
#
#     def testHetznerBillingLoad(self):
#         hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, "tests/data/hetzner/*.csv", "tests/metadata")
#         rows = hetzner_billing_with_tags.rdd.map( lambda x: x).collect()
#         for row in rows:
#             print(row)
#
#         hetzner_billing_with_tags \
#             .withColumn("CostResourceTag", concat_ws(",", col("CostResourceTag"))) \
#             .withColumn("ProductTag", concat_ws(";", col("ProductTag"))) \
#             .write.mode('overwrite').options( delimiter='\t').csv("/tmp/cloudbillingtool/hetzner_data")
