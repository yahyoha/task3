import unittest
import sys
import os
from pyspark.sql import SparkSession

from cloudbillingtool import azure_billing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestAzureBilling(unittest.TestCase):

    def testAzureBillingLoad(self):
        azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, "tests/data/azure/*.csv", "tests/data")
        rows = azure_billing_with_tags.rdd.collect()
        for row in rows:
            print(row)

        azure_billing_with_tags.write.mode('overwrite').options( delimiter='\t').csv("/tmp/cloudbillingtool/azure_data")