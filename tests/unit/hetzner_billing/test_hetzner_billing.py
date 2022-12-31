import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame
from pyspark.sql import SparkSession

import cloudbillingtool.hetzner_billing as hetzner_billing

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestHetznerBilling(unittest.TestCase):
    def testHetznerBillingLoad(self):
        hetzner_billing_with_tags = hetzner_billing.load_with_mapping(spark, "tests/data/hetzner/*.csv", "tests/data")
        hetzner_billing_with_tags.show()