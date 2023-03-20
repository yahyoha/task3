
import unittest
import os
import sys
from pyspark.sql.functions import col, concat_ws
import pandas as pd
from pyspark.sql import SparkSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloudbillingtool import azure_billing
from cloudbillingtool import hetzner_billing
from cloudbillingtool import helper
from cloudbillingtool import all_billing

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestAllBilling(unittest.TestCase):

    def testAllBillingLoad(self):

        # combine azure with hetzner billing
        all_billing_data = all_billing.generate_uniform_data_from(spark, "tests/data/azure/*.csv", "tests/data/hetzner/*.csv", "tests/data/aws/*.csv", "tests/metadata")

        output_df = all_billing_data.toDF() \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(";", col("ProductTag")))

        for row in output_df.collect():
            print(row)

        # Todo: test the schema
        # Todo: do some nice tests


if __name__ == '__main__':
    unittest.main()
