
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

    def testHelperMappingGetByResourceId(self):
        resource_mapping_df = pd.read_csv("tests/metadata/mappingfiles/resource_mapping.csv", sep='\t')
        type_mapping_df = pd.read_csv("tests/metadata/mappingfiles/type_mapping.csv", sep='\t')

        self.assertEqual( "kvm3", helper.get_by_resourceid_in_df(resource_mapping_df, 'CostResourceID', 'Produkt', '#1048599' ) )

    def testAllBillingLoad(self):

        # combine azure with hetzner billing
        all_billing_data = all_billing.generate_uniform_data_from(spark, "tests/data/azure/*.csv", "tests/data/hetzner/*.csv", "", "tests/metadata")

        output_df = all_billing_data.toDF() \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \

        for row in output_df.collect():
            print(row)

        # Todo: test the schema
        # Todo: do some nice tests


if __name__ == '__main__':
    unittest.main()
