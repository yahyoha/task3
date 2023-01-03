import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame
from pyspark.sql import SparkSession
import pandas as pd

import cloudbillingtool.azure_billing as azure_billing

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()

#
# class TestAzureBilling(unittest.TestCase):
#
#     def testAzureBillingLoad(self):
#         azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, "tests/data/azure/*.csv", "tests/data")
#         rows = azure_billing_with_tags.rdd.collect()
#         for row in rows:
#             print(row)
#
#         azure_billing_with_tags.write.mode('overwrite').options( delimiter='\t').csv("/tmp/cloudbillingtool/azure_data")