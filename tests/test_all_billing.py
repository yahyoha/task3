
import unittest
import os
import sys

import pandas as pd
from pyspark.sql import SparkSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloudbillingtool import azure_billing
from cloudbillingtool import hetzner_billing
from cloudbillingtool import helper

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()

class TestAllBilling(unittest.TestCase):

    def testHelperMappingGetByResourceId(self):
        resource_mapping_df = pd.read_csv( "tests/data/resource_mapping.csv", sep='\t')
        type_mapping_df = pd.read_csv( "tests/data/type_mapping.csv", sep='\t')

        self.assertEqual( "kvm3", helper.get_by_resourceid_in_df(resource_mapping_df, 'CostResourceID', 'Produkt', '#1048599' ) )

    def testAllBillingLoad(self):
        azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, "tests/data/azure/*.csv", "tests/data")
        hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, "tests/data/hetzner/*.csv", "tests/data")

        all_billing = azure_billing_with_tags.rdd.union(hetzner_billing_with_tags.rdd)

        for row in all_billing.toDF().collect():
            print(row)

        # Todo: test the schema
        # Todo: do some nice tests


if __name__ == '__main__':
    unittest.main()
