import unittest
import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws
from cloudbillingtool import azure_billing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestAzureBilling(unittest.TestCase):

    def testAzureBillingLoad(self):
        azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, "tests/data/azure/*.csv", "tests/metadata")

        output_df = azure_billing_with_tags \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \

        for row in output_df.collect():
            print(row)
