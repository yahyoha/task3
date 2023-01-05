import unittest
import sys
import os
from pyspark.sql import SparkSession

from cloudbillingtool import hetzner_billing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestHetznerBilling(unittest.TestCase):

    def testHetznerBillingLoad(self):
        hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, "tests/data/hetzner/*.csv", "tests/data")
        rows = hetzner_billing_with_tags.rdd.map( lambda x: x).collect()
        for row in rows:
            print(row)

        hetzner_billing_with_tags.write.mode('overwrite').options( delimiter='\t').csv("/tmp/cloudbillingtool/hetzner_data")

    def testRowTagExtraction(self):
        mapping_files_path = "tests/data"

        resource_mapping_df = pd.read_csv(mapping_files_path + "/resource_mapping.csv", sep='\t')
        type_mapping_df = pd.read_csv(mapping_files_path + "/type_mapping.csv", sep='\t')

        rowDescription='Cloud-Projekt "JJ" (01.12.2021 - 31.12.2021)'
        rowType='Cloud-Projekt "NBA"'

        tags = list(set(hetzner_billing.find_tags_in_df(resource_mapping_df, "CostResourceID",
                                               hetzner_billing.extract_costresourceid(rowDescription)) +
                            hetzner_billing.find_tags_in_df(type_mapping_df, "Type", rowType))) + ['']
        expected = ['PROD', 'IT-OPS', 'TEST', 'DEV', ''];

        tags.sort()
        expected.sort()

        self.assertEqual(tags, expected )
