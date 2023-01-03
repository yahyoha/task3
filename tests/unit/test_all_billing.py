import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame
from pyspark.sql import SparkSession
import pandas as pd

import cloudbillingtool.azure_billing as azure_billing
import cloudbillingtool.hetzner_billing as hetzner_billing

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestAllBilling(unittest.TestCase):

    def testAllBillingLoad(self):
        azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, "tests/data/azure/*.csv", "tests/data")
        hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, "tests/data/hetzner/*.csv", "tests/data")

        all_billing = azure_billing_with_tags.rdd.union(hetzner_billing_with_tags.rdd)

        for row in all_billing.collect():
            print(row)

        # Todo: test the schema
        # Todo: do some nice tests
